import sys
import re
import csv
import time
import sa
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
import asyncio


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def fetch_job_description(url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        title = page.title()
        main = page.query_selector("main")
        text = main.inner_text() if main else "No requested selector found"
        print(text)
        browser.close()
    return text


def apply(playwright, url: str,):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)

    page.get_by_role('textbox').fill('Owen')
    browser.close()



if __name__ == "__main__":
    url = "https://rbcborealis.com/program-applications/winter-2026-ml-researcher-internship/"
    with sync_playwright() as playwright:
        apply(playwright,url)

    # with sync_playwright() as playwright:
    #     run(playwright, url, "RBC")
