from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

try:
    import statsmodels.api as sm
except ModuleNotFoundError:
    sm = None


@dataclass
class SimpleRegressionResult:
    params: pd.Series
    bse: pd.Series
    tvalues: pd.Series
    pvalues: pd.Series

    def summary(self) -> str:
        return regression_summary_table(self).to_string(index=False)


def prepare_regression_data(
    car_df: pd.DataFrame,
    event_date: str,
    window_label: str,
    dependent: str = "car",
    regressors: tuple[str, ...] = ("beta", "size", "idio_vol"),
) -> pd.DataFrame:
    event_ts = pd.Timestamp(event_date)
    subset = car_df.loc[
        (car_df["event_date"] == event_ts) & (car_df["window"] == window_label)
    ].copy()
    required = [dependent, *regressors]
    missing = [col for col in required if col not in subset.columns]
    if missing:
        raise ValueError(f"Missing regression columns: {missing}")
    return subset.dropna(subset=required)


def run_car_regression(
    regression_df: pd.DataFrame,
    dependent: str = "car",
    regressors: tuple[str, ...] = ("beta", "size", "idio_vol"),
    robust_cov: str = "HC1",
):
    if sm is None:
        x = regression_df[list(regressors)].copy()
        x.insert(0, "const", 1.0)
        y = regression_df[dependent].to_numpy()
        x_values = x.to_numpy(dtype=float)
        params = np.linalg.lstsq(x_values, y, rcond=None)[0]
        residuals = y - x_values @ params
        dof = max(len(y) - x_values.shape[1], 1)
        sigma2 = float((residuals @ residuals) / dof)
        covariance = sigma2 * np.linalg.pinv(x_values.T @ x_values)
        bse = np.sqrt(np.diag(covariance))
        index = x.columns
        params_s = pd.Series(params, index=index)
        bse_s = pd.Series(bse, index=index)
        return SimpleRegressionResult(
            params=params_s,
            bse=bse_s,
            tvalues=params_s / bse_s,
            pvalues=pd.Series(np.nan, index=index),
        )

    y = regression_df[dependent]
    x = sm.add_constant(regression_df[list(regressors)])
    fit = sm.OLS(y, x).fit(cov_type=robust_cov)
    return fit


def regression_summary_table(fit) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "coef": fit.params,
            "std_err": fit.bse,
            "t_stat": fit.tvalues,
            "p_value": fit.pvalues,
        }
    ).reset_index(names="variable")
