# src/services/social_ingestion_service.py

from typing import List
from src.schemas.social_signal_schema import SocialSignal
from src.schemas.trend_signal_schema import TrendSignal


def ingest_mock_social_signals() -> List[SocialSignal]:
    """
    Temporary mock ingestion.
    Later this will be replaced by real scraper outputs.
    """
    return [
        SocialSignal(
            platform="tiktok",
            post_id="t1",
            timestamp="2026-02-10T10:00:00Z",
            text="Nachos with extra cheese!",
            hashtags=["#nachos", "#snacktime"],
            food_entities=["nachos"],
            engagement={"likes": 1200, "comments": 84, "shares": 22},
            creator_followers=54000,
            geo="US"
        ),
        SocialSignal(
            platform="instagram",
            post_id="i1",
            timestamp="2026-02-10T11:00:00Z",
            text="Late night nachos craving 😋",
            hashtags=["#nachos", "#midnightmunchies"],
            food_entities=["nachos"],
            engagement={"likes": 980, "comments": 63, "shares": 15},
            creator_followers=21000,
            geo="US"
        ),
        SocialSignal(
            platform="youtube",
            post_id="y1",
            timestamp="2026-02-10T12:00:00Z",
            text="Street style loaded nachos recipe",
            hashtags=["#nachos", "#streetfood"],
            food_entities=["nachos"],
            engagement={"likes": 1500, "comments": 120, "shares": 40},
            creator_followers=88000,
            geo="US"
        ),
    ]


def aggregate_to_trend_signal(signals: List[SocialSignal]) -> List[TrendSignal]:
    """
    Very naive v1 aggregation:
    groups by food entity and sums engagement.
    """
    trend_map = {}

    for s in signals:
        for food in s.food_entities:
            if food not in trend_map:
                trend_map[food] = {
                    "mention_count": 0,
                    "weighted_engagement": 0.0,
                    "creator_velocity": 0.0
                }

            trend_map[food]["mention_count"] += 1
            trend_map[food]["weighted_engagement"] += (
                s.engagement.get("likes", 0)
                + s.engagement.get("comments", 0)
                + s.engagement.get("shares", 0)
            )

    trends: List[TrendSignal] = []

    for food, metrics in trend_map.items():
        trends.append(
            TrendSignal(
                trend=food,
                window_hours=24,
                mention_count=metrics["mention_count"],
                weighted_engagement=float(metrics["weighted_engagement"]),
                creator_velocity=0.5,  # placeholder
                geo_distribution={"US": 1.0}
            )
        )

    return trends
def social_signals_to_series(signals, days: int = 14):
    """
    Convert aggregated social signals into a simple pseudo time series.
    This is a temporary adapter until real historical social time series exist.
    """
    if not signals:
        return [0] * days

    total_engagement = sum(
        s.engagement.get("likes", 0)
        + s.engagement.get("comments", 0)
        + s.engagement.get("shares", 0)
        for s in signals
    )

    # Create a rising series ending at total_engagement (very naive v1)
    base = max(int(total_engagement / days), 1)
    series = [base + i * int(base * 0.2) for i in range(days)]

    return series

def compute_platform_momentum(signals):
    """
    Very simple v1 momentum per platform based on engagement totals.
    Returns something like:
    {
        "tiktok": 1.2,
        "instagram": 0.6
    }
    """
    platform_totals = {}

    for s in signals:
        engagement = (
            s.engagement.get("likes", 0)
            + s.engagement.get("comments", 0)
            + s.engagement.get("shares", 0)
        )

        platform_totals.setdefault(s.platform, 0)
        platform_totals[s.platform] += engagement

    # normalize to simple relative velocities (placeholder logic)
    max_val = max(platform_totals.values()) if platform_totals else 1

    platform_velocity = {
        platform: round(total / max_val, 2)
        for platform, total in platform_totals.items()
    }

    return platform_velocity

def compute_platform_signal_agreement(signals):
    """
    Agreement based on how similar platform momentum signals are.
    """
    platform_velocity = compute_platform_momentum(signals)

    if len(platform_velocity) <= 1:
        return 0.5  # only one platform available

    values = list(platform_velocity.values())
    diff = max(values) - min(values)

    # small divergence -> high agreement
    if diff < 0.2:
        return 0.85
    # medium divergence -> medium agreement
    elif diff < 0.5:
        return 0.65
    # large divergence -> low agreement
    else:
        return 0.4
    
def detect_platform_leader(signals):
    """
    Identify which platform is leading the trend based on relative momentum.
    Returns: "tiktok", "instagram", or "both"
    """
    platform_velocity = compute_platform_momentum(signals)

    if not platform_velocity:
        return "unknown"

    if len(platform_velocity) == 1:
        return list(platform_velocity.keys())[0]

    # Compare top two platforms
    sorted_platforms = sorted(platform_velocity.items(), key=lambda x: x[1], reverse=True)
    top_platform, top_val = sorted_platforms[0]
    second_platform, second_val = sorted_platforms[1]

    # If very close, treat as both
    if abs(top_val - second_val) < 0.1:
        return "both"

    return top_platform

