import allure
import testit
from playwright.sync_api import expect

from tool_shop.data.data import SCREWS
from tool_shop.data.utils import attach_screenshot


@testit.externalId("UI-1")
@testit.displayName("Отображение списка товаров на главной странице")
@allure.title("UI-1: Проверка отображения списка товаров на главной странице")
@allure.tag('regress', 'ui', 'smoke')
@allure.feature("Каталог товаров")
@allure.severity('high')
def test_product_visibility_main_page(main_page):
    main_page.product_cards.first.wait_for(state="visible")
    actual_count = main_page.product_cards.count()
    with allure.step(f"Проверяем, что количество карточек = 9 (фактически: {actual_count})"):
        assert actual_count == 9, f"Ожидалось 9 карточек, но найдено {actual_count}"
    attach_screenshot(main_page, "Главная страница после загрузки")


@testit.externalId("UI-2")
@testit.displayName("Поиск товара по названию")
@allure.title("UI-2: Проверка отображения результатов поиска товара по названию")
@allure.tag('search', 'ui')
@allure.feature("Фильтрация и поиск")
@allure.severity('high')
def test_product_search_by_name(main_page):
    with allure.step("Ввести название товара в поле поиска и нажать на кнопку 'Search'"):
        main_page.search_by_the_name(SCREWS)
    with allure.step("Проверка, что товар по названию найден"):
        main_page.check_search_results(SCREWS)
    attach_screenshot(main_page, "Найден товар по названию")


@testit.externalId("UI-3")
@testit.displayName("Поиск товара по фильтру 'Эко-товары'")
@allure.title("UI-3: Проверка отображения результатов поиска товаров по фильтру 'Эко-товары'")
@allure.tag('search', 'ui', 'filter')
@allure.feature("Фильтрация и поиск")
@allure.severity('medium')
def test_product_search_by_filter_eco(main_page):
    with allure.step("Поставить галочку в чек-боксе 'Show only eco-friendly products' "):
        main_page.search_for_eco_tools()
    with allure.step("Проверка, что все найденные товары имеют бейдж ECO"):
        main_page.check_eco_search_results()
        attach_screenshot(main_page, "Найдены товары по по фильтру 'Эко-товары'")


@testit.externalId("UI-4")
@testit.displayName("Поиск товара по фильтру - цена + API проверка")
@allure.title("UI-4: Проверка отображения результатов поиска товаров по цене в диапазоне от 15 до 28$")
@allure.tag('search', 'ui', 'filter')
@allure.feature("Фильтрация и поиск")
@allure.severity('medium')
def test_product_search_price_range(main_page):
    with allure.step("Установить слайдеры минимального и максимального значения цены: 15 и 28 соответственно"):
        main_page.set_price_filter()
    with allure.step("Проверка, что и на ui, и в api пришло одинаковое количество товаров с ценой в указанном диапазоне"):
        main_page.check_price_filter_search_results_with_api_check()
        attach_screenshot(main_page, "Товары, в ценовом диапазоне от 15 до 28$")


@testit.externalId("UI-5")
@testit.displayName("Проверка пагинации каталога")
@allure.title("UI-5: Проверка пагинации каталога")
@allure.tag( 'ui', 'navigation')
@allure.feature("Каталог товаров")
@allure.severity('low')
def test_catalog_pagination(main_page):
    first_page_products = main_page.get_product_ids()
    with allure.step(f"Страница 1: найдено {len(first_page_products)} товаров"):
        assert len(first_page_products) == 9, "На первой странице должно быть 9 товаров"

    with allure.step("<UNK> 2: <UNK> { <UNK>"):
        previous_page_btn

