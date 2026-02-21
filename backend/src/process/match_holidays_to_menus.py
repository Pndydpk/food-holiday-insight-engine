import csv
import sqlite3
import pandas as pd
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "processed" / "uber_eats.db"
HOLIDAY_DB_PATH = PROJECT_ROOT / "data" / "processed" / "food_holidays.db"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "holiday_menu_matches.csv"

CHUNK_SIZE = 200_000  # safe for your system

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    return re.sub(r"[^a-zA-Z0-9\s]", "", text).lower()

def main():
    print("🔌 Connecting to SQLite databases...")
    conn_menus = sqlite3.connect(DB_PATH)
    conn_holidays = sqlite3.connect(HOLIDAY_DB_PATH)

    print("📥 Loading menus and holiday keywords...")
    menus = pd.read_sql("SELECT * FROM menus", conn_menus)
    holidays = pd.read_sql(
        "SELECT name, date, keywords FROM food_holiday_keywords",
        conn_holidays
    )

    conn_menus.close()
    conn_holidays.close()

    print(f"🍽 Loaded {len(menus)} menu items.")
    print(f"🎉 Loaded {len(holidays)} holidays.")

    menus["clean_name"] = menus["name"].apply(normalize_text)
    menus["clean_description"] = menus["description"].apply(normalize_text)

    # Create CSV file + header ONCE
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "holiday_name",
                "date",
                "matched_keyword",
                "restaurant_id",
                "menu_item",
                "price",
            ],
        )
        writer.writeheader()

    print("🔎 Matching holidays to menus (streaming)...")

    total_written = 0

    with open(OUTPUT_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "holiday_name",
                "date",
                "matched_keyword",
                "restaurant_id",
                "menu_item",
                "price",
            ],
        )

        for _, h in holidays.iterrows():
            holiday = h["name"]
            date = h["date"]
            keywords = str(h["keywords"]).split(", ")

            for kw in keywords:
                kw = kw.strip().lower()
                if not kw or len(kw) < 4:
                    continue

                for start in range(0, len(menus), CHUNK_SIZE):
                    end = start + CHUNK_SIZE
                    chunk = menus.iloc[start:end]

                    mask = (
                        chunk["clean_name"].str.contains(kw, na=False)
                        | chunk["clean_description"].str.contains(kw, na=False)
                    )

                    matched = chunk[mask]

                    for _, m in matched.iterrows():
                        writer.writerow({
                            "holiday_name": holiday,
                            "date": date,
                            "matched_keyword": kw,
                            "restaurant_id": m["restaurant_id"],
                            "menu_item": m["name"],
                            "price": m["price"],
                        })
                        total_written += 1

                    del chunk, matched, mask

            print(f"🎯 Completed: {holiday} | Total matches so far: {total_written}")

    print(f"\n✅ MATCHING COMPLETE")
    print(f"💾 Total rows written: {total_written}")
    print(f"📁 Output file: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()