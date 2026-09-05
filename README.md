# Tariff Policy and China A-Share Stock Reactions

This repository presents a reproducible empirical finance project on how Chinese A-share stocks reacted to the April 2025 U.S. tariff-policy announcements.

It is designed as a public portfolio repository: the code, methodology, project structure, and demonstration workflow are included, while licensed CSMAR raw data are intentionally excluded.

## Project Highlights

- Builds a market-model event-study pipeline for policy-announcement shocks.
- Computes abnormal returns, AAR, CAR, and CAAR across multiple event windows.
- Runs cross-sectional regressions to explain firm-level heterogeneity.
- Separates private licensed data from public reproducible code.
- Includes a synthetic-data demo so reviewers can run the project without access to CSMAR.

## Research Design

The reconstructed pipeline follows the thesis methodology:

- Events: April 2, April 7, and April 9, 2025 tariff-policy announcements.
- Method: market-model event study.
- Estimation window: 120 trading days before the event window.
- Event windows: `[-1,+1]`, `[-3,+3]`, and `[-5,+5]`.
- Main outputs: abnormal returns, average abnormal returns, cumulative abnormal returns, cumulative average abnormal returns, t-tests, and Chapter 4 tables/figures.
- Cross-sectional regression: April 7 CAR as the dependent variable, with `Beta`, `Size`, and `IdioVol` as explanatory variables.

Known validation target from the thesis draft:

- April 7, 2025 `[-1,+1]` CAAR should be approximately `-5.46%`, subject to matching the exact CSMAR sample and preprocessing rules.

## Repository Structure

```text
.
├── data/
│   ├── raw/              # private CSMAR exports, ignored by Git
│   ├── processed/        # cleaned intermediate data, ignored by Git
│   └── README.md
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   ├── 02_event_study.ipynb
│   ├── 03_regression.ipynb
│   └── 04_figures_tables.ipynb
├── outputs/
│   ├── figures/          # generated charts, ignored by Git
│   └── tables/           # generated CSV tables, ignored by Git
├── src/
│   ├── config.py
│   ├── data_preparation.py
│   ├── event_study.py
│   ├── market_model.py
│   ├── regression.py
│   ├── statistical_tests.py
│   └── visualization.py
└── tests/
```

## Data Availability

The original thesis data come from CSMAR and are not included in this public repository because of licensing restrictions. The repository therefore provides:

- Source code for the full analysis workflow.
- Documentation of the expected input schema.
- Synthetic sample data generation for demonstration.
- Empty `data/raw/` and `data/processed/` folders for private local use.

Place private CSMAR or equivalent source files in `data/raw/`. The pipeline expects firm-level daily stock returns and a daily market/index return series. If variable names differ across exports, update the column mapping in `src/data_preparation.py`.

Minimum required normalized columns:

- `firm_id`: stock identifier.
- `date`: trading date.
- `stock_return`: daily stock return in decimal form, for example `-0.023` for `-2.3%`.
- `market_return`: daily market/index return in decimal form.
- Optional regression fields: `market_cap`, `size`, `beta`, `idio_vol`.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the public demo:

```bash
python scripts/run_demo.py
```

The demo creates synthetic returns, runs the event-study pipeline, estimates the April 7 regression, and writes example outputs to `outputs/tables/` and `outputs/figures/`.

For the private thesis replication, add the licensed data locally and run the notebooks in order:

1. `notebooks/01_data_preparation.ipynb`
2. `notebooks/02_event_study.ipynb`
3. `notebooks/03_regression.ipynb`
4. `notebooks/04_figures_tables.ipynb`

## Reproducibility Notes

Raw CSMAR data are intentionally ignored because they may be licensed. The code and notebooks can be shared publicly, but the raw data should be supplied locally by the researcher.

When the original CSMAR files are available, regenerate the event-study tables and compare them to the reported Chapter 4 values before making final thesis claims.

## Portfolio Note

This project demonstrates empirical research implementation rather than data redistribution. The public repository is suitable for showcasing Python, financial econometrics, research design, documentation, and reproducible workflow skills while respecting third-party data licenses.
