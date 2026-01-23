import json
import os

import allure
from allure_commons.types import AttachmentType
from faker import Faker
import pytest

from tool_shop.data.data import MEASURINGTAPE, LONGNOSEPILERS, WOODSAW, THORHUMMER
from tool_shop.utils.api_client import APIClient, AuthAPIClient
from tool_shop.utils.validators import CartValidator

faker = Faker()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def measuring_tape():
    return MEASURINGTAPE

@pytest.fixture
def pilers():
    return LONGNOSEPILERS

@pytest.fixture
def woodsaw():
    return WOODSAW

@pytest.fixture
def hammer():
    return THORHUMMER

@pytest.fixture
def api_client_authenticated():

    client = AuthAPIClient()

    try:
        token_data = client.login(
            email="Scheldon@Cooper.example",
            password="BigBangTheory1!"
        )
        client.set_token(token_data["id"])
    except Exception as e:
        pytest.skip(f"Could not authenticate: {str(e)}")

    yield client

    try:
        client.logout()
    except:
        pass


@pytest.fixture
def api_admin_client():

    client = AuthAPIClient()

    try:
        token_data = client.login(
            email="admin@practicesoftwaretesting.com",
            password="welcome01"
        )
        client.set_token(token_data["access_token"])
    except Exception as e:
        pytest.skip(f"Could not authenticate as admin: {str(e)}")

    yield client

    try:
        client.logout()
    except:
        pass


@pytest.fixture
def valid_product_data():

    return {
        "id": "01KDG94CNBGKGARC43M3R2CRZG",
        "name": "Claw Hammer with Fiberglass Handle",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque quis elit ipsum. Maecenas eu tortor vel elit pharetra sodales. Praesent posuere odio mauris, id faucibus quam sollicitudin et. Suspendisse tristique sapien at mi blandit auctor. Aliquam ullamcorper, odio eget suscipit malesuada, velit magna pharetra diam, at pharetra enim lectus vel massa. Nulla vel lectus et quam feugiat interdum. Fusce hendrerit dignissim purus sed tincidunt. Cras eu ligula urna. Praesent laoreet ipsum ut dictum sodales. Proin sollicitudin imperdiet ante, suscipit dignissim nibh condimentum sagittis. Suspendisse placerat metus a enim fermentum imperdiet. In ut elementum lacus. Aliquam ut arcu a elit tempus tincidunt. Sed sem eros, ornare eu felis consequat, pulvinar consectetur urna. Etiam at cursus elit. Pellentesque aliquet, neque id viverra porta, purus arcu malesuada quam, at cursus ipsum ex nec erat.",
        "price": 20.14,
        "brand_id": "01KDG94BGG8XGAAZNZA60VME5Z",
        "category_id": "01KDG94CGJWWFY9THZVJVWGPH9",
        "is_rental": False,
        "is_location_offer": False,
        "is_stock": True,
        "co2_rating": "D",
        "is_eco_friendly": False
    }



@pytest.fixture
def valid_category_data():

    return {
        "id": "01KDG94CG93JEVGD1XWGHFFQC1",
        "name": "Hand Tools",
        "slug": "hand-tools"
    }


@pytest.fixture
def registered_user(api_client):

    reg_data = {
        "email": faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "password": "TestPass123!@"
    }

    response = api_client.post("/users/register", json=reg_data)
    assert response.status_code == 201

    user = response.json()

    return user


@pytest.fixture
def valid_payment_data():

    return {
        "payment_method": "credit-card",
        "payment_details": {
            "credit_card_number": "4532015112830366",
            "expiration_date": "12/30",
            "cvv": "123",
            "card_holder_name": "John Doe"
        }
    }


@pytest.fixture
def valid_user_registration_data():

    return {
        "email": faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "password": "TestPass123!@"
    }

@pytest.fixture
def empty_email_data():

    return {
        "email": "",
        "first_name": "Harry",
        "last_name": "Potter",
        "password": "Quiddich123!"
    }

@pytest.fixture
def invalid_password_data():

    return {
        "email": faker.email(),
        "first_name": "Homer",
        "last_name": "Simpson",
        "password": "weak"
    }

@pytest.fixture
def authenticated_user(api_client):

    with allure.step('Регистрация нового пользователя'):
        reg_data = {
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": "TestPass123!@"
        }

        response = api_client.post("/users/register", json=reg_data)

        allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                      attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")

        assert response.status_code == 201
        user = response.json()

        login_response = api_client.post("/users/login", json={
            "email": reg_data["email"],
            "password": reg_data["password"]
        })
        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        auth_client = APIClient(token=token)

        yield {
            "user": user,
            "client": auth_client,
            "token": token,
            "email": reg_data["email"],
            "password": reg_data["password"]
        }


        return user

@pytest.fixture
def new_cart_id(api_client):
    with allure.step('Создание новой корзины'):
        response = api_client.post("/carts")

        allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                      attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")

        assert response.status_code == 201

        cart = response.json()
        CartValidator.validate_cart_response(cart)

        cart_id = response.json()["id"]
        return cart_id


@pytest.fixture
def ready_cart_with_items(api_client, woodsaw, hammer):

    create_response = api_client.post("/carts")
    assert create_response.status_code in [200, 201]
    cart_id = create_response.json()["id"]

    client = api_client

    client.post(f"/carts/{cart_id}", json={"product_id": woodsaw.id, "quantity": 1})
    client.post(f"/carts/{cart_id}", json={"product_id": hammer.id, "quantity": 1})

    update_env_var(updates={"CART_ID": cart_id})

    yield {
        "id": cart_id,
        "client": client,
        "woodsaw_id": woodsaw.id,
        "hammer_id": hammer.id
    }


def update_env_var(filename=".env.local", updates: dict = None):

    if updates is None:
        updates = {}

    env_vars = {}
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()


    env_vars.update(updates)

    with open(filename, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

    for key, value in updates.items():
        os.environ[key] = value