import re

from playwright.sync_api import Page, expect


class RegistrationPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator("[data-test=\"first-full_name\"]")
        self.last_name = page.locator("[data-test=\"last-full_name\"]")
        self.date_of_birth = page.locator("[data-test=\"dob\"]")

        #adress
        self.street = page.locator("[data-test=\"street\"]")
        self.postal_code = page.locator("[data-test=\"postal_code\"]")
        self.city = page.locator("[data-test=\"city\"]")
        self.state = page.locator("[data-test=\"state\"]")
        self.country = page.locator("[data-test=\"country\"]")

        self.phone = page.locator("[data-test=\"phone\"]")
        self.email = page.locator("[data-test=\"email\"]")
        self.password = page.locator("[data-test=\"password\"]")
        self.show_password = page.locator("[data-icon=\"eye\"]")
        self.hide_password = page.locator("[data-icon=\"eye-slash\"]")
        self.password_strength = page.locator(".fill")

        self.register_submit_btn = page.locator("[data-test=\"register-submit\"]")
