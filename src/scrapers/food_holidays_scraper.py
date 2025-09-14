# src/scrapers/food_holidays_scraper.py

import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# SQLite DB path
DB_PATH = "data/processed/uber_eats.db"

# Target URL
URL = "https://nationaltoday.com/food-beverage-holidays/"

# Selenium setup
options = webdriver.ChromeOptions()
options.headless = False  # Keep browser visible to check scrolling & loading
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)

# Scroll page to load all holidays
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")
scrolls = 0

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    scrolls += 1
    print(f"📜 Scrolled {scrolls} times.")

# Grab all holiday elements
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.card"))
    )
    holiday_elements = driver.find_elements(By.CSS_SELECTOR, "article.card")
except TimeoutException:
    holiday_elements = []
    print("❌ Could not find holiday elements.")

holidays = []
for el in holiday_elements:
    try:
        name = el.find_element(By.TAG_NAME, "h3").text.strip()
        date = el.find_element(By.CLASS_NAME, "date").text.strip()
        holidays.append((name, date))
    except Exception:
        continue

driver.quit()

print(f"🔍 Found {len(holidays)} holidays.")

# Save to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_holidays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT
    )
""")

cursor.executemany("INSERT INTO food_holidays (name, date) VALUES (?, ?)", holidays)
conn.commit()
conn.close()

print(f"✅ Saved {len(holidays)} holidays to food_holidays table.")