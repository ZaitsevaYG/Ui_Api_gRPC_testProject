import allure
from playwright.sync_api import Page, expect


def attach_screenshot(page: Page, name: str = "Скриншот"):

    screenshot = page.screenshot(timeout=5000, type='jpeg')
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.JPG
    )