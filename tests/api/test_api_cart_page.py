import json
import allure
from allure_commons.types import AttachmentType
from tests.api.conftest import update_env_var
from tool_shop.utils.validators import CartValidator


@allure.title("API-14: Добавить товары в корзину")
@allure.tag('api', 'cart')
@allure.feature("Корзина")
@allure.severity('medium')
def test_post_add_products_to_cart(api_client, new_cart_id, woodsaw, pilers):

    update_env_var(updates={"CART_ID": new_cart_id})
    with allure.step("Добавление товара в корзину - в корзине 1 товар"):
        first_body = {"product_id": woodsaw.id, "quantity": 1}
        first_response = api_client.post(f"/carts/{new_cart_id}", json=first_body)
        assert first_response.status_code == 200

        first_data = first_response.json()
        CartValidator.validate_cart_item_payload(first_data)

        assert first_data["result"] == "item added or updated"

    with allure.step("Добавление второго товара"):
        second_body = {"product_id": pilers.id, "quantity": 1}
        second_response = api_client.post(f"/carts/{new_cart_id}", json=second_body)

        allure.attach(
            second_response.request.method + " " + second_response.request.url, name="Request 2nd product",
            attachment_type=allure.attachment_type.TEXT)
        allure.attach(
            json.dumps(second_response.json(), indent=4), name="Response 2nd product",
            attachment_type=allure.attachment_type.JSON)

    assert second_response.status_code == 200
    second_data = second_response.json()
    CartValidator.validate_cart_item_payload(second_data)

    if "items" in second_data:
        assert len(second_data["items"]) == 2, "Should have 2 items"
        assert woodsaw.id in [item["product_id"] for item in second_data["items"]]
        assert pilers.id in [item["product_id"] for item in second_data["items"]]

    assert woodsaw.id !=pilers.id



@allure.title("API-15: Получить данные корзины")
@allure.tag('api', 'cart')
@allure.feature("Корзина")
@allure.severity('medium')
def test_get_cart_info(ready_cart_with_items, woodsaw, hammer):
    with allure.step("Проверка возможности получить данные корзины"):
        response = ready_cart_with_items["client"].get(f"/carts/{ready_cart_with_items['id']}")
        cart = response.json()

        allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                      attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")

    assert response.status_code == 200

    assert len(cart["cart_items"]) == 2
    product_ids = [item["product_id"] for item in cart["cart_items"]]
    assert woodsaw.id in product_ids
    assert hammer.id in product_ids




@allure.title("API-16: Обновить количество товара в корзине")
@allure.tag('api', 'cart')
@allure.feature("Корзина")
@allure.severity('medium')
def test_put_change_item_quantity(ready_cart_with_items, woodsaw, hammer):
    updates ={
        "product_id": woodsaw.id,
        "quantity": 2,
    }

    with allure.step("Проверка возможности обновить количество одного товара"):
        response = ready_cart_with_items["client"].put(f"/carts/{ready_cart_with_items['id']}/product/quantity", json=updates)
        cart = response.json()

        allure.attach(body=response.request.method + " " + response.request.url, name="Request",
                      attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")

    assert response.status_code == 200
    assert cart.get("result") == "item added or updated"



@allure.title("API-17: Удалить товар из корзины")
@allure.tag('api', 'cart')
@allure.feature("Корзина")
@allure.severity('medium')
def test_delete_product_from_cart(ready_cart_with_items, measuring_tape, hammer):
    with allure.step("ДО: проверяем что товар есть (2 товара)"):
        cart_id = ready_cart_with_items["id"]
        client = ready_cart_with_items["client"]

        cart_before = client.get(f"/carts/{cart_id}")
        assert len(cart_before.json()["cart_items"]) == 2

    with allure.step("Удаление Hammer"):
        response = client.delete(f"/carts/{cart_id}/product/{hammer.id}")

        allure.attach(
            f"Status: {response.status_code}\nEmpty body",
            name="204 No Content",
            attachment_type=AttachmentType.TEXT
        )

    assert response.status_code == 204
    assert response.text == ""
    assert len(response.content) == 0

    with allure.step("Проверка оставшегося в корзине товара"):
        cart_after = client.get(f"/carts/{cart_id}")
        assert cart_after.status_code == 200

        allure.attach(
            json.dumps(cart_after.json(), indent=4),
            name="Cart AFTER delete",
            attachment_type=AttachmentType.JSON
        )

        items_after = cart_after.json()["cart_items"]
        assert len(items_after) == 1

        remaining_item = items_after[0]
        assert remaining_item["product_id"] != hammer.id

