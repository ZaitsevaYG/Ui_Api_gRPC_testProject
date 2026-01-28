import allure
from playwright.sync_api import expect

from tool_shop.data.data import SCREWS
from tool_shop.data.helpers import attach_screenshot


@allure.title("UI-1: Проверка отображения списка товаров на главной странице")
@allure.tag('regress', 'ui', 'smoke')
@allure.feature("Каталог товаров")
@allure.severity('high')
def test_product_visibility_main_page(main_page):
    main_page.product_cards.first.wait_for(state="visible")
    with allure.step("Проверка, что на главной странице отображается 9 карточек товара"):
        for i in range(9):
            expect(main_page.product_cards.nth(i)).to_be_visible()
    attach_screenshot(main_page.page, "Главная страница после загрузки")


@allure.title("UI-2: Проверка отображения результатов поиска товара по названию")
@allure.tag('search', 'ui')
@allure.feature("Фильтрация и поиск")
@allure.severity('high')
def test_product_search_by_name(main_page):
    with allure.step("Ввести название товара в поле поиска и нажать на кнопку 'Search'"):
        main_page.search_by_the_name(SCREWS)
    with allure.step("Проверка, что товар по названию найден"):
        main_page.check_search_results(SCREWS)
    attach_screenshot(main_page.page, "Найден товар по названию")


@allure.title("UI-3: Проверка отображения результатов поиска товаров по фильтру 'Эко-товары'")
@allure.tag('search', 'ui', 'filter')
@allure.feature("Фильтрация и поиск")
@allure.severity('medium')
def test_product_search_by_filter_eco(main_page):
    with allure.step("Поставить галочку в чек-боксе 'Show only eco-friendly products' "):
        main_page.search_for_eco_tools()
    with allure.step("Проверка, что все найденные товары имеют бейдж ECO"):
        main_page.check_eco_search_results()
        attach_screenshot(main_page.page, "Найдены товары по по фильтру 'Эко-товары'")


@allure.title("UI-4: Проверка отображения результатов поиска товаров по цене в диапазоне от 15 до 28$")
@allure.tag('search', 'ui', 'filter')
@allure.feature("Фильтрация и поиск")
@allure.severity('medium')
def test_product_search_price_range(main_page):
    with allure.step("Установить слайдеры минимального и максимального значения цены: 15 и 28 соответственно"):
        main_page.set_price_filter()
    with allure.step("Проверка, что и на ui, и в api пришло одинаковое количество товаров с ценой в указанном диапазоне"):
        main_page.check_price_filter_search_results_with_api_check()
        attach_screenshot(main_page.page, "Товары, в ценовом диапазоне от 15 до 28$")


@allure.title("UI-5: Проверка пагинации каталога")
@allure.tag( 'ui', 'navigation')
@allure.feature("Каталог товаров")
@allure.severity('low')
def test_catalog_pagination(main_page):

    with allure.step("🔍 Анализ grid 3x3"):
        attach_screenshot(main_page.page, "Каталог 3x3 grid")

        page1_ids = main_page.get_grid_product_ids()

        allure.attach(
            f"Page 1: {len(page1_ids)} видимых товаров\n{page1_ids}",
            "Page 1 анализ",
            attachment_type=allure.attachment_type.TEXT
        )

    main_page.next_page_btn.click()
    expect(main_page.page_2_btn).to_have_class("page-item active")

    page2_ids = main_page.get_grid_product_ids()

    # Проверка смены контента
    changed = len(set(page1_ids) ^ set(page2_ids)) / 9 * 100
    assert changed > 50, f"Смена контента: {changed:.1f}% (мало изменений)"


