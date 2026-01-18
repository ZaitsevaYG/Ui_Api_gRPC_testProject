import allure

from tool_shop.data.data import Product
from playwright.sync_api import Page, expect

from tool_shop.data.utils import attach_screenshot


class FavoritesPage:
    def __init__(self, product: Product, page: Page):
        self.page = page
        self.product = product

        self.product_in_favorites =  page.locator(f"[data-test='favorite-{product.id}']")
        self.product_name_in_fav = page.locator(f"[data-test='favorite-{product.id}'] [data-test='product-name']")
        self.product_description_in_fav = page.locator(f"[data-test='favorite-{product.id}'] [data-test='product-description']")
        self.product_delete_from_fav = page.locator(f"[data-test='favorite-{product.id}'] [data-test='delete']")

        self.no_favorites_message = page.locator("div:has-text('There are no favorites yet')")


    def check_product_in_favorites_and_delete(self, product: Product):
        with allure.step("Проверка наличия товара в избранном"):
            expect(self.product_in_favorites).to_be_visible()
            expect(self.product_name_in_fav).to_have_text(product.name)
            expect(self.product_description_in_fav).not_to_be_empty()
            attach_screenshot(self.page, "Товар добавлен в избранное.")
        expect(self.product_delete_from_fav).to_be_enabled()
        with allure.step("Проверка возможности удаления товара из избранного"):
            self.product_delete_from_fav.click(timeout=60000)
            expect(self.no_favorites_message).to_be_visible()
            expect(self.no_favorites_message).to_have_text(
                "There are no favorites yet. In order to add favorites, please go to the product listing and mark some products as your favorite."
            )
            attach_screenshot(self.page, "Товар удален из избранного")

