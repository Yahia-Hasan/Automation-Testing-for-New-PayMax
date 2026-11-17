import json
import os
import urllib3
from locust import HttpUser, task, between, events
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load cached authentication token from session.json
SESSION_FILE = os.path.join(os.path.dirname(__file__), "session.json")
AUTH_TOKEN = None

if os.path.exists(SESSION_FILE):
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            AUTH_TOKEN = data.get("token")
    except Exception as e:
        print(f"Failed to read session.json: {e}")

class BaseHospitalUser(HttpUser):
    abstract = True
    wait_time = between(1, 2.5)  # Realistic user think-time between operations

    def on_start(self):
        """Set authentication header and disable SSL verification."""
        self.client.verify = False
        if AUTH_TOKEN:
            self.client.headers.update({
                "Authorization": f"Bearer {AUTH_TOKEN}",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json"
            })

class ReceptionStaffUser(BaseHospitalUser):
    """
    Simulates high-traffic Reception Desk staff:
    Searching patients, viewing patient medical files and visit history.
    """
    weight = 40

    @task(3)
    def search_patient_by_query(self):
        query_samples = ["30854", "30855", "30856", "محمد", "أحمد"]
        # Use query parameter with name tag for unified Locust grouping
        self.client.get(
            "/api/reception/patients/search?query=30854",
            name="[Reception] Search Patient (/api/reception/patients/search)"
        )

    @task(2)
    def view_patient_details(self):
        self.client.get(
            "/api/reception/patients/30854",
            name="[Reception] Get Patient Details (/api/reception/patients/{id})"
        )

    @task(1)
    def view_patient_visits(self):
        self.client.get(
            "/api/reception/patients/30854/visits",
            name="[Reception] Get Patient Visits (/api/reception/patients/{id}/visits)"
        )


class ClinicDoctorUser(BaseHospitalUser):
    """
    Simulates Outpatient Clinic Doctors:
    Checking daily appointments and visiting lists.
    """
    weight = 25

    @task(3)
    def view_clinic_visits_queue(self):
        self.client.get(
            "/api/clinic/visits?date=2026-09-13",
            name="[Clinics] Daily Visits Queue (/api/clinic/visits)"
        )

    @task(1)
    def view_session_info(self):
        self.client.get(
            "/api/auth/me",
            name="[Core] Session Me (/api/auth/me)"
        )


class EmergencyTriageUser(BaseHospitalUser):
    """
    Simulates Emergency Room (ER) Triage Staff:
    High-frequency monitoring of active emergency cases.
    """
    weight = 15

    @task(3)
    def check_emergency_waiting_list(self):
        self.client.get(
            "/api/emergency/waiting-list",
            name="[Emergency] Waiting List Queue (/api/emergency/waiting-list)"
        )


class AccountantBillingUser(BaseHospitalUser):
    """
    Simulates Inpatient Billing Accountants:
    Accessing open accounts and rendering complex invoice calculations.
    """
    weight = 20

    @task(2)
    def view_open_reservations(self):
        self.client.get(
            "/api/accountant/reservations/open",
            name="[Billing] Open Accounts List (/api/accountant/reservations/open)"
        )

    @task(2)
    def view_regular_invoice_details(self):
        self.client.get(
            "/api/invoice-details/12746",
            name="[Billing] Open Invoice Calculation (/api/invoice-details/12746)"
        )

    @task(1)
    def view_registered_invoice_details(self):
        self.client.get(
            "/api/invoice-details/12744",
            name="[Billing] Registered Invoice Summary (/api/invoice-details/12744)"
        )
