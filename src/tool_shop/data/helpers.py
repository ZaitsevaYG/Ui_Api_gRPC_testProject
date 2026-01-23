import re

import allure
from playwright.sync_api import Page, expect


def parse_price(text: str) -> float:
    clean = text.replace("$", "").replace("\u00a0", "").strip()
    return float(clean)

def parse_discount(text: str) -> float:
    clean = text.replace("- $", "").replace("\u00a0", "").strip()
    return float(clean)

def save_auth_state(page):
    storage_state = page.context.storage_state()
    return storage_state

def attach_screenshot(page: Page, name: str = "Скриншот"):
    screenshot = page.screenshot(timeout=5000, type='jpeg')
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.JPG
    )

