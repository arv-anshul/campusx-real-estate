from ast import literal_eval
from pathlib import Path

import pandas as pd

from src.core import io

from . import _utils
from .decode_feature import DecodeFeature

DUMP_DATASET_PATH = Path("data/processed/gurgaon_10k.csv")


class DataCleaner:
    __slots__ = ("__df",)

    def __init__(self, df: pd.DataFrame) -> None:
        self.__df = df

    def _clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Returns a cleaned dataframe."""
        # Drop duplicated properties
        df.drop_duplicates(subset=["PROP_ID"], inplace=True)

        # Drop unnecessary prop types
        _ = ["studio apartment", "farm house", "serviced apartments", "other"]
        df = df.query("PROPERTY_TYPE != @_").reset_index(drop=True)

        # Extract features from `location` column
        df["location"] = df["location"].str.replace("none", "None").apply(literal_eval)
        df["LOCALITY_NAME"] = df["location"].str.get("locality_name")  # type: ignore
        df["SOCIETY_NAME"] = df["location"].str.get("society_name")  # type: ignore

        # Extract lat-long from MAP_DETAILS column
        df["MAP_DETAILS"] = df["MAP_DETAILS"].apply(literal_eval)
        df["LATITUDE"] = df["MAP_DETAILS"].str.get("latitude")  # type: ignore
        df["LONGITUDE"] = df["MAP_DETAILS"].str.get("longitude")  # type: ignore

        df["DESCRIPTION"] = df["DESCRIPTION"].str.replace("\n", " ")

        return df

    def dump_to_mongodb(self, df: pd.DataFrame) -> pd.DataFrame:
        """For now just save the dataset into `data/processed/` directory."""
        if DUMP_DATASET_PATH.exists():
            old_df = io.read_csv(DUMP_DATASET_PATH)
            df = pd.concat([old_df, df], axis="index")
            df.drop_duplicates(subset=["PROP_ID"], inplace=True)

        df.to_csv(DUMP_DATASET_PATH, index=False)
        return df

    def _fillna(self, df: pd.DataFrame) -> pd.DataFrame:
        df["TOTAL_LANDMARK_COUNT"].fillna(round(df["TOTAL_LANDMARK_COUNT"].mean()), inplace=True)
        df["AMENITIES_SCORE"].fillna(round(df["AMENITIES_SCORE"].mean()), inplace=True)

        _ = ["residential land", "independent/builder floor"]
        df["FURNISH"].fillna(df.query("PROPERTY_TYPE != @_")["FURNISH"].mode()[0], inplace=True)

        df["FACING"].fillna(df["FACING"].mode()[0], inplace=True)
        df["AGE"].fillna(df["AGE"].mode()[0], inplace=True)
        df["FLOOR_NUM"].fillna(df["FLOOR_NUM"].mode()[0], inplace=True)
        df["BEDROOM_NUM"].fillna(df["BEDROOM_NUM"].mode()[0], inplace=True)

        # BALCONY_NUM
        temp = df[df["BALCONY_NUM"].isnull()]
        temp_mapping = df.pivot_table("BALCONY_NUM", "BEDROOM_NUM", aggfunc="median").to_dict()[
            "BALCONY_NUM"
        ]
        df.loc[temp.index, "BALCONY_NUM"] = df.loc[temp.index, "BEDROOM_NUM"].map(temp_mapping)

        return df

    def initiate(self) -> pd.DataFrame:
        """
        `Load -> Decode & Clean -> Dump -> Return`
        """
        df = self.__df[_utils.IMPORTANT_INIT_COLS].map(
            lambda x: x.lower() if isinstance(x, str) else x
        )  # type: ignore

        decoder = DecodeFeature(df)
        df = decoder.run_all()

        df = self._clean_df(df)
        df = self._fillna(df)
        df.reset_index(drop=True)

        # Cluster the `FEATURES` and `AMENITIES`
        df["LUXURY_CATEGORY"] = _utils.create_LUXURY_CATEGORY(
            df[_utils.COLS_TO_CLUSTER], n_clusters=3
        )

        # Keep only required columns
        df: pd.DataFrame = df[_utils.REQUIRED_COLS].map(
            lambda x: x.lower() if isinstance(x, str) else x
        )  # type: ignore

        # Check wether the all the required cols are present
        assert sorted(df.columns.tolist()) == sorted(
            _utils.REQUIRED_COLS
        ), "Required column not exists."

        df = self.dump_to_mongodb(df)
        return df
