import allure
from playwright.sync_api import Page, expect
from src.tool_shop.data.data import Product


class ProductPage:
    def __init__(self, product: Product, page: Page):
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

        self.add_to_card = page.locator("[data-test='add-to-cart']")
        self.add_to_favorites = page.locator("[data-test='add-to-favorites']")
        
        self.alert_message = page.get_by_role("alert")
        self.go_to_cart = page.locator("[data-test='nav-cart']")
        self.cart_quantity = page.locator("[data-test='cart-quantity']")

    def navigate(self):
        with allure.step(f"Загрузка страницы товара"):
            self.page.goto(self.product.url, timeout=60000)
            expect(self.product_description).to_be_visible(timeout=60000)

    def check_product_details(self, product: Product):
        with allure.step(f"Проверка, что на странице товара отображаются верные значения и активны кнопки"):
            expect(self.product_price).to_equal(product.price)
            expect(self.product_name).to_equal(product.name)
            expect(self.product_description).to_be_visible()
            expect(self.add_to_card).not_to_be_disabled()
            expect(self.add_to_card).to_be_enabled()
            expect(self.add_to_favorites).not_to_be_disabled()
            expect(self.add_to_favorites).to_be_enabled()
            expect(self.category_badge).to_have_text(product.category)
            expect(self.brand_badge).to_have_text(product.brand)

    def check_co2_rating(self, product: Product):
        with allure.step(f"Проверка CO2 рейтинга: {product.co2}"):
            # Локатор активного рейтинга
            active_span = self.page.locator(
                '[data-test="co2-rating-badge"] .co2-letter.active'
            )
            # Проверки
            expect(active_span).to_be_visible()
            expect(active_span).to_have_text(product.co2.upper())
            expect(active_span).to_have_class(f"rating-{product.co2.lower()}")
            # Дополнительно: все spans существуют
            expect(self.page.locator('[data-test="co2-rating-badge"] .co2-letter')).to_have_count(5)






