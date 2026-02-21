# src/process/load_holidays_static.py
import sys
import os
import re
import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "food_holidays_static.csv"
DB_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH = DB_DIR / "food_holidays.db"

DEFAULT_YEAR = "2025"

def read_csv_try_encodings(path):
    encodings = ("utf-8-sig", "utf-8", "latin1", "cp1252")
    last_exc = None
    for e in encodings:
        try:
            df = pd.read_csv(path, encoding=e)
            print(f"[OK] Read CSV with encoding: {e}")
            return df
        except Exception as exc:
            last_exc = exc
            print(f"[WARN] reading CSV with encoding {e} failed: {exc}")
    raise last_exc

def map_columns_case_insensitive(df):
    # create mapping from lower -> actual col name
    lower_map = {c.strip().lower(): c for c in df.columns}
    rename = {}

    # Name column
    for candidate in ("food holidays", "food_holidays", "food-holidays", "holiday", "name", "title"):
        if candidate in lower_map:
            rename[lower_map[candidate]] = "name"
            break

    # Date columns
    for candidate in ("date", "short date", "short_date", "shortdate", "date_raw"):
        if candidate in lower_map:
            rename[lower_map[candidate]] = "date_raw"
            break

    # Year
    for candidate in ("year",):
        if candidate in lower_map:
            rename[lower_map[candidate]] = "year"
            break

    # Notes
    for candidate in ("notes", "note"):
        if candidate in lower_map:
            rename[lower_map[candidate]] = "notes"
            break

    # Month, day columns keep if present
    if "month" in lower_map and "month number" in lower_map:
        rename[lower_map["month"]] = "month_name"
        rename[lower_map["month number"]] = "month_number"
    elif "month" in lower_map:
        rename[lower_map["month"]] = "month_name"

    # Day of month / day of week
    if "day of month" in lower_map:
        rename[lower_map["day of month"]] = "day_of_month"
    if "day of week" in lower_map:
        rename[lower_map["day of week"]] = "day_of_week"

    # Apply rename where found
    if rename:
        df = df.rename(columns=rename)
    return df

def normalize_date_text(row):
    """
    - Try to convert Month Day -> YYYY-MM-DD using row['year'] or DEFAULT_YEAR.
    - If fuzzy (e.g., '3rd Sunday in July'), keep textual + year (e.g., '3rd Sunday in July 2025').
    - If empty, return ''.
    """
    months = {
        'january':1,'jan':1,'february':2,'feb':2,'march':3,'mar':3,'april':4,'apr':4,'may':5,'june':6,'jun':6,
        'july':7,'jul':7,'august':8,'aug':8,'september':9,'sep':9,'october':10,'oct':10,'november':11,'nov':11,'december':12,'dec':12
    }
    raw = ""
    if 'date_raw' in row and pd.notna(row['date_raw']):
        raw = str(row['date_raw']).strip()
    elif 'short_date' in row and pd.notna(row['short_date']):
        raw = str(row['short_date']).strip()
    if not raw:
        return ""

    # find "Month Day" like "January 4" or "Jan 4"
    m = re.search(r'([A-Za-z]+)\s+(\d{1,2})', raw)
    year = str(row.get('year') or DEFAULT_YEAR).strip()
    if m:
        mon = m.group(1).lower()
        day = int(m.group(2))
        if mon in months:
            try:
                return f"{int(year):04d}-{months[mon]:02d}-{day:02d}"
            except Exception:
                return f"{mon.title()} {day} {year}"

    # if raw contains a month name (fuzzy), append year
    for k in months.keys():
        if k in raw.lower():
            return f"{raw} {year}"

    # if raw contains a 4-digit year already, return as-is
    if re.search(r'\b\d{4}\b', raw):
        return raw

    # fallback: append year
    return f"{raw} {year}"

