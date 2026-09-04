from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from .market_model import MarketModelResult, abnormal_returns, fit_market_model


@dataclass(frozen=True)
class EventWindow:
    start: int
    end: int

    @property
    def label(self) -> str:
        return f"[{self.start:+d},{self.end:+d}]"


def add_event_time(df: pd.DataFrame, event_date: str | pd.Timestamp) -> pd.DataFrame:
    event_ts = pd.Timestamp(event_date)
    trading_dates = (
        pd.Series(df["date"].drop_duplicates().sort_values().to_numpy())
        .reset_index(drop=True)
        .to_frame(name="date")
    )
    if event_ts not in set(trading_dates["date"]):
        future_dates = trading_dates.loc[trading_dates["date"] >= event_ts, "date"]
        if future_dates.empty:
            raise ValueError(f"No trading date on or after event date {event_ts.date()}.")
        event_ts = future_dates.iloc[0]

    event_index = trading_dates.index[trading_dates["date"] == event_ts][0]
    trading_dates["event_time"] = trading_dates.index - event_index
    return df.merge(trading_dates, on="date", how="left")


def estimation_sample(
    event_df: pd.DataFrame,
    estimation_length: int = 120,
    gap: int = 1,
) -> pd.DataFrame:
    min_event_time = -gap - estimation_length
    max_event_time = -gap - 1
    return event_df.loc[
        event_df["event_time"].between(min_event_time, max_event_time)
    ].copy()


def event_sample(event_df: pd.DataFrame, window: EventWindow) -> pd.DataFrame:
    return event_df.loc[event_df["event_time"].between(window.start, window.end)].copy()


def compute_firm_abnormal_returns(
    df: pd.DataFrame,
    event_date: str | pd.Timestamp,
    window: EventWindow,
    estimation_length: int = 120,
    minimum_estimation_obs: int = 60,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    event_df = add_event_time(df, event_date)
    firm_event_rows = []
    models: list[MarketModelResult] = []

    for firm_id, firm_df in event_df.groupby("firm_id"):
        estimate_df = estimation_sample(firm_df, estimation_length=estimation_length)
        if len(estimate_df.dropna(subset=["stock_return", "market_return"])) < minimum_estimation_obs:
            continue
        model = fit_market_model(estimate_df)
        model_event_df = event_sample(firm_df, window)
        if model_event_df.empty:
            continue
        model_event_df = model_event_df.copy()
        model_event_df["event_date"] = pd.Timestamp(event_date)
        model_event_df["window"] = window.label
        model_event_df["alpha"] = model.alpha
        model_event_df["beta"] = model.beta
        model_event_df["idio_vol"] = model.idio_vol
        model_event_df["abnormal_return"] = abnormal_returns(model_event_df, model)
        firm_event_rows.append(model_event_df)
        models.append(model)

    if not firm_event_rows:
        return pd.DataFrame(), pd.DataFrame()
    return pd.concat(firm_event_rows, ignore_index=True), pd.DataFrame([m.__dict__ for m in models])


def summarize_event_window(abnormal_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if abnormal_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    aar = (
        abnormal_df.groupby(["event_date", "window", "event_time"], as_index=False)
        .agg(
            aar=("abnormal_return", "mean"),
            n_firms=("firm_id", "nunique"),
            std_ar=("abnormal_return", "std"),
        )
        .sort_values(["event_date", "window", "event_time"])
    )
    aar["caar"] = aar.groupby(["event_date", "window"])["aar"].cumsum()

    car = (
        abnormal_df.groupby(["event_date", "window", "firm_id"], as_index=False)
        .agg(
            car=("abnormal_return", "sum"),
            beta=("beta", "first"),
            idio_vol=("idio_vol", "first"),
        )
    )
    if "size" in abnormal_df.columns:
        size = abnormal_df.groupby(["event_date", "window", "firm_id"], as_index=False).agg(
            size=("size", "last")
        )
        car = car.merge(size, on=["event_date", "window", "firm_id"], how="left")

    return aar, car


def run_event_study(
    df: pd.DataFrame,
    events: Iterable,
    windows: Iterable[tuple[int, int] | EventWindow],
    estimation_length: int = 120,
) -> dict[str, pd.DataFrame]:
    abnormal_frames = []
    model_frames = []
    for event in events:
        event_date = getattr(event, "date", event)
        for window_value in windows:
            window = (
                window_value
                if isinstance(window_value, EventWindow)
                else EventWindow(*window_value)
            )
            abnormal_df, models_df = compute_firm_abnormal_returns(
                df,
                event_date=event_date,
                window=window,
                estimation_length=estimation_length,
            )
            if not abnormal_df.empty:
                abnormal_frames.append(abnormal_df)
            if not models_df.empty:
                models_df["event_date"] = pd.Timestamp(event_date)
                models_df["window"] = window.label
                model_frames.append(models_df)

    abnormal = pd.concat(abnormal_frames, ignore_index=True) if abnormal_frames else pd.DataFrame()
    models = pd.concat(model_frames, ignore_index=True) if model_frames else pd.DataFrame()
    aar, car = summarize_event_window(abnormal)
    return {"abnormal_returns": abnormal, "aar_caar": aar, "car": car, "models": models}
