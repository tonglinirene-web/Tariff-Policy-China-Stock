# Tariff Policy and China A-Share Stock Reactions

This repository reconstructs the empirical code for a thesis event study on Chinese A-share market reactions to 2025 U.S. tariff-policy announcements.

The project is organized so the licensed CSMAR source files remain outside Git, while the cleaning, event-study, regression, and output-generation steps are reproducible.

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

## Expected Input Data

Place CSMAR or equivalent source files in `data/raw/`. The pipeline expects firm-level daily stock returns and a daily market/index return series. If variable names differ across exports, update the column mapping in `src/data_preparation.py`.

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

Then run the notebooks in order, or call the source modules from your own script.

## Reproducibility Notes

Raw CSMAR data are intentionally ignored because they may be licensed. The code and notebooks can be shared publicly, but the raw data should be supplied locally by the researcher.

When the original CSMAR files are available, regenerate the event-study tables and compare them to the reported Chapter 4 values before making final thesis claims.
