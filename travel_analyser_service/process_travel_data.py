from utils.data_utils import load_excel_file_all_sheets_df


def main():
    data_parser = DataParser("travel_data.xlsx")
    data_parser.get_data()


class DataParser:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_data(self):
        file = load_excel_file_all_sheets_df("data", "travel_data.xlsx")

        self.travel_df = file["Data"].to_dict("records")
        self.emission_data = file["Emission Factors"].to_dict("records")
        self.distance_data = file["Locations"].to_dict("records")
        # cost_df sheet is a bit strangely laid out and needs some manipulation.
        cost_df = file["Price per mile"].T
        cost_df.columns = cost_df.iloc[0]
        self.cost_df = cost_df[1:].to_dict("records")[0]


if __name__ == "__main__":
    main()
