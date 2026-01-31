import allure
from selene import browser, have, be
from appium.webdriver.common.appiumby import AppiumBy
from tool_shop.data.data import User, Product
from tool_shop.data.helpers import  attach_mobile_screenshot


class AppMainPage:
    def __init__(self):
        self.search_field = (AppiumBy.ACCESSIBILITY_ID,"search-input")
        self.add_to_cart_btn = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Add to Cart").instance(0)')
        self.cart_quantity = (AppiumBy.ACCESSIBILITY_ID, "cart-quantity")
        self.cart_btn = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("cart-button")')
        self.menu_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("drawer-button")')
        self.sing_in_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign In")')
        self.email_field = (AppiumBy.ACCESSIBILITY_ID, 'email-input')
        self.password_field = (AppiumBy.ACCESSIBILITY_ID, 'password-input')
        self.login_btn = (AppiumBy.ACCESSIBILITY_ID, 'login-button')
        self.error_message = (AppiumBy.ACCESSIBILITY_ID, 'error')
        self.email_error = (AppiumBy.ACCESSIBILITY_ID, 'email-error')
        self.password_error = (AppiumBy.ACCESSIBILITY_ID, 'password-error')
        self.user_name = (AppiumBy.ACCESSIBILITY_ID, 'nav-welcome')
        self.contact = (AppiumBy.ACCESSIBILITY_ID, 'nav-contact')



    @allure.step("Поиск товара по названию")
    def search_for_the_item(self):
        browser.all((AppiumBy.ACCESSIBILITY_ID, "product-item")).with_(timeout=15)
        browser.element(self.search_field).click()
        browser.element(self.search_field).type('Thor Hammer')
        browser.element(self.search_field).click()
        browser.driver.execute_script('mobile: performEditorAction', {'action': 'search'})
        browser.driver.hide_keyboard()

        browser.element((AppiumBy.ACCESSIBILITY_ID,"product-title")).with_(timeout=30).should(have.text('Thor Hammer'))

    @allure.step("Добавление товара в корзину")
    def add_item_to_cart_and_check(self):
        current_value = 0

        cart = browser.element(self.cart_quantity).with_(timeout=3)
        if cart.wait_until(be.present):

            current_text = cart.locate().text.strip()
            if current_text.isdigit():
                current_value = int(current_text)

            else:
                current_value = 0

        attach_mobile_screenshot(f"До добавления")

        browser.element(self.add_to_cart_btn) \
            .with_(timeout=8) \
            .should(be.clickable) \
            .click()
        expected_value = current_value + 1
        browser.element(self.cart_quantity) \
            .with_(timeout=12) \
            .should(be.visible.and_(have.text(str(expected_value))))

        attach_mobile_screenshot(f"После добавления: корзина = {expected_value}")


    @allure.step("Переход в корзину")
    def go_to_cart(self):
        browser.element(self.cart_btn).with_(timeout=10).click()
        browser.element((AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Cart")')).with_(timeout=10).should(be.visible)
        attach_mobile_screenshot()


    @allure.step("Переход в меню")
    def menu_btn_click(self):
        browser.element(self.menu_btn).with_(timeout=10).click()
        browser.element((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Register")')).with_(timeout=10).should(be.visible)
        attach_mobile_screenshot()


    @allure.step("Логин в систему")
    def sing_in(self, user: User):
        browser.element(self.sing_in_btn).with_(timeout=10).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'header-title')).with_(timeout=10).should(be.visible.and_(have.text("Sign In")))
        attach_mobile_screenshot()
        browser.element(self.email_field).type(user.email)
        browser.element(self.password_field).type(user.password)

        browser.element(self.login_btn).with_(timeout=10).click()


    @allure.step("Переход на вкладку аренды")
    def rentals(self):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'rentals-tab, Rentals')).with_(timeout=10).should(be.visible)
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'rentals-tab, Rentals')).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'product-price')).with_(timeout=10).should(be.visible.and_(have.text("$136.50 per hour")))
        attach_mobile_screenshot()

    @allure.step("Переход на контакт + заполнение формы")
    def contact_form(self, user: User):
        browser.element(self.contact).with_(timeout=10).click()
        browser.element((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Contact Us")')).with_(timeout=10).should(be.visible)

        browser.element((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("First Name")')).type(user.first_name)
        browser.element((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Last Name")')).type(user.last_name)
        browser.element((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Email")')).type(user.email)
        browser.element((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Message")')).type('I want promo code')
        attach_mobile_screenshot()
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Send Message')).click()

        browser.element((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" Thanks for your message! We will contact you shortly.")')).with_(timeout=10).should(be.visible)
        attach_mobile_screenshot()

mp = AppMainPage()




