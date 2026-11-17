"""
Systematic deep probe: expand every known working controller 
with common sub-paths to map the complete API surface.
"""
import sys, os, json
sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import urllib3
urllib3.disable_warnings()

from config import Config
from client.api_client import BayMaxApiClient

client = BayMaxApiClient(Config.BASE_URL)
client.login(Config.USERNAME, Config.PASSWORD)

# ============================================================
# Known working base controllers + new ones from JS analysis
# ============================================================
probe_map = {
    # AUTH module - known working
    "auth": [
        "/api/auth/me",
        "/api/auth/auto-login",
        "/api/auth/session-debug",
        "/api/auth/computers",
        "/api/auth/accessible-forms",
        "/api/auth/authorize",
        "/api/auth/permissions",
        "/api/auth/roles",
        "/api/auth/users",
    ],
    # RECEPTION module - known working
    "reception": [
        "/api/reception/patients/search?query=a",
        "/api/reception/patients/30855",
        "/api/reception/patients/30855/visits",
        "/api/reception/patients/30855/documents",
        "/api/reception/patients/30855/history",
        "/api/reception/nationalities",
        "/api/reception/companies",
        "/api/reception/branches",
        "/api/reception/doctors",
        "/api/reception/specialties",
        "/api/reception/lookups",
        "/api/reception/surgery-booking",
        "/api/reception/surgery-bookings",
    ],
    # CLINIC module - known working
    "clinic": [
        "/api/clinic/visits?date=2026-10-17",
        "/api/clinic/specialties",
        "/api/clinic/doctors",
        "/api/clinic/waiting-list",
        "/api/clinic/visits/draft",
        "/api/clinic/lookups",
        "/api/clinic/services",
    ],
    # EMERGENCY module - known working
    "emergency": [
        "/api/emergency/waiting-list",
        "/api/emergency/cases",
        "/api/emergency/lookups",
        "/api/emergency/services",
        "/api/emergency/doctors",
    ],
    # INVOICE module - known working
    "invoice-details": [
        "/api/invoice-details/12746",
        "/api/invoice-details/lookups",
    ],
    # ACCOUNTANT module - known working
    "accountant": [
        "/api/accountant/reservations/open",
        "/api/accountant/leaving-requests",
        "/api/accountant/leaving-approval",
        "/api/accountant/invoices",
        "/api/accountant/registered-invoices",
        "/api/accountant/unregistered-invoices",
        "/api/accountant/payments",
        "/api/accountant/lookups",
    ],
    # DASHBOARDS module - known working
    "dashboards": [
        "/api/dashboards/audit",
        "/api/dashboards/stats",
        "/api/dashboards/statistics",
        "/api/dashboards/occupancy",
    ],
    # NEW: From JS analysis - waitinglist
    "waitinglist": [
        "/api/waitinglist",
        "/api/waitinglist/accommodation-rooms",
        "/api/waitinglist/icu",
        "/api/waitinglist/neonatal",
        "/api/waitinglist/patient-diets-list",
        "/api/waitinglist/attendant-diets",
        "/api/waitinglist/medical-reports",
        "/api/waitinglist/leaving-requests",
        "/api/waitinglist/leaving-approval",
        "/api/waitinglist/ipd-services",
        "/api/waitinglist/ipd-tests",
        "/api/waitinglist/lookups",
    ],
    # NEW: From JS analysis - lookups/services/stats
    "lookups": [
        "/api/lookups",
        "/api/lookups/nationalities",
        "/api/lookups/companies",
        "/api/lookups/specialties",
        "/api/lookups/doctors",
        "/api/lookups/departments",
        "/api/lookups/rooms",
        "/api/lookups/beds",
        "/api/lookups/services",
        "/api/lookups/service-groups",
        "/api/lookups/treasuries",
    ],
    "treasury-lookups": [
        "/api/treasury-lookups",
    ],
    "services": [
        "/api/services",
        "/api/services-by-groups",
    ],
    "stats": [
        "/api/stats",
        "/api/stats/dashboard",
        "/api/stats/occupancy",
    ],
    # More controllers to try
    "inpatient": [
        "/api/inpatient",
        "/api/inpatient/admissions",
        "/api/inpatient/clinical-care",
        "/api/inpatient/services",
        "/api/inpatient/medications",
        "/api/inpatient/labs",
        "/api/inpatient/rays",
        "/api/inpatient/lookups",
    ],
    "patient-services": [
        "/api/patient-services",
        "/api/patient-services/services",
        "/api/patient-services/labs",
        "/api/patient-services/rays",
        "/api/patient-services/medications",
    ],
    "patient-accounts": [
        "/api/patient-accounts",
        "/api/patient-accounts/invoices",
        "/api/patient-accounts/payments",
        "/api/patient-accounts/services",
        "/api/patient-accounts/lookups",
    ],
    "physical-therapy": [
        "/api/physical-therapy/waiting-list",
        "/api/physical-therapy/sessions",
        "/api/physical-therapy/lookups",
    ],
    "surgery": [
        "/api/surgery",
        "/api/surgery/bookings",
        "/api/surgery/names",
        "/api/surgery/prices",
        "/api/surgery/schedule",
        "/api/surgery/lookups",
    ],
    "lab": [
        "/api/lab",
        "/api/lab/requests",
        "/api/lab/results",
        "/api/lab/pending",
        "/api/lab/lookups",
    ],
    "rays": [
        "/api/rays",
        "/api/rays/requests",
        "/api/rays/results",
        "/api/rays/pending",
        "/api/rays/lookups",
    ],
    "nursing": [
        "/api/nursing",
        "/api/nursing/waiting-list",
        "/api/nursing/accommodation",
        "/api/nursing/icu",
        "/api/nursing/lookups",
    ],
    "pricelists": [
        "/api/pricelists",
        "/api/pricelists/services",
        "/api/pricelists/groups",
    ],
}

