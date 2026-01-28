import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

import grpc
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

GRPC_TARGET = "127.0.0.1:50052"
GRPC_TIMEOUT = 5

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    retry=retry_if_exception_type(grpc.RpcError)
)
def get_grpc_stub():

    channel = grpc.insecure_channel(GRPC_TARGET)
    try:
        grpc.channel_ready_future(channel).result(timeout=GRPC_TIMEOUT)
    except grpc.FutureTimeoutError:
        channel.close()
        raise ConnectionError(f"gRPC сервер недоступен на {GRPC_TARGET}")
    from product_pb2_grpc import ProductServiceStub  # ← локальный импорт после настройки путей
    return ProductServiceStub(channel)

@pytest.fixture(scope="session")
def grpc_stub():

    stub = get_grpc_stub()
    yield stub
