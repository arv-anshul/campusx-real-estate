"""
Used to decoding the columns of dataset.
"""

from ast import literal_eval

import pandas as pd

from src.core import constants as C
from src.core import io

from . import _utils


class DecodeFeature:
    def __init__(self, df: pd.DataFrame) -> None:
        self.__df = df

    @property
    def all_methods(self) -> list[str]:
        """
        List all methods of instantiated class.

        :return: All the methods `method.startswith('_decode')` and `method[-1].isupper()` in sorted form.
        """
        return [
            i for i in sorted(dir(self)) if i.startswith("decode_") and i[-1].isupper()
        ]

    def run_all(self, *skip: str) -> pd.DataFrame:
        """
        Run all the feature decoder method.

        :skip (str): Specify the methods which you don't want to run.
        :hint: List all methods of class `DecodeFeature` using `.all_methods` property.
        """
        [getattr(self, i)() for i in self.all_methods if i not in skip]
        return self.__df

    def decode_PRICE(self) -> None:
        self.__df["PRICE"] = self.__df["PRICE"].str.replace(",", "")

        # Drop properties with extraordinary prices like "price on request", "45l onwards"
        self.__df.drop(
            index=self.__df[
                self.__df["PRICE"].str.contains("bed", regex=False)
                | self.__df["PRICE"].str.contains("request", regex=False)
                # TODO: Restore it due to its heavy presence.
                | self.__df["PRICE"].str.contains("-", regex=False)
                # TODO: Restore it due to easiness.
                | self.__df["PRICE"].str.contains("onwards", regex=False)
            ].index,
            inplace=True,
        )

        def handle_price(x: str) -> str | float:
            price = None
            if " cr" in x:
                price = round(float(x.split(" ")[0]) * C.CRORE, 2)
            elif " l" in x:
                price = round(float(x.split(" ")[0]) * C.LAKH, 2)
            return price if price else x

        self.__df["PRICE"] = self.__df["PRICE"].apply(handle_price).astype(float)

    def decode_AREA(self) -> None:
        self.__df = self.__df.drop(
            index=self.__df[
                ~self.__df["AREA"].str.contains("sq.ft.", regex=False)
            ].index
        ).drop(index=self.__df[self.__df["AREA"].str.contains("-")].index)
        self.__df["AREA"] = self.__df["AREA"].str.split(" ").str.get(0).astype(float)

    def decode_FEATURES(self) -> None:
        features_df = io.read_csv(C.FACETS_PATH / "FEATURES.csv")
        features_df["values"] = features_df["label"].map(
            _utils.FEATURES_MAPPING, "ignore"
        )

        lookup_values = (
            features_df[["id", "values"]].set_index("id").to_dict()["values"]
        )
        self.__df["FEATURES_SCORE"] = self.__df["FEATURES"].apply(
            _utils.lookup_mapping, args=(lookup_values,)
        )

    def decode_FORMATTED_LANDMARK_DETAILS(self) -> None:
        self.__df["FORMATTED_LANDMARK_DETAILS"] = (
            self.__df["FORMATTED_LANDMARK_DETAILS"]
            .fillna("[]")
            .apply(literal_eval)
            .apply(lambda x: [i.get("text") for i in x])
        )

        def handle_landmarks(
            x: list[str], key: str, landmarks_group: dict[str, list[str]]
        ) -> None:
            rv: int = 0

            for i in x:
                for j in landmarks_group[key]:
                    if j in i and isinstance(i, str):
                        rv += int(i.split(" ")[0])

            self.temp_data.append(rv)
            self.__curr_idx += 1
            return

        for col_name in _utils.LANDMARKS_GROUPS.keys():
            self.__curr_idx = 0
            self.temp_data = []

            self.__df["FORMATTED_LANDMARK_DETAILS"].apply(
                handle_landmarks, args=(col_name, _utils.LANDMARKS_GROUPS)
            )
            self.__df[col_name] = self.temp_data

    def decode_BEDROOM_NUM(self) -> None:
        self.__df["BEDROOM_NUM"] = self.__df["BEDROOM_NUM"].apply(
            lambda x: x if x <= 5 else 99
        )

    def decode_BALCONY_NUM(self) -> None:
        self.__df["BALCONY_NUM"] = self.__df["BALCONY_NUM"].apply(
            lambda x: x if x <= 4 else 99
        )

    def decode_FLOOR_NUM(self) -> None:
        self.__df["FLOOR_NUM"] = self.__df["FLOOR_NUM"].apply(
            _utils.eval_numeric_values
        )
        self.__df["FLOOR_NUM"] = self.__df["FLOOR_NUM"].apply(
            lambda x: x
            if pd.isna(x)
            else "low rise"
            if x in ["g", "l", "b", "m"]
            else "low rise"
            if 1 <= x <= 3
            else "mid rise"
            if 4 <= x <= 10
            else "high rise"
        )

    def decode_AGE(self) -> None:
        age_df = io.read_csv(C.FACETS_PATH / "AGE.csv")
        lookup_values = age_df.set_index("id").to_dict()["label"]
        self.__df["AGE"] = self.__df["AGE"].map(lookup_values)

    def decode_AMENITIES(self) -> None:
        self.__df["AMENITIES"] = self.__df["AMENITIES"].str.split(",")

        amenity_df = io.read_csv(C.FACETS_PATH / "AMENITIES.csv")
        amenity_df["values"] = amenity_df["label"].map(
            _utils.AMENITIES_MAPPING, "ignore"
        )

        lookup_values = amenity_df[["id", "values"]].set_index("id").to_dict()["values"]
        self.__df["AMENITIES_SCORE"] = self.__df["AMENITIES"].apply(
            _utils.lookup_mapping, args=(lookup_values,)
        )

    def decode_FURNISH(self) -> None:
        furnish_df = io.read_csv(C.FACETS_PATH / "FURNISH.csv")
        lookup_values: dict[int, str] = furnish_df.set_index("id").to_dict()["label"]
        self.__df["FURNISH"] = self.__df["FURNISH"].map(lookup_values)

    def decode_FACING(self) -> None:
        facing_df = io.read_csv(C.FACETS_PATH / "FACING_DIRECTION.csv")
        lookup_values: dict[int, str] = facing_df.set_index("id").to_dict()["label"]
        self.__df["FACING"] = self.__df["FACING"].map(lookup_values)
