import json
import os

import allure
import testit
from allure_commons.types import AttachmentType

from tests.api.conftest import update_env_var
from tool_shop.utils.api_client import APIClient, AuthAPIClient
from tool_shop.utils.validators import ResponseValidator, UserValidator

@testit.externalId("API-6")
@testit.displayName("Создание нового пользователя")
@allure.title("API-6: Создание нового пользователя")
@allure.tag('api', 'user')
@allure.feature("Регистрация нового пользователя")
@allure.severity('high')
def test_post_create_new_user(api_client: APIClient, valid_user_registration_data):
    response = api_client.post("/users/register", json=valid_user_registration_data)

    allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                  attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")

    assert response.status_code == 201
    data = response.json()

    UserValidator.validate_user_response(data)

    assert data["email"] == valid_user_registration_data["email"]
    assert data["first_name"] == valid_user_registration_data["first_name"]
    assert data["last_name"] == valid_user_registration_data["last_name"]
    assert data["id"]
    assert "created_at" in data

    user_id = data["id"]
    update_env_var({"USER_ID": user_id})

    allure.attach(
        f"User_id: {user_id}",
        name="User id",
        attachment_type=allure.attachment_type.TEXT
    )


@testit.externalId("API-7")
@testit.displayName("Попытка регистрации с пустым полем email")
@allure.title("API-7: Попытка регистрации с пустым полем email")
@allure.tag('api', 'user')
@allure.feature("Регистрация нового пользователя")
@allure.severity('medium')
def test_post_register_invalid_email(api_client, empty_email_data):

    response = api_client.post("/users/register", json=empty_email_data)

    allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                  attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")

    assert response.status_code in [400, 422]
    error_data = response.json()
    assert "email" in str(error_data).lower()


@testit.externalId("API-8")
@testit.displayName("Попытка регистрации с коротким паролем")
@allure.title("API-8: Попытка регистрации с коротким паролем")
@allure.tag('api', 'user')
@allure.feature("Регистрация нового пользователя")
@allure.severity('high')
def test_post_register_short_password(api_client, invalid_password_data):

    response = api_client.post("/users/register", json=invalid_password_data)

    allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                  attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")

    assert response.status_code in [400, 422]
    error_data = response.json()

    assert all(keyword in str(error_data).lower()
               for keyword in ["password", "at least", "uppercase", "lowercase", "symbol", "number"])


@testit.externalId("API-9")
@testit.displayName("Логин с валидными данными. Получение токена")
@allure.title("API-9: Логин с валидными данными. Получение токена")
@allure.tag('api', 'user')
@allure.feature("Авторизация")
@allure.severity('high')
def test_post_successful_login(api_client: AuthAPIClient):
    response = api_client.post("/users/login", json={"email": "customer@practicesoftwaretesting.com", "password": "welcome01"})

    allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                  attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")

    assert response.status_code == 200
    data = response.json()

    token = data["access_token"]
    update_env_var({"AUTH_TOKEN": token})

    allure.attach(
        f"Token: {token}",
        name="Access Token",
        attachment_type=allure.attachment_type.TEXT
    )

    UserValidator.validate_token_response(data)


@testit.externalId("API-10")
@testit.displayName("Частичное изменение данных пользователя - изменить адрес")
@allure.title("API-10: Частичное изменение данных пользователя - изменить адрес")
@allure.tag('api', 'user')
@allure.feature("Пользователь")
@allure.severity('medium')
def test_patch_change_user_data(authenticated_user):
    user = authenticated_user["user"]
    auth_client = authenticated_user["client"]

    patch_data = {
        "address": {
            "street": "Santa Monica, 13",
            "city": "Los Angeles",
            "state": "California",
            "country": "USA",
            "postal_code": "15748"
        }
    }

    with allure.step("Поменять адресные данные авторизованного пользователя"):
        response = auth_client.patch(f"/users/{user['id']}", json=patch_data)
        assert response.status_code == 200

        allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                      attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")

        result = response.json()
        UserValidator.validate_patch_success_response(result)

    with allure.step("Проверка, что данные поменялись"):
        get_response = auth_client.get(f"/users/{user['id']}")
        assert get_response.status_code == 200

        allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                      attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")

        updated_user = get_response.json()
        UserValidator.validate_user_response(updated_user)

        assert updated_user["id"] == user['id']
        assert updated_user["address"]["street"] == "Santa Monica, 13"
        assert updated_user["address"]["city"] == "Los Angeles"
        assert updated_user["address"]["state"] == "California"
        assert updated_user["address"]["country"] == "USA"
        assert updated_user["address"]["postal_code"] == "15748"
        assert updated_user["first_name"] == user["first_name"]
        assert updated_user["last_name"] == user["last_name"]


@testit.externalId("API-11")
@testit.displayName("Попытка поменять данные с несуществующим id")
@allure.title("API-11: Попытка поменять данные с несуществующим id")
@allure.tag('api', 'user')
@allure.feature("Пользователь")
@allure.severity('medium')
def test_patch_change_unexisted_id(authenticated_user):

    auth_client = authenticated_user["client"]
    fake_id = "5fnke4"

    patch_data = {
        "first_name": "NewName"
    }

    with allure.step("Попытка поменять адресные данные авторизованного пользователя с несуществующим id"):
        response = auth_client.patch(f"/users/{fake_id}", json=patch_data)

        allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                      attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")

        assert response.status_code == 403

@testit.externalId("API-12")
@testit.displayName("Попытка поменять данные неавторизованным пользователем")
@allure.title("API-12: Попытка поменять данные неавторизованным пользователем")
@allure.tag('api', 'user')
@allure.feature("Пользователь")
@allure.severity('medium')
def test_patch_user_no_auth(api_client, registered_user):

    user_id = registered_user["id"]
    patch_data = {"first_name": "Unauthorized"}

    response = api_client.patch(f"/users/{user_id}", json=patch_data)

    allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                  attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")

    assert response.status_code == 401


@testit.externalId("API-13")
@testit.displayName("Попытка поменять данные другого пользователя авторизованным пользователем")
@allure.title("API-13: Попытка поменять данные другого пользователя авторизованным пользователем")
@allure.tag('api', 'user')
@allure.feature("Пользователь")
@allure.severity('medium')
def test_patch_other_user(authenticated_user):

    auth_client = authenticated_user["client"]

    patch_data = {"first_name": "Hacked"}

    other_user_id = os.getenv("USER_ID")

    with allure.step("Попытка поменять данные другого пользователя пользователя"):
        response = auth_client.patch(f"/users/{other_user_id}", json=patch_data)

        allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                      attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")

        assert response.status_code == 403


