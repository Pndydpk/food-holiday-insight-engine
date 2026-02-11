# FoodLens API – /pulse/trends (v1)

## Endpoint
GET /pulse/trends

## Purpose
Returns merchant-ready trend intelligence for food items and food holidays, including:
- global trend signals
- confidence and risk
- recommended action window
- platform-specific bias (Uber Eats, DoorDash, Retail)

## Response Schema (v1)

```json
{
  "pulse_generated_at": "string",
  "insights": [
    {
      "entity": "string",
      "category": "string",

      "series": [number],
      "baseline": {
        "mean": number,
        "std": number,
        "window": "string",
        "note": "string | null"
      },
      "current_value": number,
      "deviation_score": number,

      "velocity": number,
      "acceleration": number,
      "momentum_state": "EMERGING | FLAT | PEAKING | FATIGUED",

      "confidence_score": number,
      "risk_level": "LOW | MEDIUM | HIGH",
      "explanation": "string",

      "action_hint": "string",
      "action_window_hours": number,
      "urgency": "NOW | SOON | LATER",
      "window_explanation": "string",

      "platform_bias": {
        "uber_eats": {
          "adjusted_phase": "EMERGING | FLAT | PEAKING | FATIGUED",
          "adjusted_confidence": number,
          "urgency": "LOW | MEDIUM | HIGH",
          "recommended_action": "string"
        },
        "doordash": { "... same shape ..." },
        "retail": { "... same shape ..." }
      }
    }
  ]
}
