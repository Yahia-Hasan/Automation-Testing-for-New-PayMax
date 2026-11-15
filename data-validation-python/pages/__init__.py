"""
Pages package initialization.
Implements the Page Object Model (POM) pattern for the BayMax Patients application.
"""
from pages.base_page import BasePage
from pages.navbar_page import NavbarPage
from pages.reception_page import ReceptionPage

__all__ = ["BasePage", "NavbarPage", "ReceptionPage"]
