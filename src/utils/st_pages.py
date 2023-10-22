"""Functions for streamlit app's pages."""

import pandas as pd


def decorate_options(x):
    x = " ".join(x.split("_")).title()
    x = x.replace("Res", "Residential", 1)
    x = x.replace("Ind", "Independent", 1)
    x = x.replace("Rent", "Rental", 1)
    return x


def colorizer(s: str, c: str = "red") -> str:
    return f":{c}[{s}]"


def format_price(price: float) -> str:
    lakh = 1_00_000
    crore = 1_00_00_000

    if lakh <= price < crore:
        return f"₹ {price/lakh:.2f} Lac"
    elif crore < price:
        return f"₹ {price/crore:.2f} Cr"

    return f"₹ {price:.2f}"


def get_center_lat_lon(df: pd.DataFrame) -> dict[str, float]:
    return {"lat": df["LATITUDE"].median(), "lon": df["LONGITUDE"].median()}
