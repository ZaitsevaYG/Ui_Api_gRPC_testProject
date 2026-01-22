import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.practicesoftwaretesting.com")
    API_TOKEN = os.getenv("API_TOKEN", "")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

    # UI
    UI_BASE_URL = os.getenv("UI_BASE_URL", "http://localhost:4200/")
    BROWSER = os.getenv("BROWSER", "chromium")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

