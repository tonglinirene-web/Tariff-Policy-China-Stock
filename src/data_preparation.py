from __future__ import annotations

from pathlib import Path
from typing import Mapping

import numpy as np
import pandas as pd


DEFAULT_COLUMN_MAP = {
    "Stkcd": "firm_id",
    "stkcd": "firm_id",
    "Symbol": "firm_id",
    "symbol": "firm_id",
    "Trddt": "date",
    "trddt": "date",
    "Date": "date",
    "date": "date",
    "Dretwd": "stock_return",
    "dretwd": "stock_return",
    "Return": "stock_return",
    "ret": "stock_return",
    "Mretwd": "market_return",
    "mretwd": "market_return",
    "MarketReturn": "market_return",
    "market_return": "market_return",
    "Msmvosd": "market_cap",
    "market_cap": "market_cap",
}

REQUIRED_COLUMNS = ["firm_id", "date", "stock_return", "market_return"]


def read_table(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".txt", ".tsv"}:
        return pd.read_csv(path, sep="\t")
    raise ValueError(f"Unsupported file type: {path.suffix}")


def standardize_columns(
    df: pd.DataFrame,
    column_map: Mapping[str, str] | None = None,
) -> pd.DataFrame:
    mapping = dict(DEFAULT_COLUMN_MAP)
    if column_map:
        mapping.update(column_map)
    return df.rename(columns={col: mapping[col] for col in df.columns if col in mapping})


def clean_returns(
    df: pd.DataFrame,
    column_map: Mapping[str, str] | None = None,
    drop_missing: bool = True,
) -> pd.DataFrame:
    cleaned = standardize_columns(df, column_map)
    missing = [col for col in REQUIRED_COLUMNS if col not in cleaned.columns]
    if missing:
        raise ValueError(f"Missing required columns after standardization: {missing}")

    cleaned = cleaned.copy()
    cleaned["firm_id"] = cleaned["firm_id"].astype(str).str.zfill(6)
    cleaned["date"] = pd.to_datetime(cleaned["date"])
    cleaned["stock_return"] = pd.to_numeric(cleaned["stock_return"], errors="coerce")
    cleaned["market_return"] = pd.to_numeric(cleaned["market_return"], errors="coerce")

    if "market_cap" in cleaned.columns:
        cleaned["market_cap"] = pd.to_numeric(cleaned["market_cap"], errors="coerce")
        cleaned["size"] = np.log(cleaned["market_cap"].where(cleaned["market_cap"] > 0))

    if drop_missing:
        cleaned = cleaned.dropna(subset=REQUIRED_COLUMNS)

    cleaned = cleaned.sort_values(["firm_id", "date"]).reset_index(drop=True)
    return cleaned


def load_and_clean_returns(
    stock_returns_path: str | Path,
    market_returns_path: str | Path | None = None,
    stock_column_map: Mapping[str, str] | None = None,
    market_column_map: Mapping[str, str] | None = None,
) -> pd.DataFrame:
    stock_df = standardize_columns(read_table(stock_returns_path), stock_column_map)

    if market_returns_path is not None:
        market_df = standardize_columns(read_table(market_returns_path), market_column_map)
        market_df["date"] = pd.to_datetime(market_df["date"])
        stock_df["date"] = pd.to_datetime(stock_df["date"])
        stock_df = stock_df.merge(
            market_df[["date", "market_return"]],
            on="date",
            how="left",
            suffixes=("", "_market"),
        )
        if "market_return_market" in stock_df.columns:
            stock_df["market_return"] = stock_df["market_return"].fillna(
                stock_df["market_return_market"]
            )
            stock_df = stock_df.drop(columns=["market_return_market"])

    return clean_returns(stock_df)


def save_processed(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