# Execute probes
print("=" * 80)
print("SYSTEMATIC API ENDPOINT DEEP PROBE")
print(f"Base: {Config.BASE_URL}")
print("=" * 80)

live_endpoints = []
error_endpoints = []
not_found_endpoints = []

for module, paths in probe_map.items():
    print(f"\n{'─' * 60}")
    print(f"MODULE: {module}")
    print(f"{'─' * 60}")
    
    for path in paths:
        try:
            resp = client.get(path)
            status = resp.status_code
            size = len(resp.content)
            
            if status == 200:
                # Describe the data
                desc = f"{size}B"
                try:
                    j = resp.json()
                    if isinstance(j, list):
                        desc = f"Array[{len(j)}]"
                    elif isinstance(j, dict):
                        keys = list(j.keys())[:4]
                        desc = f"Object({keys})"
                except:
                    pass
                print(f"  ✅ {path}  →  200 ({desc})")
                live_endpoints.append({"path": path, "status": 200, "desc": desc})
            elif status in [400, 401, 403, 405, 500]:
                # Endpoint EXISTS but has issues
                error_msg = ""
                try:
                    error_msg = resp.json().get("title", resp.text[:100])
                except:
                    error_msg = resp.text[:100]
                print(f"  🔶 {path}  →  {status} ({error_msg[:60]})")
                error_endpoints.append({"path": path, "status": status, "msg": error_msg[:200]})
            else:
                not_found_endpoints.append(path)
        except Exception as e:
            print(f"  ❌ {path}  →  ERROR: {str(e)[:60]}")

# Summary
print(f"\n{'=' * 80}")
print("PROBE RESULTS SUMMARY")
print(f"{'=' * 80}")
print(f"  ✅ LIVE (200):        {len(live_endpoints)} endpoints")
print(f"  🔶 EXIST (4xx/5xx):   {len(error_endpoints)} endpoints")
print(f"  ⚠️  NOT FOUND (404):  {len(not_found_endpoints)} endpoints")

print(f"\n{'─' * 60}")
print("ALL LIVE ENDPOINTS (200 OK):")
print(f"{'─' * 60}")
for ep in live_endpoints:
    print(f"  ✅ {ep['path']}  ({ep['desc']})")

print(f"\n{'─' * 60}")
print("EXISTING BUT ERRORING ENDPOINTS (require params or POST):")
print(f"{'─' * 60}")
for ep in error_endpoints:
    print(f"  🔶 [{ep['status']}] {ep['path']}")

# Save complete results
with open("scratch/deep_probe_results.json", "w", encoding="utf-8") as f:
    json.dump({
        "live": live_endpoints,
        "erroring": error_endpoints,
        "not_found": not_found_endpoints,
    }, f, ensure_ascii=False, indent=2)

print(f"\nResults saved to scratch/deep_probe_results.json")
