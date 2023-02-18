from utils.maths_utils import distance_calculator_metres

# A very barebones test file to establish that there should be one.
# Testing should really cover all functions and a variety of edge cases,
# given more time.


def test_load_excel_file_all_sheets_df() -> None:
    london_to_paris = distance_calculator_metres((51.4706001, -0.461941), (49.0127983, 2.54999995))
    assert london_to_paris == 347200.0
