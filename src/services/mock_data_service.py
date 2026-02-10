import random
from typing import List, Dict


def generate_mock_social_series(
    days: int = 14,
    base: int = 100,
    spike: bool = True,
) -> List[float]:
    """
    Generates mock social buzz time series (e.g., post counts per day).
    
    days: number of time points
    base: baseline volume
    spike: whether to simulate a late-stage spike (emerging trend)
    """

    series = []
    level = base

    for i in range(days):
        # Normal noise
        noise = random.randint(-5, 8)
        level = max(1, level + noise)

        # Optional spike near the end to simulate trend emergence
        if spike and i > days - 4:
            level += random.randint(20, 60)

        series.append(level)

    return series


def generate_mock_trends() -> List[Dict]:
    """
    Returns mock trend candidates as if discovered by crawler.
    Some trends spike (emerging), others remain flat (fatigued/flat).
    """

    return [
        {
            "entity": "National Potato Chip Day",
            "category": "Snacks",
            "holiday_soon": True,
            "spike": True
        },
        {
            "entity": "Avocado Toast",
            "category": "Breakfast",
            "holiday_soon": False,
            "spike": True
        },
        {
            "entity": "Bubble Tea",
            "category": "Beverages",
            "holiday_soon": False,
            "spike": False  # flat trend to simulate cooling/fatigued
        },
    ]
