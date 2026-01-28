# config.py
import os
from dotenv import load_dotenv

# Загружаем .env один раз при импорте модуля
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

    # ==================== TestIT Settings ====================
    TMS_URL = os.getenv("TMS_URL", "https://team-perf.testit.software")
    TMS_PRIVATE_TOKEN = os.getenv("TMS_PRIVATE_TOKEN", "")
    TMS_PROJECT_ID = os.getenv("TMS_PROJECT_ID", "")
    TMS_CONFIGURATION_ID = os.getenv("TMS_CONFIGURATION_ID", "")
    TMS_TEST_RUN_NAME = os.getenv("TMS_TEST_RUN_NAME", "Regression Tests")
    TMS_AUTOMATIC_CREATION_TEST_CASES = os.getenv("TMS_AUTOMATIC_CREATION_TEST_CASES", "true").lower() == "true"

    # ==================== Allure Settings ====================
    ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "allure-results")


