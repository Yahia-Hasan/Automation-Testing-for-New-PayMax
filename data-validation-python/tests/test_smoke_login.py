import pytest
from selenium.webdriver.common.by import By

def test_login_flow(authenticated_driver):
    assert "4040" in authenticated_driver.current_url
    navbar = authenticated_driver.find_element(By.CSS_SELECTOR, "header.top-navbar")
    assert navbar.is_displayed()

