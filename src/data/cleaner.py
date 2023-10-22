from ast import literal_eval
from functools import cached_property
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LinearRegression

from src.core import io

from . import _utils
from ._utils import COLS_TO_ESTIMATE_AREA
from .decode_feature import DecodeFeature

DUMP_DATASET_PATH = Path("data/user/user_data.csv")


class AreaEstimator:
    __slots__ = ("df",)

    def __init__(self, df: pd.DataFrame) -> None:
        estimator_cols = [
            "BUILTUP_SQFT",
            "CARPET_SQFT",
            "SUPERBUILTUP_SQFT",
            "SUPER_SQFT",
        ]
        self.df = df[estimator_cols].copy(True)

    def _impute_with_super_area(self) -> None:
        temp = self.df[
            self.df["BUILTUP_SQFT"].isnull() & self.df["SUPER_SQFT"].notnull()
        ]["SUPER_SQFT"]
        self.df.loc[temp.index, "BUILTUP_SQFT"] = temp

    def _train_model(self, X_cols: list[str]) -> LinearRegression:
        dropped_df = self.df.dropna(subset=X_cols + ["BUILTUP_SQFT"], how="any")
        model = LinearRegression()
        model.fit(dropped_df[X_cols], dropped_df["BUILTUP_SQFT"])
        return model

    def _estimate_area(self, X_cols: list[str]) -> None:
        model = self._train_model(X_cols)

        # Filter dataset to make prediction
        # --- --- --- --- HOW --- --- --- --- #
        # - BUILTUP_SQFT must be null.
        # - CARPET_SQFT/SUPERBUILTUP_SQFT must not be null.
        data_for_pred = self.df[self.df["BUILTUP_SQFT"].isnull()].dropna(subset=X_cols)

        # Calculate the area estimates and inplace them
        estimates = model.predict(data_for_pred[X_cols]).round(0).astype(int)
        self.df.loc[data_for_pred.index, "BUILTUP_SQFT"] = estimates

    def estimate(self) -> pd.Series:
        self._impute_with_super_area()
        self._estimate_area(["CARPET_SQFT", "SUPERBUILTUP_SQFT"])
        self._estimate_area(["CARPET_SQFT"])
        self._estimate_area(["SUPERBUILTUP_SQFT"])
        return self.df["BUILTUP_SQFT"]


class DataCleaner:
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
        """For now just save the dataset into `data/user/` directory."""
        if DUMP_DATASET_PATH.exists():
            old_df = io.read_csv(DUMP_DATASET_PATH)
            df = pd.concat([old_df, df], axis="index")
            df.drop_duplicates(subset=["PROP_ID"], inplace=True)

        df.to_csv(DUMP_DATASET_PATH, index=False)
        return df

    def _fillna(self, df: pd.DataFrame) -> pd.DataFrame:
        df["TOTAL_LANDMARK_COUNT"].fillna(
            round(df["TOTAL_LANDMARK_COUNT"].mean()), inplace=True
        )
        df["AMENITIES_SCORE"].fillna(round(df["AMENITIES_SCORE"].mean()), inplace=True)

        _ = ["residential land", "independent/builder floor"]
        df["FURNISH"].fillna(
            df.query("PROPERTY_TYPE != @_")["FURNISH"].mode()[0], inplace=True
        )

        df["FACING"].fillna(df["FACING"].mode()[0], inplace=True)
        df["AGE"].fillna(df["AGE"].mode()[0], inplace=True)
        df["FLOOR_NUM"].fillna(df["FLOOR_NUM"].mode()[0], inplace=True)
        df["BEDROOM_NUM"].fillna(df["BEDROOM_NUM"].mode()[0], inplace=True)

        # BALCONY_NUM
        temp = df[df["BALCONY_NUM"].isnull()]
        temp_mapping = df.pivot_table(
            "BALCONY_NUM", "BEDROOM_NUM", aggfunc="median"
        ).to_dict()["BALCONY_NUM"]
        df.loc[temp.index, "BALCONY_NUM"] = df.loc[temp.index, "BEDROOM_NUM"].map(
            temp_mapping
        )

        return df

    @cached_property
    def is_v2_dataset(self) -> bool:
        return set(COLS_TO_ESTIMATE_AREA).issubset(self.__df.columns.tolist())

    def initiate(self) -> pd.DataFrame:
        """
        `Load -> Decode & Clean -> Dump -> Return`
        """
        area_estimator = AreaEstimator(self.__df) if self.is_v2_dataset else None

        df = self.__df[_utils.IMPORTANT_INIT_COLS].map(
            lambda x: x.lower() if isinstance(x, str) else x
        )  # type: ignore
        decoder = DecodeFeature(df)

        if area_estimator is not None:
            df = decoder.run_all("decode_AREA")
            df["AREA"] = area_estimator.estimate()
        else:
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
