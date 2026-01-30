
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:

    UI_BASE_URL = os.getenv("UI_BASE_URL", "http://localhost:4200/")
    BROWSER = os.getenv("BROWSER", "chromium")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # Замедление для демонстрации
    PAGE_TIMEOUT = int(os.getenv("PAGE_TIMEOUT", "30000"))  # ms

    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8091/")
    API_TOKEN = os.getenv("API_TOKEN", "")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))  # seconds

    GRPC_HOST = os.getenv("GRPC_HOST", "localhost")
    GRPC_PORT = int(os.getenv("GRPC_PORT", "50051"))

    ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "allure-results")

    BSTACK_USERNAME = os.getenv('BSTACK_USERNAME', "janazaitseva_ckHfp4")
    BSTACK_ACCESSKEY = os.getenv("BSTACK_ACCESSKEY", "ULcqpKU4NxAupDncjgJV")


