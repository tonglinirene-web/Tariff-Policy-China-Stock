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
FIRST_EVENT_DATE = "2025-04-02"
ESTIMATION_WINDOW = (-120, -21)
ESTIMATION_LENGTH = 120
REGRESSION_EVENT = "2025-04-07"
REGRESSION_WINDOW = (-1, 1)
ANALYSIS_START_DATE = "2024-12-01"
ANALYSIS_END_DATE = "2025-05-31"

VALIDATION_TARGETS = {
    ("2025-04-02", -1, 1): {
        "metric": "CAAR",
        "expected": 0.0111,
        "tolerance": 0.0025,
        "note": "Reported Chapter 4 target: April 2 [-1,+1] CAAR approximately +1.11%.",
    },
    ("2025-04-07", -1, 1): {
        "metric": "CAAR",
        "expected": -0.0546,
        "tolerance": 0.0025,
        "note": "Reported Chapter 4 target: April 7 [-1,+1] CAAR approximately -5.46%.",
    },
    ("2025-04-09", -1, 1): {
        "metric": "CAAR",
        "expected": 0.0149,
        "tolerance": 0.0025,
        "note": "Reported Chapter 4 target: April 9 [-1,+1] CAAR approximately +1.49%.",
    },
    ("2025-04-02", -3, 3): {
        "metric": "CAAR",
        "expected": -0.0589,
        "tolerance": 0.0025,
        "note": "Reported robustness target: April 2 [-3,+3] CAAR approximately -5.89%.",
    },
    ("2025-04-02", -5, 5): {
        "metric": "CAAR",
        "expected": -0.0623,
        "tolerance": 0.0025,
        "note": "Reported robustness target: April 2 [-5,+5] CAAR approximately -6.23%.",
    },
    ("2025-04-07", -3, 3): {
        "metric": "CAAR",
        "expected": -0.0156,
        "tolerance": 0.0025,
        "note": "Reported robustness target: April 7 [-3,+3] CAAR approximately -1.56%.",
    },
    ("2025-04-07", -5, 5): {
        "metric": "CAAR",
        "expected": -0.0143,
        "tolerance": 0.0025,
        "note": "Reported robustness target: April 7 [-5,+5] CAAR approximately -1.43%.",
    },
    ("2025-04-09", -3, 3): {
        "metric": "CAAR",
        "expected": -0.0101,
        "tolerance": 0.0025,
        "note": "Reported robustness target: April 9 [-3,+3] CAAR approximately -1.01%.",
    },
    ("2025-04-09", -5, 5): {
        "metric": "CAAR",
        "expected": -0.0094,
        "tolerance": 0.0025,
        "note": "Reported robustness target: April 9 [-5,+5] CAAR approximately -0.94%.",
    },
}

REGRESSION_TARGETS = {
    "event_date": "2025-04-07",
    "window": "[-1,+1]",
    "observations": 5461,
    "r_squared": 0.198,
    "coefficients": {
        "const": -0.1622,
        "beta": 3.1765,
        "size": 0.0065,
        "idio_vol": -1.0092,
    },
}
