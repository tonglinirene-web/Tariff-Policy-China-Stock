# Data Directory

Use this folder for local CSMAR data and cleaned intermediate datasets.

## Raw Data

Put original CSMAR exports in `data/raw/`. These files are ignored by Git and should not be uploaded to a public repository.

Expected inputs:

- Firm-level daily A-share returns.
- Daily market or benchmark index returns.
- Firm-level characteristics for the regression, especially market capitalization if `Size` must be calculated.

Expected normalized schema:

| Column | Meaning |
| --- | --- |
| `firm_id` | Stock identifier |
| `date` | Trading date |
| `stock_return` | Daily stock return in decimal form |
| `market_return` | Daily benchmark return in decimal form |
| `market_cap` or `size` | Firm size proxy |

## Processed Data

Cleaned files produced by the notebooks or scripts should be written to `data/processed/`. These are also ignored by Git so the repository can stay public without redistributing licensed data.

## Public Demo Data

For portfolio review, the repository can generate synthetic data through `scripts/run_demo.py`. These data are artificial and exist only to demonstrate the analysis workflow.
