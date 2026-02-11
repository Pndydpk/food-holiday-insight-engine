# src/services/platform_profiles.py

PLATFORM_PROFILES = {
    "uber_eats": {
        "trend_latency_hours": 18,
        "impulse_factor": 0.7,
        "promo_sensitivity": 0.6,
        "data_maturity": 0.9
    },
    "doordash": {
        "trend_latency_hours": 6,
        "impulse_factor": 0.9,
        "promo_sensitivity": 0.8,
        "data_maturity": 0.85
    },
    "retail": {
        "trend_latency_hours": 72,
        "impulse_factor": 0.3,
        "promo_sensitivity": 0.4,
        "data_maturity": 0.6
    }
}
