import allure
from selene import browser, have, be
from tool_shop.data.data import TESTUSER1, THORHUMMER, WRONGUSER, WRONGMAIL, SHORTPASSWORD
from tool_shop.data.helpers import attach_mobile_screenshot
from tool_shop.pages.android_app_pages.app_main_page import mp


@allure.title("APP-1: Проверка возможности аутентифицироваться через мобильное приложение")
@allure.tag('mobile', 'auth')
@allure.feature("Аутентификация")
@allure.severity('critical')
def test_app_login(android_mobile_management):
    mp.menu_btn_click()
    mp.sing_in(TESTUSER1)
    attach_mobile_screenshot()



@allure.title("APP-2: Проверка возможности отправить контакт-форму")
@allure.tag('mobile', 'contact')
@allure.feature("Контакт-форма")
@allure.severity('low')
def test_app_contact_form(android_mobile_management):
    mp.menu_btn_click()
    mp.contact_form(TESTUSER1)


@allure.title("APP-3: Поиск товара по названию")
@allure.tag('mobile', 'search')
@allure.feature("Поиск")
@allure.severity('high')
def test_app_search_for_an_item(android_mobile_management):
    mp.search_for_the_item()
    attach_mobile_screenshot()


@allure.title("APP-4: Добавление в корзину различных товаров продукт + арендный товар")
@allure.tag('mobile', 'product')
@allure.feature("Действия с товаром")
@allure.severity('high')
def test_app_add_products_rental_to_carts(android_mobile_management):
    mp.add_item_to_cart_and_check()
    mp.rentals()
    mp.add_item_to_cart_and_check()
    mp.go_to_cart()


@allure.title("APP-8: Попытка залогиниться с несуществующим пользователем")
@allure.tag('mobile', 'auth')
@allure.feature("Аутентификация")
@allure.severity('high')
def test_app_login_unexistent_user(android_mobile_management):
    mp.menu_btn_click()
    mp.sing_in(WRONGUSER)
    browser.element(mp.error_message).with_(timeout=10).should(be.visible.and_(have.text("Unauthorized")))
    attach_mobile_screenshot()

@allure.title("APP-9: Попытка залогиниться с невалидным email")
@allure.tag('mobile', 'auth')
@allure.feature("Аутентификация")
@allure.severity('high')
def test_app_bad_email(android_mobile_management):
    mp.menu_btn_click()
    mp.sing_in(WRONGMAIL)
    browser.element(mp.email_error).with_(timeout=10).should(be.visible.and_(have.text("Invalid email format")))
    attach_mobile_screenshot()


@allure.title("APP-10: Попытка залогиниться с невалидным паролем")
@allure.tag('mobile', 'auth')
@allure.feature("Аутентификация")
@allure.severity('high')
def test_app_bad_password(android_mobile_management):
    mp.menu_btn_click()
    mp.sing_in(SHORTPASSWORD)
    browser.element(mp.password_error).with_(timeout=10).should(be.visible.and_(have.text("Password must be between 6 and 40 characters")))
    attach_mobile_screenshot()


