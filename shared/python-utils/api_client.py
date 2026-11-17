import logging
from typing import Any, Dict, Optional
import requests
import urllib3
from unified_config import UnifiedConfig

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("BayMaxApiClient")


class BayMaxApiClient:
    """Unified REST API client for BayMax Patients system."""

    def __init__(
        self,
        base_url: str = UnifiedConfig.BASE_URL,
        timeout: int = UnifiedConfig.TIMEOUT,
        verify_ssl: bool = False
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.token: Optional[str] = None
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def set_token(self, token: str) -> None:
        """Set the Bearer token for authorized requests."""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Bearer token successfully set in session headers.")

    def clear_token(self) -> None:
        """Remove Bearer token from session."""
        self.token = None
        self.session.headers.pop("Authorization", None)

    def login(
        self,
        username: str = UnifiedConfig.USERNAME,
        password: str = UnifiedConfig.PASSWORD
    ) -> requests.Response:
        """Authenticate with the API directly if modern login endpoint exists."""
        url = f"{self.base_url}/api/auth/login"
        payload = {"userName": username, "password": password}
        logger.info(f"Attempting direct API login: {url}")

        response = self.session.post(url, json=payload, timeout=self.timeout, verify=self.verify_ssl)
        if response.status_code == 200:
            try:
                res_json = response.json()
                token = res_json.get("data", {}).get("token") or res_json.get("token")
                if token:
                    self.set_token(token)
                    logger.info("Login successful. Token acquired.")
            except Exception as e:
                logger.error(f"Failed to parse login response JSON: {e}")
        return response

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Generic HTTP request method with logging and SSL bypass."""
        endpoint = endpoint.lstrip("/")
        url = f"{self.base_url}/{endpoint}" if not endpoint.startswith("http") else endpoint

        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
        if "verify" not in kwargs:
            kwargs["verify"] = self.verify_ssl

        logger.info(f"HTTP {method.upper()} -> {url}")
        if "params" in kwargs and kwargs["params"]:
            logger.info(f"Query Params: {kwargs['params']}")
        if "json" in kwargs and kwargs["json"]:
            logger.info(f"Request Body: {kwargs['json']}")

        try:
            response = self.session.request(method=method, url=url, **kwargs)
            logger.info(f"HTTP {response.status_code} ({response.elapsed.total_seconds():.3f}s) <- {url}")
            return response
        except requests.RequestException as e:
            logger.error(f"Request failed for {method.upper()} {url}: {e}")
            raise

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json: Optional[Any] = None, **kwargs) -> requests.Response:
        return self.request("POST", endpoint, json=json, **kwargs)

    def put(self, endpoint: str, json: Optional[Any] = None, **kwargs) -> requests.Response:
        return self.request("PUT", endpoint, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)

    def patch(self, endpoint: str, json: Optional[Any] = None, **kwargs) -> requests.Response:
        return self.request("PATCH", endpoint, json=json, **kwargs)
