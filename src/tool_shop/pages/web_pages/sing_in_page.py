import allure
from playwright.sync_api import Page, expect

from tool_shop.data.data import User
from config import Config
from tool_shop.data.helpers import attach_screenshot


class SingInPage:
    def __init__(self, page: Page):
        self.page = page

        self.email = page.locator("[data-test='email']")
        self.password = page.locator("[data-test='password']")
        self.show_password = page.locator("[data-icon='eye']")
        self.hide_password = page.locator("[data-icon='eye-slash']")
        self.submit_btn = page.locator("[data-test='login-submit']")

        self.my_account_title = page.locator("[data-test='page-title']")
        self.error_message_box = page.locator("[data-test='login-error']")

    def navigate(self):
        with allure.step(f"Загрузка страницы логина"):
            self.page.goto( f"{Config.UI_BASE_URL}/auth/login", timeout=60000)
            expect(self.email).to_be_visible(timeout=60000)

    def singing_in(self, user: User):

        with allure.step("Внести данные юзера"):
            expect(self.email).to_be_visible()
            self.email.fill(user.email)
            self.password.fill(user.password)
            expect(self.password).to_have_attribute("type", "password")

        with allure.step("Нажать кнопку 'Показать пароль'"):
            self.show_password.click(timeout=6000)
            expect(self.password).to_have_attribute("type", "text")
            attach_screenshot(self.page, "Нажата кнопка 'Показать пароль'")

        with allure.step("Нажать кнопку 'Скрыть пароль'"):
            self.hide_password.click(timeout=6000)
            expect(self.password).to_have_attribute("type", "password")
            attach_screenshot(self.page, "Нажата кнопка 'Скрыть пароль'")

        with allure.step("Нажать кнопку 'Login'"):
            self.submit_btn.click(timeout=6000)


    def check_successful_login (self):
        expect(self.page).to_have_url("http://localhost:4200/account", timeout=15000)
        expect(self.my_account_title).to_be_visible(timeout=10000)
        expect(self.my_account_title).to_have_text("My account")
        attach_screenshot(self.page, "Логин успешно совершен. Перенаправление на страницу 'Мой аккаунт'")


    def check_unsuccessful_login(self):
        expect(self.error_message_box).to_be_visible(timeout=6000)
        expect(self.error_message_box).to_have_text("Invalid email or password")
        attach_screenshot(self.page, "Логин не совершен. Возникает ошибка")


