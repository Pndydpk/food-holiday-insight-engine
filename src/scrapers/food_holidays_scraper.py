# src/scrapers/food_holidays_scraper.py

import os
import time
import sqlite3
import logging
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import urllib3
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# SQLite DB path
DB_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "food_holidays.db")

def check_site_accessibility(url, max_retries=3):
    """Check if the site is accessible using requests library with retries"""
    session = requests.Session()
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to access site (attempt {attempt + 1}/{max_retries})...")
            response = session.get(
                url,
                verify=False,
                timeout=30,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            )
            if response.status_code == 200:
                logger.info("Successfully accessed the site!")
                return True
            logger.warning(f"Got status code {response.status_code}")
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
            continue
    logger.error("All attempts to access site failed")
    return False

# Target URL - try different URLs with more reliable sources
URLS = [
    "https://foodimentary.com/today-in-national-food-holidays/",
    "https://www.checkiday.com/categories/food",
    "https://www.daysoftheyear.com/categories/food-drink/",
    "https://www.holidayscalendar.com/categories/food/"
]

def get_best_url():
    """Try different URLs and return the one that works best"""
    for url in URLS:
        try:
            logger.info(f"Trying URL: {url}")
            response = requests.get(
                url,
                verify=False,
                timeout=30,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            )
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Check for presence of holiday-related content
                if any(word in response.text.lower() for word in ['holiday', 'food day', 'national day']):
                    logger.info(f"Found valid content at: {url}")
                    return url
        except Exception as e:
            logger.warning(f"Error checking {url}: {str(e)}")
            continue
    return URLS[0]  # Default to first URL if none work well

URL = get_best_url()

# Function to scrape holidays from a page
def scrape_holidays(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    try:
        logger.info(f"🌐 Fetching content from {url}")
        session = requests.Session()
        
        # First make a HEAD request to check content type
        head = session.head(url, headers=headers, verify=False, timeout=30)
        content_type = head.headers.get('content-type', '').lower()
        
        if 'text/html' not in content_type:
            logger.warning(f"Unexpected content type: {content_type}")
        
        # Now make the GET request with proper encoding handling
        response = session.get(url, headers=headers, verify=False, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        
        # Try to decode the content
        try:
            content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            content = response.content.decode('latin-1')
        
        soup = BeautifulSoup(content, 'html.parser')
        logger.info("✅ Successfully parsed the page")
        
        # Debug: Print part of the HTML for analysis
        logger.info("HTML Preview:")
        logger.info(soup.prettify()[:1000])
        
        # Try different CSS selectors for holiday elements
        holiday_elements = []
        selectors = [
            'article.holiday-card',
            'div.holiday-item',
            'div.calendar-entry',
            'div.holiday-listing article',
            'article.post-summary',
            '.post-item',
            'article.card',
            '.holiday-grid article',
            '.calendar-day',
            '.food-holiday'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                logger.info(f"Found {len(elements)} elements with selector: {selector}")
                holiday_elements = elements
                break
        
        if not holiday_elements:
            # Try finding elements by structure
            elements = soup.find_all(['article', 'div'], class_=lambda x: x and any(
                term in x.lower() for term in ['holiday', 'calendar', 'event', 'food-day']
            ))
            if elements:
                logger.info(f"Found {len(elements)} elements by class name analysis")
                holiday_elements = elements
        
        holidays = []
        for element in holiday_elements:
            try:
                # Try to find the holiday name
                name = None
                name_candidates = [
                    element.find(['h1', 'h2', 'h3', 'h4']),
                    element.find(class_=lambda x: x and any(
                        term in x.lower() for term in ['title', 'name', 'heading']
                    )),
                    element.find('a', href=True)
                ]
                
                for candidate in name_candidates:
                    if candidate and candidate.text.strip():
                        name = candidate.text.strip()
                        break
                
                # Try to find the date
                date = None
                date_candidates = [
                    element.find(class_=lambda x: x and any(
                        term in x.lower() for term in ['date', 'time', 'when']
                    )),
                    element.find('time'),
                    element.find(text=lambda x: x and any(
                        month in x.lower() for month in [
                            'january', 'february', 'march', 'april', 'may', 'june',
                            'july', 'august', 'september', 'october', 'november', 'december'
                        ]
                    ))
                ]
                
                for candidate in date_candidates:
                    if candidate:
                        date_text = candidate.text.strip() if hasattr(candidate, 'text') else candidate.strip()
                        if date_text:
                            date = date_text
                            break
                
                if name and date:
                    logger.info(f"Found holiday: {name} on {date}")
                    holidays.append((name, date))
                
            except Exception as e:
                logger.warning(f"Error extracting holiday info: {str(e)}")
                continue
        
        return holidays
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching content: {str(e)}")
        return []

# Scrape holidays from the URL
logger.info("Starting holiday scraping...")
holidays = scrape_holidays(URL)
logger.info(f"🎉 Finished scraping. Found {len(holidays)} holidays.")

print(f"🔍 Found {len(holidays)} holidays.")

# Ensure the database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

try:
    # Save to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,  -- Ensure no duplicate holidays
            date TEXT
        )
    """)

    # Use INSERT OR REPLACE to handle duplicates gracefully
    cursor.executemany(
        "INSERT OR REPLACE INTO food_holidays (name, date) VALUES (?, ?)", 
        holidays
    )
    conn.commit()
    print(f"✅ Saved {len(holidays)} holidays to food_holidays table.")
except sqlite3.Error as e:
    print(f"❌ Database error: {str(e)}")
    raise
finally:
    if 'conn' in locals():
        conn.close()