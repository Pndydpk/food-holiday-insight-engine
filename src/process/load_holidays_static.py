# src/process/load_holidays_static.py
import os
from pathlib import Path
import sqlite3
import pandas as pd
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "food_holidays_static.csv"
DB_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH = DB_DIR / "food_holidays.db"

def read_csv_with_fallback(path):
    last_exc = None
    for enc in ("utf-8-sig", "utf-8", "latin1", "cp1252"):
        try:
            df = pd.read_csv(path, encoding=enc)
            print(f"✅ Read CSV with encoding: {enc}")
            return df
        except Exception as e:
            last_exc = e
    raise last_exc

def main():
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Looking for CSV: {CSV_PATH}")

    if not CSV_PATH.exists():
        print(f"❌ ERROR: CSV not found at {CSV_PATH}")
        sys.exit(1)

    # Read CSV
    try:
        df = read_csv_with_fallback(CSV_PATH)
    except Exception as e:
        print(f"❌ Failed to read CSV: {e}")
        sys.exit(1)

    # Show basic info
    print(f"Columns found: {list(df.columns)}")
    print(f"Rows loaded from CSV: {len(df)}")

    # Basic normalization: ensure common columns exist
    # If your CSV already has desired columns, this will not change them.
    col_map = {}
    for c in df.columns:
        lc = c.strip().lower()
        if 'food' in lc and 'holiday' in lc:
            col_map[c] = 'name'
        elif lc == 'date' or lc.startswith('date') or 'date' in lc:
            col_map[c] = 'date_raw'
        elif 'year' in lc:
            col_map[c] = 'year'
        elif 'note' in lc:
            col_map[c] = 'notes'
        else:
            # leave other columns as-is
            col_map[c] = c

    df = df.rename(columns=col_map)

    # If there's no 'name'/'date_raw' columns after mapping, try some common fallbacks
    if 'name' not in df.columns:
        # try 'Food Holidays' exact name
        if 'Food Holidays' in df.columns:
            df = df.rename(columns={'Food Holidays':'name'})
    if 'date_raw' not in df.columns:
        if 'Date' in df.columns:
            df = df.rename(columns={'Date':'date_raw'})

    if 'name' not in df.columns or 'date_raw' not in df.columns:
        print("❌ CSV is missing required columns. Found columns:", list(df.columns))
        print("Expected at least 'Food Holidays' (mapped to name) and 'Date' (mapped to date_raw).")
        sys.exit(1)

    # Clean whitespace
    df['name'] = df['name'].astype(str).str.strip()
    print("DEBUG COLUMNS:", list(df.columns))
    df['date_raw'] = df['date_raw'].astype(str).str.strip()

    # Ensure year column exists, if missing set to 2025
    if 'year' not in df.columns:
        df['year'] = '2025'
    else:
        df['year'] = df['year'].astype(str).str.strip().replace('', '2025').fillna('2025')

    # Try to create normalized date column where possible (Month Day -> YYYY-MM-DD)
    import re
    months = {
        'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
        'july':7,'august':8,'september':9,'october':10,'november':11,'december':12,
        'jan':1,'feb':2,'mar':3,'apr':4,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12
    }

    def normalize_date_text(row):
        txt = str(row.get('date_raw','')).strip()
        # look for Month Day
        m = re.search(r'([A-Za-z]+)\s+(\d{1,2})', txt)
        if m:
            mon = m.group(1).lower()
            day = int(m.group(2))
            if mon in months:
                try:
                    return f"{int(row.get('year', '2025')):04d}-{months[mon]:02d}-{day:02d}"
                except Exception:
                    return f"{mon.title()} {day} {row.get('year','2025')}"
        # if textual like 'Third Sunday in July', append year
        for k in months:
            if k in txt.lower():
                return f"{txt} {row.get('year','2025')}"
        # fallback
        return f"{txt} {row.get('year','2025')}"

    df['date'] = df.apply(normalize_date_text, axis=1)

    # Reorder columns: name, date, year, plus others
    cols = ['name','date','year'] + [c for c in df.columns if c not in ('name','date','year')]
    df = df[cols]

    # Ensure DB dir exists
    os.makedirs(DB_DIR, exist_ok=True)

    # Write to SQLite (replace table)
    conn = sqlite3.connect(DB_PATH)
    try:
        df.to_sql('food_holidays', conn, if_exists='replace', index=False)
    finally:
        conn.close()

    print(f"✅ Successfully wrote {len(df)} rows to {DB_PATH} -> table 'food_holidays'")

    # Print a small preview
    preview = df.head(10)
    print("\nPreview (first 10 rows):")
    print(preview.to_string(index=False))

if __name__ == "__main__":
    main()