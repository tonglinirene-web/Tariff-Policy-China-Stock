# Data Directory

Use this folder for local CSMAR data and cleaned intermediate datasets.

## Raw Data

Put original CSMAR exports in `data/raw/`. These files are ignored by Git.

Expected inputs:

- Firm-level daily A-share returns.
- Daily market or benchmark index returns.
- Firm-level characteristics for the regression, especially market capitalization if `Size` must be calculated.

## Processed Data

Cleaned files produced by the notebooks or scripts should be written to `data/processed/`. These are also ignored by Git so the repository can stay public without redistributing licensed data.
