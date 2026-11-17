from typing import List, Tuple, Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from config import settings

Locator = Tuple[By, str]

class BasePage:
    """
    Base Page Object providing core WebDriver interaction methods with strict Explicit Waits.
    Designed specifically for Angular 21, PrimeNG, and Arabic RTL interfaces.
    """

    def __init__(self, driver: WebDriver, timeout: int = settings.DEFAULT_TIMEOUT) -> None:
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator: Locator, timeout: int = None) -> WebElement:
        """Waits for and returns a single WebElement present in the DOM."""
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.presence_of_element_located(locator),
            message=f"Element with locator {locator} was not present within {t}s."
        )

    def find_all(self, locator: Locator, timeout: int = None) -> List[WebElement]:
        """Waits for and returns all matching WebElements present in the DOM."""
        t = timeout if timeout is not None else self.timeout
        try:
            return WebDriverWait(self.driver, t).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []

    def wait_visible(self, locator: Locator, timeout: int = None) -> WebElement:
        """Waits until the element is visible on screen and not hidden."""
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located(locator),
            message=f"Element {locator} was not visible within {t}s."
        )

    def wait_clickable(self, locator: Locator, timeout: int = None) -> WebElement:
        """Waits until the element is visible and enabled to receive clicks."""
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator),
            message=f"Element {locator} was not clickable within {t}s."
        )

    def click(self, locator: Locator, timeout: int = None) -> None:
        """
        Safely clicks an element with explicit wait.
        Falls back to JavaScript click if intercepted by Angular animation/overlays.
        """
        element = self.wait_clickable(locator, timeout)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.scroll_into_view(element)
            self.driver.execute_script("arguments[0].click();", element)

    def send_keys(self, locator: Locator, text: str, clear_first: bool = True, timeout: int = None) -> None:
        """
        Safely types text into an input field (supports Arabic UTF-8 text and triggers Angular change events).
        """
        element = self.wait_clickable(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Locator, timeout: int = None) -> str:
        """Returns the trimmed text content of a visible element."""
        return self.wait_visible(locator, timeout).text.strip()

    def get_attribute(self, locator: Locator, attribute: str, timeout: int = None) -> str:
        """Returns the value of a given attribute for an element."""
        element = self.find(locator, timeout)
        return element.get_attribute(attribute)

    def is_visible(self, locator: Locator, timeout: int = 3) -> bool:
        """Checks if an element is currently visible without failing."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            ) is not None
        except TimeoutException:
            return False

    def scroll_into_view(self, element_or_locator: Union[WebElement, Locator]) -> None:
        """Scrolls element into center view using JavaScript."""
        if isinstance(element_or_locator, tuple):
            element = self.find(element_or_locator)
        else:
            element = element_or_locator
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
            element
        )

    def wait_for_invisibility(self, locator: Locator, timeout: int = None) -> bool:
        """Waits until an element (like loading spinner or modal) is hidden or removed."""
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.invisibility_of_element_located(locator),
            message=f"Element {locator} did not become invisible within {t}s."
        )

