from pathlib import Path

import pandas as pd
import streamlit as st


def read_csv(fp: Path, **kwargs) -> pd.DataFrame:
    """Uses `pd.read_csv()` to read the `fp`."""
    if not fp.exists():
        st.exception(FileNotFoundError(f"'{fp}' not exists."))
        st.stop()

    df = pd.read_csv(fp, **kwargs)
    return df
