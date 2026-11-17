import os
import json
import logging
import pytest
import requests
from config import Config
from client.api_client import BayMaxApiClient
from selenium_login import BayMaxSeleniumAuth

logger = logging.getLogger("BayMaxConftest")

@pytest.fixture(scope="session")
def base_url():
    return Config.BASE_URL

@pytest.fixture(scope="session")
def api_client():
    """Provides an unauthenticated BayMaxApiClient instance."""
    return BayMaxApiClient(base_url=Config.BASE_URL, timeout=Config.TIMEOUT, verify_ssl=False)

@pytest.fixture(scope="session")
def auth_client():
    """
    Provides an authenticated BayMaxApiClient instance with Bearer Token.
    Reuses existing session.json token if valid; otherwise launches headless Selenium login.
    """
    client = BayMaxApiClient(base_url=Config.BASE_URL, timeout=Config.TIMEOUT, verify_ssl=False)
    session_file = "session.json"
    token = None

    # 1. Try loading cached token
    if os.path.exists(session_file):
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                token = data.get("token")
        except Exception as e:
            logger.warning(f"Could not read cached session: {e}")

    # 2. Verify cached token or re-authenticate via Selenium
    is_valid = False
    if token:
        client.set_token(token)
        try:
            res = client.get("/api/auth/me")
            if res.status_code == 200:
                is_valid = True
                logger.info("Cached JWT token is valid.")
            else:
                logger.info("Cached token returned non-200. Re-authenticating via Selenium...")
        except Exception as e:
            logger.warning(f"Error testing cached token: {e}")

    if not is_valid:
        logger.info("Running automated Selenium login bridge...")
        auth = BayMaxSeleniumAuth(headless=True)
        try:
            login_result = auth.perform_full_login(
                username=Config.USERNAME,
                password=Config.PASSWORD
            )
            token = login_result.get("token")
        finally:
            auth.close()

        if not token:
            pytest.fail("Selenium authentication bridge failed to obtain JWT token.")

        client.set_token(token)

    return client
