import math
from datetime import datetime

from travel_analyser_service.process_travel_data import DataParser

# A very barebones test file to establish that there should be one.
# Testing should really cover all functions and a variety of edge cases,
# given more time.


def test_data_parser() -> None:
    data_parser = DataParser()
    output_data = data_parser.process_data("travel_data.xlsx")
    assert "Emissions" in output_data.columns
    assert "Emissions Per km" in output_data.columns
    assert "Distance Travelled km" in output_data.columns


# There should really be tests for each of the individual functions in test_data_parser with edge cases and sample data,
# But I really don't have time!! Here's an example of what I'm talking about:


def test_get_locations_success() -> None:
    data_parser = DataParser()
    data_parser.distance_data = [
        {"Airport": "LHR", "City": "London", "Country": "GB", "Latitude": 51.4706001, "Longitude": -0.461941},
        {"Airport": "GVA", "City": "Geneva", "Country": "CH", "Latitude": 46.2380981, "Longitude": 6.10895014},
    ]
    sample_row = {
        "Air/Rail/Taxi": "Air",
        "Ticket Supplier": "British",
        "Departure": "Geneva",
        "Arrival": "London",
        "Unnamed: 4": "GVA-LHR",
        "Currency": math.nan,
        "Price": math.nan,
        "Travel date": datetime.strptime("2020-02-17 00:00:00", "%Y-%m-%d %H:%M:%S"),
    }
    output_data = data_parser.get_locations(sample_row)
    assert output_data == ((46.2380981, 6.10895014), (51.4706001, -0.461941))
