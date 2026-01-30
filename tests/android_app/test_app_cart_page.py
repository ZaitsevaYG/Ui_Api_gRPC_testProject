import allure

from tool_shop.data.data import TESTUSER1
from tool_shop.pages.android_app_pages.app_cart_page import cp
from tool_shop.pages.android_app_pages.app_main_page import mp


@allure.title("APP-5: Увеличение и уменьшение количества товара в корзине")
@allure.tag('mobile', 'cart')
@allure.feature("Корзина")
@allure.severity('high')
def test_app_decrease_increase_item_quantity(android_mobile_management):
    mp.add_item_to_cart_and_check()
    mp.go_to_cart()
    cp.increase_item_quantity(0)
    cp.decrease_item_quantity(0)


@allure.title("APP-6: Удаление товара из корзины")
@allure.tag('mobile', 'cart')
@allure.feature("Корзина")
@allure.severity('medium')
def test_app_delete_item_from_cart(android_mobile_management):
    mp.add_item_to_cart_and_check()
    mp.go_to_cart()
    cp.delete_from_cart(0)
    cp.empty_cart_check()

@allure.title("APP-7: Покупка товара - happy path")
@allure.tag('mobile', 'cart')
@allure.feature("Корзина")
@allure.severity('high')
def test_app_successful_checkout(android_mobile_management):
    mp.add_item_to_cart_and_check()
    mp.go_to_cart()
    cp.proceed_to_cart()
    cp.cart_sign_in(TESTUSER1)
    cp.signed_in_user_test_check_and_checkout(TESTUSER1)
    cp.fill_address_info(TESTUSER1)
    cp.fill_payment_info()

