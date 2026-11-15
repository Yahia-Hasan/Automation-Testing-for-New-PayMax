import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("BayMaxHomePage")

class HomePage(BasePage):
    """Page object for the modern BayMax Dashboard / Home screen."""

    URL = "https://196.218.246.250:4040/home"

    # Locators
    TXT_WELCOME_HEADER = (By.XPATH, "//h1 | //div[contains(@class, 'welcome-text')]//h1")
    NAV_DROPDOWN_ADMISSION = (By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'مكتب الدخول')]")
    NAV_LINK_RECEPTION = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception']")
    NAV_LINK_OCCUPANCY = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception/occupancy-report']")
    NAV_LINK_ADMISSION_DISCHARGE = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception/admission-discharge-report']")
    NAV_LINK_SURGERY_BOOKING = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception/surgery-booking']")
    NAV_LINK_LEAVING_REQUESTS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/waiting-list/leaving-requests']")
    NAV_LINK_ACCOUNTANT_LEAVING = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/accountant/leaving-requests']")
    NAV_LINK_EMERGENCY_TRANSFERS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception/emergency-transfers']")
    NAV_LINK_LEAVING_APPROVAL_REPORT = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception/leaving-approval-report']")

    NAV_DROPDOWN_CLINIC = (By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'العيادات الخارجية')]")
    NAV_LINK_CLINIC_WAITING = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/clinic/waiting-list']")

    NAV_DROPDOWN_INFODESK = (By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'الاستعلامات')]")
    NAV_LINK_PRICE_LISTS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/info-desk/price-lists']")
    NAV_LINK_DOCTORS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/info-desk/doctors']")
    NAV_LINK_SHIFT_MANAGERS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/info-desk/shift-managers']")
    NAV_LINK_SURGERY_NAMES = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/info-desk/surgery-names']")
    NAV_LINK_SURGERY_PRICES = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/info-desk/surgery-prices']")
    NAV_LINK_SURGERY_AGENDA = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/info-desk/surgery-agenda']")
    NAV_LINK_CLINIC_AGENDA = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/info-desk/clinic-agenda']")
    NAV_LINK_PHONE_BOOK = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/info-desk/phone-book']")
    NAV_LINK_SURGERY_WAITING = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/info-desk/surgeries']")
    NAV_LINK_PACKAGES = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/info-desk/packages']")

    NAV_DROPDOWN_RESIDENTS = (By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'المرضى المقيمين')]")
    NAV_LINK_INPATIENTS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception/inpatients']")
    NAV_LINK_ICU = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception/icu']")
    NAV_LINK_NEONATAL = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception/neonatal']")
    NAV_LINK_ATTENDANTS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception/attendants']")
    NAV_LINK_ROOM_MANAGEMENT = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception/room-management']")
    NAV_LINK_ROOM_MAP = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/reception/rooms']")

    NAV_DROPDOWN_RAYS = (By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'الأشعة')]")
    NAV_LINK_RAYS_WAITING = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/rays/waiting-list']")
    NAV_LINK_RAYS_STATUS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/rays/status']")
    NAV_LINK_RAYS_DETAILS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/rays/details']")

    NAV_DROPDOWN_LAB = (By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'المعمل وبنك الدم')]")
    NAV_LINK_LAB_WAITING = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/lab/waiting-list']")
    NAV_LINK_LAB_BLOOD_WAITING = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/lab/blood-waiting-list']")
    NAV_LINK_LAB_DETAILS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/lab/details']")
    NAV_LINK_LAB_BLOOD_STATUS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/lab/blood-bank-status']")
    NAV_LINK_LAB_RESULTS_INQUIRY = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/lab/results-inquiry']")

    # Navbar - Physical Therapy
    NAV_DROPDOWN_PT = (By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'العلاج الطبيعي')]")
    NAV_LINK_PT_WAITING = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/physical-therapy/waiting-list']")

    # Navbar - Patient Accounts
    NAV_DROPDOWN_PATIENT_ACCOUNTS = (By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'حسابات المرضى')]")
    NAV_LINK_UNREGISTERED_INVOICES = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/patient-accounts/unregistered-invoices']")
    NAV_LINK_REGISTERED_INVOICES = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/patient-accounts/registered-invoices']")
    NAV_LINK_PATIENT_CHECKUPS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/patient-accounts/patient-checkups']")
    NAV_LINK_PATIENT_SETTLEMENTS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/patient-accounts/patient-settlements']")
    NAV_LINK_TECHNICIAN_BANK = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/patient-accounts/technician-bank']")
    NAV_LINK_MERGE_PATIENTS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/patient-accounts/merge-patients']")

    # Navbar - Emergency (الإسعاف والطوارئ)
    NAV_DROPDOWN_EMERGENCY = (By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'الإسعاف والطوارئ')]")
    NAV_LINK_EMERGENCY_WAITING = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/emergency/waiting-list']")
    NAV_LINK_EMERGENCY_EDIT_VISIT = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/emergency/edit-visit']")
    NAV_LINK_EMERGENCY_ADM_DISCH = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/emergency/admission-discharge-report']")
    NAV_LINK_EMERGENCY_MED_REPORTS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/emergency/medical-reports']")
    NAV_LINK_EMERGENCY_BED_OCCUPANCY = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/emergency/bed-occupancy']")
    NAV_LINK_EMERGENCY_CANCEL_LEAVED = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/emergency/cancel-leaved']")

    # Navbar - Clinics (العيادات الخارجية)
    NAV_DROPDOWN_CLINICS = (By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'العيادات الخارجية')]")
    NAV_LINK_CLINIC_WAITING = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/clinic/waiting-list']")
    NAV_LINK_CLINIC_DETAILS_REPORT = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/clinic/visit-details-report']")
    NAV_LINK_CLINIC_PATIENTS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/clinic/patients']")
    NAV_LINK_CLINIC_EDIT_VISIT = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/clinic/edit-visit']")
    NAV_LINK_CLINIC_CANCEL_LEAVED = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/clinic/cancel-leaved-visit']")
    NAV_LINK_CLINIC_MED_REPORTS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/clinic/medical-reports']")

    # Navbar - Nursing (سكرتارية التمريض)
    NAV_DROPDOWN_NURSING = (By.XPATH, "//div[contains(@class, 'nav-dropdown')]//button[contains(., 'سكرتارية التمريض')]")
    NAV_LINK_NURSING_ROOMS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/waiting-list/accomodation-rooms']")
    NAV_LINK_NURSING_ICU = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/waiting-list/icu']")
    NAV_LINK_NURSING_NEONATAL = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/waiting-list/neonatal']")
    NAV_LINK_NURSING_PATIENT_DIETS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/waiting-list/patient-diets-list']")
    NAV_LINK_NURSING_ATTENDANT_DIETS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/waiting-list/attendant-diets']")
    NAV_LINK_NURSING_MED_REPORTS = (By.XPATH, "//div[contains(@class, 'dropdown-menu')]//a[@href='/waiting-list/medical-reports']")

    # Quick Access Cards
    CARD_PATIENT_FILE = (By.XPATH, "//*[contains(@class, 'action-card') and .//h3[contains(text(), 'ملف مريض')]]")
    CARD_CLINIC_PATIENTS = (By.XPATH, "//*[contains(@class, 'action-card') and .//h3[contains(text(), 'المرضى بالعيادات')]]")
    CARD_EMERGENCY_PATIENTS = (By.XPATH, "//*[contains(@class, 'action-card') and .//h3[contains(text(), 'المرضى بالطوارئ')]]")

    def open(self) -> "HomePage":
        logger.info(f"Opening Home dashboard: {self.URL}")
        self.driver.get(self.URL)
        self.is_loaded()
        return self

    def is_loaded(self) -> bool:
        """Verifies dashboard is displayed."""
        return self.is_visible(self.TXT_WELCOME_HEADER, timeout=10)

    def get_welcome_title(self) -> str:
        """Returns the welcome greeting text, e.g. 'مساء الخير، Ma3n Administrator'."""
        return self.get_text(self.TXT_WELCOME_HEADER)

    def open_reception(self) -> None:
        """Navigates to the Patient File / Reception page."""
        logger.info("Navigating to Reception / Patient File...")
        # Check if Quick Access card is directly visible
        if self.is_visible(self.CARD_PATIENT_FILE, timeout=3):
            logger.info("Clicking Quick Access card: ملف مريض")
            self.click(self.CARD_PATIENT_FILE)
        else:
            logger.info("Opening via navbar: مكتب الدخول -> الملف الطبى")
            self.click(self.NAV_DROPDOWN_ADMISSION)
            self.click(self.NAV_LINK_RECEPTION)
        self.wait_for_url_contains("/reception", timeout=10)

    def open_occupancy_report(self) -> None:
        """Navigates to Hospital Occupancy Report (/reception/occupancy-report)."""
        logger.info("Navigating to Occupancy Report via navbar: مكتب الدخول -> تقرير إشغال المستشفى...")
        self.click(self.NAV_DROPDOWN_ADMISSION)
        self.click(self.NAV_LINK_OCCUPANCY)
        self.wait_for_url_contains("/reception/occupancy-report", timeout=15)

    def open_admission_discharge_report(self) -> None:
        """Navigates to Admission & Discharge Report (/reception/admission-discharge-report)."""
        logger.info("Navigating to Admission & Discharge Report via navbar: مكتب الدخول -> تقرير الدخول والخروج...")
        self.click(self.NAV_DROPDOWN_ADMISSION)
        self.click(self.NAV_LINK_ADMISSION_DISCHARGE)
        self.wait_for_url_contains("/reception/admission-discharge-report", timeout=15)

    def open_surgery_booking(self) -> None:
        """Navigates to Surgery Booking (/reception/surgery-booking)."""
        logger.info("Navigating to Surgery Booking via navbar: مكتب الدخول -> حجز العمليات...")
        self.click(self.NAV_DROPDOWN_ADMISSION)
        self.click(self.NAV_LINK_SURGERY_BOOKING)
        self.wait_for_url_contains("/reception/surgery-booking", timeout=15)

    def open_leaving_requests(self) -> None:
        """Navigates to Inpatients Pending Discharge (/waiting-list/leaving-requests)."""
        logger.info("Navigating to Leaving Requests via navbar: مكتب الدخول -> المرضى الداخلي قيد الخروج...")
        self.click(self.NAV_DROPDOWN_ADMISSION)
        self.click(self.NAV_LINK_LEAVING_REQUESTS)
        self.wait_for_url_contains("/waiting-list/leaving-requests", timeout=15)

    def open_accountant_leaving_requests(self) -> None:
        """Navigates to Patient Discharge Requests (/accountant/leaving-requests)."""
        logger.info("Navigating to Accountant Leaving Requests via navbar: مكتب الدخول -> طلبات خروج المرضى...")
        self.click(self.NAV_DROPDOWN_ADMISSION)
        self.click(self.NAV_LINK_ACCOUNTANT_LEAVING)
        self.wait_for_url_contains("/accountant/leaving-requests", timeout=15)

    def open_emergency_transfers(self) -> None:
        """Navigates to Emergency Transfers (/reception/emergency-transfers)."""
        logger.info("Navigating to Emergency Transfers via navbar: مكتب الدخول -> طلبات تحويل المرضى من الطوارئ...")
        self.click(self.NAV_DROPDOWN_ADMISSION)
        self.click(self.NAV_LINK_EMERGENCY_TRANSFERS)
        self.wait_for_url_contains("/reception/emergency-transfers", timeout=15)

    def open_leaving_approval_report(self) -> None:
        """Navigates to Leaving Approval Report (/reception/leaving-approval-report)."""
        logger.info("Navigating to Leaving Approval Report via navbar: مكتب الدخول -> تقرير تأكيد طلبات المغادرة...")
        self.click(self.NAV_DROPDOWN_ADMISSION)
        self.click(self.NAV_LINK_LEAVING_APPROVAL_REPORT)
        self.wait_for_url_contains("/reception/leaving-approval-report", timeout=15)

    def open_clinic_waiting_list(self) -> None:
        """Navigates to Clinic Waiting List."""
        logger.info("Navigating to Clinic Waiting List...")
        self.click(self.NAV_DROPDOWN_CLINIC)
        self.click(self.NAV_LINK_CLINIC_WAITING)
        self.wait_for_url_contains("/clinic/waiting-list", timeout=10)

    def open_price_lists(self) -> None:
        """Navigates to InfoDesk Price Lists."""
        logger.info("Navigating to InfoDesk Price Lists...")
        self.click(self.NAV_DROPDOWN_INFODESK)
        self.click(self.NAV_LINK_PRICE_LISTS)
        self.wait_for_url_contains("/info-desk/price-lists", timeout=10)

    def open_shift_managers(self) -> None:
        """Navigates to Shift Managers."""
        logger.info("Navigating to Shift Managers...")
        self.click(self.NAV_DROPDOWN_INFODESK)
        self.click(self.NAV_LINK_SHIFT_MANAGERS)
        self.wait_for_url_contains("/info-desk/shift-managers", timeout=10)

    def open_surgery_names(self) -> None:
        """Navigates to Surgery Names."""
        logger.info("Navigating to Surgery Names...")
        self.click(self.NAV_DROPDOWN_INFODESK)
        self.click(self.NAV_LINK_SURGERY_NAMES)
        self.wait_for_url_contains("/info-desk/surgery-names", timeout=10)

    def open_surgery_prices(self) -> None:
        """Navigates to Surgery Prices."""
        logger.info("Navigating to Surgery Prices...")
        self.click(self.NAV_DROPDOWN_INFODESK)
        self.click(self.NAV_LINK_SURGERY_PRICES)
        self.wait_for_url_contains("/info-desk/surgery-prices", timeout=10)

    def open_surgery_agenda(self) -> None:
        """Navigates to Surgery Agenda."""
        logger.info("Navigating to Surgery Agenda...")
        self.click(self.NAV_DROPDOWN_INFODESK)
        self.click(self.NAV_LINK_SURGERY_AGENDA)
        self.wait_for_url_contains("/info-desk/surgery-agenda", timeout=10)

    def open_clinic_agenda(self) -> None:
        """Navigates to Clinic Agenda."""
        logger.info("Navigating to Clinic Agenda...")
        self.click(self.NAV_DROPDOWN_INFODESK)
        self.click(self.NAV_LINK_CLINIC_AGENDA)
        self.wait_for_url_contains("/info-desk/clinic-agenda", timeout=10)

    def open_phone_book(self) -> None:
        """Navigates to Phone Book."""
        logger.info("Navigating to Phone Book...")
        self.click(self.NAV_DROPDOWN_INFODESK)
        self.click(self.NAV_LINK_PHONE_BOOK)
        self.wait_for_url_contains("/info-desk/phone-book", timeout=10)

    def open_surgery_waiting(self) -> None:
        """Navigates to Surgery Waiting List."""
        logger.info("Navigating to Surgery Waiting List...")
        self.click(self.NAV_DROPDOWN_INFODESK)
        self.click(self.NAV_LINK_SURGERY_WAITING)
        self.wait_for_url_contains("/info-desk/surgeries", timeout=10)

    def open_packages(self) -> None:
        """Navigates to Packages inquiry."""
        logger.info("Navigating to Packages...")
        self.click(self.NAV_DROPDOWN_INFODESK)
        self.click(self.NAV_LINK_PACKAGES)
        self.wait_for_url_contains("/info-desk/packages", timeout=10)

    def open_emergency_waiting_list(self) -> None:
        """Navigates to Emergency Waiting List."""
        logger.info("Navigating to Emergency Waiting List...")
        if self.is_visible(self.CARD_EMERGENCY_PATIENTS, timeout=3):
            self.click(self.CARD_EMERGENCY_PATIENTS)
        else:
            self.driver.get("https://196.218.246.250:4040/emergency/waiting-list")
        self.wait_for_url_contains("/emergency/waiting-list", timeout=10)

    def open_inpatients_rooms(self) -> None:
        """Navigates to Inpatients in Rooms (/reception/inpatients)."""
        logger.info("Navigating to Inpatients Rooms via navbar: المرضى المقيمين -> المرضى بالغرف...")
        self.click(self.NAV_DROPDOWN_RESIDENTS)
        self.click(self.NAV_LINK_INPATIENTS)
        self.wait_for_url_contains("/reception/inpatients", timeout=10)

    def open_icu(self) -> None:
        """Navigates to ICU Inpatients (/reception/icu)."""
        logger.info("Navigating to ICU via navbar: المرضى المقيمين -> المرضى بالرعاية المركزة...")
        self.click(self.NAV_DROPDOWN_RESIDENTS)
        self.click(self.NAV_LINK_ICU)
        self.wait_for_url_contains("/reception/icu", timeout=10)

    def open_neonatal(self) -> None:
        """Navigates to Neonatal Inpatients (/reception/neonatal)."""
        logger.info("Navigating to Neonatal via navbar: المرضى المقيمين -> المرضى بالحضانة...")
        self.click(self.NAV_DROPDOWN_RESIDENTS)
        self.click(self.NAV_LINK_NEONATAL)
        self.wait_for_url_contains("/reception/neonatal", timeout=10)

    def open_attendants(self) -> None:
        """Navigates to Patient Attendants (/reception/attendants)."""
        logger.info("Navigating to Attendants via navbar: المرضى المقيمين -> مرافقو المرضى...")
        self.click(self.NAV_DROPDOWN_RESIDENTS)
        self.click(self.NAV_LINK_ATTENDANTS)
        self.wait_for_url_contains("/reception/attendants", timeout=10)

    def open_room_management(self) -> None:
        """Navigates to Room Management (/reception/room-management)."""
        logger.info("Navigating to Room Management via navbar: المرضى المقيمين -> إدارة الغرف...")
        self.click(self.NAV_DROPDOWN_RESIDENTS)
        self.click(self.NAV_LINK_ROOM_MANAGEMENT)
        self.wait_for_url_contains("/reception/room-management", timeout=10)

    def open_room_map(self) -> None:
        """Navigates to Room Occupancy Map (/reception/rooms)."""
        logger.info("Navigating to Room Map via navbar: المرضى المقيمين -> إشغال الغرف (خريطة)...")
        self.click(self.NAV_DROPDOWN_RESIDENTS)
        self.click(self.NAV_LINK_ROOM_MAP)
        self.wait_for_url_contains("/reception/rooms", timeout=10)

    def open_rays_waiting(self) -> None:
        """Navigates to Rays Waiting List (/rays/waiting-list)."""
        logger.info("Navigating to Rays Waiting List via navbar: الأشعة -> قائمة انتظار الأشعة...")
        self.click(self.NAV_DROPDOWN_RAYS)
        self.click(self.NAV_LINK_RAYS_WAITING)
        self.wait_for_url_contains("/rays/waiting-list", timeout=10)

    def open_rays_status(self) -> None:
        """Navigates to Rays Status (/rays/status)."""
        logger.info("Navigating to Rays Status via navbar: الأشعة -> موقف تنفيذ حالات الأشعة وطباعة الاستيكر...")
        self.click(self.NAV_DROPDOWN_RAYS)
        self.click(self.NAV_LINK_RAYS_STATUS)
        self.wait_for_url_contains("/rays/status", timeout=10)

    def open_rays_details(self) -> None:
        """Navigates to Rays Details Report (/rays/details)."""
        logger.info("Navigating to Rays Details via navbar: الأشعة -> تقرير تفصيلي بالأشعة...")
        self.click(self.NAV_DROPDOWN_RAYS)
        self.click(self.NAV_LINK_RAYS_DETAILS)
        self.wait_for_url_contains("/rays/details", timeout=10)

    def open_lab_waiting(self) -> None:
        """Navigates to Lab Waiting List (/lab/waiting-list)."""
        logger.info("Navigating to Lab Waiting List via navbar: المعمل وبنك الدم -> قائمة انتظار التحاليل...")
        self.click(self.NAV_DROPDOWN_LAB)
        self.click(self.NAV_LINK_LAB_WAITING)
        self.wait_for_url_contains("/lab/waiting-list", timeout=10)

    def open_lab_blood_waiting(self) -> None:
        """Navigates to Blood Bank Waiting List (/lab/blood-waiting-list)."""
        logger.info("Navigating to Blood Waiting List via navbar: المعمل وبنك الدم -> قائمة انتظار بنك الدم...")
        self.click(self.NAV_DROPDOWN_LAB)
        self.click(self.NAV_LINK_LAB_BLOOD_WAITING)
        self.wait_for_url_contains("/lab/blood-waiting-list", timeout=10)

    def open_lab_details(self) -> None:
        """Navigates to Lab Detailed Report (/lab/details)."""
        logger.info("Navigating to Lab Details via navbar: المعمل وبنك الدم -> تقرير بالتحاليل التفصيلي...")
        self.click(self.NAV_DROPDOWN_LAB)
        self.click(self.NAV_LINK_LAB_DETAILS)
        self.wait_for_url_contains("/lab/details", timeout=10)

    def open_lab_blood_status(self) -> None:
        """Navigates to Blood Bank Status (/lab/blood-bank-status)."""
        logger.info("Navigating to Blood Bank Status via navbar: المعمل وبنك الدم -> استعلام عن بنك الدم...")
        self.click(self.NAV_DROPDOWN_LAB)
        self.click(self.NAV_LINK_LAB_BLOOD_STATUS)
        self.wait_for_url_contains("/lab/blood-bank-status", timeout=10)

    def open_lab_results_inquiry(self) -> None:
        """Navigates to Lab Results Inquiry (/lab/results-inquiry)."""
        logger.info("Navigating to Lab Results Inquiry via navbar: المعمل وبنك الدم -> استعلام عن نتائج التحاليل...")
        self.click(self.NAV_DROPDOWN_LAB)
        self.click(self.NAV_LINK_LAB_RESULTS_INQUIRY)
        self.wait_for_url_contains("/lab/results-inquiry", timeout=10)

    def open_inpatients(self) -> None:
        """Navigates to Inpatients list."""
        logger.info("Navigating to Inpatients...")
        self.driver.get("https://196.218.246.250:4040/reception/inpatients")
        self.wait_for_url_contains("/reception/inpatients", timeout=10)

    def open_registered_invoices(self) -> None:
        """Navigates to Registered Patient Invoices."""
        logger.info("Navigating to Registered Invoices via navbar: حسابات المرضى -> فواتير المرضى...")
        self.click(self.NAV_DROPDOWN_PATIENT_ACCOUNTS)
        self.click(self.NAV_LINK_REGISTERED_INVOICES)
        self.wait_for_url_contains("/patient-accounts/registered-invoices", timeout=10)

    # Physical Therapy Navigation
    def open_pt_waiting_list(self) -> None:
        """Navigates to Physical Therapy Waiting List (/physical-therapy/waiting-list)."""
        logger.info("Navigating to Physical Therapy Waiting List via navbar: العلاج الطبيعي -> قائمة انتظار العلاج الطبيعي...")
        self.click(self.NAV_DROPDOWN_PT)
        self.click(self.NAV_LINK_PT_WAITING)
        self.wait_for_url_contains("/physical-therapy/waiting-list", timeout=10)

    # Patient Accounts Navigation
    def open_unregistered_invoices(self) -> None:
        """Navigates to Unregistered Invoices (/patient-accounts/unregistered-invoices)."""
        logger.info("Navigating to Unregistered Invoices via navbar: حسابات المرضى -> كشوف الحساب المفتوحة...")
        self.click(self.NAV_DROPDOWN_PATIENT_ACCOUNTS)
        self.click(self.NAV_LINK_UNREGISTERED_INVOICES)
        self.wait_for_url_contains("/patient-accounts/unregistered-invoices", timeout=10)

    def open_patient_checkups(self) -> None:
        """Navigates to Patient Checkups / Inpatient Accounts (/patient-accounts/patient-checkups)."""
        logger.info("Navigating to Patient Checkups via navbar: حسابات المرضى -> حسابات المرضى الداخلي...")
        self.click(self.NAV_DROPDOWN_PATIENT_ACCOUNTS)
        self.click(self.NAV_LINK_PATIENT_CHECKUPS)
        self.wait_for_url_contains("/patient-accounts/patient-checkups", timeout=10)

    def open_patient_settlements(self) -> None:
        """Navigates to Patient Settlements / Debts (/patient-accounts/patient-settlements)."""
        logger.info("Navigating to Patient Settlements via navbar: حسابات المرضى -> مديونيات المرضى...")
        self.click(self.NAV_DROPDOWN_PATIENT_ACCOUNTS)
        self.click(self.NAV_LINK_PATIENT_SETTLEMENTS)
        self.wait_for_url_contains("/patient-accounts/patient-settlements", timeout=10)

    def open_technician_bank(self) -> None:
        """Navigates to Technician Bank (/patient-accounts/technician-bank)."""
        logger.info("Navigating to Technician Bank via navbar: حسابات المرضى -> بنك الفنيين...")
        self.click(self.NAV_DROPDOWN_PATIENT_ACCOUNTS)
        self.click(self.NAV_LINK_TECHNICIAN_BANK)
        self.wait_for_url_contains("/patient-accounts/technician-bank", timeout=10)

    def open_merge_patients(self) -> None:
        """Navigates to Merge Patients (/patient-accounts/merge-patients)."""
        logger.info("Navigating to Merge Patients via navbar: حسابات المرضى -> دمج بين المرضى...")
        self.click(self.NAV_DROPDOWN_PATIENT_ACCOUNTS)
        self.click(self.NAV_LINK_MERGE_PATIENTS)
        self.wait_for_url_contains("/patient-accounts/merge-patients", timeout=10)

    # Emergency Navigation (الإسعاف والطوارئ)
    def open_emergency_waiting(self) -> None:
        """Navigates to Emergency Waiting List (/emergency/waiting-list)."""
        logger.info("Navigating to Emergency Waiting List: الإسعاف والطوارئ -> المرضى بالطوارئ...")
        self.click(self.NAV_DROPDOWN_EMERGENCY)
        self.click(self.NAV_LINK_EMERGENCY_WAITING)
        self.wait_for_url_contains("/emergency/waiting-list", timeout=10)

    def open_emergency_edit_visit(self) -> None:
        """Navigates to Edit Emergency Visit (/emergency/edit-visit)."""
        logger.info("Navigating to Edit Emergency Visit: الإسعاف والطوارئ -> تعديل زيارة بالطوارئ...")
        self.click(self.NAV_DROPDOWN_EMERGENCY)
        self.click(self.NAV_LINK_EMERGENCY_EDIT_VISIT)
        self.wait_for_url_contains("/emergency/edit-visit", timeout=10)

    def open_emergency_adm_disch(self) -> None:
        """Navigates to Emergency Admission & Discharge (/emergency/admission-discharge-report)."""
        logger.info("Navigating to Emergency Admission/Discharge: الإسعاف والطوارئ -> تقرير الدخول والخروج بالطوارئ...")
        self.click(self.NAV_DROPDOWN_EMERGENCY)
        self.click(self.NAV_LINK_EMERGENCY_ADM_DISCH)
        self.wait_for_url_contains("/emergency/admission-discharge-report", timeout=10)

    def open_emergency_med_reports(self) -> None:
        """Navigates to Emergency Medical Reports (/emergency/medical-reports)."""
        logger.info("Navigating to Emergency Medical Reports: الإسعاف والطوارئ -> التقارير الطبية للإسعاف والطوارئ...")
        self.click(self.NAV_DROPDOWN_EMERGENCY)
        self.click(self.NAV_LINK_EMERGENCY_MED_REPORTS)
        self.wait_for_url_contains("/emergency/medical-reports", timeout=10)

    def open_emergency_bed_occupancy(self) -> None:
        """Navigates to Emergency Bed Occupancy (/emergency/bed-occupancy)."""
        logger.info("Navigating to Emergency Bed Occupancy: الإسعاف والطوارئ -> تقرير اشغال أسرة الطوارئ...")
        self.click(self.NAV_DROPDOWN_EMERGENCY)
        self.click(self.NAV_LINK_EMERGENCY_BED_OCCUPANCY)
        self.wait_for_url_contains("/emergency/bed-occupancy", timeout=10)

    def open_emergency_cancel_leaved(self) -> None:
        """Navigates to Cancel Leaved Emergency Patient (/emergency/cancel-leaved)."""
        logger.info("Navigating to Cancel Leaved Emergency: الإسعاف والطوارئ -> إلغاء خروج مريض طوارئ تم إغلاقها...")
        self.click(self.NAV_DROPDOWN_EMERGENCY)
        self.click(self.NAV_LINK_EMERGENCY_CANCEL_LEAVED)
        self.wait_for_url_contains("/emergency/cancel-leaved", timeout=10)

    # Clinics Navigation (العيادات الخارجية)
    def open_clinic_waiting(self) -> None:
        """Navigates to Clinic Waiting List (/clinic/waiting-list)."""
        logger.info("Navigating to Clinic Waiting List: العيادات الخارجية -> قائمة انتظار العيادات...")
        self.click(self.NAV_DROPDOWN_CLINICS)
        self.click(self.NAV_LINK_CLINIC_WAITING)
        self.wait_for_url_contains("/clinic/waiting-list", timeout=10)

    def open_clinic_details_report(self) -> None:
        """Navigates to Detailed Clinic Report (/clinic/visit-details-report)."""
        logger.info("Navigating to Detailed Clinic Report: العيادات الخارجية -> تقرير العيادات التفصيلي...")
        self.click(self.NAV_DROPDOWN_CLINICS)
        self.click(self.NAV_LINK_CLINIC_DETAILS_REPORT)
        self.wait_for_url_contains("/clinic/visit-details-report", timeout=10)

    def open_clinic_patients(self) -> None:
        """Navigates to Patients in Clinics (/clinic/patients)."""
        logger.info("Navigating to Patients in Clinics: العيادات الخارجية -> المرضى بالعيادات...")
        self.click(self.NAV_DROPDOWN_CLINICS)
        self.click(self.NAV_LINK_CLINIC_PATIENTS)
        self.wait_for_url_contains("/clinic/patients", timeout=10)

    def open_clinic_edit_visit(self) -> None:
        """Navigates to Edit Clinic Visit (/clinic/edit-visit)."""
        logger.info("Navigating to Edit Clinic Visit: العيادات الخارجية -> تعديل زيارة عيادات...")
        self.click(self.NAV_DROPDOWN_CLINICS)
        self.click(self.NAV_LINK_CLINIC_EDIT_VISIT)
        self.wait_for_url_contains("/clinic/edit-visit", timeout=10)

    def open_clinic_cancel_leaved(self) -> None:
        """Navigates to Cancel Leaved Clinic Patient (/clinic/cancel-leaved-visit)."""
        logger.info("Navigating to Cancel Leaved Clinic Patient: العيادات الخارجية -> إلغاء خروج مريض عيادات مُغلقة...")
        self.click(self.NAV_DROPDOWN_CLINICS)
        self.click(self.NAV_LINK_CLINIC_CANCEL_LEAVED)
        self.wait_for_url_contains("/clinic/cancel-leaved-visit", timeout=10)

    def open_clinic_med_reports(self) -> None:
        """Navigates to Clinic Medical Reports (/clinic/medical-reports)."""
        logger.info("Navigating to Clinic Medical Reports: العيادات الخارجية -> التقارير الطبية للعيادات الخارجية...")
        self.click(self.NAV_DROPDOWN_CLINICS)
        self.click(self.NAV_LINK_CLINIC_MED_REPORTS)
        self.wait_for_url_contains("/clinic/medical-reports", timeout=10)

    # Nursing Navigation (سكرتارية التمريض)
    def open_nursing_rooms(self) -> None:
        """Navigates to Nursing Inpatients in Rooms (/waiting-list/accomodation-rooms)."""
        logger.info("Navigating to Nursing Inpatients: سكرتارية التمريض -> المرضى بالغرف...")
        self.click(self.NAV_DROPDOWN_NURSING)
        self.click(self.NAV_LINK_NURSING_ROOMS)
        self.wait_for_url_contains("/waiting-list/accomodation-rooms", timeout=10)

    def open_nursing_icu(self) -> None:
        """Navigates to Nursing ICU Patients (/waiting-list/icu)."""
        logger.info("Navigating to Nursing ICU: سكرتارية التمريض -> المرضى بالرعاية المركزة...")
        self.click(self.NAV_DROPDOWN_NURSING)
        self.click(self.NAV_LINK_NURSING_ICU)
        self.wait_for_url_contains("/waiting-list/icu", timeout=10)

    def open_nursing_neonatal(self) -> None:
        """Navigates to Nursing Neonatal Patients (/waiting-list/neonatal)."""
        logger.info("Navigating to Nursing Neonatal: سكرتارية التمريض -> المرضى بالحضانة...")
        self.click(self.NAV_DROPDOWN_NURSING)
        self.click(self.NAV_LINK_NURSING_NEONATAL)
        self.wait_for_url_contains("/waiting-list/neonatal", timeout=10)

    def open_nursing_patient_diets(self) -> None:
        """Navigates to Patient Diets List (/waiting-list/patient-diets-list)."""
        logger.info("Navigating to Patient Diets: سكرتارية التمريض -> قائمة طلبات الأنظمة الغذائية للمرضي...")
        self.click(self.NAV_DROPDOWN_NURSING)
        self.click(self.NAV_LINK_NURSING_PATIENT_DIETS)
        self.wait_for_url_contains("/waiting-list/patient-diets-list", timeout=10)

    def open_nursing_attendant_diets(self) -> None:
        """Navigates to Attendant Diets List (/waiting-list/attendant-diets)."""
        logger.info("Navigating to Attendant Diets: سكرتارية التمريض -> قائمة طلبات الأنظمة الغذائية للمرافقين...")
        self.click(self.NAV_DROPDOWN_NURSING)
        self.click(self.NAV_LINK_NURSING_ATTENDANT_DIETS)
        self.wait_for_url_contains("/waiting-list/attendant-diets", timeout=10)

    def open_nursing_med_reports(self) -> None:
        """Navigates to Inpatient Medical Reports (/waiting-list/medical-reports)."""
        logger.info("Navigating to Inpatient Medical Reports: سكرتارية التمريض -> التقارير الطبية للمرضى الداخلي...")
        self.click(self.NAV_DROPDOWN_NURSING)
        self.click(self.NAV_LINK_NURSING_MED_REPORTS)
        self.wait_for_url_contains("/waiting-list/medical-reports", timeout=10)

