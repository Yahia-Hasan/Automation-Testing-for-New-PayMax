"""
Network Interceptor: Navigate key BayMax screens via Selenium and capture
all XHR/fetch API calls made by the Angular frontend.
This reveals the REAL API endpoint paths.
"""
import sys, os, json, time
sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_login import BayMaxSeleniumAuth

# Setup Chrome with performance logging to capture network calls
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(options=chrome_options)

BASE = "https://196.218.246.250:4040"
API_BASE = "Patients-Modern-BE"

# Login first
print("Logging in...")
auth = BayMaxSeleniumAuth(headless=True)
login_result = auth.perform_full_login("sysadmin", "Ma3an2025")
token = login_result.get("token")
cookies = login_result.get("cookies", [])
auth.close()

# Set up authenticated session in new driver
driver.get(f"{BASE}/reception")
time.sleep(1)

# Add auth token via localStorage/cookie
driver.execute_script(f"""
    localStorage.setItem('token', '{token}');
    localStorage.setItem('jwt', '{token}');
""")
for cookie in cookies:
    try:
        driver.add_cookie(cookie)
    except:
        pass

# Pages to visit
pages = [
    ("/reception", "Reception"),
    ("/reception/patient/30855", "Patient Details"),
    ("/clinic/waiting", "Clinic Waiting"),
    ("/clinic/visits/draft?patientCode=30855&clientId=52&mode=opd", "OPD Draft Visit"),
    ("/emergency/waiting-list", "Emergency Waiting"),
    ("/waiting-list/accommodation-rooms", "Nursing - Accommodation"),
    ("/waiting-list/icu", "Nursing - ICU"),
    ("/waiting-list/medical-reports", "Nursing - Medical Reports"),
    ("/patient-accounts/invoice-details?rid=12746", "Invoice Details"),
    ("/inpatient/clinical-care?reservToken=CfDJ8KcUxlP3wTpIkfqEIRtHon7zSAyPB2lIYbCHCWrqBp7K4jkMTKXk5axOsUN82puPKlT-g3kDxq_2u17f2Nbo30AlOJpkeRYjWxGWxs0ataq_nI5P2Hkl9_cnHr5BBTAPOQ", "Clinical Care"),
    ("/physical-therapy/waiting-list", "Physical Therapy"),
    ("/accountant/leaving-requests", "Leaving Requests"),
    ("/surgery/bookings", "Surgery Bookings"),
]

all_api_calls = {}

for path, label in pages:
    url = f"{BASE}{path}"
    print(f"\n{'─' * 60}")
    print(f"Navigating: {label} → {url}")
    print(f"{'─' * 60}")
    
    try:
        driver.get(url)
        time.sleep(3)  # wait for all API calls to complete
        
        # Extract network logs
        logs = driver.get_log("performance")
        api_calls = set()
        
        for entry in logs:
            try:
                log_data = json.loads(entry["message"])
                msg = log_data.get("message", {})
                method = msg.get("method", "")
                
                if method == "Network.requestWillBeSent":
                    params = msg.get("params", {})
                    request = params.get("request", {})
                    req_url = request.get("url", "")
                    req_method = request.get("method", "GET")
                    
                    # Filter only API calls
                    if API_BASE in req_url and "/api/" in req_url:
                        # Extract the API path
                        api_path = req_url.split(API_BASE)[1] if API_BASE in req_url else req_url
                        # Remove query string for grouping
                        clean_path = api_path.split("?")[0]
                        query = api_path.split("?")[1] if "?" in api_path else ""
                        
                        call_key = f"{req_method} {clean_path}"
                        api_calls.add(call_key)
                        
                        full_info = f"{req_method} {api_path}"
                        if label not in all_api_calls:
                            all_api_calls[label] = []
                        if full_info not in all_api_calls[label]:
                            all_api_calls[label].append(full_info)
                            
            except Exception:
                pass
        
        for call in sorted(api_calls):
            print(f"  📡 {call}")
            
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")

driver.quit()

# Summary
print("\n" + "=" * 80)
print("COMPLETE API ENDPOINT MAP (from live network interception)")
print("=" * 80)

# Collect unique endpoints
unique_endpoints = set()
for label, calls in all_api_calls.items():
    for call in calls:
        method_path = call.split("?")[0]
        unique_endpoints.add(method_path)

# Group by module
module_map = {}
for ep in sorted(unique_endpoints):
    parts = ep.split("/api/")
    if len(parts) > 1:
        api_part = parts[1]
        module = api_part.split("/")[0]
        if module not in module_map:
            module_map[module] = []
        module_map[module].append(ep)

for module, eps in sorted(module_map.items()):
    print(f"\n  📦 {module}:")
    for ep in sorted(eps):
        print(f"    {ep}")

# Save results
with open("scratch/intercepted_api_map.json", "w", encoding="utf-8") as f:
    json.dump({
        "by_page": all_api_calls,
        "unique_endpoints": sorted(list(unique_endpoints)),
        "by_module": {k: sorted(v) for k, v in module_map.items()}
    }, f, ensure_ascii=False, indent=2)

print(f"\nTotal unique API endpoints discovered: {len(unique_endpoints)}")
print("Results saved to scratch/intercepted_api_map.json")
