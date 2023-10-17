import pandas as pd

from src.core.errors import DataValidationError
from src.data import _utils


def validate_dataset(df: pd.DataFrame):
    if sorted(df.columns.tolist()) == sorted(_utils.IMPORTANT_INIT_COLS):
        raise DataValidationError(
            "Dataset must have the important initial columns. "
            f"Column: {set(df.columns.tolist()) & set(_utils.IMPORTANT_INIT_COLS)} not present."
        )

    if df["PRICE"].isnull().sum() != 0:
        raise DataValidationError("PRICE column contains null values.")
