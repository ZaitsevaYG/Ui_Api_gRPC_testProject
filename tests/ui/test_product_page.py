import allure
from playwright.sync_api import expect
from tool_shop.data.data import THORHUMMER, LONGNOSEPILERS
from tool_shop.data.helpers import attach_screenshot
from tool_shop.pages.web_pages.main_page import MainPage
from tool_shop.pages.web_pages.product_page import ProductPage


@allure.title("UI-6: Проверка отображения данных о товаре на странице продукта")
@allure.tag('product', 'ui',)
@allure.feature("Продукт: Действия с товаром")
@allure.severity('high')
def test_product_description_page_check(page):
    with allure.step("Переход на карточку товара через клик на главной странице"):
        main_page = MainPage(page)
        main_page.navigate()
        main_page.search_and_click_from_main_page(THORHUMMER)

    with allure.step("Проверка отображаемой информации и активности кнопок на странице товара"):
        product_page = ProductPage(page,THORHUMMER)
        product_page.check_product_details()
        product_page.check_co2_rating()
        attach_screenshot(page, "Страница с данными товара")


@allure.title("UI-7: Проверка функции добавления товара в корзину")
@allure.tag('product', 'ui', 'card')
@allure.feature("Продукт: Действия с товаром")
@allure.severity('critical')
def test_add_to_cart(product_page):
    with allure.step("Добавление товара в корзину"):
        product_page.add_to_cart_and_check()
        attach_screenshot(product_page.page, "Товар добавлен в корзину")



@allure.title("UI-17: Проверка функции невозможности добавления товара 'Out of stock' в корзину")
@allure.tag('product', 'ui')
@allure.feature("Продукт: Действия с товаром")
@allure.severity('medium')
def test_out_of_stock_item (page):
    with allure.step("Переход на страницу товара, которого нет в наличии"):
        product_page = ProductPage(page, LONGNOSEPILERS)
        product_page.navigate()

    with allure.step("Проверка невозможности добавить товар в корзину"):
        expect(product_page.out_of_stock).to_be_visible()
        expect(product_page.out_of_stock).to_contain_text("Out of stock")
        expect(product_page.add_to_card_btn).to_be_disabled()
        attach_screenshot(product_page.page)


@allure.title("UI-17: Проверка функции невозможности добавления товара в избранное неавторизованным пользователем")
@allure.tag('product', 'ui')
@allure.feature("Продукт: Действия с товаром")
@allure.severity('medium')
def test_add_to_fav_unauthorised(product_page):
    with allure.step("Добавление товара в избранное. Пользователь не авторизован"):
        expect(product_page.add_to_favorites_btn).to_be_visible()
        expect(product_page.add_to_favorites_btn).to_be_enabled()
        product_page.add_to_favorites_btn.click(timeout=1000)
        expect(product_page.alert_message).to_be_visible()
        attach_screenshot(product_page.page, "Товар не добавлен в избранное")
        expect(product_page.alert_message).to_have_text("Unauthorized, can not add product to your favorite list.")


