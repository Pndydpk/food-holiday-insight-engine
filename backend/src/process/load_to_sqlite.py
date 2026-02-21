import os
import sqlite3
import pandas as pd

# Paths
RAW_PATH = os.path.join(os.getcwd(), 'data', 'raw')
PROCESSED_PATH = os.path.join(os.getcwd(), 'data', 'processed')
DB_PATH = os.path.join(PROCESSED_PATH, 'uber_eats.db')

restaurants_csv = os.path.join(RAW_PATH, 'restaurants_big.csv')
menus_csv = os.path.join(RAW_PATH, 'restaurant_menus_big.csv')

# Create processed folder if it doesn't exist
os.makedirs(PROCESSED_PATH, exist_ok=True)

# Connect to SQLite (creates file if not exists)
conn = sqlite3.connect(DB_PATH)
print("✅ Connected to SQLite database:", DB_PATH)

# ----------------------------
# Helper function to load CSV in chunks
# ----------------------------
def load_csv_to_sqlite(csv_path, table_name, chunk_size=100_000, max_chunks=None):
    print(f"➡️ Loading {csv_path} into table '{table_name}' with chunksize={chunk_size}")
    try:
        chunk_iter = pd.read_csv(csv_path, chunksize=chunk_size, on_bad_lines='skip', engine='python')
        for i, chunk in enumerate(chunk_iter, start=1):
            chunk.to_sql(table_name, conn, if_exists='append', index=False)
            print(f"✅ Chunk {i} written to '{table_name}'")
            if max_chunks and i >= max_chunks:
                print(f"⚠️ Stopping after {max_chunks} chunks (for testing)")
                break
    except Exception as e:
        print(f"❌ Error loading {table_name}: {e}")

# ----------------------------
# Load Restaurants
# ----------------------------
load_csv_to_sqlite(restaurants_csv, 'restaurants', chunk_size=100_000)

# ----------------------------
# Load Menus
# ----------------------------
load_csv_to_sqlite(menus_csv, 'menus', chunk_size=100_000)

# ----------------------------
# Close connection
# ----------------------------
conn.close()
print("✅ All data loaded into SQLite successfully!")