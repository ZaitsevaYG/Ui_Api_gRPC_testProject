import time

import allure
import testit
from playwright.sync_api import expect
from tool_shop.data.data import THORHUMMER,  WOODSAW, MEASURINGTAPE
from tool_shop.data.utils import attach_screenshot, parse_price
from tool_shop.pages.web_pages.cart_page import CartPage
from tool_shop.pages.web_pages.product_page import ProductPage



@testit.externalId("UI-14")
@testit.displayName("Проверка данных + цены о товаре в корзине")
@allure.title("UI-14: Проверка отображения данных о товаре + цены в корзине")
@allure.tag('ui', 'cart')
@allure.feature("Корзина")
@allure.severity('medium')
def test_product_details_check(page):
    with allure.step("Пользователь добавляет эко товар в корзину"):
        product_page = ProductPage(page,WOODSAW)
        product_page.navigate()
        product_page.add_to_cart()
        product_page.go_to_cart()

    with allure.step("Проверка данных товара в корзине, расчет эко-дисконта"):
        cart_page = CartPage(page)
        expect(cart_page.proceed_to_checkout_cart).to_be_visible(timeout=60000)
        cart_page.checkout_check_data_eco(WOODSAW)
        cart_page.price_math_with_discount()
        attach_screenshot(cart_page.page)
        total_1_item = cart_page.cart_total.inner_text()
        total_1_item = parse_price(total_1_item)

    with allure.step("Изменение количества товара + изменение цены"):
        cart_page.change_item_quantity()
        attach_screenshot(cart_page.page)
        total_2_items = cart_page.cart_total.inner_text()
        total_2_items = parse_price(total_2_items)
        assert total_2_items != total_1_item


@testit.externalId("UI-15")
@testit.displayName("Удаление товара из корзины: 2 товара + перерасчет цены")
@allure.title("UI-15: Проверка удаления товара из корзины: 2 товара + перерасчет цены")
@allure.tag('ui', 'cart')
@allure.feature("Корзина")
@allure.severity('medium')
def test_delete_1_item_price_check(page):
    with allure.step("Пользователь добавляет 2 товара в корзину"):
        # 1 item
        product_page = ProductPage(page,THORHUMMER)
        product_page.navigate()
        product_page.add_to_cart()
        time.sleep(2)
        # 2 item
        product_page = ProductPage(page,MEASURINGTAPE)
        product_page.navigate()
        product_page.add_to_cart()
        time.sleep(2)

    with allure.step("Переход в корзину"):
        product_page.go_to_cart()
        cart_page = CartPage(page)
        cart_page.items_count = 2
        expect(cart_page.proceed_to_checkout_cart).to_be_visible(timeout=60000)

    with allure.step("Удаление первого товара из корзины"):
        total_2_items = cart_page.cart_total.inner_text()
        total_2_items = parse_price(total_2_items)
        cart_page.delete_first_item_from_cart()

    with allure.step("Проверка перерасчета стоимости после удаления товара"):
        cart_page.price_math(1)
        attach_screenshot(cart_page.page)
        total_1_item = cart_page.cart_total.inner_text()
        total_1_item = parse_price(total_1_item)
        assert total_2_items != total_1_item


@testit.externalId("UI-16")
@testit.displayName("Удаление всех товаров из корзины")
@allure.title("UI-16: Проверка удаления всех товаров из корзины")
@allure.tag('ui', 'cart')
@allure.feature("Корзина")
@allure.severity('medium')
def test_delete_all_items(page):
    with allure.step("Пользователь добавляет товар в корзину"):
        product_page = ProductPage(page, MEASURINGTAPE)
        product_page.navigate()
        product_page.add_to_cart()
        product_page.go_to_cart()
        attach_screenshot(product_page.page)
        cart_page = CartPage(page)

    with allure.step("Удаление товара из корзины"):
        expect(cart_page.delete_from_cart_btn).to_be_visible(timeout=10000)
        expect(cart_page.alert_message).to_be_hidden(timeout=10000)
        cart_page.delete_from_cart_btn.click(timeout=1000)
        expect(cart_page.alert_message).to_be_visible()
        expect(cart_page.alert_message).to_have_text("Product deleted.")
        attach_screenshot(cart_page.page)
        expect(cart_page.cart_container).to_contain_text("The cart is empty. Nothing to display.")



