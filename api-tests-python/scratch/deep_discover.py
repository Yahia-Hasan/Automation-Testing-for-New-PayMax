"""
Deep JS analysis: download main bundle, find lazy-loaded chunks, 
and extract ALL API endpoints from all chunks.
"""
import sys, os, re, json
sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import requests
import urllib3
urllib3.disable_warnings()

BASE = "https://196.218.246.250:4040"
session = requests.Session()
session.verify = False

# Step 1: Get the main page
resp = session.get(BASE)
html = resp.text

# Find all JS references
js_files = re.findall(r'src="([^"]*\.js)"', html)
print(f"Initial JS files from HTML: {js_files}")

# Step 2: Download main JS and find chunk references
all_js_content = {}
for js_file in js_files:
    url = f"{BASE}/{js_file.lstrip('/')}"
    resp = session.get(url, timeout=30)
    if resp.status_code == 200:
        all_js_content[js_file] = resp.text
        print(f"Downloaded {js_file}: {len(resp.text)/1024:.0f}KB")

# Look for chunk patterns in main JS
main_js = all_js_content.get("main-ZR7YYZSI.js", "")

# Find chunk file references - Angular uses patterns like:
# - import("./chunk-XXXX.js")
# - e.u("chunk-XXXX")  
# - lazy loaded module patterns
chunk_patterns = [
    r'"([a-zA-Z0-9_\-]+\-[A-Z0-9]+\.js)"',
    r"'([a-zA-Z0-9_\-]+\-[A-Z0-9]+\.js)'",
    r'"(chunk\-[a-zA-Z0-9]+\.js)"',
    r'"([a-zA-Z0-9_]+\.[a-f0-9]+\.js)"',
]

chunk_files = set()
for pattern in chunk_patterns:
    matches = re.findall(pattern, main_js)
    chunk_files.update(matches)

# Also check for dynamic import patterns like e(1234) -> "1234-HASH.js"
# Angular CLI pattern: number-hash.js
number_chunks = re.findall(r'"(\d+\-[A-Z0-9a-z]+\.js)"', main_js)
chunk_files.update(number_chunks)

# Also find via loadChildren patterns
load_patterns = re.findall(r'loadComponent[^}]*?"([^"]+)"', main_js)
chunk_files.update(load_patterns)

print(f"\nFound {len(chunk_files)} potential chunk files")
for cf in sorted(chunk_files)[:30]:
    print(f"  {cf}")

# Step 3: Download ALL chunk files and search for API endpoints
print(f"\n{'=' * 60}")
print("Downloading and scanning chunks for API endpoints...")
print(f"{'=' * 60}")

all_endpoints = set()
api_pattern = re.compile(r'["\'/](api/[a-zA-Z][a-zA-Z0-9\-_/]+)[\?"\'/]')

# Also scan main JS
for name, content in all_js_content.items():
    matches = api_pattern.findall(content)
    for m in matches:
        all_endpoints.add("/" + m.rstrip("/"))
    # Also look for interpolated patterns
    interp = re.findall(r'`[^`]*(/api/[^`]+)`', content)
    for m in interp:
        all_endpoints.add(m)

for chunk_file in sorted(chunk_files):
    url = f"{BASE}/{chunk_file}"
    try:
        resp = session.get(url, timeout=15)
        if resp.status_code == 200 and len(resp.text) > 100:
            content = resp.text
            print(f"  ✅ {chunk_file} ({len(content)/1024:.0f}KB)")
            
            matches = api_pattern.findall(content)
            for m in matches:
                all_endpoints.add("/" + m.rstrip("/"))
            
            # Template literals
            interp = re.findall(r'`[^`]*(/api/[^`]+)`', content)
            for m in interp:
                all_endpoints.add(m)
            
            # Also look for HttpClient calls with string concat
            # e.g. this.http.get(this.apiUrl + "/something")
            concat_patterns = re.findall(r'["\'](/[a-zA-Z\-]+/[a-zA-Z\-]+)["\']', content)
            # Don't add these as they might be UI routes
            
            all_js_content[chunk_file] = content
        elif resp.status_code == 404:
            pass  # chunk doesn't exist at this path
    except Exception as e:
        pass

# Step 4: Also try to find chunks from known Angular patterns
# Try common numeric chunk names
print(f"\nProbing numeric chunks (0-50)...")
for i in range(51):
    # Try different hash patterns
    for suffix in ["js"]:
        url = f"{BASE}/chunk-{i}.{suffix}"
        try:
            resp = session.get(url, timeout=5)
            if resp.status_code == 200 and len(resp.text) > 100:
                content = resp.text
                print(f"  ✅ chunk-{i}.{suffix} ({len(content)/1024:.0f}KB)")
                matches = api_pattern.findall(content)
                for m in matches:
                    all_endpoints.add("/" + m.rstrip("/"))
        except:
            pass

