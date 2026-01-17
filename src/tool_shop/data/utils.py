import re

import allure
from playwright.sync_api import Page, expect


def extract_price_from_text(text: str) -> float:
    match = re.search(r"[\d.,]+", text)
    if not match:
        raise ValueError(f"Не удалось извлечь цену из: {text}")
    return float(match.group().replace(",", "."))


def attach_screenshot(page: Page, name: str = "Скриншот"):

    screenshot = page.screenshot(timeout=5000, type='jpeg')
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.JPG
    )