from typing import List, Dict
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class NavbarPage(BasePage):
    """
    Page Object for the BayMax Patients Top Navbar Component.
    Handles dropdown interactions, menu items, and responsive navigation controls.
    """

    # Locators
    NAVBAR_CONTAINER = (By.CSS_SELECTOR, "header.top-navbar")
    BRAND_LOGO = (By.CSS_SELECTOR, "header.top-navbar a.navbar-brand")
    USER_MENU_BTN = (By.CSS_SELECTOR, "header.top-navbar button.user-menu-btn")
    SEARCH_BTN = (By.CSS_SELECTOR, "header.top-navbar button.search-btn")
    BODY = (By.TAG_NAME, "body")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def is_navbar_visible(self) -> bool:
        """Checks if the top navbar is visible."""
        return self.is_visible(self.NAVBAR_CONTAINER)

    def get_dropdown_button(self, name: str):
        """Returns the dropdown button WebElement matching the visible Arabic text."""
        xpath = f"//header[contains(@class,'top-navbar')]//button[contains(@class,'nav-group-btn')][.//span[contains(text(),'{name}')] or contains(text(),'{name}')]"
        return self.find((By.XPATH, xpath))

    def get_dropdown_container(self, name: str):
        """Returns the parent .nav-dropdown container for a given dropdown button."""
        xpath = f"//header[contains(@class,'top-navbar')]//div[contains(@class,'nav-dropdown')][.//span[contains(text(),'{name}')] or .//button[contains(text(),'{name}')]]"
        return self.find((By.XPATH, xpath))

    def is_dropdown_open(self, name: str) -> bool:
        """Checks whether a dropdown container has the '.open' class."""
        container = self.get_dropdown_container(name)
        classes = container.get_attribute("class") or ""
        return "open" in classes.split()

    def open_dropdown(self, name: str) -> None:
        """Clicks the dropdown button to open it if not already open."""
        if not self.is_dropdown_open(name):
            btn = self.get_dropdown_button(name)
            self.click((By.XPATH, f"//header[contains(@class,'top-navbar')]//button[contains(@class,'nav-group-btn')][.//span[contains(text(),'{name}')] or contains(text(),'{name}')]"))
            # Wait for .open class on container
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: self.is_dropdown_open(name),
                message=f"Dropdown '{name}' did not gain '.open' class within {self.timeout}s."
            )

    def close_dropdown(self, name: str) -> None:
        """Clicks the dropdown button again to close it if open."""
        if self.is_dropdown_open(name):
            btn_xpath = f"//header[contains(@class,'top-navbar')]//button[contains(@class,'nav-group-btn')][.//span[contains(text(),'{name}')] or contains(text(),'{name}')]"
            self.click((By.XPATH, btn_xpath))
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: not self.is_dropdown_open(name),
                message=f"Dropdown '{name}' did not close within {self.timeout}s."
            )

    def get_open_dropdown_items(self) -> List[Dict[str, str]]:
        """
        Returns all dropdown items (text and href) currently visible inside the open dropdown.
        """
        items_locator = (By.CSS_SELECTOR, "header.top-navbar .nav-dropdown.open .dropdown-menu a.dropdown-item")
        elements = self.find_all(items_locator)
        result = []
        for el in elements:
            result.append({
                "text": el.text.strip(),
                "href": el.get_attribute("href") or ""
            })
        return result

    def click_dropdown_item_by_href(self, href_suffix: str) -> None:
        """Clicks an item in the open dropdown by its href attribute."""
        item_xpath = f"//header[contains(@class,'top-navbar')]//div[contains(@class,'nav-dropdown') and contains(@class,'open')]//a[contains(@class,'dropdown-item') and contains(@href,'{href_suffix}')]"
        self.click((By.XPATH, item_xpath))

    def click_dropdown_item_by_text(self, text: str) -> None:
        """Clicks an item in the open dropdown by its visible text."""
        item_xpath = f"//header[contains(@class,'top-navbar')]//div[contains(@class,'nav-dropdown') and contains(@class,'open')]//a[contains(@class,'dropdown-item')][contains(text(),'{text}')]"
        self.click((By.XPATH, item_xpath))

    def click_outside(self) -> None:
        """Simulates click-outside by clicking on the document body to dismiss open dropdowns."""
        self.driver.execute_script("document.body.click();")

