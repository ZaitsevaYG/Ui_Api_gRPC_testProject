from faker import Faker
import pytest

from tool_shop.data.data import MEASURINGTAPE, LONGNOSEPILERS
from tool_shop.utils.api_client import APIClient, AuthAPIClient

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
def api_client_authenticated():

    client = AuthAPIClient()

    try:
        token_data = client.login(
            email="customer@practicesoftwaretesting.com",
            password="welcome01"
        )
        client.set_token(token_data["access_token"])
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
def valid_brand_data():

    return {
        "id": "01KDG94BGG8XGAAZNZA60VME5Z",
        "name": "ForgeFlex Tools",
        "slug": "forgeflex-tools",

    }


@pytest.fixture
def valid_category_data():

    return {
        "id": "01KDG94CG93JEVGD1XWGHFFQC1",
        "name": "Hand Tools",
        "slug": "hand-tools"
    }


# @pytest.fixture
# def valid_contact_message_data():
#
#     return {
#         "first_name": "John",
#         "last_name": "Doe",
#         "email": "john@example.com",
#         "subject": "Test Subject",
#         "body": "This is a test message"
#     }


# @pytest.fixture
# def valid_cart_item_data():
#
#     return {
#         "product_id": "1",
#         "quantity": 2
#     }


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