from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd
from datetime import date

# -------------------------------------------------
# App initialization (THIS WAS MISSING)
# -------------------------------------------------
app = FastAPI(title="Food Holiday Insight Engine")

# -------------------------------------------------
# CORS (frontend ↔ backend)
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "Food Holiday Insight Engine API is running",
        "endpoints": ["/holidays/upcoming"]
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Paths
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent.parent
HOLIDAYS_CSV = PROJECT_ROOT / "data" / "raw" / "food_holidays_static.csv"

# -------------------------------------------------
# Health check
# -------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------------------------------
# Upcoming holidays (date-aware)
# -------------------------------------------------
@app.get("/holidays/upcoming")
def upcoming_holidays(
    days: int = 10,
    base_date: str | None = Query(default=None),
):
    df = pd.read_csv(HOLIDAYS_CSV, parse_dates=["date"])

    if base_date:
        today = pd.to_datetime(base_date)
    else:
        today = pd.to_datetime(date.today())

    df["days_from_today"] = (df["date"] - today).dt.days

    upcoming = df[
        (df["days_from_today"] >= 0)
        & (df["days_from_today"] <= days)
    ].sort_values("date")

    return upcoming[["name", "date", "days_from_today"]].rename(
        columns={"name": "holiday_name"}
    ).to_dict(orient="records")