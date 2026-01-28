import pandas as pd
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent.parent
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "holiday_menu_matches.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "top_dishes_per_holiday.csv"

CHUNK_SIZE = 1_000_000

def main():
    print("📥 Computing top dishes per holiday (chunked)...")

    counts = defaultdict(int)

    for chunk in pd.read_csv(
        INPUT_PATH,
        chunksize=CHUNK_SIZE,
        usecols=["holiday_name", "menu_item"]
    ):
        for _, row in chunk.iterrows():
            key = (row["holiday_name"], row["menu_item"])
            counts[key] += 1

        print(f"Processed {len(chunk)} rows...")

    # Convert to DataFrame
    df = pd.DataFrame(
        [(h, m, c) for (h, m), c in counts.items()],
        columns=["holiday_name", "menu_item", "match_count"]
    )

    # Keep top 5 dishes per holiday
    df = (
        df.sort_values(["holiday_name", "match_count"], ascending=[True, False])
          .groupby("holiday_name")
          .head(5)
          .reset_index(drop=True)
    )

    df.to_csv(OUTPUT_PATH, index=False)

    print("✅ Top dishes per holiday computed")
    print(f"📁 Output saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
