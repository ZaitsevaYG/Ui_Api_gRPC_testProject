import re

import allure
from playwright.sync_api import Page, expect
from src.tool_shop.data.data import Product, User
from config import Config
from tool_shop.data.helpers import attach_screenshot, parse_price, parse_discount


class CartPage:
    def __init__(self, page: Page):
        self.page = page

        self.cart_container = page.locator("app-cart")
        self.product_name = page.locator("[data-test='product-title']")
        self.product_price = page.locator("[data-test='product-price']")
        self.product_quantity = page.get_by_role("spinbutton",  name=re.compile(r"^Quantity for"))
        self.subtotal = page.locator("[data-test='cart-subtotal']")
        self.eco_friendly_discount = page.locator("[data-test='cart-eco-discount']")
        self.delete_from_cart_btn = page.locator(".btn.btn-danger")
        self.proceed_to_checkout_cart = page.locator("[data-test='proceed-1']")
        self.alert_message = page.get_by_role("alert")
        self.proceed_to_checkout_guest = page.locator("[data-test='proceed-2-guest']")


        self.logged_text = page.locator("app-login")
        self.as_guest = page.get_by_role("tab", name="Continue as Guest")
        self.guest_email = page.locator("[data-test='guest-email']")
        self.guest_first_name = page.locator("[data-test='guest-first-name']")
        self.guest_last_name = page.locator("[data-test='guest-last-name']")
        self.guest_submit = page.locator("[data-test='guest-submit']")
        self.proceed_to_checkout_singin = page.locator("[data-test='proceed-2']")
        self.user_email = page.locator("[data-test='email']")
        self.user_password = page.locator("[data-test='password']")
        self.user_login_submit = page.locator("[data-test='login-submit']")

        self.billing_street = page.locator("[data-test='street']")
        self.billing_city = page.locator("[data-test='city']")
        self.billing_state = page.locator("[data-test='state']")
        self.billing_country = page.locator("[data-test='country']")
        self.billing_postcode = page.locator("[data-test='postal_code']")
        self.proceed_to_checkout_billing = page.locator("[data-test='proceed-3']")

        self.payment_method = page.locator("[data-test='payment-method']")
        self.credit_card_number = page.locator("[data-test='credit_card_number']")
        self.expiration_date = page.locator("[data-test='expiration_date']")
        self.cvv = page.locator("[data-test='cvv']")
        self.card_holder_name = page.locator("[data-test='card_holder_name']")
        self.confirm_btn = page.locator("[data-test='finish']")

        self.payment_message = page.locator("[data-test='payment-success-message']")

        #for math
        self.rows = page.locator('tbody tr:has([data-test="product-title"])')
        self.cart_total = page.locator('[data-test="cart-total"]')
        self.cart_subtotal = page.locator('[data-test="cart-subtotal"]')
        self.eco_discount = page.locator("[data-test='cart-eco-discount']")

    def navigate(self):
        with allure.step(f"Загрузка страницы логина"):
            self.page.goto( f"{Config.UI_BASE_URL}/checkout", timeout=60000)
            expect(self.proceed_to_checkout_cart).to_be_visible(timeout=60000)

    def checkout_check_data_eco(self, product: Product):
        with allure.step(f"Проверить количество, цену и общую сумму"):
            expect(self.product_name).to_be_visible()
            expect(self.product_name).to_have_text(product.name)
            expect(self.product_quantity).to_be_visible()
            expect(self.product_price).to_have_text(f"${product.price}")
            expect(self.subtotal).to_have_text(f"${product.price}")
            expect(self.eco_friendly_discount).to_be_visible()
            expect(self.delete_from_cart_btn).to_be_enabled()
            expect(self.proceed_to_checkout_cart).to_be_enabled()

    def proceed_to_checkout_first_window(self):
        with allure.step(f"Переход к покупке товара- нажать на кнопку 'Proceed to checkout'"):
            expect(self.proceed_to_checkout_cart).to_be_enabled()
            self.proceed_to_checkout_cart.click()

    def singin_window_logged_user(self, user: User):
        with allure.step(f"Переход кo второй странице корзины - Sing In -> User already logged in -> 'Proceed to checkout'"):
            expect(self.logged_text).to_be_visible(timeout=6000)
            expect(self.logged_text).to_have_text(f"Hello {user.full_name}, you are already logged in. You can proceed to checkout.")
            attach_screenshot(self.page)
            expect(self.proceed_to_checkout_singin).to_be_enabled()
            self.proceed_to_checkout_singin.click(timeout=6000)

    def sining_in_via_cart(self, user: User):
        with allure.step(f"Переход кo второй странице корзины - Sing In -> Login -> 'Proceed to checkout'"):
            expect(self.user_email).to_be_visible(timeout=6000)
            self.user_email.fill(user.email)
            self.user_password.fill(user.password)
            attach_screenshot(self.page)
            self.user_login_submit.click(timeout=10000)
            expect(self.logged_text).to_have_text(
                f"Hello {user.full_name}, you are already logged in. You can proceed to checkout. Proceed to checkout")
            attach_screenshot(self.page)
            expect(self.proceed_to_checkout_singin).to_be_enabled()
            self.proceed_to_checkout_singin.click(timeout=6000)


    def billing_window(self, user: User):
        with allure.step(f"Переход к третьей странице корзины - Billing Address -> 'Proceed to checkout'"):
            expect(self.billing_street).to_be_visible(timeout=6000)
            self.billing_street.fill(user.street)
            self.billing_city.fill(user.city)
            self.billing_state.fill(user.state)
            self.billing_country.fill(user.country)
            self.billing_postcode.fill(user.postcode)
            attach_screenshot(self.page)
            self.proceed_to_checkout_billing.click(timeout=6000)

    def payment_window_cash(self):
        with allure.step(f"Переход к четвертой странице корзины - Payment -> Cash on Delivery -> 'Confirm'"):
            expect(self.payment_method).to_be_visible(timeout=6000)
            self.payment_method.select_option(value='Cash on Delivery')
            attach_screenshot(self.page)
            self.confirm_btn.click(timeout=6000)
            expect(self.payment_message).to_be_visible(timeout=6000)
            attach_screenshot(self.page)

    def payment_window_card(self, user: User):
        with allure.step(f"Переход к четвертой странице корзины - Payment -> Credit Card -> 'Confirm'"):
            expect(self.payment_method).to_be_visible(timeout=6000)
            self.payment_method.select_option(value='Credit Card')
            attach_screenshot(self.page)
            self.credit_card_number.fill("1234-1234-1234-1234")
            self.expiration_date.fill("12/2030")
            self.cvv.fill("546")
            self.card_holder_name.fill(f"{user.full_name}")
            attach_screenshot(self.page)
            self.confirm_btn.click(timeout=6000)
            expect(self.payment_message).to_be_visible(timeout=6000)
            attach_screenshot(self.page)

    def singin_window_guest_user(self, user: User):
        with allure.step(f"Переход кo второй странице корзины - Sing In -> Continue as Guest ->'Proceed to checkout'"):
            expect(self.as_guest).to_be_visible(timeout=6000)
            self.as_guest.click(timeout=6000)
            expect(self.guest_email).to_be_visible(timeout=6000)
            attach_screenshot(self.page)
            self.guest_email.fill(user.email)
            self.guest_first_name.fill(user.first_name)
            self.guest_last_name.fill(user.last_name)
            self.guest_submit.click(timeout=6000)
            expect(self.logged_text).to_be_visible(timeout=6000)
            expect(self.logged_text).to_have_text(f"Continuing as guest: {user.first_name} {user.last_name} ({user.email}) Proceed to checkout ")
            attach_screenshot(self.page)
            self.proceed_to_checkout_guest.click(timeout=6000)

    def price_math(self, expected_items: int):
        self.page.wait_for_timeout(10000)
        expect(self.rows).to_have_count(expected_items)
        calculated_total = 0.0

        for i in range(self.rows.count()):
            row = self.rows.nth(i)

            quantity = int(row.locator('[data-test="product-quantity"]').input_value())
            unit_price_text = row.locator('[data-test="product-price"]').inner_text()
            line_total_text = row.locator('[data-test="line-price"]').inner_text()

            unit_price = parse_price(unit_price_text)
            line_total_ui = parse_price(line_total_text)


            expected_line_total = round(unit_price * quantity, 2)
            assert line_total_ui == expected_line_total, (
                f"Строка {i}: цена ${unit_price} * qty {quantity} "
                f"= {expected_line_total}, но UI показывает {line_total_ui}"
            )

            calculated_total += expected_line_total

        cart_total = self.cart_total.inner_text()
        cart_total_ui = parse_price(cart_total)

        assert round(calculated_total, 2) == cart_total_ui, (
            f"Сумма строк {calculated_total}, но общий тотал {cart_total_ui}"
        )

    def price_math_with_discount(self):
        row = self.rows.nth(0)
        quantity = int(row.locator('[data-test="product-quantity"]').input_value())
        unit_price_text = row.locator('[data-test="product-price"]').inner_text()
        line_total_text = row.locator('[data-test="line-price"]').inner_text()
        unit_price = parse_price(unit_price_text)
        line_total_ui = parse_price(line_total_text)
        subtotal_ui = parse_price(self.subtotal.inner_text())
        assert unit_price * quantity == line_total_ui
        assert line_total_ui == subtotal_ui

        expect(self.eco_discount).to_be_visible(timeout=6000)
        discount_ui = parse_discount(self.eco_discount.inner_text())
        exp_discount = round(subtotal_ui * 0.05, 2)
        expected_discount = parse_discount(str(exp_discount))
        assert discount_ui == expected_discount, f"Discount: ожид -{expected_discount}, UI {discount_ui}"

        expected_total = round(subtotal_ui - discount_ui, 2)
        total_ui = parse_price(self.cart_total.inner_text())
        assert total_ui == expected_total, f"Total: ожид {expected_total}, UI {total_ui}"


    def delete_first_item_from_cart(self):
        first_row = self.rows.nth(0)
        expect(self.alert_message).to_be_hidden(timeout=10000)
        first_row.locator(".btn.btn-danger").click(timeout=1000)
        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_have_text("Product deleted.")
        attach_screenshot(self.page)
        expect(self.rows).to_have_count(1)
        expect(self.cart_total).to_be_visible(timeout=10000)
        expect(self.rows).to_have_count(1, timeout=10000)

    def change_item_quantity(self):
        expect(self.alert_message).to_be_hidden(timeout=10000)
        self.product_quantity.fill("2")
        self.product_quantity.press("Enter")
        self.product_quantity.press("Enter")
        expect(self.alert_message).to_be_visible()
        expect(self.alert_message).to_have_text("Product quantity updated.")
        attach_screenshot(self.page)

















