from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_caar_curves(aar_caar_df: pd.DataFrame, output_path: str | Path | None = None):
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(9, 5))
    plot_df = aar_caar_df.copy()
    plot_df["event_date"] = pd.to_datetime(plot_df["event_date"]).dt.strftime("%Y-%m-%d")
    sns.lineplot(
        data=plot_df,
        x="event_time",
        y="caar",
        hue="event_date",
        style="window",
        marker="o",
        ax=ax,
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Trading days relative to event")
    ax.set_ylabel("CAAR")
    ax.set_title("Cumulative Average Abnormal Returns")
    fig.tight_layout()
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
    return fig, ax


def plot_car_distribution(car_df: pd.DataFrame, output_path: str | Path | None = None):
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data=car_df, x="car", hue="window", kde=True, ax=ax)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("CAR")
    ax.set_title("Firm-Level Cumulative Abnormal Returns")
    fig.tight_layout()
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300)
    return fig, ax
