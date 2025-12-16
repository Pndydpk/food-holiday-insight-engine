import sqlite3
import re
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "processed" / "food_holidays.db"

STOPWORDS = {
    "national", "international", "day", "week", "month",
    "the", "of", "and", "for", "world", "global",
    "food", "drink", "festival", "celebration",
    "cook", "cooking", "hot", "cold", "sweet",
    "healthy", "appreciation", "lover", "lovers"
}

def clean_and_split(name):
    name = name.lower()
    name = re.sub(r"[^a-zA-Z0-9\s]", "", name)
    parts = name.split()
    return [p for p in parts if p not in STOPWORDS]

def generate_keyword_list(name):
    parts = clean_and_split(name)
    if not parts:
        return []
    keywords = set(p for p in parts if len(p) >= 4)


    # Add 2-word combos ("chocolate cake")
    for i in range(len(parts) - 1):
        keywords.add(parts[i] + " " + parts[i+1])

    return list(keywords)

def main():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM food_holidays", conn)

    df["keywords"] = df["name"].apply(lambda x: ", ".join(generate_keyword_list(str(x))))

    # Store results in a new table
    df.to_sql("food_holiday_keywords", conn, if_exists="replace", index=False)

    conn.close()

    print("✅ Keyword generation complete!")
    print(df[["name", "keywords"]].head(10))

if __name__ == "__main__":
    main()
