from typing import Any

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import FunctionTransformer, Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler


def get_preprocessor(
    ord_cols: dict[str, list[str | int]] | None,
    ohe_cols: list[str] | None,
) -> ColumnTransformer:
    transformers: list[tuple[str, Any, list[str]]] = [
        (
            "log1p_area",
            FunctionTransformer(func=np.log1p, inverse_func=np.expm1, validate=True),
            ["AREA"],
        )
    ]

    if ord_cols:
        transformers.append(
            (
                "ord",
                OrdinalEncoder(categories=list(ord_cols.values())),
                list(ord_cols.keys()),
            )
        )

    if ohe_cols:
        transformers.append(
            (
                "ohe",
                # FIXME: Improve the OneHotEncoding.
                # TODO: Remove `handle_unknown` parameter and do something else.
                OneHotEncoder(sparse_output=False, handle_unknown="ignore"),
                ohe_cols,
            )
        )

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")
    return preprocessor


def create_pipeline(preprocessor: ColumnTransformer | None) -> Pipeline:
    pipe = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("reg_model", RandomForestRegressor(n_estimators=500)),
        ]
    )

    if preprocessor:
        pipe.steps.insert(0, ("preprocessor", preprocessor))

    return pipe
