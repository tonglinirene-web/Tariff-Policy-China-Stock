from __future__ import annotations

import numpy as np
import pandas as pd


def make_synthetic_returns(
    start: str = "2024-08-01",
    end: str = "2025-04-30",
    n_firms: int = 120,
    seed: int = 2025,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start, end)
    event_shocks = {
        pd.Timestamp("2025-04-02"): 0.0037,
        pd.Timestamp("2025-04-03"): 0.0037,
        pd.Timestamp("2025-04-04"): 0.0037,
        pd.Timestamp("2025-04-07"): -0.0182,
        pd.Timestamp("2025-04-08"): -0.0182,
        pd.Timestamp("2025-04-09"): -0.0182,
        pd.Timestamp("2025-04-10"): 0.0050,
    }

    market_returns = pd.Series(
        rng.normal(0.0002, 0.009, len(dates)),
        index=dates,
        name="market_return",
    )
    rows = []
    for firm_num in range(n_firms):
        firm_id = f"{firm_num + 1:06d}"
        beta = rng.normal(1.0, 0.25)
        size = rng.normal(21.5, 1.0)
        idio_scale = rng.uniform(0.008, 0.028)
        for date in dates:
            market_return = market_returns.loc[date]
            shock = event_shocks.get(date, 0.0)
            sensitivity = 1.0 + 0.25 * (idio_scale > 0.018) - 0.05 * (size > 22)
            stock_return = (
                0.0001
                + beta * market_return
                + sensitivity * shock
                + rng.normal(0, idio_scale)
            )
            rows.append(
                {
                    "firm_id": firm_id,
                    "date": date,
                    "stock_return": stock_return,
                    "market_return": market_return,
                    "size": size,
                }
            )
    return pd.DataFrame(rows)
