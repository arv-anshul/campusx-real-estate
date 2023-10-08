import typing as t

import streamlit as st

PropertyAlias: t.TypeAlias = t.Literal[
    "res_apartment",
    "rent_apartment",
    "ind_floor",
    "rent_ind_floor",
    "ind_house",
    "res_land",
]
CAT_COLS_Key: t.TypeAlias = t.Literal["ord_cols", "ohe_cols"]

DatasetType: t.TypeAlias = t.Literal["main", "user"]
ModelType: t.TypeAlias = t.Literal["price_predictor"]


def stop() -> t.NoReturn:
    """
    Implement `st.stop()` function in this way to avoid the type annotation problems.
    """
    st.stop()
    raise NotImplementedError("Error while stopping the execution.")
