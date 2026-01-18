import allure
import testit


from tool_shop.data.data import THORHUMMER
from tool_shop.data.utils import attach_screenshot
from tool_shop.pages.web_pages.favorites_page import FavoritesPage
from tool_shop.pages.web_pages.main_page import MainPage
from tool_shop.pages.web_pages.product_page import ProductPage


@testit.externalId("UI-6")
@testit.displayName("Отображение элементов на странице товара")
@allure.title("UI-6: Проверка отображения данных о товаре на странице продукта")
@allure.tag('product', 'ui',)
@allure.feature("Продукт")
@allure.severity('high')
def test_product_description_page_check(page):
    with allure.step("Переход на карточку товара через клик на главной странице"):
        main_page = MainPage(page)
        main_page.navigate()
        main_page.search_and_click_from_main_page(THORHUMMER)

    with allure.step("Переход на карточку товара через клик на главной странице"):
        product_page = ProductPage(page,THORHUMMER)
        product_page.check_product_details(THORHUMMER)
        product_page.check_co2_rating(THORHUMMER)
        attach_screenshot(page, "Страница с данными товара")

@testit.externalId("UI-7")
@testit.displayName("Добавление товара в корзину")
@allure.title("UI-7: Проверка функции добавления товара в корзину")
@allure.tag('product', 'ui', 'card')
@allure.feature("Действия с товаром")
@allure.severity('high')
def test_add_to_cart(product_page):
    with allure.step("Добавление товара в корзину"):
        product_page.add_to_cart_and_check()
        attach_screenshot(product_page.page, "Товар добавлен в корзину")




