import sys
from pathlib import Path

import testit

sys.path.insert(0, str(Path(__file__).parent))
# ===================================================

import grpc
import pytest
import product_pb2
from tests.grpc.grpc_utils import log_grpc_request, log_grpc_response, log_grpc_error
import allure

@testit.externalId("GRPC-1")
@testit.displayName("Успешное получение продукта по существующему ID")
@allure.title("GRPC-1: Успешное получение продукта по существующему ID")
@allure.description("Проверка метода GetProduct с валидным ID=1")
@allure.tag('grpc')
@allure.feature("gRPC")
@allure.severity('critical')
def test_get_product_success(grpc_stub):
    # Arrange
    request = product_pb2.GetProductRequest(id=1)
    request = log_grpc_request("product.ProductService/GetProduct", request)

    # Act
    response = grpc_stub.GetProduct(request, timeout=5)
    response = log_grpc_response("product.ProductService/GetProduct", response)

    # Assert
    assert response.id == 1, f"Ожидался ID=1, получен {response.id}"
    assert response.name.strip(), "Имя продукта не должно быть пустым"
    assert response.price >= 0, f"Цена не может быть отрицательной: {response.price}"
    assert isinstance(response.is_rental, bool), "is_rental должен быть булевым типом"

@testit.externalId("GRPC-2")
@testit.displayName("Ошибка при запросе несуществующего продукта")
@allure.title("GRPC-2: Ошибка при запросе несуществующего продукта")
@allure.description("Сервер должен вернуть NOT_FOUND для несуществующего ID")
@allure.tag('grpc')
@allure.feature("gRPC")
@allure.severity('medium')
def test_get_product_not_found(grpc_stub):
     # Arrange
    request = product_pb2.GetProductRequest(id=999999)
    request = log_grpc_request("product.ProductService/GetProduct", request)

    # Act & Assert
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.GetProduct(request, timeout=5)

    log_grpc_error("NOT_FOUND", exc_info.value)

    # Проверяем код ошибки
    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND, \
        f"Ожидался NOT_FOUND, получен {exc_info.value.code()}"


@testit.externalId("GRPC-3")
@testit.displayName("Валидация отрицательного ID")
@allure.title("GRPC-3: Валидация отрицательного ID")
@allure.description("Сервер должен отклонять отрицательные ID с ошибкой INVALID_ARGUMENT")
@allure.tag('grpc')
@allure.feature("gRPC")
@allure.severity('low')
def test_get_product_invalid_id(grpc_stub):
    # Arrange
    request = product_pb2.GetProductRequest(id=-100)
    request = log_grpc_request("product.ProductService/GetProduct", request)

    # Act & Assert
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.GetProduct(request, timeout=5)

    log_grpc_error("INVALID_ARGUMENT", exc_info.value)

    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT, \
        f"Ожидался INVALID_ARGUMENT, получен {exc_info.value.code()}"



@pytest.mark.parametrize("product_id", [1, 2, 3])
@testit.externalId("GRPC-4")
@testit.displayName("GRPC-4: Параметризованный тест для продуктов [ID={product_id}]")
@allure.title("Параметризованный тест для продуктов [ID={product_id}]")
@allure.description("Проверка получения нескольких продуктов из демо-базы")
@allure.tag('grpc')
@allure.feature("gRPC")
@allure.severity('medium')
def test_get_product_multiple_ids(grpc_stub, product_id):
    # Arrange
    request = product_pb2.GetProductRequest(id=product_id)
    request = log_grpc_request(f"product.ProductService/GetProduct (ID={product_id})", request)

    # Act
    response = grpc_stub.GetProduct(request, timeout=5)
    response = log_grpc_response(f"product.ProductService/GetProduct (ID={product_id})", response)

    # Assert
    assert response.id == product_id, f"ID в ответе ({response.id}) не совпадает с запрошенным ({product_id})"
    assert len(response.name) > 0, f"Имя продукта пустое для ID={product_id}"
    assert response.price > 0, f"Цена должна быть положительной для ID={product_id}"