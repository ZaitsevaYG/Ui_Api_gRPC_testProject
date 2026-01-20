import re

import allure
from playwright.sync_api import Page, expect
from src.tool_shop.data.data import Product
from tool_shop.data.utils import attach_screenshot


class ProductPage:
    def __init__(self, page: Page, product: Product):
        self.page = page
        self.product = product

        self.product_price = page.locator("[data-test='unit-price']")
        self.product_name = page.locator("[data-test='product-name']")
        self.product_description = page.locator("[data-test='product-description']")
        self.co_rating = page.locator("[data-test='co2-rating-badge']")
        self.category_badge = page.locator('span[aria-label="category"]')
        self.brand_badge = page.locator('span[aria-label="brand"]')

        self.quantity = page.locator("[data-test='quantity']")
        self.increase_quantity = page.locator("[data-test='increase-quantity']")
        self.decrease_quantity = page.locator("[data-test='decrease-quantity']")

        self.add_to_card_btn = page.locator("[data-test='add-to-cart']")
        self.add_to_favorites_btn = page.locator("[data-test='add-to-favorites']")
        
        self.alert_message = page.get_by_role("alert")
        self.go_to_cart_btn = page.locator("[data-test='nav-cart']")
        self.cart_quantity = page.locator("[data-test='cart-quantity']")
        self.go_to_favorites_btn = page.locator("[data-test='nav-my-favorites']")
        self.nav_account_toggle = page.locator("[data-test='nav-menu']")
        self.nav_favorites_link = page.locator("[data-test='nav-my-favorites']")

    def navigate(self):
        with allure.step(f"Загрузка страницы товара"):
            self.page.goto(self.product.url, timeout=60000)
            expect(self.product_description).to_be_visible(timeout=60000)

    def check_product_details(self):
        with allure.step(f"Проверка, что на странице товара отображаются верные значения и активны кнопки"):
            expect(self.product_price).to_have_text(str(self.product.price))
            expect(self.product_name).to_have_text(self.product.name)
            expect(self.product_description).to_be_visible()
            expect(self.add_to_card_btn).to_be_enabled()
            expect(self.add_to_favorites_btn).to_be_enabled()
            expect(self.category_badge).to_have_text(self.product.category)
            expect(self.brand_badge).to_have_text(self.product.brand)
            expect(self.product_description).not_to_be_empty()

    def check_co2_rating(self):
        with allure.step(f"Проверка CO2 рейтинга: {self.product.co2}"):
            active_span = self.page.locator('[data-test="co2-rating-badge"] .co2-letter.active')

            expect(active_span).to_be_visible()
            expect(active_span).to_have_text(self.product.co2.upper())

            expect(active_span).to_have_class(re.compile(rf"rating-{re.escape(self.product.co2.lower())}"))



    def add_to_cart_and_check(self):
        expect(self.add_to_card_btn).to_be_visible()
        expect(self.add_to_card_btn).to_be_enabled()
        self.add_to_card_btn.click(timeout=10000)
        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_have_text("Product added to shopping cart.")
        attach_screenshot(self.page, "Товар добавлен в корзину")
        expect(self.go_to_cart_btn).to_be_visible()
        expect(self.cart_quantity).to_have_text("1")

    def add_to_cart(self):
        expect(self.add_to_card_btn).to_be_visible()
        expect(self.add_to_card_btn).to_be_enabled()
        self.add_to_card_btn.click(timeout=10000)

    def add_to_favorites_and_check(self):
        expect(self.add_to_favorites_btn).to_be_visible(timeout=10000)
        expect(self.add_to_favorites_btn).to_be_enabled()
        self.add_to_favorites_btn.click(timeout=10000)
        expect(self.alert_message).to_be_visible()
        attach_screenshot(self.page, "Товар добавлен в избранное")
        expect(self.alert_message).to_have_text("Product added to your favorites list.")

    def add_to_favorites(self):
        expect(self.add_to_favorites_btn).to_be_visible()
        expect(self.add_to_favorites_btn).to_be_enabled()
        self.page.hover("[data-test='nav-profile']")
        self.page.wait_for_selector("[data-test='nav-my-favorites']", state="visible")
        self.add_to_favorites_btn.click(timeout=10000)

    def go_to_favorites(self):
        self.nav_account_toggle.hover()
        self.nav_account_toggle.click()
        self.page.wait_for_timeout(500)
        self.nav_favorites_link.click()
        expect(self.page).to_have_url("http://localhost:4200/account/favorites")

    def debug_menu(self):


        nav_elements = self.page.locator("[data-test*='nav']").all()
        for i, el in enumerate(nav_elements):
            print(f"{i}. {el.get_attribute('data-test')} = {el.text_content()}")

        self.page.hover("[data-test='nav-account']")
        self.page.wait_for_timeout(1000)





