import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "rainfall_lookup.csv")

RAIN_DF = pd.read_csv(CSV_PATH)

def rainfall_from_subdivision(sub_division):
    row = RAIN_DF[RAIN_DF["SUBDIVISION"] == sub_division]
    if row.empty:
        raise ValueError(f"No rainfall data for {sub_division}")
    return int(row.iloc[0]["ANNUAL"])
