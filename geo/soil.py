import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "soil_depth_lookup.csv")

SOIL_DF = pd.read_csv(CSV_PATH)

def soil_depth_from_state(state):
    row = SOIL_DF[SOIL_DF["STATE"] == state]
    if row.empty:
        raise ValueError(f"No soil depth data for {state}")
    return row.iloc[0]["DOMINANT_SOIL_DEPTH"]
