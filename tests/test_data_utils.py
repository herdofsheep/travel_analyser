import pandas as pd

from utils.data_utils import load_excel_file_all_sheets_df

# A very barebones test file to establish that there should be one.
# Testing should really cover all functions and a variety of edge cases,
# given more time.


def test_load_excel_file_all_sheets_df() -> None:
    data = load_excel_file_all_sheets_df(".data", "travel_data.xlsx")
    assert len(data) == 4
    assert isinstance(data["Data"], pd.DataFrame)
