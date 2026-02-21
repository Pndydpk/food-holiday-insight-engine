import pandas as pd
import numpy as np
import os

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw')
os.makedirs(RAW_PATH, exist_ok=True)

# -----------------------------
# Load original restaurants CSV
# -----------------------------
restaurants = pd.read_csv(os.path.join(RAW_PATH, 'restaurants.csv'))

# -----------------------------
# Expand restaurants (manageable)
# -----------------------------
scale_restaurants = 50  # adjust to get ~2.5M restaurants if original ~50k
restaurants_big = pd.concat([restaurants]*scale_restaurants, ignore_index=True)
restaurants_big['restaurant_id'] = range(1, len(restaurants_big)+1)
restaurants_big['rating'] = np.round(np.random.uniform(1, 5, size=len(restaurants_big)), 2)

restaurants_big.to_csv(os.path.join(RAW_PATH, 'restaurants_big.csv'), index=False)
print(f"✅ Restaurants expanded: {len(restaurants_big)} rows")

# -----------------------------
# Read and expand menu in chunks
# -----------------------------
chunksize = 500_000  # 0.5M rows per chunk
menu_csv_path = os.path.join(RAW_PATH, 'restaurant_menus_big.csv')
chunksize = 500_000

# Create iterator
menu_reader = pd.read_csv(
    os.path.join(RAW_PATH, 'restaurant-menus.csv'),
    engine='python',
    on_bad_lines='skip',
    chunksize=chunksize
)

for i, chunk in enumerate(menu_reader):
    try:
        # Process the chunk
        chunk['menu_id'] = range(i*chunksize + 1, i*chunksize + len(chunk) + 1)
        chunk['restaurant_id'] = np.random.choice(restaurants_big['restaurant_id'], size=len(chunk))
        chunk['price'] = np.round(np.random.uniform(50, 500, size=len(chunk)), 2)

        # Write to CSV
        if i == 0:
            chunk.to_csv(menu_csv_path, index=False)
        else:
            chunk.to_csv(menu_csv_path, index=False, mode='a', header=False)

        print(f"✅ Chunk {i+1} processed and written")
        
    except Exception as e:
        print(f"⚠️ Warning: skipping chunk {i+1} due to error: {e}")
        continue

print(f"✅ Big data CSVs generated in {RAW_PATH}")