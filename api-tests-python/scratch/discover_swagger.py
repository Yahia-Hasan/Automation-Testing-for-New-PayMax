"""
Deep probe: try swagger and common API discovery endpoints to find the real route map.
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

# Try swagger endpoints
swagger_paths = [
    "/swagger/v1/swagger.json",
    "/swagger/index.html",
    "/swagger",
    "/api-docs",
    "/openapi.json",
    "/api/swagger.json",
]

print("=" * 80)
print("SWAGGER / API DOCS DISCOVERY")
print("=" * 80)

swagger_json = None
for path in swagger_paths:
    try:
        resp = client.get(path)
        print(f"  {path}  →  {resp.status_code} ({len(resp.content)}B)")
        if resp.status_code == 200 and len(resp.content) > 500:
            try:
                swagger_json = resp.json()
                print(f"    → Got JSON with {len(swagger_json)} top-level keys")
            except:
                print(f"    → Not JSON, likely HTML ({resp.content[:100]})")
    except Exception as e:
        print(f"  {path}  →  ERROR: {e}")

# If we got swagger JSON, extract all paths
if swagger_json and "paths" in swagger_json:
    paths = swagger_json["paths"]
    print(f"\n{'=' * 80}")
    print(f"DISCOVERED {len(paths)} API PATHS FROM SWAGGER")
    print(f"{'=' * 80}")
    
    # Group by module prefix
    modules = {}
    for path, methods in paths.items():
        parts = path.strip("/").split("/")
        if len(parts) >= 3:
            module_key = parts[1]  # e.g. /api/MODULE/...
        elif len(parts) >= 2:
            module_key = parts[1]
        else:
            module_key = "root"
        
        if module_key not in modules:
            modules[module_key] = []
        
        for method in methods.keys():
            modules[module_key].append({"method": method.upper(), "path": path})
    
    for module_name, endpoints in sorted(modules.items()):
        print(f"\n  📦 {module_name} ({len(endpoints)} endpoints):")
        for ep in endpoints[:10]:  # show first 10
            print(f"    {ep['method']:6s} {ep['path']}")
        if len(endpoints) > 10:
            print(f"    ... and {len(endpoints) - 10} more")
    
    # Save full swagger
    with open("scratch/swagger_full.json", "w", encoding="utf-8") as f:
        json.dump(swagger_json, f, ensure_ascii=False, indent=2)
    print(f"\nFull swagger saved to scratch/swagger_full.json")
    
    # Save module summary
    module_summary = {k: [ep for ep in v] for k, v in modules.items()}
    with open("scratch/api_modules_from_swagger.json", "w", encoding="utf-8") as f:
        json.dump(module_summary, f, ensure_ascii=False, indent=2)
    print(f"Module summary saved to scratch/api_modules_from_swagger.json")
else:
    print("\nSwagger JSON not available. Trying alternative discovery...")
    
    # Try probing more specific paths based on what we know from the UI
    print("\n" + "=" * 80)
    print("ALTERNATIVE: Probing paths based on known UI patterns")
    print("=" * 80)
    
    alt_paths = [
        # Inpatient patterns (from UI route /waiting-list/*)
        "/api/WaitingList/accommodation-rooms",
        "/api/WaitingList/icu",
        "/api/WaitingList/neonatal",
        "/api/WaitingList/patient-diets-list",
        "/api/WaitingList/attendant-diets",
        "/api/WaitingList/medical-reports",
        # Patient services
        "/api/PatientServices/services",
        "/api/PatientServices/labs",
        "/api/PatientServices/rays",
        # Reception patterns  
        "/api/Patient/search?query=a",
        "/api/Patient/30855",
        "/api/Patients/search?query=a",
        # Clinic
        "/api/Visit/list",
        "/api/Visits/list",
        "/api/ClinicVisit/waiting-list",
        # Emergency
        "/api/Emergency/waiting-list",
        "/api/EmergencyCase/waiting-list",
        # Accountant
        "/api/Accountant/leaving-requests",
        "/api/LeavingRequest/list",
        # Invoice
        "/api/Invoice/details/12746",
        "/api/InvoiceDetails/12746",
        "/api/PatientAccount/invoices",
        # Surgery
        "/api/SurgeryBooking/list",
        "/api/Operation/bookings",
    ]
    
    for path in alt_paths:
        try:
            resp = client.get(path)
            icon = "✅" if resp.status_code == 200 else "⚠️" if resp.status_code in [400,404] else "❌"
            size = len(resp.content)
            print(f"  {icon} GET {path}  →  {resp.status_code} ({size}B)")
            if resp.status_code == 200 and size > 10:
                try:
                    j = resp.json()
                    if isinstance(j, list):
                        print(f"      → Array with {len(j)} items")
                    elif isinstance(j, dict):
                        print(f"      → Object keys: {list(j.keys())[:5]}")
                except:
                    pass
        except Exception as e:
            print(f"  ❌ GET {path}  →  ERROR: {str(e)[:60]}")
