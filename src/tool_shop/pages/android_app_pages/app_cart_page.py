import allure
from selene import browser, have, be
from appium.webdriver.common.appiumby import AppiumBy
from tool_shop.data.data import User, Product
from tool_shop.data.helpers import attach_mobile_screenshot


class AppCartPage:
    def __init__(self):
        self.cart_login_text = (AppiumBy.ACCESSIBILITY_ID, 'nav-welcome')


    @allure.step("Увеличить количество товара в корзине")
    def increase_item_quantity(self, item_number):

        product_quantity = browser.all((AppiumBy.ACCESSIBILITY_ID, 'quantity')).element(item_number)
        product_price = browser.all((AppiumBy.ACCESSIBILITY_ID, 'item-total-price')).element(item_number)


        current_quantity = int(product_quantity.locate().text)
        expected_quantity = current_quantity + 1

        current_price_text = product_price.locate().text

        current_price = float(current_price_text.replace('$', '').replace(',', ''))
        expected_price = current_price * 2

        attach_mobile_screenshot(f"До увеличения: кол-во={current_quantity}, цена={current_price_text}")


        browser.element((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().description("Increase Quantity").instance({item_number})'
        )).click()

        product_quantity.with_(timeout=10).should(have.text(str(expected_quantity)))

        expected_price_formatted = f"${expected_price:.2f}"
        product_price.with_(timeout=10).should(have.text(expected_price_formatted))

        attach_mobile_screenshot(f"После увеличения: кол-во={expected_quantity}, цена={expected_price_formatted}")

    @allure.step("Уменьшить количество товара в корзине")
    def decrease_item_quantity(self, item_number):
        product_quantity = browser.all((AppiumBy.ACCESSIBILITY_ID, 'quantity')).element(item_number)
        product_price = browser.all((AppiumBy.ACCESSIBILITY_ID, 'item-total-price')).element(item_number)

        current_quantity = int(product_quantity.locate().text)
        expected_quantity = current_quantity - 1

        current_price_text = product_price.locate().text
        current_price = float(current_price_text.replace('$', '').replace(',', ''))
        expected_price = current_price / 2

        attach_mobile_screenshot(f"До уменьшения: кол-во={current_quantity}, цена={current_price_text}")

        browser.element((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().description("Decrease Quantity").instance({item_number})'
        )).click()

        product_quantity.with_(timeout=10).should(have.text(str(expected_quantity)))

        expected_price_formatted = f"${expected_price:.2f}"
        product_price.with_(timeout=10).should(have.text(expected_price_formatted))

        attach_mobile_screenshot(f"После уменьшения: кол-во={expected_quantity}, цена={expected_price_formatted}")

    @allure.step("Удалить товар из корзины")
    def delete_from_cart(self, item_number: int):
        cart_item = browser.element((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().description("cart-item").instance({item_number})'
        ))

        attach_mobile_screenshot("Перед удалением")

        product_name_element = browser.all((AppiumBy.ACCESSIBILITY_ID, 'product-name')).element(item_number)
        product_name_element.should(be.visible)
        deleted_product_name = product_name_element.locate()


        browser.driver.execute_script('mobile: swipeGesture', {
            'elementId': deleted_product_name.id,
            'direction': 'left',
            'percent': 0.8,
            'speed': 1200
        })

        attach_mobile_screenshot("После свайпа")

        delete_btn = browser.element((AppiumBy.ACCESSIBILITY_ID, "Remove"))
        delete_btn.with_(timeout=3).should(be.visible.and_(be.clickable))
        delete_btn.click()


        cart_item.with_(timeout=5).should(be.absent)

        all_product_names = [
            el.locate().text
            for el in browser.all((AppiumBy.ACCESSIBILITY_ID, 'product-name'))[:3]
            if el.wait_until(be.present)
        ]
        assert deleted_product_name not in all_product_names

        attach_mobile_screenshot("После удаления товара")

    @allure.step("Проверка пустой корзины")
    def empty_cart_check(self):
        browser.element((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Cart")')).with_(timeout=5).should(be.visible)
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'empty-cart')).should(be.visible.and_(have.text("Cart is empty.")))
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'total-price')).should(be.visible.and_(have.text("Total: $0.00")))
        attach_mobile_screenshot()


    @allure.step("Купить товары в корзине -> Proceed to Checkout")
    def proceed_to_cart(self):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'proceed-button')).should(be.visible.and_(be.clickable))
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'proceed-button')).click()

    @allure.step("Проверка текста после нажатия Proceed to Checkout для же авторизованного пользователя")
    def signed_in_user_test_check_and_checkout(self, user: User):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'nav-welcome')).with_(timeout=7).should(be.visible)
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'nav-welcome')).should(have.text(f"Hello {user.first_name}, you are already logged in. You can proceed to checkout."))
        attach_mobile_screenshot()
        browser.element((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Proceed to Checkout")')).click()

    @allure.step("Проверка возможности залогиниться из корзины")
    def cart_sign_in(self, user: User):
        browser.element((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter your email & password")')).with_(timeout=10).should(be.visible)
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'email-input')).type(user.email)
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'password-input')).type(user.password)
        attach_mobile_screenshot()
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'login-button')).click()


    @allure.step("Заполнить адрес")
    def fill_address_info(self, user: User):
        browser.element((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Enter your address")')).with_(timeout=5).should(be.visible)
        browser.element((AppiumBy.ACCESSIBILITY_ID,'address-input')).type(user.street)
        browser.element((AppiumBy.ACCESSIBILITY_ID,'city-input')).type(user.city)
        browser.element((AppiumBy.ACCESSIBILITY_ID,'state-input')).type(user.state)
        browser.element((AppiumBy.ACCESSIBILITY_ID,'country-input')).type(user.country)
        browser.element((AppiumBy.ACCESSIBILITY_ID,'postcode-input')).type(user.postcode)
        attach_mobile_screenshot()
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'proceed-button')).click()

    @allure.step("Заполнить платежную информацию")
    def fill_payment_info(self):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'account-name-input')).with_(timeout=5).should(be.visible)
        browser.element((AppiumBy.ACCESSIBILITY_ID,'validate-button')).with_(timeout=5).should(be.visible)
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'validate-button')).with_(timeout=5).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'confirmation-message')).with_(timeout=5).should(be.visible)
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'confirmation-message')).should(have.text('Payment was successful'))
        attach_mobile_screenshot()


cp = AppCartPage()




