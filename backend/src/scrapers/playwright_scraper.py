# src/scrapers/playwright_scraper.py

from playwright.sync_api import sync_playwright
import json
import os

# -----------------------------
# 1️⃣ Set up paths (Windows-friendly)
# -----------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_RAW_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw')

# Create folder if it doesn't exist
os.makedirs(DATA_RAW_PATH, exist_ok=True)

# -----------------------------
# 2️⃣ Prepare to capture JSON
# -----------------------------
captured_data = []

def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=True → runs in background
        page = browser.new_page()

        # Replace this URL with the target site you want to scrape
        page.goto("https://www.ubereats.com/")

        # Capture JSON network responses
        def handle_response(response):
            if "application/json" in response.headers.get("content-type", ""):
                try:
                    json_data = response.json()
                    captured_data.append(json_data)
                except:
                    pass  # ignore responses that fail

        page.on("response", handle_response)

        # Wait some time to capture responses
        page.wait_for_timeout(10000)  # 10 seconds
        browser.close()

    # -----------------------------
    # 3️⃣ Save captured JSON
    # -----------------------------
    output_file = os.path.join(DATA_RAW_PATH, 'restaurants.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(captured_data, f, ensure_ascii=False, indent=4)

    print(f"✅ JSON saved to {output_file}")

# -----------------------------
# 4️⃣ Run scraper
# -----------------------------
if __name__ == "__main__":
    run_scraper()