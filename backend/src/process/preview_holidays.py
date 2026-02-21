# src/process/preview_holidays.py
import sqlite3
import pandas as pd

DB = "data/processed/food_holidays.db"

conn = sqlite3.connect(DB)
print("Connected to:", DB)

# 1) Total count
cnt = pd.read_sql("SELECT COUNT(*) AS total FROM food_holidays;", conn)
print("\nTotal rows in food_holidays:")
print(cnt.to_string(index=False))

# 2) Count per year (should be 2025)
year_counts = pd.read_sql("SELECT year, COUNT(*) AS cnt FROM food_holidays GROUP BY year ORDER BY year;", conn)
print("\nRows per year:")
print(year_counts.to_string(index=False))

# 3) First 15 rows ordered by date (some dates may be textual)
preview = pd.read_sql("SELECT id, name, date, year FROM food_holidays ORDER BY date LIMIT 15;", conn)
print("\nPreview (first 15 rows ordered by date):")
print(preview.to_string(index=False))

conn.close()
