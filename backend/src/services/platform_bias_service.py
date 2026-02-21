# src/services/platform_bias_service.py

from src.services.platform_profiles import PLATFORM_PROFILES


def adjust_for_platform(raw_signal: dict, platform: str):
    profile = PLATFORM_PROFILES[platform]

    # Adjust confidence based on platform data maturity
    adjusted_confidence = raw_signal["confidence_score"] * profile["data_maturity"]

    phase = raw_signal["momentum_state"]
    velocity = raw_signal["velocity"]

    # Simple phase adjustment logic (v1)
    if velocity > 0.6 and profile["trend_latency_hours"] <= 8:
        adjusted_phase = "PEAKING"
    elif velocity < 0.2:
        adjusted_phase = "FATIGUED"
    else:
        adjusted_phase = phase

    # Urgency mapping
    if adjusted_phase == "PEAKING":
        urgency = "HIGH"
    elif adjusted_phase == "EMERGING":
        urgency = "MEDIUM"
    else:
        urgency = "LOW"

    action_map = {
        "PEAKING": "Launch promotion immediately",
        "EMERGING": "Prepare promo creatives",
        "FLAT": "Monitor trend",
        "FATIGUED": "Avoid new campaigns"
    }

    return {
        "adjusted_phase": adjusted_phase,
        "adjusted_confidence": round(adjusted_confidence, 2),
        "urgency": urgency,
        "recommended_action": action_map.get(adjusted_phase, "Monitor")
    }


def run_platform_bias_engine(raw_signal: dict):
    results = {}

    for platform in PLATFORM_PROFILES.keys():
        results[platform] = adjust_for_platform(raw_signal, platform)

    return results
