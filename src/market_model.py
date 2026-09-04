from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class MarketModelResult:
    firm_id: str
    alpha: float
    beta: float
    idio_vol: float
    n_obs: int


def fit_market_model(estimation_df: pd.DataFrame) -> MarketModelResult:
    required = {"firm_id", "stock_return", "market_return"}
    missing = required.difference(estimation_df.columns)
    if missing:
        raise ValueError(f"Missing columns for market model: {sorted(missing)}")
    if estimation_df["firm_id"].nunique() != 1:
        raise ValueError("fit_market_model expects one firm at a time.")

    model_df = estimation_df.dropna(subset=["stock_return", "market_return"])
    if len(model_df) < 30:
        raise ValueError("At least 30 estimation observations are required.")

    x = np.column_stack([np.ones(len(model_df)), model_df["market_return"].to_numpy()])
    y = model_df["stock_return"].to_numpy()
    alpha, beta = np.linalg.lstsq(x, y, rcond=None)[0]
    residuals = y - x @ np.array([alpha, beta])
    residual_std = float(pd.Series(residuals).std(ddof=1))

    return MarketModelResult(
        firm_id=str(model_df["firm_id"].iloc[0]),
        alpha=float(alpha),
        beta=float(beta),
        idio_vol=residual_std,
        n_obs=int(len(model_df)),
    )


def expected_returns(df: pd.DataFrame, model: MarketModelResult) -> pd.Series:
    return model.alpha + model.beta * df["market_return"]


def abnormal_returns(df: pd.DataFrame, model: MarketModelResult) -> pd.Series:
    return df["stock_return"] - expected_returns(df, model)


def summarize_models(models: list[MarketModelResult]) -> pd.DataFrame:
    return pd.DataFrame([model.__dict__ for model in models])
