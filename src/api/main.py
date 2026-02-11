import random
random.seed(42)

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
from datetime import date
from pathlib import Path

# Services
from src.services.mock_data_service import generate_mock_social_series, generate_mock_trends
from src.services.baseline_service import compute_baseline_and_deviation
from src.services.momentum_service import compute_momentum
from src.services.confidence_service import compute_confidence_score
from src.services.action_window_service import estimate_action_window
from src.services.platform_bias_service import run_platform_bias_engine
from src.services.social_ingestion_service import (
    ingest_mock_social_signals,
    aggregate_to_trend_signal,
    social_signals_to_series,
    compute_platform_signal_agreement,
    detect_platform_leader,
)

app = FastAPI(title="FoodLens API", version="0.1.0")

# CORS (frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later
    allow_methods=["*"],
    allow_headers=["*"],
)

# Absolute paths relative to project root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
HOLIDAYS_CSV = ROOT_DIR / "data" / "raw" / "food_holidays_static.csv"
POPULARITY_CSV = ROOT_DIR / "data" / "processed" / "holiday_popularity.csv"


# -------------------------
# Health
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------
# Holidays (existing endpoint)
# -------------------------
@app.get("/holidays/upcoming")
def upcoming_holidays(
    days: int = Query(default=10, ge=1, le=60),
    base_date: str | None = Query(default=None),
):
    """
    Returns upcoming food holidays within N days,
    enriched with historical popularity score.
    """

    if not HOLIDAYS_CSV.exists() or not POPULARITY_CSV.exists():
        raise HTTPException(
            status_code=500,
            detail="Holiday data files missing. Check data/raw and data/processed folders."
        )

    df_holidays = pd.read_csv(HOLIDAYS_CSV, parse_dates=["date"])
    df_pop = pd.read_csv(POPULARITY_CSV)

    df = pd.merge(
        df_holidays,
        df_pop,
        left_on="name",
        right_on="holiday_name",
        how="left"
    )
    df["popularity_score"] = df["popularity_score"].fillna(0)

    if base_date:
        requested_date = pd.to_datetime(base_date)
    else:
        requested_date = pd.to_datetime(date.today())

    # Temporary static year alignment (to be refactored later)
    search_date = requested_date.replace(year=2025)

    df["days_from_today"] = (df["date"] - search_date).dt.days

    upcoming = df[
        (df["days_from_today"] >= 0) &
        (df["days_from_today"] <= days)
    ].sort_values("date")

    return upcoming[["name", "date", "days_from_today", "popularity_score"]].rename(
        columns={"name": "holiday_name"}
    ).to_dict(orient="records")


# -------------------------
# Debug: Baseline Service
# -------------------------
@app.get("/debug/baseline")
def debug_baseline():
    history = [100, 110, 95, 105, 98, 102, 108, 115, 120]
    current_value = 145
    return compute_baseline_and_deviation(history, current_value)


# -------------------------
# Debug: Momentum
# -------------------------
@app.get("/debug/momentum")
def debug_momentum():
    series = [10, 12, 15, 21, 30, 45, 70]
    return compute_momentum(series)


# -------------------------
# Debug: Confidence
# -------------------------
@app.get("/debug/confidence")
def debug_confidence():
    return compute_confidence_score(
        deviation_score=2.6,
        momentum_state="EMERGING",
        signal_agreement=0.8,
        context_confirmation=0.6,
        platform_leader="tiktok",
    )


