from typing import Self

import pandas as pd

from src.core.constants import CITY_CSV, LOCALITY_NAME_CSV


class FormOptions:
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(FormOptions, cls).__new__(cls)
            cls._instance._init_options()
        return cls._instance

    def _init_options(self) -> None:
        self.FURNISH: list[str] = ["Unfurnished", "Semifurnished", "Furnished"]
        self.FACING: list[str] = [
            "North-East",
            "East",
            "North",
            "South-East",
            "South",
            "West",
            "South-West",
            "North-West",
        ]
        self.AGE: list[str] = [
            "10+ Year Old Property",
            "5-10 Year Old Property",
            "1-5 Year Old Property",
            "0-1 Year Old Property",
            "Under Construction",
        ]
        self.BEDROOM_NUM: list[int] = [1, 2, 3, 4, 5, 99]
        self.BALCONY_NUM: list[int] = [0, 1, 2, 3, 4, 99]
        self.FLOOR_NUM: list[str] = ["low rise", "mid rise", "high rise"]
        self.CITY: list[str] = self.__load_cities()

    def __load_cities(self) -> list[str]:
        df = pd.read_csv(CITY_CSV)
        return df["CITY"].tolist()

    def LOCALITY_NAME(self, city_: str) -> list[str]:
        locality = pd.read_csv(LOCALITY_NAME_CSV).merge(
            pd.read_csv(CITY_CSV), how="inner", on="CITY_ID"
        )
        return locality.query("CITY==@city_")["LOCALITY_NAME"].tolist()


form_options = FormOptions()
