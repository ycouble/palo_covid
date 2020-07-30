import os
import pandas as pd

DATAPOINTS_COLS = ["Country", "Date", "Confirmed", "Deaths", "Recovered", "Source"]
DATAPOINTS_INDEX = ["Country", "Date"]
DATAPOINTS_PATH = "../data/covid/aggregated/date_country.csv"

WORLD_PATH = "../data/covid/aggregated/world.csv"


def tag_source(df, tag):
    df["Source"] = tag
    return df


def integrate_srk(path):
    df = pd.read_csv(path, parse_dates=["ObservationDate"])
    clean_df = (
        df.rename(columns={"Country/Region": "Country", "ObservationDate": "Date"})
        .astype({"Confirmed": int, "Deaths": int, "Recovered": int})
        .groupby(by=DATAPOINTS_INDEX)
        .agg({"Confirmed": "sum", "Deaths": "sum", "Recovered": "sum"})
    )
    return tag_source(clean_df, "srk")


def aggregate_world(in_path=DATAPOINTS_PATH):
    return (
        get_aggregated(in_path)
        .groupby(["Source", "Date"])
        .agg({"Confirmed": "sum", "Deaths": "sum", "Recovered": "sum"})
    )


def write_data(clean_df, output_path, reset=False):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if reset:
        clean_df.to_csv(output_path)
    else:
        existing_df = pd.read_csv(output_path).set_index(DATAPOINTS_INDEX)
        pd.concat([existing_df, clean_df]).to_csv(output_path)


def get_aggregated(in_path=DATAPOINTS_PATH):
    return pd.read_csv(in_path, parse_dates=["Date"])


def get_world(in_path=WORLD_PATH):
    return pd.read_csv(in_path, parse_dates=["Date"])
