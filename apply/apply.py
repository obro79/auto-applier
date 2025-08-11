import sys
import re
import csv
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_driver(headless: bool = True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=opts)  # Selenium Manager resolves driver
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)  # light implicit wait for find_element
    return driver


def run(url: str, take_screenshot: bool):
    driver = build_driver(headless=True)
    try:
        driver.get(url)

        if take_screenshot:
            __capture_screenshot(driver, url)
        else:
            __save_page_text(driver, "main", url)
    finally:
        driver.quit()


def process_url(url, take_screenshot, retries=2, backoff_factor=1):
    for attempt in range(retries + 1):
        try:
            run(url, take_screenshot)
            break
        except WebDriverException as e:
            if attempt < retries:
                sleep_time = backoff_factor * (2 ** attempt)
                print(f"Error processing URL {url}, retrying in {sleep_time}s... ({attempt + 1}/{retries})")
                time.sleep(sleep_time)
            else:
                print(f"Failed to process URL {url} after {retries + 1} attempts: {e}")


def __save_page_text(driver, selector, url):
    title = driver.title or url
    try:
        main_text = driver.find_element(By.CSS_SELECTOR, selector).text
        if not main_text.strip():
            main_text = "Selector found but empty text"
    except NoSuchElementException:
        main_text = "No requested selector found"

    filename = __safe_filename_from(title) + ".txt"
    path = OUTPUT_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"URL: {url}\n")
        f.write(f"Title: {title}\n\n")
        f.write(main_text)

    print(f"Data saved as {path}")


def __capture_screenshot(driver, url):
    title = driver.title or url
    filename = __safe_filename_from(title) + ".png"
    path = OUTPUT_DIR / filename
    driver.save_screenshot(str(path))
    print(f"Screenshot saved as {path}")


def __safe_filename_from(title: str) -> str:
    safe = re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_")
    return safe or "page"


def read_urls_from_csv(file_path):
    urls = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            urls.append(row["loc"])
    return urls


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <csv_file> [--screenshot]")
        sys.exit(1)

    csv_file = sys.argv[1]
    take_screenshot = "--screenshot" in sys.argv

    urls = read_urls_from_csv(csv_file)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_url, url, take_screenshot) for url in urls]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error processing URL: {e}")
