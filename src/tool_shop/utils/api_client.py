import allure
import requests
from typing import Dict, Any
from config import Config


class APIClient:

    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = base_url or Config.API_BASE_URL
        self.token = token or Config.API_TOKEN
        self.timeout = Config.API_TIMEOUT


    def _get_headers(self, **kwargs) -> Dict[str, str]:

        headers = {
            "Content-Type": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        headers.update(kwargs)
        return headers

    with allure.step("API Request"):
        def get(self, endpoint: str, params: Dict[str, Any] = None, **kwargs) -> requests.Response:

            url = f"{self.base_url}{endpoint}"
            return requests.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=self.timeout,
                **kwargs
            )
    with allure.step("API Request"):
        def post(self, endpoint: str, data: Dict[str, Any] = None, files=None, **kwargs) -> requests.Response:
            url = f"{self.base_url}{endpoint}"

            if files:
                headers = {k: v for k, v in self._get_headers().items() if k != "Content-Type"}
                return requests.post(url, headers=headers, data=data, files=files, timeout=self.timeout, **kwargs)


            if data is not None:
                kwargs["json"] = data

            return requests.post(
                url,
                headers=self._get_headers(),
                timeout=self.timeout,
                **kwargs)

    with allure.step("API Request"):
        def put(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> requests.Response:

            if data is not None:
                kwargs["json"] = data

            url = f"{self.base_url}{endpoint}"
            return requests.put(
                url,
                headers=self._get_headers(),
                timeout=self.timeout,
                **kwargs
            )

    with allure.step("API Request"):
        def patch(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> requests.Response:

            url = f"{self.base_url}{endpoint}"

            if data is not None:
                kwargs["json"] = data

            return requests.patch(
                url,
                headers=self._get_headers(),
                timeout=self.timeout,
                **kwargs
            )

    with allure.step("API Request"):
        def delete(self, endpoint: str, **kwargs) -> requests.Response:

            url = f"{self.base_url}{endpoint}"
            return requests.delete(
                url,
                headers=self._get_headers(),
                timeout=self.timeout,
                **kwargs
            )


class AuthAPIClient(APIClient):

    def login(self, email: str, password: str) -> Dict[str, Any]:

        response = self.post(
            "/users/login",
            data={"email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()

    def set_token(self, token: str):
        self.token = token

    def refresh_token(self) -> Dict[str, Any]:
        response = self.get("/users/refresh")
        response.raise_for_status()
        data = response.json()
        self.set_token(data.get("access_token"))
        return data

    def logout(self):
        response = self.get("/users/logout")
        response.raise_for_status()
        self.token = None
        return response.json()

    def get_current_user(self) -> Dict[str, Any]:
        response = self.get("/users/me")
        response.raise_for_status()
        return response.json()




