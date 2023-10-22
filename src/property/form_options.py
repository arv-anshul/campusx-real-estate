from pathlib import Path
from typing import Self

import streamlit as st

from src.core import io
from src.typing import DatasetType, PropertyAlias


class FormOptions:
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(FormOptions, cls).__new__(cls)
            cls._instance._init_options()
        return cls._instance

    def _init_options(self) -> None:
        self.FURNISH: list[str] = ["unfurnished", "semifurnished", "furnished"]
        self.FACING: list[str] = [
            "north-east",
            "east",
            "north",
            "south-east",
            "south",
            "west",
            "south-west",
            "north-west",
        ]
        self.AGE: list[str] = [
            "10+ year old property",
            "5-10 year old property",
            "1-5 year old property",
            "0-1 year old property",
            "under construction",
        ]
        self.BEDROOM_NUM: list[int] = [1, 2, 3, 4, 5, 99]
        self.BALCONY_NUM: list[int] = [0, 1, 2, 3, 4, 99]
        self.FLOOR_NUM: list[str] = ["low rise", "mid rise", "high rise"]
        self.LUXURY_CATEGORY: dict[int, str] = {
            0: "Budget",
            1: "Semi-Luxury",
            2: "Full-Luxury",
        }

    @staticmethod
    @st.cache_data
    def CITY(dataset_type: DatasetType, prop_type: PropertyAlias) -> list[str]:
        fp = Path("data") / dataset_type / f"{prop_type}.csv"
        df = io.read_csv(fp)

        cities = df["CITY"].unique().tolist()
        return sorted(map(lambda x: x.title(), cities))

    @staticmethod
    @st.cache_data
    def LOCALITY_NAME(
        city_: str, dataset_type: DatasetType, prop_type: PropertyAlias
    ) -> list[str]:
        fp = Path("data") / dataset_type / f"{prop_type}.csv"
        df = io.read_csv(fp)

        city_ = city_.lower()
        localities = df.query("CITY==@city_")["LOCALITY_NAME"].unique().tolist()
        return sorted(map(lambda x: x.title(), localities))


form_options = FormOptions()
