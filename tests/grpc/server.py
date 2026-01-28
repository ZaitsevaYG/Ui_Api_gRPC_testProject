import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
# ===================================================

import grpc
from concurrent import futures

from tests.grpc import product_pb2, product_pb2_grpc

PRODUCTS = {
    1: product_pb2.GetProductResponse(
        id=1, name="Bolt Cutters", description="Bolt Cutters. Red colour", price=199.99, is_rental=False
    ),
    2: product_pb2.GetProductResponse(
        id=2, name="Safety Goggles", description="Safety Goggles. Eco tool", price=49.99, is_rental=False
    ),
    3: product_pb2.GetProductResponse(
        id=3, name="Bulldozer", description="Bulldozer", price=349.99, is_rental=True
    ),
}


class ProductServiceImpl(product_pb2_grpc.ProductServiceServicer):
    def GetProduct(self, request, context):
        print(f"📥GetProduct(id={request.id})")

        if request.id <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"ID продукта должен быть положительным числом, получено: {request.id}")
            return product_pb2.GetProductResponse()

        if request.id not in PRODUCTS:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Продукт #{request.id} не найден")
            return product_pb2.GetProductResponse()

        return PRODUCTS[request.id]


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceImpl(), server)


    port = server.add_insecure_port('127.0.0.1:50052')
    server.start()

    print(f"gRPC демо-сервер ЗАПУЩЕН на порту {port}")
    print("   Доступные продукты:")
    for pid, p in PRODUCTS.items():
        print(f"     • ID {pid}: {p.name} — ${p.price} ({'аренда' if p.is_rental else 'покупка'})")
    print("\n   Для остановки нажмите Ctrl+C\n")

    server.wait_for_termination()


if __name__ == '__main__':
    serve()