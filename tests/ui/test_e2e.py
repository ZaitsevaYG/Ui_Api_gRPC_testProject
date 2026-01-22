import time

import allure
import testit
from playwright.sync_api import Page, expect
from tool_shop.data.data import THORHUMMER, TESTUSER1, WOODSAW, GUESTUSER, MEASURINGTAPE
from tool_shop.data.helpers import attach_screenshot, parse_price
from tool_shop.pages.web_pages.cart_page import CartPage
from tool_shop.pages.web_pages.favorites_page import FavoritesPage
from tool_shop.pages.web_pages.product_page import ProductPage
from tool_shop.pages.web_pages.sing_in_page import SingInPage


@testit.externalId("UI-8")
@testit.displayName("Добавление товара в избранное")
@allure.title("UI-8: Проверка функции добавления товара в избранное")
@allure.tag('product', 'ui', 'favorites')
@allure.feature("Действия с товаром")
@allure.severity('medium')
def test_add_to_favorites_e2e(page):
    # Логин
    login_page = SingInPage(page)
    login_page.navigate()
    login_page.singing_in(TESTUSER1)


    logged_user_menu = page.locator('[data-test="nav-menu"]')
    expect(logged_user_menu).to_contain_text("Jane Doe", timeout=10000)

    # Товар
    product_page = ProductPage(page, THORHUMMER)
    product_page.navigate()

    # Избранное

    product_page.add_to_favorites_and_check()
    product_page.go_to_favorites()

    fav_page = FavoritesPage(page, THORHUMMER)
    attach_screenshot(fav_page.page, "Избранное")

    with allure.step("Переход на страницу избранного и взаимодействие с товаром"):
        fav_page.check_product_in_favorites_and_delete()


@testit.externalId("UI-12")
@testit.displayName("Оформление заказа зарегистрированным пользователем")
@allure.title("UI-12: Проверка возможности оформить заказ зарегистрированным пользователем")
@allure.tag('ui', 'cart')
@allure.feature("Корзина")
@allure.severity('critical')
def test_successful_checkout_logged_user_e2e(page):

    with allure.step("Пользователь добавляет 2 товара в корзину"):
        # 1 item
        product_page1 = ProductPage(page,THORHUMMER)
        product_page1.navigate()
        product_page1.add_to_cart()
        # 2 item
        product_page2 = ProductPage(page,MEASURINGTAPE)
        product_page2.navigate()
        product_page2.add_to_cart()

    with allure.step("Переход в корзину"):
        product_page2.go_to_cart()
        cart_page = CartPage(page)
        cart_page.items_count = 2
        expect(cart_page.proceed_to_checkout_cart).to_be_visible(timeout=60000)

    with allure.step("Покупка товара - happy path - Logged user, Cash billing"):
        cart_page.proceed_to_checkout_cart.click()
        cart_page.sining_in_via_cart(TESTUSER1)
        cart_page.billing_window(TESTUSER1)
        cart_page.payment_window_cash()

@testit.externalId("UI-13")
@testit.displayName("Оформление заказа пользователем-гостем")
@allure.title("UI-13: Проверка возможности оформить заказ зарегистрированным пользователем-гостем")
@allure.tag('ui', 'cart')
@allure.feature("Корзина")
@allure.severity('critical')
def test_successful_checkout_guest_user_e2e(page):
    with allure.step("Пользователь добавляет товар в корзину"):
        product_page = ProductPage(page,WOODSAW)
        product_page.navigate()
        product_page.add_to_cart()

    with allure.step("Переход в корзину"):
        product_page.go_to_cart()
        cart_page = CartPage(page)
        expect(cart_page.proceed_to_checkout_cart).to_be_visible(timeout=60000)

    with allure.step("Покупка товара - happy path - Guest user, Card billing"):
        cart_page.proceed_to_checkout_cart.click()
        cart_page.singin_window_guest_user(GUESTUSER)
        cart_page.billing_window(GUESTUSER)
        cart_page.payment_window_card(GUESTUSER)



