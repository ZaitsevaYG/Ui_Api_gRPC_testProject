import re
from typing import Dict, Any, List, Type
from datetime import datetime


class ResponseValidator:

    @staticmethod
    def validate_status_code(response_status: int, expected: int) -> bool:
        assert response_status == expected, (
            f"Expected status {expected}, got {response_status}"
        )
        return True

    @staticmethod
    def validate_is_list(data: Any) -> bool:
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        return True

    @staticmethod
    def validate_is_dict(data: Any) -> bool:
        assert isinstance(data, dict), f"Expected dict, got {type(data)}"
        return True

    @staticmethod
    def validate_required_fields(data: Dict, required_fields: List[str]) -> bool:
        missing_fields = [field for field in required_fields if field not in data]
        assert not missing_fields, (
            f"Missing required fields: {missing_fields}"
        )
        return True

    @staticmethod
    def validate_field_type(data: Dict, field: str, expected_type: Type | tuple ) -> bool:
        assert field in data, f"Field '{field}' not found"
        assert isinstance(data[field], expected_type), (
            f"Field '{field}' expected {expected_type}, got {type(data[field])}"
        )
        return True

    @staticmethod
    def validate_string_not_empty(value: str) -> bool:
        assert value and isinstance(value, str), (
            f"Expected non-empty string, got {value}"
        )
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        assert re.match(email_pattern, email), f"Invalid email format: {email}"
        return True

    @staticmethod
    def validate_uuid(value: str) -> bool:
        uuid_pattern = r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$'
        assert re.match(uuid_pattern, value, re.IGNORECASE), (
            f"Invalid UUID format: {value}"
        )
        return True

    @staticmethod
    def validate_numeric(value: Any, min_val: float = None, max_val: float = None) -> bool:
        assert isinstance(value, (int, float)), (
            f"Expected numeric value, got {type(value)}"
        )
        if min_val is not None:
            assert value >= min_val, f"Value {value} is less than minimum {min_val}"
        if max_val is not None:
            assert value <= max_val, f"Value {value} is greater than maximum {max_val}"
        return True

    @staticmethod
    def validate_datetime(value: str, datetime_format: str = "%Y-%m-%d %H:%M:%S") -> bool:
        try:
            datetime.strptime(value, datetime_format)
            return True
        except ValueError:
            raise AssertionError(f"Invalid datetime format: {value}")

    @staticmethod
    def validate_date(value: str, date_format: str = "%Y-%m-%d") -> bool:
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            raise AssertionError(f"Invalid date format: {value}")

    @staticmethod
    def validate_enum(value: str, allowed_values: List[str]) -> bool:
        assert value in allowed_values, (
            f"Value '{value}' not in allowed values: {allowed_values}"
        )
        return True


class BrandValidator(ResponseValidator):

    @staticmethod
    def validate_brand_response(brand: Dict) -> bool:

        BrandValidator.validate_required_fields(
            brand,
            ["id", "name", "slug"]
        )
        BrandValidator.validate_field_type(brand, "id", str)
        BrandValidator.validate_field_type(brand, "name", str)
        BrandValidator.validate_field_type(brand, "slug", str)
        return True

    @staticmethod
    def validate_brand_request(brand: Dict) -> bool:

        BrandValidator.validate_required_fields(brand, ["name", "slug"])
        BrandValidator.validate_string_not_empty(brand["name"])
        BrandValidator.validate_string_not_empty(brand["slug"])
        return True


class ProductValidator(ResponseValidator):

    @staticmethod
    def validate_product_response(product: Dict) -> bool:

        ProductValidator.validate_required_fields(
            product,
            ["id", "name", "description", "price", "brand", "category"]
        )
        ProductValidator.validate_field_type(product, "id", str)
        ProductValidator.validate_field_type(product, "name", str)
        ProductValidator.validate_field_type(product, "price", (int, float))
        ProductValidator.validate_numeric(product["price"], min_val=0)
        return True

    @staticmethod
    def validate_product_request(product: Dict) -> bool:

        ProductValidator.validate_required_fields(
            product,
            ["name", "description", "price", "brand_id", "category_id"]
        )
        ProductValidator.validate_string_not_empty(product["name"])
        ProductValidator.validate_numeric(product["price"], min_val=0)
        return True

    @staticmethod
    def validate_paginated_products(data: Dict) -> bool:

        ResponseValidator.validate_required_fields(
            data,
            ["current_page", "data", "last_page", "per_page", "total"]
        )
        ResponseValidator.validate_is_list(data["data"])
        for product in data["data"]:
            ProductValidator.validate_product_response(product)
        return True


