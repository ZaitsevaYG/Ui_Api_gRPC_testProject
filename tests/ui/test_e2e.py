import allure
import testit

from tool_shop.data.data import THORHUMMER
from tool_shop.data.utils import attach_screenshot
from tool_shop.pages.web_pages.favorites_page import FavoritesPage
from tool_shop.pages.web_pages.product_page import ProductPage


@testit.externalId("UI-8")
@testit.displayName("Добавление товара в избранное")
@allure.title("UI-8: Проверка функции добавления товара в избранное")
@allure.tag('product', 'ui', 'favorites')
@allure.feature("Действия с товаром")
@allure.severity('medium')
def test_add_to_favorites_e2e(page):
    product_page = ProductPage(page, THORHUMMER)

    with allure.step("Добавление товара в избранное"):
        product_page.add_to_favorites_and_check()


    with allure.step("Переход через меню в избранное"):
        product_page.go_to_favorites_btn.click(timeout=60000)

    fav_page = FavoritesPage(page, THORHUMMER)
    attach_screenshot(fav_page .page, "Избранное")

    with allure.step("Переход на страницу избранного и взаимодействие с товаром"):
        fav_page.check_product_in_favorites_and_delete(THORHUMMER)


