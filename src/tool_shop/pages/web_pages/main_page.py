
from playwright.sync_api import Page, expect
import allure

class MainPage:

    def __init__(self, page: Page):
        self.page = page

        #Навигационное меню
        self.home_btn = page.locator("[data-test=\"nav-home\"]")
        self.categories_btn = page.locator("[data-test=\"nav-categories\"]")
        self.contact_btn = page.locator("[data-test=\"nav-contact\"]")
        self.sing_in_btn = page.locator("[data-test=\"nav-sign-in\"]")

        #Фильтры
        self.sort_dropdown_price_desc = page.locator("[data-test=\"sort\"]").select_option("price,desc")
        self.search_field = page.locator("[data-test=\"search-query\"]")
        self.search_btn = page.locator("[data-test=\"search-submit\"]")
        self.filters_power_tools = page.locator("#filters").get_by_text("Power Tools")
        self.filters_brand = page.get_by_text("ForgeFlex Tools")
        self.filters_sustainability = page.get_by_text("Show only eco-friendly")

        #Пагинация
        self.previous_page_btn = page.get_by_role("button", name="Previous")
        self.next_page_btn = page.get_by_role("button", name="Next")
        self.third_page_btn = page.get_by_role("button", name="Page-3")
        self.fifth_page_btn = page.get_by_role("button", name="Page-5")

        #Элемент
        self.product_card = page.locator("[data-test=\"product-name\"]")

