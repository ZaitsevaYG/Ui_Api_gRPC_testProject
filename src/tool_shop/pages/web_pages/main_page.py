import requests
from playwright.sync_api import Page, expect
import allure
import json
from tool_shop.data.utils import extract_price_from_text
from tool_shop.data.data import main_link, Product


class MainPage:

    def __init__(self, page: Page):
        self.page = page

        #Навигационное меню
        self.home_btn = page.locator("[data-test=\"nav-home\"]")
        self.categories_btn = page.locator("[data-test=\"nav-categories\"]")
        self.contact_btn = page.locator("[data-test=\"nav-contact\"]")
        self.sing_in_btn = page.locator("[data-test=\"nav-sign-in\"]")

        #Фильтры
        self.sort_dropdown_price_desc = page.locator("[data-test=\"sort\"]")
        self.search_field = page.locator("[data-test=\"search-query\"]")
        self.search_btn = page.locator("[data-test=\"search-submit\"]")
        self.filters_power_tools = page.locator("#filters").get_by_text("Power Tools")
        self.filters_brand = page.get_by_text("ForgeFlex Tools")
        self.filters_sustainability = page.get_by_text("Show only eco-friendly")
        self.min_price_slider = page.locator(".ngx-slider-pointer-min")
        self.max_price_slider = page.locator(".ngx-slider-pointer-max")

        #Пагинация
        self.previous_page_btn = page.get_by_role("button", name="Previous")
        self.previous_page_li = page.locator("li.page-item:has(a[aria-label='Previous'])")
        self.next_page_btn = page.get_by_role("button", name="Next")
        self.page_1_btn = page.locator("a[aria-label='Page-1']").locator("..")
        self.page_2_btn = page.locator("a[aria-label='Page-2']").locator("..")

        #Элемент
        self.product_cards  = page.locator("a.card[data-test^='product-']")
        self.search_caption = page.locator("[data-test='search-caption']")
        self.search_completed = page.locator("[data-test='search_completed']")
        self.product_card_name = page.locator("[data-test='product-name']")
        self.product_card_price = page.locator("[data-test='product-price']")
        self.eco_badge = page.locator("[data-test='eco-badge']")
        self.rating_badge = page.locator("[data-test='co2-rating-badge']")



    def navigate(self):
        with allure.step(f"Загрузка основной страницы сайта"):
            self.page.goto(main_link, wait_until='networkidle', timeout=60000)
            expect(self.product_cards.first).to_be_visible(timeout=10000)


    def search_by_the_name(self, product: Product):
        self.search_field.click()
        self.search_field.type(product.name)
        self.search_btn.click()

    def search_and_click_from_main_page(self, product: Product):
        self.search_field.click()
        self.search_field.fill(product.name)
        self.search_btn.click(timeout=10000)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        expect(self.search_caption).to_be_visible(timeout=10000)
        self.page.wait_for_timeout(2000)
        self.product_card_name.scroll_into_view_if_needed(timeout=10000)

        expect(self.product_card_name).to_be_visible(timeout=10000)

        expect(self.product_card_name).to_have_text(product.name)
        self.product_card_name.click(timeout=10000)

    def check_search_results(self, product: Product):
        expect(self.search_caption).to_be_visible(timeout=10000)
        expect(self.search_completed).to_be_visible(timeout=10000)
        expect(self.search_caption).to_have_text(f"Searched for: {product.name}")
        expect(self.product_card_name.first).to_be_visible(timeout=10000)
        for i in range(self.product_card_name.count()):
            name_text = self.product_card_name.nth(i).text_content().strip()

            assert product.name.lower() in name_text.lower(), \
                f"Название '{name_text}' не содержит '{product.name}'"

    def search_for_eco_tools(self):
        self.filters_sustainability.click(timeout=10000)
        self.product_cards.first.scroll_into_view_if_needed(timeout=10000)


    def check_eco_search_results(self):
        self.page.wait_for_function("""
            () => {
                const cards = Array.from(document.querySelectorAll("a[data-test^='product-']"));
                const visible = cards.filter(el => {
                    const style = window.getComputedStyle(el);
                    return style.display !== 'none' && style.visibility !== 'hidden';
                });
                return visible.every(el => el.querySelector("[data-test='eco-badge']"));
            }
        """, timeout=10000)

    def set_price_filter(self):
        # Минимум
        self.min_price_slider.focus()
        current = int(self.min_price_slider.get_attribute("aria-valuenow"))
        while current < 15:
            self.page.keyboard.press("ArrowRight")
            current += 1
            self.page.wait_for_timeout(50)

        # Максимум
        self.max_price_slider.focus()
        current = int(self.max_price_slider.get_attribute("aria-valuenow"))
        while current > 28:
            self.page.keyboard.press("ArrowLeft")
            current -= 1
            self.page.wait_for_timeout(50)

    def check_price_filter_search_results_with_api_check(self):
        self.page.wait_for_load_state("networkidle")

        max_retries = 3
        ui_prices = []

        for attempt in range(max_retries):
            try:
                # Ждём появления карточек
                cards_locator = self.page.locator("[data-test^='product-']")
                expect(cards_locator.first).to_be_visible(timeout=5000)

                # Получаем количество карточек
                count = cards_locator.count()

                if count == 0:
                    raise Exception("Нет товаров после фильтрации")

                # Собираем цены атомарно
                price_locator = self.page.locator("[data-test='product-price']")
                price_texts = price_locator.all_text_contents()

                ui_prices = [
                    round(extract_price_from_text(text), 2)
                    for text in price_texts
                    if text.strip()
                ]

                break

            except Exception as e:
                if attempt < max_retries - 1:
                    self.page.wait_for_timeout(1000)
                    continue
                raise e

        with allure.step(f"UI: {len(ui_prices)} товаров в диапазоне 15–28"):
            allure.attach(str(ui_prices), "UI Prices", allure.attachment_type.TEXT)

        # API запрос
        response = requests.get(
            "http://localhost:8091/products",
            params={"between": "price,15,28"}
        )
        response.raise_for_status()

        api_data = response.json()
        if isinstance(api_data, dict) and "data" in api_data:
            api_prices = [round(float(p["price"]), 2) for p in api_data["data"]]
        else:
            api_prices = [round(float(p["price"]), 2) for p in api_data]

        with allure.step(f"API: {len(api_prices)} товаров"):
            allure.attach(str(api_prices), "API Prices", allure.attachment_type.TEXT)

        # Сравнение
        assert sorted(ui_prices) == sorted(api_prices), \
            f"Mismatch!\nUI: {sorted(ui_prices)}\nAPI: {sorted(api_prices)}"


    def get_grid_product_ids(self):
        return self.page.evaluate("""
            () => {
                const cards = Array.from(document.querySelectorAll('a.card[data-test^="product-"]'));
                const viewport = {
                    top: 0, bottom: window.innerHeight * 0.8,
                    left: 0, right: window.innerWidth
                };

                // Только карточки в основной зоне просмотра
                const gridCards = cards.filter(card => {
                    const rect = card.getBoundingClientRect();
                    return rect.top < viewport.bottom * 0.7 &&  // Верхняя 70% viewport
                           rect.width > 100 && rect.height > 100 &&  // Размер grid карточки
                           card.querySelector('[data-test="product-price"]');  // Имеет цену
                });

                return gridCards.slice(0, 9).map(c => c.getAttribute('data-test'));
            }
        """)



    def wait_for_products(self, count=9, timeout=10000):
        expect(self.product_cards).to_have_count(count, timeout=timeout)

    def get_product_ids(self):
        self.wait_for_products()
        count = self.product_cards.count()

        return [
            self.product_cards.nth(i).get_attribute("data-test")
            for i in range(count)
        ]

