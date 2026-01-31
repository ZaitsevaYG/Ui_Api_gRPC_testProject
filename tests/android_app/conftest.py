import allure
import allure_commons
import pytest
from appium.options.android import UiAutomator2Options
from selene import browser, support
import os
from appium import webdriver
from tool_shop.data.helpers import attach_bstack_video


# Для прогона на реальном девайсе, подключенным к компу
#
# @pytest.fixture(scope='function', autouse=True)
# def android_mobile_management():
#     options = UiAutomator2Options().load_capabilities({
#         "platformName": "Android",
#         "deviceName": "JMS_L09",
#         "appActivity": "io.testsmith.practicesoftwaretesting.MainActivity",
#         "appPackage": "io.testsmith.practicesoftwaretesting",
#         "app": "C:/Users/PC/Downloads/practice-software-testing.apk"
#     })
#
#     browser.config.driver = webdriver.Remote(
#         command_executor='http://127.0.0.1:4723',
#         options=options
#     )
#
#     browser.config.timeout = float(os.getenv('timeout', '10.0'))
#     browser.config._wait_decorator = support._logging.wait_with(
#         context=allure_commons._allure.StepContext
#     )
#     try:
#         yield
#     finally:
#
#         if browser.driver:
#             try:
#                 browser.quit()
#             except:
#                 pass
#             browser.config.driver = None


@pytest.fixture(scope='function', autouse=True)
def android_mobile_management():
    browser.config.driver = None
    options = UiAutomator2Options().load_capabilities({
        "platformName": "Android",
        "platformVersion": "14.0",
        "deviceName": "Google Pixel 8 Pro",
        "app": "bs://7f72b4ebe2cb7bf50806cda4b014685802184572",
        "appWaitActivity": "*",

        "noReset": False,
        "fullReset": False,
        "autoGrantPermissions": True,  #

        'bstack:options': {
            "projectName": "ToolShop test automation",
            "buildName": "browserstack-build-1",
            "sessionName": "BStack auto",

            "userName": "janazaitseva_ckHfp4",
            "accessKey": "ULcqpKU4NxAupDncjgJV",
        }
    })

    driver = webdriver.Remote("http://hub.browserstack.com/wd/hub", options=options)
    browser.config.driver = driver

    browser.config.timeout = float(os.getenv('timeout', '15.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    session_id = browser.driver.session_id

    yield


    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )

    with allure.step('tear down app session'):
        driver.terminate_app("io.testsmith.practicesoftwaretesting")
        driver.quit()
        browser.config.driver = None

    attach_bstack_video(session_id)