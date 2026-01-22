from faker import Faker
import pytest
from tool_shop.utils.api_client import APIClient, AuthAPIClient

faker = Faker()

@pytest.fixture
def api_client():
    return APIClient()


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
        "name": "Test Hammer",
        "description": "A quality test hammer",
        "price": 19.99,
        "brand_id": "1",
        "category_id": "1",
        "is_rental": False,
        "is_location_offer": False,
        "is_stock": True
    }


@pytest.fixture
def valid_user_data(request):
    test_name = request.node.name.replace("test_", "").replace("_", "_")
    return {
        "email": f"{test_name}_{faker.uuid4()[:8]}@example.com",
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "password": "TestPassword123!"
    }


@pytest.fixture
def valid_brand_data():

    return {
        "name": "Test Brand",
        "slug": "test-brand"
    }


@pytest.fixture
def valid_category_data():

    return {
        "name": "Test Category",
        "slug": "test-category"
    }


@pytest.fixture
def valid_contact_message_data():

    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "subject": "Test Subject",
        "body": "This is a test message"
    }


@pytest.fixture
def valid_cart_item_data():

    return {
        "product_id": "1",
        "quantity": 2
    }


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