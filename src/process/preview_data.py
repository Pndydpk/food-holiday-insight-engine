import sqlite3
import pandas as pd

# Connect to SQLite database
DB_PATH = "data/processed/uber_eats.db"
conn = sqlite3.connect(DB_PATH)

# Preview 5 restaurants
restaurants_preview = pd.read_sql_query("SELECT * FROM restaurants LIMIT 5;", conn)
print("Restaurants preview:")
print(restaurants_preview)

print("\n" + "-"*50 + "\n")

# Preview 5 menu items
menus_preview = pd.read_sql_query("SELECT * FROM menus LIMIT 5;", conn)
print("Menus preview:")
print(menus_preview)

conn.close()