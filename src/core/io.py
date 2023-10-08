from pathlib import Path
from typing import Any

import dill
import pandas as pd
import streamlit as st

from src.typing import stop as _stop


def read_csv(fp: Path, **kwargs) -> pd.DataFrame:
    """Uses `pd.read_csv()` to read the `fp`."""
    if not fp.exists():
        st.exception(FileNotFoundError(f"'{fp}' not exists."))
        _stop()

    df = pd.read_csv(fp, **kwargs)
    return df


def dill_load(fp: Path) -> Any:
    with fp.open("rb") as f:
        return dill.load(f)


def dill_dump(obj: Any, fp: Path) -> Any:
    with fp.open("wb") as f:
        return dill.dump(obj, f)
