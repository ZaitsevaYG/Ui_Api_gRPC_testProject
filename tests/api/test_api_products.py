import json
import allure
from allure_commons.types import AttachmentType
from tool_shop.utils.api_client import APIClient
from tool_shop.utils.validators import ResponseValidator, ProductValidator


@allure.title("API-1: Получение всех товаров")
@allure.tag('api', 'product')
@allure.feature("Продукт")
@allure.severity('high')
def test_get_all_products(api_client: APIClient):
    response = api_client.get("/products")

    allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                  attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")

    ResponseValidator.validate_status_code(response.status_code, 200)
    data = response.json()
    ProductValidator.validate_paginated_products(data)


@allure.title("API-2: Получение товара по ID")
@allure.tag('api', 'product')
@allure.feature("Продукт")
@allure.severity('high')
def test_get_product_by_id(api_client: APIClient, pilers):
    response = api_client.get(f"/products/{pilers.id}")

    allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                  attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")

    ResponseValidator.validate_status_code(response.status_code, 200)
    data = response.json()
    ProductValidator.validate_product_response(data)


@allure.title("API-3: Получение товаров, отсортированных по цене")
@allure.tag('api', 'product', 'filter')
@allure.feature("Фильтрация и поиск")
@allure.severity('medium')
def test_get_products_filtered_by_price(api_client: APIClient):
    response = api_client.get("/products", params={"between": "price,20,100"})

    allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                  attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")

    ResponseValidator.validate_status_code(response.status_code, 200)
    data = response.json()
    ProductValidator.validate_paginated_products(data)

    for product in data["data"]:
        assert 20 <= product["price"] <= 100



@allure.title("API-4: Поиск товаров по названию")
@allure.tag('api', 'product', 'search')
@allure.feature("Фильтрация и поиск")
@allure.severity('medium')
def test_get_products_search_by_name(api_client: APIClient):
    search_query = "Hammer"
    response = api_client.get("/products/search", params={"q": search_query})

    allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                  attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")

    ResponseValidator.validate_status_code(response.status_code, 200)
    data = response.json()
    ProductValidator.validate_paginated_products(data)


@allure.title("API-5: Поиск связанных товаров")
@allure.tag('api', 'product', 'search')
@allure.feature("Фильтрация и поиск")
@allure.severity('low')
def test_get_related_products(api_client: APIClient, measuring_tape):

    response = api_client.get(f"/products/{measuring_tape.id}/related")

    allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                  attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")

    ResponseValidator.validate_status_code(response.status_code, 200)
    data = response.json()
    ResponseValidator.validate_is_list(data)

    for product in data:
        ProductValidator.validate_product_response(product)
