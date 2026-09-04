from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUT_TABLES = PROJECT_ROOT / "outputs" / "tables"
OUTPUT_FIGURES = PROJECT_ROOT / "outputs" / "figures"


@dataclass(frozen=True)
class EventDefinition:
    name: str
    date: str
    description: str


EVENTS = [
    EventDefinition(
        name="2025-04-02",
        date="2025-04-02",
        description="Initial U.S. tariff-policy announcement.",
    ),
    EventDefinition(
        name="2025-04-07",
        date="2025-04-07",
        description="Detailed tariff-policy escalation announcement.",
    ),
    EventDefinition(
        name="2025-04-09",
        date="2025-04-09",
        description="Policy confirmation or follow-up announcement.",
    ),
]

EVENT_WINDOWS = [(-1, 1), (-3, 3), (-5, 5)]
ESTIMATION_LENGTH = 120
REGRESSION_EVENT = "2025-04-07"
REGRESSION_WINDOW = (-1, 1)

VALIDATION_TARGETS = {
    ("2025-04-07", -1, 1): {
        "metric": "CAAR",
        "expected": -0.0546,
        "tolerance": 0.0025,
        "note": "Reported Chapter 4 target: approximately -5.46%.",
    }
}
