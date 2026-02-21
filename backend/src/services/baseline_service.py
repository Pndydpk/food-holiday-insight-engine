from typing import List, Dict
import numpy as np


def compute_baseline_stats(history: List[float]) -> Dict:
    """
    Compute baseline mean and standard deviation from historical values.
    history: list of historical signal values for comparable time buckets
    """

    if not history or len(history) < 3:
        # Not enough data, fallback to safe defaults
        return {
            "mean": 0.0,
            "std": 1.0,
            "window": f"{len(history)}_points",
            "note": "Insufficient history; using fallback baseline."
        }

    mean = float(np.mean(history))
    std = float(np.std(history))

    # Prevent divide-by-zero later
    if std == 0:
        std = 1.0

    return {
        "mean": round(mean, 2),
        "std": round(std, 2),
        "window": f"{len(history)}_points",
        "note": None
    }


def compute_deviation_score(current_value: float, baseline_mean: float, baseline_std: float) -> float:
    """
    Compute normalized deviation (z-score style).
    """
    return round((current_value - baseline_mean) / baseline_std, 2)


def compute_baseline_and_deviation(history: List[float], current_value: float) -> Dict:
    """
    Convenience wrapper: computes baseline stats and deviation score together.
    """

    baseline = compute_baseline_stats(history)
    deviation_score = compute_deviation_score(
        current_value=current_value,
        baseline_mean=baseline["mean"],
        baseline_std=baseline["std"]
    )

    return {
        "baseline": baseline,
        "current_value": current_value,
        "deviation_score": deviation_score
    }
