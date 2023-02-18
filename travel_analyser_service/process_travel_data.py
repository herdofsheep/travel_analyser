import copy
from typing import Dict, Optional, Tuple

import pandas as pd

from utils.data_utils import is_empty_cell, load_excel_file_all_sheets_df, save_df_to_csv, string_match
from utils.maths_utils import distance_calculator_metres, set_to_significant_figures


def main():
    data_parser = DataParser()
    cleaned_data = data_parser.process_data("travel_data.xlsx")
    save_df_to_csv("travel_info_cleaned", cleaned_data)


class DataParser:
    def __init__(self):
        # miles * 1.60934 = km
        # per-mile * 1/1.60934 = per-km
        # 1/1.60934 = 0.62137
        self.per_miles_conversion_rate = 0.62137

    def process_data(self, file_name: str) -> pd.DataFrame:
        """A function to collect and clean travel data and combine data to enable calculations of emission data."""
        print(f"Starting data parsing for {file_name}")

        output_data = self.get_data_from_file(file_name)
        for row in output_data:
            # if there is no price, we need two locations to calculate distance.
            if is_empty_cell(str(row["Price"])) and "-" in str(row["Unnamed: 4"]):
                (emissions_per_km_rate, distance_km,) = self.calculate_emissions_from_distance(row)
            else:
                (emissions_per_km_rate, distance_km,) = self.calculate_emissions_from_price(row)

            emissions = distance_km * emissions_per_km_rate
            # give to 3 significant figures, which is how precise we can realistically expect this caluculator to be.
            row["Emissions"] = set_to_significant_figures(emissions, 3)
            row["Emissions Per km"] = set_to_significant_figures(emissions_per_km_rate, 3)
            row["Distance Travelled km"] = set_to_significant_figures(distance_km, 3)
            if is_empty_cell(emissions):
                row["Emissions"] = "Cannot be calculated with provided data"
            if is_empty_cell(emissions_per_km_rate):
                row["Emissions Per km"] = "Cannot be calculated with provided data"
            if is_empty_cell(distance_km):
                row["Distance Travelled km"] = "Cannot be calculated with provided data"
        return pd.DataFrame.from_dict(output_data)

    def get_data_from_file(self, file_name: str) -> Dict:
        """A function to read data from provided sheet- not very flexible! Requires sheets with specific names."""
        print("Collecting and separating data for initial parse...")
        file = load_excel_file_all_sheets_df(".data", file_name)

        travel_df = file["Data"].to_dict("records")
        self.travel_df = travel_df
        self.emission_data = file["Emission Factors"].to_dict("records")
        self.distance_data = file["Locations"].to_dict("records")
        # cost_df sheet is a bit strangely laid out and needs some manipulation.
        cost_df = file["Price per mile"].T
        cost_df.columns = cost_df.iloc[0]
        self.cost_df = cost_df[1:].to_dict("records")[0]

        return copy.deepcopy(travel_df)

    def get_locations(self, row: Dict) -> Tuple[Optional[Tuple], Optional[Tuple]]:
        loc_one = row["Unnamed: 4"][:3]
        loc_two = row["Unnamed: 4"][4:7]
        loc_one_pos = next(
            ((x["Latitude"], x["Longitude"]) for x in self.distance_data if string_match(x["Airport"], loc_one)),
            None,
        )
        loc_two_pos = next(
            ((x["Latitude"], x["Longitude"]) for x in self.distance_data if string_match(x["Airport"], loc_two)),
            None,
        )
        # Fallback to location name rather than station code
        if loc_one_pos is None:
            loc_name = row["Departure"]
            loc_one_pos = next(
                (
                    (x["Latitude"], x["Longitude"])
                    for x in self.distance_data
                    if string_match(x["City"], loc_name)
                ),
                None,
            )
        if loc_two_pos is None:
            loc_name = row["Arrival"]
            loc_two_pos = next(
                (
                    (x["Latitude"], x["Longitude"])
                    for x in self.distance_data
                    if string_match(x["City"], loc_name)
                ),
                None,
            )
        if not (loc_one_pos or loc_two_pos):
            message = f"""no way of getting location data for row {row},
            ensure get_locations is only passed rows with corresponding station or location data in 'Locations' sheet."""
            print(message)
            raise Exception(message)
        return (loc_one_pos, loc_two_pos)

    def calculate_emissions_from_price(self, row: Dict) -> Tuple[float, float]:
        # Add data for special case if trip is in UK
        # This check only checks if in London, should be broader
        # with a full list of UK cities and/or compare station/airport codes.
        in_gbr = "London" in row["Arrival"] or "London" in row["Departure"]

        # sourcery skip: raise-specific-error
        emissions_per_km_rate = None

        # values for Taxi rows
        if string_match(row["Air/Rail/Taxi"], "taxi"):
            taxi_emission_data = [x for x in self.emission_data if string_match(x["travel_type"], "taxis")]
            if row["Ticket Supplier"] == "UBER":
                emissions_per_km_rate = next(
                    x["value"] for x in taxi_emission_data if string_match(x["supplier"], "UBER")
                )
            if not emissions_per_km_rate:
                if in_gbr:
                    emissions_per_km_rate = next(
                        x["value"]
                        for x in taxi_emission_data
                        if is_empty_cell(x["supplier"]) and string_match(x["geography"], "GBR")
                    )
                else:
                    emissions_per_km_rate = next(
                        x["value"]
                        for x in taxi_emission_data
                        if is_empty_cell(x["supplier"]) and string_match(x["geography"], "All")
                    )
            price_per_km = self.cost_df["taxi"] * self.per_miles_conversion_rate

        # values for Bus rows
        elif string_match(row["Air/Rail/Taxi"], "bus"):
            emissions_per_km_rate = next(
                x["value"] for x in self.emission_data if string_match(x["travel_type"], "bus")
            )
            price_per_km = self.cost_df["bus"] * 0.62137

        # we should have no 'price' rows without a corresponding travel type in cost_df (Price Per Mile sheet), if not, raise exception.
        else:
            message = f"""Calculate_emissions_from_price can only handle taxi and bus prices.
                        {row['Air/Rail/Taxi']} travel type given."""
            # Would be good to set up a specific Exception type class but seems a bit overkill for limited time and a non-ideal exception anyway.
            raise Exception(message)

        price = row["Price"]
        distance_km = price / price_per_km
        return emissions_per_km_rate, distance_km

    def calculate_emissions_from_distance(self, row: Dict) -> Tuple[float, float]:
        """Function to use distance information to calculate emissions.
        Only accepts rows with two locations (and so calculable distance from 'Locations' sheet)
        All rows with two locations have a '-' delimiter so uses that as a filter."""
        if "-" not in str(row["Unnamed: 4"]):
            message = "Distance emissions calculator requires two locations"
            print(message)
            raise Exception(message)

        loc_one, loc_two = self.get_locations(row)
        row["Departure Coordinates"] = loc_one
        row["Arrival Coordinates"] = loc_two

        # values for Air rows
        if string_match(row["Air/Rail/Taxi"], "air"):
            in_gbr = string_match(row["Ticket Supplier"], "british")
            air_emission_data = [x for x in self.emission_data if string_match(x["travel_type"], "flight")]
            if in_gbr:
                emissions_per_km_rate = next(
                    x["value"] for x in air_emission_data if string_match(x["geography"], "GBR-Domestic")
                )
            else:
                emissions_per_km_rate = next(
                    x["value"] for x in air_emission_data if string_match(x["geography"], "All")
                )

        # values for Train rows
        elif string_match(row["Air/Rail/Taxi"], "train"):
            emissions_per_km_rate = next(x["value"] for x in self.emission_data if x["travel_type"] == "train")

        # we should have no 'price' rows without a corresponding travel type in cost_df (Price Per Mile sheet), if not, raise exception.
        else:
            message = f"""calculate_emissions_from_distance can only handle air and train prices.
                        {row['Air/Rail/Taxi']} travel type given."""
            print(message)
            # Would be good to set up a specific Exception type class but seems a bit overkill for limited time and a non-ideal exception anyway.
            raise Exception(message)

        distance_km = distance_calculator_metres(loc_one, loc_two) / 1000
        return emissions_per_km_rate, distance_km


if __name__ == "__main__":
    main()
