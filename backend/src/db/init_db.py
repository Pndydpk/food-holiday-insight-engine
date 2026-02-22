# src/db/init_db.py

import sqlite3
from pathlib import Path

# Path to SQLite DB file
DB_PATH = Path(__file__).resolve().parent / "foodlens.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_social_signals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT,
        post_id TEXT,
        posted_at TEXT,
        text TEXT,
        hashtags TEXT,
        food_entities TEXT,
        likes INTEGER,
        comments INTEGER,
        shares INTEGER,
        views INTEGER,
        creator_followers INTEGER,
        geo TEXT,
        ingested_at TEXT,
        raw_payload TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ DB initialized at", DB_PATH)


if __name__ == "__main__":
    init_db()