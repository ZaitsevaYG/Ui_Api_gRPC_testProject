from selene import browser
import allure
import config
from playwright.sync_api import Page


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
def attach_mobile_screenshot(name: str = "Скриншот"):
    screenshot = browser.driver.get_screenshot_as_png()
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.PNG
    )


def attach_bstack_video(session_id):

    import requests
    bstack_session = requests.get(
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        auth=("janazaitseva_ckHfp4", "ULcqpKU4NxAupDncjgJV"),
    ).json()
    print(bstack_session)
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML,
    )