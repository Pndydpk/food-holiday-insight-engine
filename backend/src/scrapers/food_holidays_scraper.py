# src/scrapers/food_holidays_scraper.py
import os, time, sqlite3, logging
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("food_holidays_scraper")

PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "food_holidays.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Try a few candidate URLs (we will attempt the first that returns content)
URLS = [
    "https://foodimentary.com/today-in-national-food-holidays/",
    "https://www.daysoftheyear.com/what-to-eat/",
    "https://www.checkiday.com/categories/food"
]

def init_driver(visible=True):
    opts = Options()
    if not visible:
        opts.add_argument("--headless=new")
    else:
        # visible browser
        opts.headless = False
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--window-size=1400,1000")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    return driver

def fetch_and_parse(url, visible=True, scroll_pause=2, scroll_attempts=10):
    logger.info(f"Opening: {url} (visible={visible})")
    driver = init_driver(visible=visible)
    try:
        driver.get(url)
    except Exception as e:
        logger.error(f"Driver.get() failed: {e}")
        driver.quit()
        return None

    # Scroll loop: attempt several scrolls to let JS load content
    prev_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(scroll_attempts):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)  # wait for additional JS/XHR
        new_height = driver.execute_script("return document.body.scrollHeight")
        logger.info(f"Scrolled {i+1}/{scroll_attempts} — height {prev_height}->{new_height}")
        if new_height == prev_height:
            break
        prev_height = new_height

    # small wait for last XHRs
    logger.info("Waiting 3s for final render...")
    time.sleep(3)

    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")
    return soup

def extract_holidays_from_soup(soup):
    if soup is None:
        return []

    # Debug: print a small preview (first 800 chars)
    snippet = soup.prettify()[:800].replace("\n"," ")
    logger.info("Page snippet (first 800 chars):\n" + snippet)

    # Candidate selectors / heuristics (try each until we find content)
    candidate_selectors = [
        ("article", ["h1","h2","h3"], ["time",".date","span"]),
        ("article.card", ["h3","h2","h1"], [".date","time","span"]),
        (".holiday", ["h3","h2","h1"], [".holiday-date","time",".date"]),
        (".post-item", ["h2","h3","h1"], ["time",".date"]),
        (".entry", ["h1","h2","h3"], ["time",".date"]),
        (".archive-item", ["h2","h3"], ["time",".date"]),
    ]

    for sel, title_tags, date_selectors in candidate_selectors:
        nodes = soup.select(sel)
        if not nodes:
            continue
        logger.info(f"Selector '{sel}' returned {len(nodes)} nodes — attempting extraction")
        holidays = []
        for node in nodes:
            # title
            title = None
            for t in title_tags:
                el = node.find(t)
                if el and el.get_text(strip=True):
                    title = el.get_text(strip=True)
                    break
            if not title:
                # fallback: anchor text
                a = node.find("a")
                if a and a.get_text(strip=True):
                    title = a.get_text(strip=True)
            # date
            date_text = None
            for dsel in date_selectors:
                try:
                    if dsel.startswith("."):
                        el = node.select_one(dsel)
                    else:
                        el = node.find(dsel)
                except:
                    el = None
                if el:
                    date_text = el.get_text(strip=True)
                    break
            # final validation
            if title:
                holidays.append((title, date_text if date_text else "N/A"))
        if holidays:
            logger.info(f"Extracted {len(holidays)} holidays using selector '{sel}'")
            return holidays

    # As a last resort: find all elements whose class contains "holiday" or "food"
    fallback = []
    for node in soup.find_all(['div','article','li']):
        cls = " ".join(node.get("class") or [])
        if any(term in cls.lower() for term in ("holiday","food","day","event")):
            text = node.get_text(" ", strip=True)
            if text and len(text) < 300:  # heuristic
                fallback.append((text[:80], "N/A"))
    if fallback:
        logger.info(f"Fallback extracted {len(fallback)} items")
    return fallback

def save_to_db(holidays):
    if not holidays:
        logger.warning("No holidays to save.")
        return 0
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS food_holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            date TEXT
        )
    """)
    cur.executemany("INSERT OR IGNORE INTO food_holidays (name, date) VALUES (?, ?)", holidays)
    conn.commit()
    conn.close()
    return len(holidays)

def main(visible=True):
    # try each candidate URL until one yields results
    for url in URLS:
        soup = fetch_and_parse(url, visible=visible, scroll_pause=2, scroll_attempts=12)
        holidays = extract_holidays_from_soup(soup)
        if holidays:
            saved = save_to_db(holidays)
            logger.info(f"Saved {saved} holidays from {url}")
            print(f"✅ Found and saved {saved} holidays from {url}")
            return
    # If none worked:
    print("⚠️ Scraper found 0 holidays on all candidate sites.")

if __name__ == "__main__":
    main(visible=True)   # visible=True so you can watch the browserfoo