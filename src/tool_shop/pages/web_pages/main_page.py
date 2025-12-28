
from playwright.sync_api import Page, expect


class MainPage:

    def __init__(self, page: Page):
        self.page = page

        #Навигационное меню
        self.home_btn = page.locator("[data-test=\"nav-home\"]")
        self.categories_btn = page.locator("[data-test=\"nav-categories\"]")
        self.contact_btn = page.locator("[data-test=\"nav-contact\"]")
        self.sing_in_btn = page.locator("[data-test=\"nav-sign-in\"]")
