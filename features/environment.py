"""Set up a browser for Behave tests (requires Chrome or Chromium)."""
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def before_all(context):
    context.base_url = os.getenv("BASE_URL", "http://127.0.0.1:8080")
    context.wait_seconds = 10
    options = Options()
    if os.getenv("HEADLESS", "1") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    context.driver = webdriver.Chrome(options=options)


def after_all(context):
    context.driver.quit()
