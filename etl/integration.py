import pandas as pd

OUTPUT_COLS = ["Country", "Date", "Confirmed", "Deaths", "Recovered", "Source"]
OUTPUT_INDEX = ["Country", "Date"]
OUTPUT_PATH = "../data/covid/aggregated/date_country.csv"

def tag_source(df, tag):
    df["Source"] = tag
    return df

def integrate_srk(path):
    df = pd.read_csv(path, parse_dates=["ObservationDate"])
    clean_df = (
        df.rename(columns={"Country/Region": "Country", "ObservationDate": "Date"})
        .groupby(by=OUTPUT_INDEX)
        .agg({"Confirmed": "sum", "Deaths": "sum", "Recovered": "sum"})
    )
    return tag_source(clean_df, "srk")

def write_data(clean_df, output_path=OUTPUT_PATH, reset=False):
    if reset:
        clean_df.to_csv(output_path)
    else:
        existing_df = pd.read_csv(output_path).set_index(OUTPUT_INDEX)
        pd.concat([existing_df, clean_df]).to_csv(output_path)

def get_aggregated(in_path=OUTPUT_PATH):
    return pd.read_csv(in_path, parse_dates["Date"]).set_index(OUTPUT_INDEX)
