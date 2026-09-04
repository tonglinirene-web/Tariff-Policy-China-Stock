import numpy as np
import pandas as pd

from src.event_study import EventWindow, run_event_study
from src.statistical_tests import validate_caar_targets


def make_synthetic_returns():
    dates = pd.bdate_range("2024-09-01", "2025-04-15")
    event_date = pd.Timestamp("2025-04-07")
    rows = []
    rng = np.random.default_rng(7)
    for firm_num in range(10):
        beta = 0.8 + firm_num * 0.03
        for date in dates:
            market_return = 0.001 * np.sin(len(rows) / 15)
            shock = -0.0546 / 3 if abs(np.busday_count(event_date.date(), date.date())) <= 1 else 0
            stock_return = 0.0002 + beta * market_return + shock + rng.normal(0, 0.004)
            rows.append(
                {
                    "firm_id": f"{firm_num:06d}",
                    "date": date,
                    "stock_return": stock_return,
                    "market_return": market_return,
                    "size": 20 + firm_num * 0.1,
                }
            )
    return pd.DataFrame(rows)


def test_event_study_outputs_are_created():
    df = make_synthetic_returns()
    result = run_event_study(df, ["2025-04-07"], [(-1, 1)], estimation_length=120)
    assert not result["abnormal_returns"].empty
    assert not result["aar_caar"].empty
    assert not result["car"].empty
    assert {"firm_id", "car", "beta", "idio_vol", "size"}.issubset(result["car"].columns)


def test_validation_table_reports_targets():
    df = make_synthetic_returns()
    result = run_event_study(df, ["2025-04-07"], [EventWindow(-1, 1)], estimation_length=120)
    validation = validate_caar_targets(
        result["aar_caar"],
        {("2025-04-07", -1, 1): {"expected": -0.0546, "tolerance": 0.02}},
    )
    assert validation.loc[0, "metric"] == "CAAR"
    assert validation.loc[0, "within_tolerance"]
