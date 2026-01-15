import re

import pytest

from tool_shop.pages.web_pages.main_page import MainPage


def extract_price_from_text(text: str) -> float:
    match = re.search(r"[\d.,]+", text)
    if not match:
        raise ValueError(f"Не удалось извлечь цену из: {text}")
    return float(match.group().replace(",", "."))

@pytest.fixture
def main_page(browser):
    context = browser.new_context()
    page = context.new_page()
    mp = MainPage(page)
    mp.navigate()
    yield mp
    context.close()
