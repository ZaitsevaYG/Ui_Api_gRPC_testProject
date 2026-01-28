# tests/grpc/conftest.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))  # ← КРИТИЧЕСКИ ВАЖНО: только папка grpc

import grpc
import pytest

GRPC_TARGET = "127.0.0.1:50052"
GRPC_TIMEOUT = 5


@pytest.fixture(scope="session")
def grpc_channel():

    channel = grpc.insecure_channel(GRPC_TARGET)

    try:
        grpc.channel_ready_future(channel).result(timeout=GRPC_TIMEOUT)
    except grpc.FutureTimeoutError:
        pytest.fail(
            f"gRPC сервер недоступен на {GRPC_TARGET}\n"
            f"   Запустите: python -m tests.grpc.server\n"
        )

    yield channel
    channel.close()


@pytest.fixture(scope="session")
def grpc_stub(grpc_channel):

    import product_pb2_grpc  # ← Теперь импорт сработает!
    return product_pb2_grpc.ProductServiceStub(grpc_channel)