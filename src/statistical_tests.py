from __future__ import annotations

import numpy as np
import pandas as pd

try:
    from scipy import stats
except ModuleNotFoundError:
    stats = None


def one_sample_ttest(values: pd.Series, null: float = 0.0) -> dict[str, float]:
    sample = pd.Series(values).dropna()
    if len(sample) < 2:
        return {"mean": np.nan, "t_stat": np.nan, "p_value": np.nan, "n": int(len(sample))}
    t_stat = (sample.mean() - null) / (sample.std(ddof=1) / np.sqrt(len(sample)))
    if stats is not None:
        _, p_value = stats.ttest_1samp(sample, popmean=null)
    else:
        p_value = np.nan
    return {
        "mean": float(sample.mean()),
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "n": int(len(sample)),
    }


def car_tests(car_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for keys, group in car_df.groupby(["event_date", "window"]):
        event_date, window = keys
        result = one_sample_ttest(group["car"])
        rows.append({"event_date": event_date, "window": window, **result})
    return pd.DataFrame(rows)


def aar_tests(abnormal_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for keys, group in abnormal_df.groupby(["event_date", "window", "event_time"]):
        event_date, window, event_time = keys
        result = one_sample_ttest(group["abnormal_return"])
        rows.append(
            {
                "event_date": event_date,
                "window": window,
                "event_time": event_time,
                **result,
            }
        )
    return pd.DataFrame(rows)


def validate_caar_targets(
    aar_caar_df: pd.DataFrame,
    validation_targets: dict[tuple[str, int, int], dict],
) -> pd.DataFrame:
    rows = []
    for (event_date, start, end), target in validation_targets.items():
        label = f"[{start:+d},{end:+d}]"
        event_ts = pd.Timestamp(event_date)
        subset = aar_caar_df.loc[
            (aar_caar_df["event_date"] == event_ts)
            & (aar_caar_df["window"] == label)
            & (aar_caar_df["event_time"] == end)
        ]
        actual = float(subset["caar"].iloc[0]) if not subset.empty else np.nan
        expected = float(target["expected"])
        tolerance = float(target.get("tolerance", 0.0))
        rows.append(
            {
                "event_date": event_ts,
                "window": label,
                "metric": target.get("metric", "CAAR"),
                "actual": actual,
                "expected": expected,
                "difference": actual - expected if not np.isnan(actual) else np.nan,
                "within_tolerance": abs(actual - expected) <= tolerance
                if not np.isnan(actual)
                else False,
                "note": target.get("note", ""),
            }
        )
    return pd.DataFrame(rows)
