import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "holiday_menu_matches.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "holiday_popularity.csv"

CHUNK_SIZE = 1_000_000  # safe for your system

def main():
    print("📥 Computing holiday popularity (chunked)...")

    holiday_counts = {}

    for chunk in pd.read_csv(INPUT_PATH, chunksize=CHUNK_SIZE):
        counts = chunk["holiday_name"].value_counts()

        for holiday, cnt in counts.items():
            holiday_counts[holiday] = holiday_counts.get(holiday, 0) + cnt

        print(f"Processed {len(chunk)} rows...")

    # Convert to DataFrame
    popularity_df = (
        pd.DataFrame(holiday_counts.items(), columns=["holiday_name", "match_count"])
        .sort_values("match_count", ascending=False)
        .reset_index(drop=True)
    )

    # Normalize to 0–100
    max_count = popularity_df["match_count"].max()
    popularity_df["popularity_score"] = (
        (popularity_df["match_count"] / max_count) * 100
    ).round(2)

    popularity_df.to_csv(OUTPUT_PATH, index=False)

    print("✅ Holiday popularity computed successfully")
    print(f"📁 Output saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
