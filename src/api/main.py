from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import date
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Setup absolute paths relative to this script
# This moves up from src/api to the project root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
HOLIDAYS_CSV = ROOT_DIR / "data" / "raw" / "food_holidays_static.csv"
POPULARITY_CSV = ROOT_DIR / "data" / "processed" / "holiday_popularity.csv"

@app.get("/holidays/upcoming")
def upcoming_holidays(
    days: int = 10,
    base_date: str | None = Query(default=None),
):
    # 2. Load datasets using the absolute paths
    try:
        df_holidays = pd.read_csv(HOLIDAYS_CSV, parse_dates=["date"])
        df_pop = pd.read_csv(POPULARITY_CSV)
    except FileNotFoundError as e:
        return {"error": f"File not found: {e.filename}. Check your directory structure!"}

    # 3. Merge logic
    df = pd.merge(df_holidays, df_pop, left_on="name", right_on="holiday_name", how="left")
    df["popularity_score"] = df["popularity_score"].fillna(0)

    # 4. Date handling
    if base_date:
        requested_date = pd.to_datetime(base_date)
    else:
        requested_date = pd.to_datetime(date.today())

    # Logic to handle 2025 static data
    search_date = requested_date.replace(year=2025)
    df["days_from_today"] = (df["date"] - search_date).dt.days

    # 5. Filter and Sort
    upcoming = df[
        (df["days_from_today"] >= 0) & 
        (df["days_from_today"] <= days)
    ].sort_values("date")

    return upcoming[["name", "date", "days_from_today", "popularity_score"]].rename(
        columns={"name": "holiday_name"}
    ).to_dict(orient="records")