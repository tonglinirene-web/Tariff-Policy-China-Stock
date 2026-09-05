from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.config import (  # noqa: E402
    ESTIMATION_WINDOW,
    EVENT_WINDOWS,
    EVENTS,
    OUTPUT_FIGURES,
    OUTPUT_TABLES,
    REGRESSION_EVENT,
    REGRESSION_WINDOW,
    VALIDATION_TARGETS,
)
from src.demo_data import make_synthetic_returns  # noqa: E402
from src.event_study import run_event_study  # noqa: E402
from src.regression import (  # noqa: E402
    prepare_regression_data,
    regression_summary_table,
    run_car_regression,
)
from src.statistical_tests import aar_tests, car_tests, validate_caar_targets  # noqa: E402

try:
    from src.visualization import plot_caar_curves, plot_car_distribution  # noqa: E402
except ModuleNotFoundError:
    plot_caar_curves = None
    plot_car_distribution = None


def main() -> None:
    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)
    OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)

    returns = make_synthetic_returns()
    results = run_event_study(
        returns,
        events=EVENTS,
        windows=EVENT_WINDOWS,
        estimation_window=ESTIMATION_WINDOW,
    )

    for name, table in results.items():
        table.to_csv(OUTPUT_TABLES / f"demo_{name}.csv", index=False)

    aar_tests(results["abnormal_returns"]).to_csv(
        OUTPUT_TABLES / "demo_aar_tests.csv", index=False
    )
    car_tests(results["car"]).to_csv(OUTPUT_TABLES / "demo_car_tests.csv", index=False)
    validate_caar_targets(results["aar_caar"], VALIDATION_TARGETS).to_csv(
        OUTPUT_TABLES / "demo_validation.csv", index=False
    )

    window_label = f"[{REGRESSION_WINDOW[0]:+d},{REGRESSION_WINDOW[1]:+d}]"
    regression_df = prepare_regression_data(
        results["car"],
        event_date=REGRESSION_EVENT,
        window_label=window_label,
    )
    fit = run_car_regression(regression_df)
    regression_summary_table(fit).to_csv(
        OUTPUT_TABLES / "demo_april7_regression.csv", index=False
    )

    if plot_caar_curves is not None and plot_car_distribution is not None:
        plot_caar_curves(results["aar_caar"], OUTPUT_FIGURES / "demo_caar_curves.png")
        plot_car_distribution(results["car"], OUTPUT_FIGURES / "demo_car_distribution.png")
    else:
        print("Figure generation skipped because plotting packages are not installed.")

    print("Demo complete. Outputs written to outputs/tables and outputs/figures.")


if __name__ == "__main__":
    main()
