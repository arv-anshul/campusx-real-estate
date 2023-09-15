import pandas as pd
import streamlit as st

from src.property.entity import PropertyType


def get_df_from_session_state(prop: PropertyType):
    return pd.DataFrame.from_dict(
        {k: v for k in prop.schema.ALL_COLS for i, v in st.session_state.items() if k == i},
        orient="index",
    ).T


def format_99_option(x: int):
    """Format the encode value `99` in **BEDROOM_NUM** and **BALCONY_NUM** feature."""
    if x == 99 or x == "99":
        return "More than Above"
    return x


def query_for_rental_property(
    df: pd.DataFrame,
    extra_query: str | None,
) -> pd.DataFrame:
    """Return the rental properties dataframe from the passed dataframe."""
    df = pd.concat(
        [
            df[df["DESCRIPTION"].str.contains(" rent ") & (df["PRICE"] < 20)],
            df.query(extra_query if extra_query else "PRICE<0"),
        ]
    ).drop_duplicates(ignore_index=True)
    return df
