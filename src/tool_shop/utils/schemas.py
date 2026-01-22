import json

with open("openapi.json") as f:
    openapi = json.load(f)

PRODUCT_SCHEMA = openapi["components"]["schemas"]["Product"]