# -------------------------
# THE PULSE (Unified Intelligence Endpoint)
# -------------------------
@app.get("/pulse/trends")
def pulse_trends(source: str = Query(default="mock")):
    insights = []

    # --- Ingestion ---
    if source == "social":
        social_signals = ingest_mock_social_signals()
        trend_signals = aggregate_to_trend_signal(social_signals)

        trends = [
            {
                "entity": t.trend,
                "category": "Social Trend",
                "spike": True,
                "holiday_soon": False,  # social trends not tied to holidays (v1)
            }
            for t in trend_signals
        ]
    else:
        social_signals = None
        trends = generate_mock_trends()

    # --- Inference Loop ---
    for t in trends:

        # 1) Time series
        if source == "social":
            series = social_signals_to_series(social_signals, days=14)
        else:
            series = generate_mock_social_series(
                days=14,
                base=100,
                spike=t.get("spike", True)
            )

        # 2) Baseline vs current
        history = series[:-1]
        current_value = series[-1]
        baseline_result = compute_baseline_and_deviation(history, current_value)

        # 3) Momentum
        momentum = compute_momentum(series)

        # 4) Signal agreement
        if source == "social":
            signal_agreement = compute_platform_signal_agreement(social_signals)
        else:
            signal_agreement = 0.8 if t["holiday_soon"] else 0.5

        # 5) Context confirmation
        context_confirmation = 1.0 if t["holiday_soon"] else 0.2

        # 6) Platform leader
        if source == "social":
            platform_leader = detect_platform_leader(social_signals)
        else:
            platform_leader = None

        # 7) Confidence
        confidence = compute_confidence_score(
            deviation_score=baseline_result["deviation_score"],
            momentum_state=momentum["momentum_state"],
            signal_agreement=signal_agreement,
            context_confirmation=context_confirmation,
            platform_leader=platform_leader,
        )

        # 8) Action window
        action_window = estimate_action_window(
            momentum_state=momentum["momentum_state"],
            velocity=momentum["velocity"],
            acceleration=momentum["acceleration"],
            deviation_score=baseline_result["deviation_score"],
        )

        # 9) Action hint
        if confidence["confidence_score"] > 0.8 and momentum["momentum_state"] == "EMERGING":
            action_hint = "Launch promotion (early window)"
        elif confidence["confidence_score"] > 0.6 and momentum["momentum_state"] == "PEAKING":
            action_hint = "Boost visibility (short window)"
        elif momentum["momentum_state"] == "FATIGUED":
            action_hint = "Avoid heavy spend; trend is cooling"
        else:
            action_hint = "Monitor"

        # 10) Platform bias
        platform_bias = run_platform_bias_engine({
            "momentum_state": momentum["momentum_state"],
            "velocity": momentum["velocity"],
            "confidence_score": confidence["confidence_score"],
        })

        insights.append({
            "entity": t["entity"],
            "category": t["category"],
            "series": series,
            "baseline": baseline_result["baseline"],
            "current_value": current_value,
            "deviation_score": baseline_result["deviation_score"],
            "velocity": momentum["velocity"],
            "acceleration": momentum["acceleration"],
            "momentum_state": momentum["momentum_state"],
            "confidence_score": confidence["confidence_score"],
            "risk_level": confidence["risk_level"],
            "explanation": confidence["explanation"],
            "action_hint": action_hint,
            "action_window_hours": action_window["action_window_hours"],
            "urgency": action_window["urgency"],
            "window_explanation": action_window["window_explanation"],
            "platform_bias": platform_bias,
        })

    return {
        "pulse_generated_at": source,
        "insights": insights
    }
# -------------------------
# DEBUG: Pulse Internals (Social Ingestion & Platform Signals)
# -------------------------
@app.get("/pulse/debug")
def pulse_debug():
    social_signals = ingest_mock_social_signals()

    platform_velocity = None
    signal_agreement = None
    platform_leader = None

    if social_signals:
        from src.services.social_ingestion_service import compute_platform_momentum

        platform_velocity = compute_platform_momentum(social_signals)
        signal_agreement = compute_platform_signal_agreement(social_signals)
        platform_leader = detect_platform_leader(social_signals)

    return {
        "raw_social_signals": [s.dict() for s in social_signals],
        "platform_velocity": platform_velocity,
        "signal_agreement": signal_agreement,
        "platform_leader": platform_leader,
    }
