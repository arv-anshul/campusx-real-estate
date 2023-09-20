import pandas as pd

ORD_COLS_MAPPING = {
    "FURNISH": ["unfurnished", "semifurnished", "furnished"],
    "AGE": [
        "10+ year old property",
        "5-10 year old property",
        "1-5 year old property",
        "0-1 year old property",
        "under construction",
    ],
    "BEDROOM_NUM": [1, 2, 3, 4, 5, 99],
    "BALCONY_NUM": [0, 1, 2, 3, 4, 99],
    "FLOOR_NUM": ["low rise", "mid rise", "high rise"],
    "LUXURY_CATEGORY": [0, 1, 2],
}


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
