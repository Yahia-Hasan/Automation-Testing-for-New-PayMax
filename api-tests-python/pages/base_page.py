import os
import re
import time
import logging
from typing import Tuple, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger("BayMaxUI")

class BasePage:
    """Base class for all Page Objects in the BayMax UI automation suite."""

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.screenshots_base_dir = "screenshots"
        os.makedirs(self.screenshots_base_dir, exist_ok=True)
        self.page_subfolder = self._resolve_page_subfolder()
        self.screenshots_dir = os.path.join(self.screenshots_base_dir, self.page_subfolder)
        os.makedirs(self.screenshots_dir, exist_ok=True)

    def _resolve_page_subfolder(self) -> str:
        """Derives a dedicated directory name for each page object (e.g. RaysWaitingListPage -> rays_waiting_list)."""
        if hasattr(self, "PAGE_FOLDER") and self.PAGE_FOLDER:
            return self.PAGE_FOLDER
        name = self.__class__.__name__
        if name in ("BasePage", "Base"):
            return "general"
        name = re.sub(r'Page$', '', name)
        s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s).lower()

    def find(self, locator: Tuple[By, str], timeout: int = 10) -> WebElement:
        """Wait for and find a visible element."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except Exception as e:
            logger.error(f"Element not found with locator {locator}: {e}")
            self.take_screenshot(f"not_found_{locator[1][:20]}")
            raise

    def find_all(self, locator: Tuple[By, str], timeout: int = 5) -> List[WebElement]:
        """Find all matching elements, waiting briefly for presence."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except Exception:
            return []

    def click(self, locator: Tuple[By, str], timeout: int = 10) -> None:
        """Wait for element to be clickable and click it."""
        try:
            elem = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            elem.click()
            logger.info(f"Clicked on element: {locator}")
        except Exception as e:
            logger.warning(f"Standard click failed for {locator} ({e}), falling back to JavaScript click.")
            elem = self.find(locator, timeout=timeout)
            self.driver.execute_script("arguments[0].click();", elem)

    def type_text(self, locator: Tuple[By, str], text: str, timeout: int = 10, clear: bool = True) -> None:
        """Wait for input field and type text into it."""
        elem = self.find(locator, timeout=timeout)
        if clear:
            elem.clear()
        elem.send_keys(text)
        logger.info(f"Typed '{text}' into {locator}")

    def get_text(self, locator: Tuple[By, str], timeout: int = 10) -> str:
        """Get visible text from an element."""
        elem = self.find(locator, timeout=timeout)
        return elem.text.strip()

    def is_visible(self, locator: Tuple[By, str], timeout: int = 5) -> bool:
        """Check whether an element is visible on the screen."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def select_ng_option(self, locator: Tuple[By, str], option_text: str, timeout: int = 8) -> None:
        """Interact with Angular ng-select component to choose an option."""
        elem = self.find(locator, timeout=timeout)
        elem.click()
        time.sleep(0.5)
        option_loc = (By.XPATH, f"//div[contains(@class, 'ng-dropdown-panel')]//div[contains(@class, 'ng-option') and contains(., '{option_text}')]")
        opt_elem = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(option_loc)
        )
        opt_elem.click()
        logger.info(f"Selected '{option_text}' in ng-select {locator}")
        time.sleep(0.5)

    def set_date_input(self, locator: Tuple[By, str], date_str: str, timeout: int = 10) -> None:
        """Sets HTML5 date input value via JavaScript to ensure cross-locale correctness."""
        elem = self.find(locator, timeout=timeout)
        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, elem, date_str)
        time.sleep(0.3)
        logger.info(f"Set date value '{date_str}' on {locator}")


    def wait_for_url_contains(self, substring: str, timeout: int = 15) -> bool:
        """Wait until current URL contains a specific substring."""
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(substring)
        )

    def take_screenshot(self, name: str, folder: Optional[str] = None) -> str:
        """Capture screenshot and save to dedicated page subfolder under screenshots/."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        target_dir = os.path.join(self.screenshots_base_dir, folder) if folder else self.screenshots_dir
        os.makedirs(target_dir, exist_ok=True)
        sanitized_name = "".join(c for c in name if c.isalnum() or c in ("-", "_"))
        filepath = os.path.join(target_dir, f"{sanitized_name}_{timestamp}.png")
        self.driver.save_screenshot(filepath)
        logger.info(f"Screenshot captured: {filepath}")
        return filepath
