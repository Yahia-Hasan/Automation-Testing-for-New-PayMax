import time
import pytest
from pages.invoice_details_page import InvoiceDetailsPage
from pages.package_invoice_details_page import PackageInvoiceDetailsPage
from pages.ipd_package_invoice_page import IpdPackageInvoicePage
from pages.inpatient_patient_services_page import InpatientPatientServicesPage

class TestPatientInvoicesAndServicesUI:
    """
    Test suite covering deep nested patient billing & service management screens:
    1. Unregistered Regular Invoice Details (/patient-accounts/invoice-details?rid=12746)
    2. Unregistered Quantitative Package Invoice (/patient-accounts/package-invoice-details?rid=12747)
    3. Unregistered Financial Package Invoice (/patient-accounts/ipd-package-invoice?rid=12731)
    4. Registered Invoice Details (/patient-accounts/invoice-details?rid=12744)
    5. Inpatient Patient Services (/waiting-list/patient-services?ReservID=...&AccomID=...)
    """

    def test_01_unregistered_regular_invoice_details(self, auth_driver):
        """1. Verify Unregistered Regular Invoice Details screen (rid=12746)."""
        inv_page = InvoiceDetailsPage(auth_driver)
        inv_page.open_for_reservation(12746)

        assert inv_page.is_loaded(), "Unregistered regular invoice details failed to load."
        assert "/patient-accounts/invoice-details" in auth_driver.current_url
        assert "rid=12746" in auth_driver.current_url

        # Check services table
        row_count = inv_page.get_services_row_count()
        assert row_count > 0, "Invoice services table should have rows."

        inv_page.take_screenshot("01_unregistered_regular_invoice_loaded", folder="invoice_details_unregistered")

    def test_02_unregistered_package_invoice_details(self, auth_driver):
        """2. Verify Unregistered Quantitative Package Invoice Details screen (rid=12747)."""
        pkg_page = PackageInvoiceDetailsPage(auth_driver)
        pkg_page.open_for_reservation(12747)

        assert pkg_page.is_loaded(), "Quantitative package invoice details failed to load."
        assert "/patient-accounts/package-invoice-details" in auth_driver.current_url
        assert "rid=12747" in auth_driver.current_url

        items_count = pkg_page.get_items_count()
        assert items_count > 0, "Package items table should display package lines."

        pkg_page.take_screenshot("01_package_invoice_details_loaded", folder="package_invoice_details")

    def test_03_unregistered_ipd_package_financial_invoice(self, auth_driver):
        """3. Verify Unregistered Financial IPD Package Invoice screen (rid=12731)."""
        ipd_page = IpdPackageInvoicePage(auth_driver)
        ipd_page.open_for_reservation(12731)

        assert ipd_page.is_loaded(), "Financial package invoice failed to load."
        assert "/patient-accounts/ipd-package-invoice" in auth_driver.current_url
        assert "rid=12731" in auth_driver.current_url

        services_count = ipd_page.get_services_count()
        assert services_count > 0, "Financial package services table should have rows."

        ipd_page.take_screenshot("01_ipd_package_invoice_loaded", folder="ipd_package_invoice")

    def test_04_registered_invoice_details(self, auth_driver):
        """4. Verify Registered Invoice Details screen (rid=12744)."""
        inv_page = InvoiceDetailsPage(auth_driver)
        inv_page.open_for_reservation(12744)

        assert inv_page.is_loaded(), "Registered invoice details failed to load."
        assert "/patient-accounts/invoice-details" in auth_driver.current_url
        assert "rid=12744" in auth_driver.current_url
        assert inv_page.is_registered_invoice(), "Should detect registered invoice buttons or tabs."

        # Test switching across available tabs
        inv_page.switch_tab("accounting")
        inv_page.take_screenshot("01_registered_invoice_accounting", folder="invoice_details_registered")

        inv_page.switch_tab("surgeries")
        inv_page.take_screenshot("02_registered_invoice_surgeries", folder="invoice_details_registered")

        inv_page.switch_tab("accommodations")
        inv_page.take_screenshot("03_registered_invoice_accommodations", folder="invoice_details_registered")

        inv_page.switch_tab("icu")
        inv_page.take_screenshot("04_registered_invoice_icu", folder="invoice_details_registered")

        inv_page.switch_tab("summary")
        inv_page.take_screenshot("05_registered_invoice_summary", folder="invoice_details_registered")

    def test_05_inpatient_patient_services_full_flow(self, auth_driver):
        """5. Verify Inpatient Patient Services screen & Service Categories (Lab, Rays, Blood, Diets, etc.)."""
        reserv_token = "CfDJ8KcUxlP3wTpIkfqEIRtHon7zSAyPB2lIYbCHCWrqBp7K4jkMTKXk5axOsUN82puPKlT-g3kDxq_2u17f2Nbo30AlOJpkeRYjWxGWxs0ataq_nI5P2Hkl9_cnHr5BBTAPOQ"
        accom_token = "CfDJ8KcUxlP3wTpIkfqEIRtHon7OgT6pBpREID8flcN6k4JcDwSkHUmjfUN4cqbPAEP_yrAaMlYRDvHAtlfNvD88XA4UikMEacqBo7EBAZJvs514FgLI0ryWqOtEPLWSktt3Vg"

        services_page = InpatientPatientServicesPage(auth_driver)
        services_page.open_with_tokens(reserv_token, accom_token)

        assert services_page.is_loaded(), "Inpatient patient services screen failed to load."
        assert "/waiting-list/patient-services" in auth_driver.current_url

        services_page.take_screenshot("01_patient_services_overview", folder="inpatient_patient_services")

        # Test entering short code and notes
        services_page.enter_short_code("101")
        services_page.enter_notes("طلب تحاليل وأشعة للمريض الداخلي - متابعة سريرية")
        services_page.take_screenshot("02_patient_services_form_entered", folder="inpatient_patient_services")

        # Test clicking new to reset form
        services_page.click_new()

        # Test clicking favorites
        services_page.click_favorites()
        services_page.take_screenshot("03_patient_services_favorites_clicked", folder="inpatient_patient_services")

        # Verify tables count
        assert services_page.get_tables_count() > 0, "Patient services screen should contain services and orders tables."
