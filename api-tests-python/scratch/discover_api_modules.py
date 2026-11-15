"""
Discover all available API modules and their key endpoints on the live BayMax server.
Probes critical financial, clinical, and administrative endpoints to map what's available.
"""
import sys, os
sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import json
import urllib3
urllib3.disable_warnings()

from config import Config
from client.api_client import BayMaxApiClient

client = BayMaxApiClient(Config.BASE_URL)
client.login(Config.USERNAME, Config.PASSWORD)

# ============================================================
# Module Discovery: probe key endpoints per module
# ============================================================
modules_to_probe = {
    "Auth": [
        ("GET", "/api/auth/me"),
        ("GET", "/api/auth/session-debug"),
        ("GET", "/api/auth/computers"),
    ],
    "Reception": [
        ("GET", "/api/reception/patients/search?query=a"),
        ("GET", "/api/reception/patients/30855"),
        ("GET", "/api/reception/nationalities"),
        ("GET", "/api/reception/companies"),
        ("GET", "/api/reception/branches"),
    ],
    "Clinic (OPD)": [
        ("GET", "/api/clinic/visits?date=2026-10-17"),
        ("GET", "/api/clinic/specialties"),
        ("GET", "/api/clinic/doctors"),
        ("GET", "/api/clinic/waiting-list"),
    ],
    "Emergency": [
        ("GET", "/api/emergency/waiting-list"),
        ("GET", "/api/emergency/cases"),
    ],
    "Inpatient / Admission": [
        ("GET", "/api/inpatient/departments"),
        ("GET", "/api/inpatient/rooms"),
        ("GET", "/api/inpatient/beds"),
        ("GET", "/api/inpatient/waiting-list"),
        ("GET", "/api/inpatient/admissions"),
    ],
    "Patient Accounts / Invoices": [
        ("GET", "/api/patient-accounts/invoices"),
        ("GET", "/api/patient-accounts/invoice-details?rid=12746"),
        ("GET", "/api/invoice-details/12746"),
        ("GET", "/api/patient-accounts/services"),
        ("GET", "/api/patient-accounts/payments"),
    ],
    "Accountant": [
        ("GET", "/api/accountant/reservations/open"),
        ("GET", "/api/accountant/leaving-requests"),
        ("GET", "/api/accountant/leaving-approval"),
    ],
    "Nursing": [
        ("GET", "/api/nursing/waiting-list"),
        ("GET", "/api/nursing/accommodation-rooms"),
        ("GET", "/api/nursing/icu"),
        ("GET", "/api/nursing/medical-reports"),
    ],
    "Lab": [
        ("GET", "/api/lab/requests"),
        ("GET", "/api/lab/results"),
        ("GET", "/api/lab/pending"),
    ],
    "Radiology (Rays)": [
        ("GET", "/api/rays/requests"),
        ("GET", "/api/rays/results"),
        ("GET", "/api/rays/pending"),
    ],
    "Pharmacy / Medications": [
        ("GET", "/api/pharmacy/medications"),
        ("GET", "/api/pharmacy/dispensing"),
        ("GET", "/api/medications/list"),
    ],
    "Surgery / Operations": [
        ("GET", "/api/surgery/bookings"),
        ("GET", "/api/surgery/schedule"),
        ("GET", "/api/operations/bookings"),
    ],
    "Physical Therapy": [
        ("GET", "/api/physical-therapy/waiting-list"),
        ("GET", "/api/physical-therapy/sessions"),
    ],
    "Dashboards / Audit": [
        ("GET", "/api/dashboards/audit"),
        ("GET", "/api/dashboards/statistics"),
        ("GET", "/api/dashboards/occupancy"),
    ],
    "Price Lists / Services": [
        ("GET", "/api/pricelists"),
        ("GET", "/api/services/categories"),
        ("GET", "/api/services/list"),
    ],
    "Blood Bank": [
        ("GET", "/api/blood-bank/requests"),
        ("GET", "/api/blood-bank/inventory"),
    ],
    "Treasuries / Cashier": [
        ("GET", "/api/treasuries"),
        ("GET", "/api/treasuries/transactions"),
    ],
}

print("=" * 80)
print("BayMax API Module Discovery Report")
print(f"Base URL: {Config.BASE_URL}")
print("=" * 80)

results = {}
for module_name, endpoints in modules_to_probe.items():
    print(f"\n{'─' * 60}")
    print(f"MODULE: {module_name}")
    print(f"{'─' * 60}")
    module_results = []
    for method, endpoint in endpoints:
        try:
            resp = client.get(endpoint) if method == "GET" else client.post(endpoint)
            status = resp.status_code
            # Try to get response size
            body_len = len(resp.content)
            # Check if it has data
            has_data = False
            data_count = "N/A"
            if status == 200:
                try:
                    j = resp.json()
                    if isinstance(j, list):
                        has_data = len(j) > 0
                        data_count = str(len(j))
                    elif isinstance(j, dict):
                        d = j.get("data", j)
                        if isinstance(d, list):
                            has_data = len(d) > 0
                            data_count = str(len(d))
                        else:
                            has_data = True
                            data_count = "object"
                except:
                    pass
            
            status_icon = "✅" if status == 200 else "⚠️" if status in [400, 404] else "❌"
            print(f"  {status_icon} {method} {endpoint}  →  {status} ({body_len}B) [records: {data_count}]")
            module_results.append({
                "method": method,
                "endpoint": endpoint,
                "status": status,
                "body_size": body_len,
                "has_data": has_data,
                "data_count": data_count,
            })
        except Exception as e:
            print(f"  ❌ {method} {endpoint}  →  ERROR: {str(e)[:80]}")
            module_results.append({
                "method": method,
                "endpoint": endpoint,
                "status": "ERROR",
                "error": str(e)[:200],
            })
    results[module_name] = module_results

# Summary
print("\n" + "=" * 80)
print("SUMMARY: Module Availability")
print("=" * 80)
for module_name, module_results in results.items():
    live_count = sum(1 for r in module_results if r.get("status") == 200)
    total = len(module_results)
    status = "🟢 LIVE" if live_count > 0 else "🔴 DOWN/NOT FOUND"
    print(f"  {status} {module_name}: {live_count}/{total} endpoints responding")

# Save to JSON for later use
with open("scratch/api_discovery_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nResults saved to scratch/api_discovery_results.json")
