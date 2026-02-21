import pandas as pd
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent

HOLIDAYS_CSV = PROJECT_ROOT / "data" / "raw" / "food_holidays_static.csv"
POPULARITY_PATH = PROJECT_ROOT / "data" / "processed" / "holiday_popularity.csv"
TOP_DISHES_PATH = PROJECT_ROOT / "data" / "processed" / "top_dishes_per_holiday.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "upcoming_holiday_insights.csv"

def main():
    today = pd.Timestamp(datetime.today().date())
    print(f"📅 System date detected as: {today.date()}")

    # Load holidays from CSV
    holidays = pd.read_csv(
        HOLIDAYS_CSV,
        parse_dates=["date"]
    )

    # Normalize column names
    holidays = holidays.rename(columns={
        "name": "holiday_name",
    })

    # Keep only future holidays
    holidays = holidays[holidays["date"] >= today].copy()
    holidays["days_from_today"] = (holidays["date"] - today).dt.days

    # Load popularity
    popularity = pd.read_csv(POPULARITY_PATH)

    # Load top dishes (top 1 dish per holiday)
    top_dishes = (
        pd.read_csv(TOP_DISHES_PATH)
        .sort_values(["holiday_name", "match_count"], ascending=[True, False])
        .drop_duplicates("holiday_name")
        [["holiday_name", "menu_item"]]
        .rename(columns={"menu_item": "top_dish"})
    )

    # Merge all datasets
    insights = (
        holidays[["holiday_name", "date", "days_from_today"]]
        .merge(popularity, on="holiday_name", how="left")
        .merge(top_dishes, on="holiday_name", how="left")
        .sort_values("days_from_today")
        .reset_index(drop=True)
    )

    insights.to_csv(OUTPUT_PATH, index=False)

    print("✅ Upcoming holiday insights generated")
    print(f"📁 Output saved to: {OUTPUT_PATH}")
    print(f"📊 Total upcoming holidays: {len(insights)}")

if __name__ == "__main__":
    main()
