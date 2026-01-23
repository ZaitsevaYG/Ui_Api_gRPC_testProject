import json
import os

import allure
import testit
from allure_commons.types import AttachmentType

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
    with open(".env.local", "a") as f:
        f.write(f"\nUSER_ID={user_id}\n")

    os.environ["USER_ID"] = user_id

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
    with open(".env.local", "a") as f:
        f.write(f"\nAUTH_TOKEN={token}\n")

    os.environ["AUTH_TOKEN"] = token  # Для текущей сессии
    print(f"AUTH_TOKEN={token[:30]}... added to env")

    allure.attach(
        f"Token: {token}",
        name="Access Token",
        attachment_type=allure.attachment_type.TEXT
    )

    UserValidator.validate_token_response(data)
