from typing import Dict


def estimate_action_window(
    momentum_state: str,
    velocity: float,
    acceleration: float,
    deviation_score: float,
) -> Dict:
    """
    Estimates how long the merchant has to act on this trend.
    Returns hours + urgency label.
    """

    # Default windows (in hours)
    if momentum_state == "EMERGING":
        base_hours = 72
    elif momentum_state == "PEAKING":
        base_hours = 24
    elif momentum_state == "FATIGUED":
        base_hours = 8
    else:
        base_hours = 48

    # Adjust based on how extreme the spike is
    if deviation_score > 3:
        base_hours *= 0.7  # very hot trends burn faster
    elif deviation_score < 1:
        base_hours *= 1.2  # mild trends linger longer

    # Adjust based on acceleration
    if acceleration < 0:
        base_hours *= 0.6  # decay has started
    elif acceleration > 0.2:
        base_hours *= 0.8  # fast rise → fast saturation

    hours = max(6, int(base_hours))

    # Urgency labels
    if hours <= 18:
        urgency = "NOW"
    elif hours <= 48:
        urgency = "SOON"
    else:
        urgency = "NORMAL"


    explanation = generate_window_explanation(
        momentum_state, deviation_score, acceleration, hours
    )

    return {
        "action_window_hours": hours,
        "urgency": urgency,
        "window_explanation": explanation
    }


def generate_window_explanation(
    momentum_state: str,
    deviation_score: float,
    acceleration: float,
    hours: int
) -> str:
    parts = []

    if momentum_state == "EMERGING":
        parts.append("Trend is in early growth phase")
    elif momentum_state == "PEAKING":
        parts.append("Trend is near peak attention")
    elif momentum_state == "FATIGUED":
        parts.append("Trend momentum is declining")
    else:
        parts.append("Trend momentum is stable")

    if deviation_score > 3:
        parts.append("High spike suggests short-lived hype cycle")

    if acceleration < 0:
        parts.append("Engagement growth is slowing")

    parts.append(f"Estimated effective window: ~{hours} hours")

    return ". ".join(parts) + "."
