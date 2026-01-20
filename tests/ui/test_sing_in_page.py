import allure
import testit

from tool_shop.data.data import TESTUSER1, WRONGUSER


@testit.externalId("UI-9")
@testit.displayName("Логин")
@allure.title("UI-9: Проверка возможности залогиниться с действительными почтой и паролем")
@allure.tag('ui', 'auth')
@allure.feature("Логин")
@allure.severity('high')
def test_successful_login(singin_page):
    singin_page.singing_in(TESTUSER1)
    singin_page.check_successful_login()


@testit.externalId("UI-10")
@testit.displayName("Логин")
@allure.title("UI-10: Проверка невозможности залогиниться с несуществующими в базе почтой и паролем")
@allure.tag('ui', 'auth')
@allure.feature("Логин")
@allure.severity('high')
def test_successful_login(singin_page):
    singin_page.singing_in(WRONGUSER)
    singin_page.check_unsuccessful_login()
