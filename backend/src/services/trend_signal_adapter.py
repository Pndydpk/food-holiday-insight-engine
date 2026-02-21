# src/services/trend_signal_adapter.py

from src.schemas.trend_signal_schema import TrendSignal

def mock_series_to_trend_signal(entity: str, series: list[int], window_hours: int = 24) -> TrendSignal:
    mention_count = int(sum(series))
    weighted_engagement = float(sum(series) * 0.6)  # placeholder weighting
    creator_velocity = float((series[-1] - series[0]) / max(len(series), 1))

    geo_distribution = {
        "US": 0.7,
        "CA": 0.3
    }

    return TrendSignal(
        trend=entity,
        window_hours=window_hours,
        mention_count=mention_count,
        weighted_engagement=weighted_engagement,
        creator_velocity=creator_velocity,
        geo_distribution=geo_distribution
    )
