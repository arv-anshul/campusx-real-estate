from pathlib import Path

import pandas as pd


def read_csv(fp: Path, **kwargs) -> pd.DataFrame:
    """Uses `pd.read_csv()` to read the `fp`."""
    df = pd.read_csv(fp, **kwargs)
    return df
