import math
import os
from datetime import datetime
from typing import Dict

import pandas as pd


def match(thing_one: str, thing_two: str) -> bool:
    return thing_one.lower().strip() == thing_two.lower().strip()


def is_empty_cell(entry: float) -> bool:
    return False if str(entry) != "nan" else bool(math.isnan(entry))


def load_excel_file_all_sheets_df(file_path: str, file_name: str) -> Dict:
    db_output = {}
    path = os.path.abspath(os.path.join(os.getcwd(), file_path))
    loc = os.path.join(path, file_name)
    excel_file = pd.ExcelFile(loc)

    for sheet in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        # Price per mile is a bit strangely laid out and needs some manipulation. Not happy about this hard-coded fix
        # But a generalised solution is going to take too long to justify!
        if sheet == "Price per mile":
            df = pd.read_excel(excel_file, sheet_name=sheet, header=None)
        db_output[sheet] = df

    return db_output


def save_df_to_csv(name, df, path="script_outputs", with_date=False):
    name.replace(".csv", "")

    if with_date:
        df_name = f"{name}_{datetime.now().strftime('%Y%m%d')}.csv"
    else:
        df_name = f"{name}.csv"

    print(f"Saving data {df_name}")
    output_path = os.path.abspath(os.path.join(os.getcwd(), path))
    loc = os.path.join(output_path, df_name)

    if not os.path.exists(output_path):
        os.mkdir(output_path)
    with open(loc, "w"):
        df.to_csv(loc, index=False)