def main():
    if not CSV_PATH.exists():
        print(f"[ERROR] CSV not found at: {CSV_PATH}")
        sys.exit(1)

    # Read CSV with fallback encodings
    try:
        df = read_csv_try_encodings(CSV_PATH)
    except Exception as e:
        print("[ERROR] Could not read CSV:", e)
        sys.exit(1)

    print("[DEBUG] Original columns:", list(df.columns)[:30])

    # Map columns (case-insensitive)
    df = map_columns_case_insensitive(df)
    print("[DEBUG] Columns after mapping:", list(df.columns)[:40])
    # --- START: deduplicate columns with same name by coalescing values ---
    # If mapping produced duplicate column names (e.g., two 'date_raw'), fix by merging them.
    cols = list(df.columns)
    dup_names = [name for name in cols if cols.count(name) > 1]
    if dup_names:
        dup_set = sorted(set(dup_names))
        print(f"[WARN] Duplicate column names detected after mapping: {dup_set}")
        for name in dup_set:
            # select all columns with this name
            same = [c for c in df.columns if c == name]
            if len(same) <= 1:
                continue
            # create a single Series with first non-null value across the duplicate columns
            # use bfill across columns (axis=1) then pick first column
            merged = df.loc[:, same].bfill(axis=1).iloc[:, 0]
            # drop the old duplicate columns
            df = df.drop(columns=same)
            # assign merged series back as single column
            df[name] = merged
        print("[OK] Duplicate columns merged. Columns now:", list(df.columns))
    # --- END deduplicate block ---

    # Ensure required columns
    if 'name' not in df.columns:
        # try more heuristics
        candidates = [c for c in df.columns if ('holiday' in c.lower() and 'food' in c.lower()) or ('holiday' in c.lower())]
        if candidates:
            df = df.rename(columns={candidates[0]: 'name'})
    if 'date_raw' not in df.columns:
        candidates = [c for c in df.columns if 'date' in c.lower()]
        if candidates:
            df = df.rename(columns={candidates[0]: 'date_raw'})

    if 'name' not in df.columns or 'date_raw' not in df.columns:
        print("[ERROR] Could not map required columns. Found columns:", list(df.columns))
        sys.exit(1)

    # Clean text columns
    df['name'] = df['name'].astype(str).str.strip()
    df['date_raw'] = df['date_raw'].astype(str).str.strip()

    # Ensure year column
    if 'year' not in df.columns:
        df['year'] = DEFAULT_YEAR
    else:
        df['year'] = df['year'].astype(str).str.strip().replace('', DEFAULT_YEAR).fillna(DEFAULT_YEAR)

    # Create normalized date
    df['date'] = df.apply(normalize_date_text, axis=1)

    # Reorder columns to put name,date,year first
    cols = ['name','date','year'] + [c for c in df.columns if c not in ('name','date','year')]
    df = df[cols]

    # Write cleaned CSV (overwrite)
    try:
        df.to_csv(CSV_PATH, index=False, encoding='utf-8')
        print(f"[OK] Wrote cleaned CSV back to: {CSV_PATH} (rows: {len(df)})")
    except Exception as e:
        print("[WARN] Could not write cleaned CSV with utf-8, trying latin1. Error:", e)
        df.to_csv(CSV_PATH, index=False, encoding='latin1')
        print(f"[OK] Wrote cleaned CSV with latin1 to: {CSV_PATH} (rows: {len(df)})")

    # Ensure db folder exists
    os.makedirs(DB_DIR, exist_ok=True)

    # Load into SQLite (replace table)
    try:
        conn = sqlite3.connect(DB_PATH)
        df.to_sql('food_holidays', conn, if_exists='replace', index=False)
        conn.close()
        print(f"[OK] Loaded {len(df)} rows into SQLite DB: {DB_PATH} -> table 'food_holidays'")
    except Exception as e:
        print("[ERROR] Failed to write to SQLite:", e)
        sys.exit(1)

    # Small preview
    print("\nPreview (first 10 rows):")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    import pandas as pd
    main()
