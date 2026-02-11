# src/schemas/trend_signal_schema.py

from pydantic import BaseModel
from typing import Dict

class TrendSignal(BaseModel):
    trend: str                 # e.g., "birria tacos", "bubble tea"
    window_hours: int         # aggregation window size
    mention_count: int        # total mentions in window
    weighted_engagement: float  # likes/comments/shares weighted score
    creator_velocity: float  # how fast creators are picking this up
    geo_distribution: Dict[str, float]  # {"US": 0.7, "CA": 0.3}