class UserValidator(ResponseValidator):

    @staticmethod
    def validate_user_response(user: Dict) -> bool:

        UserValidator.validate_required_fields(
            user,
            ["id", "email", "first_name", "last_name"]
        )
        UserValidator.validate_field_type(user, "id", str)
        UserValidator.validate_field_type(user, "email", str)
        UserValidator.validate_email(user["email"])
        return True

    @staticmethod
    def validate_user_request(user: Dict) -> bool:

        required_fields = ["email", "first_name", "last_name", "password"]
        UserValidator.validate_required_fields(user, required_fields)
        UserValidator.validate_email(user["email"])
        UserValidator.validate_string_not_empty(user["first_name"])
        UserValidator.validate_string_not_empty(user["last_name"])
        UserValidator.validate_string_not_empty(user["password"])
        return True

    @staticmethod
    def validate_token_response(token_data: Dict) -> bool:

        UserValidator.validate_required_fields(
            token_data,
            ["access_token", "token_type", "expires_in"]
        )
        UserValidator.validate_string_not_empty(token_data["access_token"])
        assert token_data["token_type"] == "bearer", "Invalid token type"
        return True


class CartValidator(ResponseValidator):

    @staticmethod
    def validate_cart_response(cart: Dict) -> bool:

        CartValidator.validate_required_fields(cart, ["id"])
        CartValidator.validate_field_type(cart, "id", str)
        return True

    @staticmethod
    def validate_cart_item_payload(item: Dict) -> bool:

        CartValidator.validate_required_fields(item, ["product_id", "quantity"])
        CartValidator.validate_field_type(item, "product_id", str)
        CartValidator.validate_field_type(item, "quantity", int)
        CartValidator.validate_numeric(item["quantity"], min_val=1)
        return True


class CategoryValidator(ResponseValidator):

    @staticmethod
    def validate_category_response(category: Dict) -> bool:

        CategoryValidator.validate_required_fields(
            category,
            ["id", "name", "slug"]
        )
        CategoryValidator.validate_field_type(category, "id", str)
        CategoryValidator.validate_string_not_empty(category["name"])
        return True

    @staticmethod
    def validate_category_tree_response(category: Dict) -> bool:

        CategoryValidator.validate_category_response(category)
        if "sub_categories" in category:
            assert isinstance(category["sub_categories"], list), (
                "sub_categories should be a list"
            )
        return True

    @staticmethod
    def validate_category_request(category: Dict) -> bool:

        CategoryValidator.validate_required_fields(category, ["name", "slug"])
        CategoryValidator.validate_string_not_empty(category["name"])
        return True


class InvoiceValidator(ResponseValidator):

    @staticmethod
    def validate_invoice_response(invoice: Dict) -> bool:

        InvoiceValidator.validate_required_fields(
            invoice,
            ["id", "invoice_number", "user_id", "status", "total"]
        )
        InvoiceValidator.validate_enum(
            invoice["status"],
            ["AWAITING_FULFILLMENT", "ON_HOLD", "AWAITING_SHIPMENT", "SHIPPED", "COMPLETED"]
        )
        InvoiceValidator.validate_numeric(invoice["total"], min_val=0)
        return True

    @staticmethod
    def validate_invoice_status(status: str) -> bool:

        valid_statuses = [
            "AWAITING_FULFILLMENT",
            "ON_HOLD",
            "AWAITING_SHIPMENT",
            "SHIPPED",
            "COMPLETED"
        ]
        InvoiceValidator.validate_enum(status, valid_statuses)
        return True


class FavoriteValidator(ResponseValidator):

    @staticmethod
    def validate_favorite_response(favorite: Dict) -> bool:

        FavoriteValidator.validate_required_fields(
            favorite,
            ["id", "product_id", "user_id"]
        )
        return True

    @staticmethod
    def validate_favorite_request(favorite: Dict) -> bool:

        FavoriteValidator.validate_required_fields(favorite, ["product_id"])
        return True


class PaymentValidator(ResponseValidator):

    @staticmethod
    def validate_payment_request(payment: Dict) -> bool:

        PaymentValidator.validate_required_fields(
            payment,
            ["payment_method", "payment_details"]
        )
        valid_methods = [
            "bank-transfer",
            "cash-on-delivery",
            "credit-card",
            "buy-now-pay-later",
            "gift-card"
        ]
        PaymentValidator.validate_enum(payment["payment_method"], valid_methods)
        return True


class ContactMessageValidator(ResponseValidator):

    @staticmethod
    def validate_contact_request(message: Dict) -> bool:

        ContactMessageValidator.validate_required_fields(
            message,
            ["first_name", "email", "subject", "body"]
        )
        ContactMessageValidator.validate_email(message["email"])
        return True

    @staticmethod
    def validate_contact_response(message: Dict) -> bool:

        ContactMessageValidator.validate_required_fields(
            message,
            ["id", "first_name", "email", "subject", "body"]
        )
        return True
