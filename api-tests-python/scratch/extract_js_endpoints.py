"""
Extract API endpoint paths from the Angular frontend JavaScript bundles.
The compiled Angular app contains all API paths as string literals.
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

# Step 1: Get the main page and find JS bundle files
print("Fetching main page to find JS bundles...")
resp = session.get(BASE)
html = resp.text

# Find all JS file references
js_files = re.findall(r'src="([^"]*\.js)"', html)
print(f"Found {len(js_files)} JS files:")
for f in js_files:
    print(f"  {f}")

# Step 2: Download each JS file and search for API patterns
all_endpoints = set()
api_patterns = [
    # Common Angular HttpClient patterns
    r'["\'](?:/api/[a-zA-Z0-9/_\-{}\?&=]+)["\']',
    r'["\'](?:api/[a-zA-Z0-9/_\-{}\?&=]+)["\']',
    # Template literal patterns
    r'`[^`]*?/api/[^`]*?`',
]

for js_file in js_files:
    url = f"{BASE}/{js_file.lstrip('/')}" if not js_file.startswith("http") else js_file
    print(f"\nDownloading: {js_file} ...")
    try:
        resp = session.get(url, timeout=30)
        if resp.status_code != 200:
            print(f"  ❌ Status {resp.status_code}")
            continue
        
        content = resp.text
        size_kb = len(content) / 1024
        print(f"  Size: {size_kb:.0f} KB")
        
        # Search for API patterns
        found_in_file = set()
        for pattern in api_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # Clean up the match
                clean = match.strip("\"'`")
                if "/api/" in clean:
                    # Normalize
                    api_path = clean
                    if not api_path.startswith("/"):
                        api_path = "/" + api_path
                    found_in_file.add(api_path)
        
        if found_in_file:
            print(f"  Found {len(found_in_file)} API references:")
            for ep in sorted(found_in_file)[:20]:
                print(f"    📡 {ep}")
            if len(found_in_file) > 20:
                print(f"    ... and {len(found_in_file) - 20} more")
        
        all_endpoints.update(found_in_file)
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:80]}")

# Step 3: Group by module
print(f"\n{'=' * 80}")
print(f"TOTAL UNIQUE API ENDPOINTS FOUND IN JS BUNDLES: {len(all_endpoints)}")
print(f"{'=' * 80}")

module_map = {}
for ep in sorted(all_endpoints):
    parts = ep.split("/api/")
    if len(parts) > 1:
        rest = parts[1]
        module = rest.split("/")[0]
        if module not in module_map:
            module_map[module] = []
        module_map[module].append(ep)

for module, eps in sorted(module_map.items()):
    print(f"\n  📦 {module} ({len(eps)} endpoints):")
    for ep in sorted(eps):
        print(f"    {ep}")

# Save
with open("scratch/js_extracted_endpoints.json", "w", encoding="utf-8") as f:
    json.dump({
        "total": len(all_endpoints),
        "all_endpoints": sorted(list(all_endpoints)),
        "by_module": {k: sorted(v) for k, v in module_map.items()}
    }, f, ensure_ascii=False, indent=2)

print(f"\nSaved to scratch/js_extracted_endpoints.json")
