# src/services/social_ingestion_service.py

from typing import List, Optional
from datetime import datetime
import random
import json
import sqlite3
from pathlib import Path
from random import randint
from datetime import timedelta

from src.schemas.social_signal_schema import SocialSignal
from src.schemas.trend_signal_schema import TrendSignal


# -------------------------
# Social Source Abstraction (MVP)
# -------------------------
class SocialSource:
    def fetch_signals(self) -> List[SocialSignal]:
        raise NotImplementedError


class DummySocialSource(SocialSource):
    """
    Dummy source to simulate TikTok / Instagram / YouTube signals.
    This bypasses TikTok ban and lets us test the full pipeline.
    """
    def fetch_signals(self) -> List[SocialSignal]:
        platforms = ["tiktok", "instagram", "youtube"]
        foods = ["nachos", "ramen", "boba"]

        signals: List[SocialSignal] = []

        for food in foods:
            for platform in platforms:
                likes = random.randint(300, 5000)
                comments = random.randint(20, 300)
                shares = random.randint(5, 80)

                signals.append(
                    SocialSignal(
                        platform=platform,
                        post_id=f"{platform}_{food}_{random.randint(1,10000)}",
                        timestamp="2026-02-15T10:00:00Z",
                        text=f"Trending {food} content",
                        hashtags=[f"#{food}", "#foodtrend"],
                        food_entities=[food],
                        engagement={"likes": likes, "comments": comments, "shares": shares},
                        creator_followers=random.randint(5000, 150000),
                        geo="US"
                    )
                )

        return signals


# -------------------------
# Ingestion Entry Point
# -------------------------
def ingest_social_signals(source: Optional[SocialSource] = None) -> List[SocialSignal]:
    """
    Unified ingestion entrypoint.
    Default = DummySocialSource (MVP).
    Later swap with real TikTok/Instagram/YouTube sources.
    """
    source = source or DummySocialSource()
    signals = source.fetch_signals()
    save_raw_social_signals(signals)
    return signals


# -------------------------
# DB Persistence (MVP)
# -------------------------
DB_PATH = Path(__file__).resolve().parent.parent / "db" / "foodlens.db"

def save_raw_social_signals(signals: List[SocialSignal]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for s in signals:
        backdated_time = datetime.utcnow() - timedelta(days=randint(0, 6))

        cursor.execute("""
            INSERT INTO raw_social_signals (
                platform, post_id, posted_at, text,
                hashtags, food_entities,
                likes, comments, shares, views,
                creator_followers, geo, ingested_at,
                raw_payload
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s.platform,
            s.post_id,
            s.timestamp,  # assuming s.timestamp is the post time
            s.text,
            json.dumps(s.hashtags),
            json.dumps(s.food_entities),
            s.engagement.get("likes", 0),
            s.engagement.get("comments", 0),
            s.engagement.get("shares", 0),
            s.engagement.get("views", 0),   # 👈 new
            s.creator_followers,
            s.geo,
            backdated_time.isoformat(),     # 👈 ingestion time (simulated)
            json.dumps(s.dict())            # 👈 store full raw object
        ))

    conn.commit()
    conn.close()
# -------------------------
# Aggregation + Adapters (Existing Logic)
# -------------------------
def aggregate_to_trend_signal(signals: List[SocialSignal]) -> List[TrendSignal]:
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
    if not signals:
        return [0] * days

    total_engagement = sum(
        s.engagement.get("likes", 0)
        + s.engagement.get("comments", 0)
        + s.engagement.get("shares", 0)
        for s in signals
    )

    base = max(int(total_engagement / days), 1)
    series = [base + i * int(base * 0.2) for i in range(days)]
    return series


def compute_platform_momentum(signals):
    platform_totals = {}

    for s in signals:
        engagement = (
            s.engagement.get("likes", 0)
            + s.engagement.get("comments", 0)
            + s.engagement.get("shares", 0)
        )

        platform_totals.setdefault(s.platform, 0)
        platform_totals[s.platform] += engagement

    max_val = max(platform_totals.values()) if platform_totals else 1

    return {
        platform: round(total / max_val, 2)
        for platform, total in platform_totals.items()
    }


def compute_platform_signal_agreement(signals):
    platform_velocity = compute_platform_momentum(signals)

    if len(platform_velocity) <= 1:
        return 0.5

    values = list(platform_velocity.values())
    diff = max(values) - min(values)

    if diff < 0.2:
        return 0.85
    elif diff < 0.5:
        return 0.65
    else:
        return 0.4


def detect_platform_leader(signals):
    platform_velocity = compute_platform_momentum(signals)

    if not platform_velocity:
        return "unknown"

    if len(platform_velocity) == 1:
        return list(platform_velocity.keys())[0]

    sorted_platforms = sorted(platform_velocity.items(), key=lambda x: x[1], reverse=True)
    top_platform, top_val = sorted_platforms[0]
    second_platform, second_val = sorted_platforms[1]

    if abs(top_val - second_val) < 0.1:
        return "both"

    return top_platform
# -------------------------
# DB Read (Debug)
# -------------------------
def fetch_recent_raw_social_signals(limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            platform, post_id, timestamp, text,
            hashtags, food_entities,
            likes, comments, shares,
            creator_followers, geo, ingested_at
        FROM raw_social_signals
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "platform": r[0],
            "post_id": r[1],
            "timestamp": r[2],
            "text": r[3],
            "hashtags": r[4],
            "food_entities": r[5],
            "likes": r[6],
            "comments": r[7],
            "shares": r[8],
            "creator_followers": r[9],
            "geo": r[10],
            "ingested_at": r[11],
        })

    return results
# -------------------------
# Time Series from DB (MVP)
# -------------------------
def build_entity_time_series_from_db(food: str, days: int = 14):
    """
    Build a simple daily engagement time series for a given food entity
    from raw_social_signals table.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            substr(ingested_at, 1, 10) as day,
            SUM(likes + comments + shares) as total_engagement
        FROM raw_social_signals
        WHERE food_entities LIKE ?
        GROUP BY day
        ORDER BY day ASC
        LIMIT ?
    """, (f'%"{food}"%', days))

    rows = cursor.fetchall()
    conn.close()

    # If no history yet, fallback
    if not rows:
        return [0] * days

    series = [r[1] for r in rows]

    # Pad if fewer days than requested
    if len(series) < days:
        padding = [series[0]] * (days - len(series))
        series = padding + series

    return series
datetime.utcnow().isoformat()