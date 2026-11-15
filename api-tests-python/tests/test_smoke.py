import pytest
import requests
from datetime import date
from config import Config
from client.api_client import BayMaxApiClient

def extract_list_or_data(response_json):
    """Safely extracts a list or object from either wrapped {'data': ...} or direct json."""
    if isinstance(response_json, dict):
        return response_json.get("data", response_json)
    return response_json

class TestSmokeSuite:
    """
    Suggested Smoke Test suite from the BayMax Patients API test guide:
    1. POST /api/auth/login
    2. GET /api/auth/me
    3. GET /api/reception/patients/search?query=...
    4. GET /api/reception/patients/{patientCode}
    5. GET /api/clinic/visits?date=YYYY-MM-DD
    6. GET /api/clinic/visits/{visitCode}/services-page (treasuries must not be [])
    7. GET /api/emergency/waiting-list
    8. GET /api/invoice-details/{reservationId}
    9. GET /api/dashboards/audit
    """

    discovered_patient_code = Config.PATIENT_CODE
    discovered_visit_code = Config.VISIT_CODE
    discovered_reservation_id = Config.RESERVATION_ID

    def test_01_login(self, api_client: BayMaxApiClient):
        """Step 1: Test Login endpoint and verify Bearer token is returned."""
        try:
            response = api_client.login(username=Config.USERNAME, password=Config.PASSWORD)
        except requests.ConnectionError:
            pytest.fail(f"Connection failed: BayMax API server is not reachable at {Config.BASE_URL}.")

        assert response.status_code == 200, f"Login failed with status {response.status_code}: {response.text}"
        
        data = response.json()
        token = data.get("data", {}).get("token") or data.get("token")
        assert token, "Login succeeded but token is missing in response body."

    def test_02_get_me(self, auth_client: BayMaxApiClient):
        """Step 2: Test /api/auth/me and verify active session properties."""
        response = auth_client.get("/api/auth/me")
        assert response.status_code == 200, f"Get /api/auth/me failed: {response.text}"
        
        session_data = extract_list_or_data(response.json())
        assert "userId" in session_data or "userName" in session_data, "Session missing user identity."

    def test_03_patient_search(self, auth_client: BayMaxApiClient):
        """Step 3: Test patient search and extract sample patientCode."""
        response = auth_client.get("/api/reception/patients/search", params={"query": "ا"})
        assert response.status_code == 200, f"Patient search failed: {response.text}"
        
        patients = extract_list_or_data(response.json())
        if isinstance(patients, list) and len(patients) > 0:
            first_patient = patients[0]
            TestSmokeSuite.discovered_patient_code = str(first_patient.get("patientCode") or first_patient.get("code") or "")

    def test_04_patient_details(self, auth_client: BayMaxApiClient):
        """Step 4: Test getting patient details using discovered or configured patientCode."""
        patient_code = TestSmokeSuite.discovered_patient_code or Config.PATIENT_CODE
        if not patient_code:
            pytest.skip("No patientCode available for details lookup.")
            
        response = auth_client.get(f"/api/reception/patients/{patient_code}")
        assert response.status_code == 200, f"Get patient details failed for code {patient_code}: {response.text}"

    def test_05_clinic_visits(self, auth_client: BayMaxApiClient):
        """Step 5: Test GET /api/clinic/visits with current date."""
        today_str = date.today().strftime("%Y-%m-%d")
        response = auth_client.get("/api/clinic/visits", params={"date": today_str})
        assert response.status_code == 200, f"Get clinic visits failed: {response.text}"
        
        visits = extract_list_or_data(response.json())
        if isinstance(visits, list) and len(visits) > 0:
            first_visit = visits[0]
            TestSmokeSuite.discovered_visit_code = str(first_visit.get("visitCode") or first_visit.get("code") or "")
        elif TestSmokeSuite.discovered_patient_code:
            # Fallback: check discovered patient's historical visits
            pv_res = auth_client.get(f"/api/reception/patients/{TestSmokeSuite.discovered_patient_code}/visits")
            if pv_res.status_code == 200:
                p_visits = extract_list_or_data(pv_res.json())
                if isinstance(p_visits, list) and len(p_visits) > 0:
                    TestSmokeSuite.discovered_visit_code = str(p_visits[0].get("visitCode") or "")

    def test_06_clinic_services_page(self, auth_client: BayMaxApiClient):
        """Step 6: Test services-page and verify treasuries list is not empty."""
        visit_code = TestSmokeSuite.discovered_visit_code or Config.VISIT_CODE
        if not visit_code:
            pytest.skip("No visitCode available to test services page.")

        response = auth_client.get(f"/api/clinic/visits/{visit_code}/services-page")
        assert response.status_code == 200, f"Get services page failed for visit {visit_code}: {response.text}"
        
        page_data = extract_list_or_data(response.json())
        treasuries = page_data.get("treasuries")
        assert treasuries is not None, "Key 'treasuries' is missing from services-page DTO."
        assert len(treasuries) > 0, "Treasuries list must not be empty (as highlighted in test guide)."

    def test_07_emergency_waiting_list(self, auth_client: BayMaxApiClient):
        """Step 7: Test emergency waiting list endpoint."""
        response = auth_client.get("/api/emergency/waiting-list")
        assert response.status_code == 200, f"Emergency waiting list failed: {response.text}"

    def test_08_invoice_details(self, auth_client: BayMaxApiClient):
        """Step 8: Test inpatient invoice details for a reservation."""
        reservation_id = TestSmokeSuite.discovered_reservation_id or Config.RESERVATION_ID
        if not reservation_id:
            res = auth_client.get("/api/accountant/reservations/open")
            if res.status_code == 200:
                res_data = extract_list_or_data(res.json())
                if isinstance(res_data, list) and len(res_data) > 0:
                    reservation_id = str(res_data[0].get("reservationId") or res_data[0].get("id") or "")
                    TestSmokeSuite.discovered_reservation_id = reservation_id

        if not reservation_id:
            pytest.skip("No reservationId available to test invoice details.")

        response = auth_client.get(f"/api/invoice-details/{reservation_id}")
        assert response.status_code == 200, f"Get invoice details failed for reservation {reservation_id}: {response.text}"

    def test_09_dashboards_audit(self, auth_client: BayMaxApiClient):
        """Step 9: Test dashboards audit endpoint (may require privilege)."""
        response = auth_client.get("/api/dashboards/audit")
        assert response.status_code in [200, 403], f"Unexpected status code for audit dashboard: {response.status_code} - {response.text}"
