from playwright.sync_api import Page

from src.tool_shop.data.data import Product


class AccountPage:
    def __init__(self, product: Product, page: Page):
        self.page = page
        self.go_to_favorites = page.locator('[data-test="nav-favorites"]')
        self.go_to_profile = page.locator('[data-test="nav-profile"]')
        self.go_to_invoices = page.locator('[data-test="nav-invoices"]')
        self.go_to_messages = page.locator('[data-test="nav-messages"]')

        self.product_in_fav = page.locator("[data-test^='favorite-'] [data-test='product-full_name']")
        self.delete_from_fav = page.locator('[data-test^="favorite-"] [data-test="delete"]')


