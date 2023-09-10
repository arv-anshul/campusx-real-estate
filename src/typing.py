import typing as t

PropertyAlias: t.TypeAlias = t.Literal[
    "res_apartment",
    "rent_apartment",
    "ind_floor",
    "rent_ind_floor",
    "ind_house",
    "res_land",
]
CAT_COLS_Key: t.TypeAlias = t.Literal["ord_cols", "ohe_cols"]