# Step 5: Check the app-config.js for base URL info
app_config = all_js_content.get("app-config.js", "")
print(f"\napp-config.js content:\n{app_config[:500]}")

# Step 6: Now let's also try to discover by using the pattern we know works
# We know /api/auth/*, /api/reception/*, /api/clinic/*, /api/emergency/* work
# Let's try ALL combinations with common controller names
print(f"\n{'=' * 60}")
print("Brute-force probing common ASP.NET controller endpoints...")
print(f"{'=' * 60}")

from config import Config
from client.api_client import BayMaxApiClient

client = BayMaxApiClient(Config.BASE_URL)
client.login(Config.USERNAME, Config.PASSWORD)

# Common ASP.NET controller names for a hospital ERP
controllers = [
    "auth", "reception", "clinic", "emergency", "inpatient",
    "patient", "patients", "visit", "visits", "admission",
    "bed", "beds", "room", "rooms", "department", "departments",
    "doctor", "doctors", "nurse", "nursing", "lab", "laboratory",
    "radiology", "rays", "pharmacy", "medication", "medications",
    "surgery", "operation", "operations", "diet", "diets",
    "blood", "bloodbank", "physical-therapy", "physiotherapy",
    "invoice", "invoices", "payment", "payments", "account", "accounts",
    "accountant", "cashier", "treasury", "treasuries",
    "service", "services", "pricelist", "pricelists",
    "insurance", "company", "companies", "nationality", "nationalities",
    "dashboard", "dashboards", "report", "reports", "audit",
    "waiting-list", "waitinglist", "accommodation", "icu", "neonatal",
    "transfer", "discharge", "leaving", "booking", "bookings",
    "medical-report", "medical-reports", "patient-service", "patient-services",
    "clinical-care", "clinical", "care",
    "branch", "branches", "computer", "computers", "user", "users",
    "permission", "permissions", "role", "roles",
    "notification", "notifications", "log", "logs",
    "setting", "settings", "config", "configuration",
    "document", "documents", "attachment", "attachments", "upload",
    "search", "lookup", "dropdown", "combo",
    "invoice-details", "patient-accounts",
]

live_endpoints = []
for ctrl in controllers:
    url_path = f"/api/{ctrl}"
    try:
        resp = client.get(url_path)
        if resp.status_code == 200:
            size = len(resp.content)
            try:
                j = resp.json()
                if isinstance(j, list):
                    desc = f"Array[{len(j)}]"
                elif isinstance(j, dict):
                    desc = f"Object({list(j.keys())[:3]})"
                else:
                    desc = str(type(j).__name__)
            except:
                desc = f"{size}B"
            print(f"  ✅ GET {url_path}  →  200 ({desc})")
            live_endpoints.append(url_path)
            all_endpoints.add(url_path)
        elif resp.status_code == 405:
            # Method not allowed = endpoint exists but needs POST/PUT
            print(f"  🔶 GET {url_path}  →  405 (exists, needs different method)")
            live_endpoints.append(url_path + " [405-METHOD]")
            all_endpoints.add(url_path)
        elif resp.status_code in [400, 401, 403, 500]:
            # These indicate the endpoint EXISTS but has issues
            print(f"  🔶 GET {url_path}  →  {resp.status_code} (endpoint exists)")
            live_endpoints.append(url_path + f" [{resp.status_code}]")
            all_endpoints.add(url_path)
    except:
        pass

# Summary
print(f"\n{'=' * 80}")
print(f"FINAL RESULTS: {len(all_endpoints)} unique API paths discovered")
print(f"{'=' * 80}")

module_map = {}
for ep in sorted(all_endpoints):
    parts = ep.lstrip("/").split("/")
    if len(parts) >= 2 and parts[0] == "api":
        module = parts[1]
        if module not in module_map:
            module_map[module] = []
        module_map[module].append(ep)

for module, eps in sorted(module_map.items()):
    print(f"\n  📦 {module} ({len(eps)} endpoints):")
    for ep in sorted(eps):
        print(f"    {ep}")

# Save
with open("scratch/all_discovered_endpoints.json", "w", encoding="utf-8") as f:
    json.dump({
        "total": len(all_endpoints),
        "live_endpoints": live_endpoints,
        "all_endpoints": sorted(list(all_endpoints)),
        "by_module": {k: sorted(v) for k, v in module_map.items()}
    }, f, ensure_ascii=False, indent=2)

print(f"\nSaved to scratch/all_discovered_endpoints.json")
