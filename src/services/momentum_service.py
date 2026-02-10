from typing import List, Dict
import numpy as np


def compute_velocity(series: List[float], window: int = 3) -> float:
    """
    Velocity = average % change over the last N points.
    Example: measures how fast buzz is growing recently.
    """
    if len(series) < window + 1:
        return 0.0

    recent = series[-(window + 1):]
    pct_changes = []

    for i in range(1, len(recent)):
        prev = recent[i - 1]
        curr = recent[i]

        if prev == 0:
            continue

        pct_changes.append((curr - prev) / prev)

    if not pct_changes:
        return 0.0

    return round(float(np.mean(pct_changes)), 3)


def compute_acceleration(series: List[float], window: int = 3) -> float:
    """
    Acceleration = change in velocity between two recent windows.
    Detects whether momentum is increasing or slowing down.
    """
    if len(series) < (2 * window + 1):
        return 0.0

    first_window = series[-(2 * window + 1):-(window + 1)]
    second_window = series[-(window + 1):]

    v1 = compute_velocity(first_window, window=window)
    v2 = compute_velocity(second_window, window=window)

    return round(v2 - v1, 3)


def classify_momentum_state(velocity: float, acceleration: float) -> str:
    """
    Classifies trend phase based on velocity + acceleration.
    """

    if velocity > 0.2 and acceleration > 0:
        return "EMERGING"

    if velocity > 0.2 and abs(acceleration) <= 0.05:
        return "PEAKING"

    if velocity > 0.1 and acceleration < 0:
        return "FATIGUED"

    return "FLAT"


def compute_momentum(series: List[float]) -> Dict:
    """
    Wrapper function to compute velocity, acceleration, and momentum state.
    """
    velocity = compute_velocity(series)
    acceleration = compute_acceleration(series)
    state = classify_momentum_state(velocity, acceleration)

    return {
        "velocity": velocity,
        "acceleration": acceleration,
        "momentum_state": state
    }
