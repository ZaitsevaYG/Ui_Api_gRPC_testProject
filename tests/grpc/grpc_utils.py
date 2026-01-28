
import grpc
from allure import step, attach
from allure_commons.types import AttachmentType
from google.protobuf.json_format import MessageToJson, MessageToDict


@step("gRPC запрос → {method_name}")
def log_grpc_request(method_name: str, request):

    request_json = MessageToJson(
        request,
        ensuring_ascii=False,
        indent=2,
        including_default_value_fields=True
    )


    attach(
        body=request_json,
        name=f"Запрос: {method_name}",
        attachment_type=AttachmentType.JSON
    )


    request_text = f"Метод: {method_name}\n{str(request)}"
    attach(
        body=request_text,
        name=f"Кратко: {method_name}",
        attachment_type=AttachmentType.TEXT,
        extension="txt"
    )

    return request


@step("gRPC ответ ← {method_name}")
def log_grpc_response(method_name: str, response):

    response_json = MessageToJson(
        response,
        ensuring_ascii=False,
        indent=2,
        including_default_value_fields=True
    )

    attach(
        body=response_json,
        name=f"Ответ: {method_name}",
        attachment_type=AttachmentType.JSON
    )


    summary = f"ID: {getattr(response, 'id', 'N/A')} | Название: {getattr(response, 'name', 'N/A')}"
    attach(
        body=summary,
        name=f"Сводка: {method_name}",
        attachment_type=AttachmentType.TEXT,
        extension="txt"
    )

    return response


@step("Ожидаем ошибку gRPC: {expected_code}")
def log_grpc_error(expected_code: str, exception: grpc.RpcError):

    error_details = (
        f"Ожидаемый код: {expected_code}\n"
        f"Фактический код: {exception.code()}\n"
        f"Сообщение: {exception.details()}\n"
        f"Debug Info: {exception.debug_error_string() if hasattr(exception, 'debug_error_string') else 'N/A'}"
    )

    attach(
        body=error_details,
        name=f"gRPC Ошибка",
        attachment_type=AttachmentType.TEXT,
        extension="txt"
    )

    return exception