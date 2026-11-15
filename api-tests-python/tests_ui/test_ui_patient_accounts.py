import pytest
from pages.home_page import HomePage
from pages.patient_accounts_page import (
    UnregisteredInvoicesPage,
    RegisteredInvoicesPage,
    PatientCheckupsPage,
    PatientSettlementsPage,
    TechnicianBankPage,
    MergePatientsPage,
)

class TestPatientAccountsUI:
    """UI Test Suite covering all 6 Patient Accounts screens."""

    def test_01_unregistered_invoices(self, auth_driver):
        """1. Verify Open Statements of Account (/patient-accounts/unregistered-invoices)."""
        home = HomePage(auth_driver).open()
        home.open_unregistered_invoices()

        page = UnregisteredInvoicesPage(auth_driver)
        assert page.is_loaded(), "Unregistered invoices page failed to load."
        assert "/patient-accounts/unregistered-invoices" in auth_driver.current_url

        page.filter_today_entrance()
        page.take_screenshot("test_unregistered_invoices_today_entrance")

        page.click_search()
        page.take_screenshot("test_unregistered_invoices_searched")

    def test_02_registered_invoices(self, auth_driver):
        """2. Verify Registered Patient Invoices (/patient-accounts/registered-invoices)."""
        home = HomePage(auth_driver).open()
        home.open_registered_invoices()

        page = RegisteredInvoicesPage(auth_driver)
        assert page.is_loaded(), "Registered invoices page failed to load."
        assert "/patient-accounts/registered-invoices" in auth_driver.current_url

        page.filter_today_exit()
        page.take_screenshot("test_registered_invoices_today_exit")

        page.click_search()
        page.take_screenshot("test_registered_invoices_searched")

    def test_03_patient_checkups(self, auth_driver):
        """3. Verify Inpatient Accounts (/patient-accounts/patient-checkups)."""
        home = HomePage(auth_driver).open()
        home.open_patient_checkups()

        page = PatientCheckupsPage(auth_driver)
        assert page.is_loaded(), "Patient checkups page failed to load."
        assert "/patient-accounts/patient-checkups" in auth_driver.current_url

        page.click_search()
        page.take_screenshot("test_patient_checkups_searched")

    def test_04_patient_settlements(self, auth_driver):
        """4. Verify Patient Settlements / Debts (/patient-accounts/patient-settlements)."""
        home = HomePage(auth_driver).open()
        home.open_patient_settlements()

        page = PatientSettlementsPage(auth_driver)
        assert page.is_loaded(), "Patient settlements page failed to load."
        assert "/patient-accounts/patient-settlements" in auth_driver.current_url

        page.click_search()
        page.take_screenshot("test_patient_settlements_searched")

    def test_05_technician_bank(self, auth_driver):
        """5. Verify Technician Bank (/patient-accounts/technician-bank)."""
        home = HomePage(auth_driver).open()
        home.open_technician_bank()

        page = TechnicianBankPage(auth_driver)
        assert page.is_loaded(), "Technician bank page failed to load."
        assert "/patient-accounts/technician-bank" in auth_driver.current_url

        page.click_search()
        page.take_screenshot("test_technician_bank_searched")

    def test_06_merge_patients(self, auth_driver):
        """6. Verify Merge Patients (/patient-accounts/merge-patients)."""
        home = HomePage(auth_driver).open()
        home.open_merge_patients()

        page = MergePatientsPage(auth_driver)
        assert page.is_loaded(), "Merge patients page failed to load."
        assert "/patient-accounts/merge-patients" in auth_driver.current_url

        page.fill_codes("999991", "999992")
        page.take_screenshot("test_merge_patients_inputs_filled")
