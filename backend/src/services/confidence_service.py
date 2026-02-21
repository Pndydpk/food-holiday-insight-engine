from typing import Dict, Optional


def compute_confidence_score(
    deviation_score: float,
    momentum_state: str,
    signal_agreement: float = 1.0,
    context_confirmation: float = 0.0,
    platform_leader: Optional[str] = None,
) -> Dict:
    """
    Computes overall confidence score for a trend.
    
    deviation_score: normalized abnormality (e.g., z-score from baseline)
    momentum_state: EMERGING / PEAKING / FATIGUED / FLAT
    signal_agreement: 0 to 1 (how consistent signals are across platforms)
    context_confirmation: 0 to 1 (holiday, Google Trends, news etc.)
    platform_leader: optional ("tiktok", "instagram", "youtube", "both", "unknown")
    """

    # Normalize deviation into 0–1 band
    deviation_component = min(max(deviation_score / 3.0, 0.0), 1.0)

    # Momentum weighting
    momentum_weights = {
        "EMERGING": 1.0,
        "PEAKING": 0.7,
        "FATIGUED": 0.3,
        "FLAT": 0.1,
    }
    momentum_component = momentum_weights.get(momentum_state, 0.1)

    # Weighted agreement model (your "trade secret" v1)
    confidence = (
        0.4 * deviation_component +
        0.3 * momentum_component +
        0.2 * signal_agreement +
        0.1 * context_confirmation
    )

    confidence = round(min(confidence, 1.0), 3)

    # Risk level
    if confidence >= 0.75:
        risk = "LOW"
    elif confidence >= 0.45:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    explanation = generate_explanation(
        deviation_score,
        momentum_state,
        signal_agreement,
        context_confirmation,
        confidence,
        risk,
        platform_leader
    )

    return {
        "confidence_score": confidence,
        "risk_level": risk,
        "explanation": explanation
    }


def generate_explanation(
    deviation_score: float,
    momentum_state: str,
    signal_agreement: float,
    context_confirmation: float,
    confidence: float,
    risk: str,
    platform_leader: Optional[str] = None,
) -> str:
    parts = []

    # Baseline deviation explanation
    if deviation_score > 2:
        parts.append("Buzz is significantly above normal baseline")
    elif deviation_score > 1:
        parts.append("Buzz is moderately above baseline")
    else:
        parts.append("Buzz is close to normal levels")

    # Momentum explanation
    if momentum_state == "EMERGING":
        parts.append("Momentum is building rapidly (early trend phase)")
    elif momentum_state == "PEAKING":
        parts.append("Trend is near peak attention")
    elif momentum_state == "FATIGUED":
        parts.append("Momentum is slowing down")
    else:
        parts.append("Trend momentum is flat")

    # Cross-platform agreement explanation
    if signal_agreement >= 0.75:
        parts.append("Signals strongly align across platforms")
    elif signal_agreement >= 0.55:
        parts.append("Signals are moderately aligned across platforms")
    else:
        parts.append("Signals diverge across platforms, reducing confidence")

    # Platform leader explanation (optional)
    if platform_leader:
        if platform_leader == "both":
            parts.append("Momentum is similar across platforms")
        elif platform_leader == "unknown":
            pass
        else:
            parts.append(f"{platform_leader.capitalize()} is leading this trend")

    # Context explanation
    if context_confirmation > 0.5:
        parts.append("Context signals support this trend (e.g., holiday/event)")
    else:
        parts.append("Context signals provide limited support for this trend")

    parts.append(f"Overall confidence: {confidence} (Risk: {risk})")

    return ". ".join(parts) + "."
