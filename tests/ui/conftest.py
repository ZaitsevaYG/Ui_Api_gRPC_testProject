
import pytest

from tool_shop.data.data import THORHUMMER
from tool_shop.pages.web_pages.main_page import MainPage
from tool_shop.pages.web_pages.product_page import ProductPage
from tool_shop.pages.web_pages.sing_in_page import SingInPage


@pytest.fixture
def main_page(browser):
    context = browser.new_context()
    page = context.new_page()
    mp = MainPage(page)
    mp.navigate()
    yield mp
    context.close()

@pytest.fixture
def product_page(browser):
    context = browser.new_context()
    page = context.new_page()
    pp = ProductPage(page, THORHUMMER)
    pp.navigate()
    yield pp
    context.close()

@pytest.fixture
def singin_page(browser):
    context = browser.new_context()
    page = context.new_page()
    sp = SingInPage(page)
    sp.navigate()
    yield sp
    context.close()

