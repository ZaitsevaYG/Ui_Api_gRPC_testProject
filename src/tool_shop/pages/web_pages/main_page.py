import requests
import response
from playwright.sync_api import Page, expect
import allure

from tests.ui.conftest import extract_price_from_text
from tool_shop.data.data import main_link, Product


class MainPage:

    def __init__(self, page: Page, product: Product):
        self.page = page
        self.product = product

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
        self.min_price_slider = page.get_by_role("slider", name="ngx-slider")
        self.max_price_slider = page.get_by_role("slider", name="ngx-slider-max")

        #Пагинация
        self.previous_page_btn = page.get_by_role("button", name="Previous")
        self.next_page_btn = page.get_by_role("button", name="Next")
        self.third_page_btn = page.get_by_role("button", name="Page-3")
        self.fifth_page_btn = page.get_by_role("button", name="Page-5")

        #Элемент
        self.product_cards = page.locator("[data-test^='product-']")
        self.search_caption = page.locator("[data-test='search-caption']")
        self.search_completed = page.locator("[data-test='search_completed']")
        self.product_card_name = page.locator("[data-test='product-name']")
        self.product_card_price = page.locator("[data-test='product-price']")
        self.eco_badge = page.locator("[data-test='eco-badge']")
        self.rating_badge = page.locator("[data-test='co2-rating-badge']")


    def navigate_main_page(self):
        self.page.goto(main_link, wait_until='domcontentloaded', timeout=60000)
        expect(self.product_cards.first).to_be_visible(timeout=10000)


    def search_by_the_name(self, product):
        self.search_field.click()
        self.search_field.type(product.name)
        self.search_btn.click()

    def check_search_results(self, product):
        expect(self.search_caption).to_be_visible(timeout=10000)
        expect(self.search_completed).to_be_visible(timeout=10000)
        expect(self.search_caption).to_have_text(f"Searched for: {product.name}")
        expect(self.product_card_name).to_have_text(product.name)

    def search_for_eco_tools(self):
        self.filters_sustainability.click(timeout=10000)


    def check_eco_search_results(self):
        total_count = self.product_cards.count()
        for i in range(total_count):
            card = self.product_cards.nth(i)

            eco_badge = card.locator("[data-test='eco-badge']")
            expect(eco_badge).to_be_visible(timeout=5000)

            rating_badge = card.locator("[data-test='co2-rating-badge']")
            expect(rating_badge).to_be_visible(timeout=5000)
            active_letter_el = rating_badge.locator("span.active")
            active_letter = active_letter_el.text_content().strip()

            with allure.step(f"Карточка #{i + 1}: CO2 рейтинг = '{active_letter}'"):
                assert active_letter in ["A", "B"], \
                    f"Карточка #{i + 1}: ожидается A или B, получено '{active_letter}'"


    def set_price_filter(self):
        self.min_price_slider.drag_to(self.page.locator(".ngx-slider-pointer").nth(15))
        self.max_price_slider.drag_to(self.page.locator(".ngx-slider-pointer").nth(28))
        expect(self.product_cards.count()).to_equal(9)


    def check_price_filter_search_results_with_api_check(self):
        ui_prices = []
        for i in range (self.product_cards.count()):
            price_text = self.product_cards.nth(i).locator("[data-test='product-price']").text_content()
            ui_prices.append(round(extract_price_from_text(price_text), 2))
        with allure.step(f"UI: {len(ui_prices)} товаров в диапазоне 15–28"):
            pass


        response = requests.get(
            "http://localhost:8091/products",
            params={"between": "price, 15, 28"}
        )
        response.raise_for_status()
        api_prices = [round(float(p["price"]), 2) for p in response.json()]

        assert sorted(ui_prices) == sorted(api_prices)

    def get_product_ids(self):
        ids = []
        for i in range(self.product_cards.count()):
            full_attr = self.product_cards.nth(i).get_attribute("data-test") or ""
            ids.append(full_attr)
        return ids




