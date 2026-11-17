"""
Final approach: Download ALL chunk files, search for apiUrl references,
and extract the actual API endpoint paths used in HTTP calls.
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

# Get main JS and find ALL chunk files
resp = session.get(f"{BASE}/main-ZR7YYZSI.js")
main_js = resp.text

# Find chunk references
chunk_refs = set(re.findall(r'"\./(chunk-[A-Z0-9a-z]+\.js)"', main_js))
print(f"Found {len(chunk_refs)} chunk references")

# Download all chunks
all_content = {}
for chunk in sorted(chunk_refs):
    resp = session.get(f"{BASE}/{chunk}", timeout=15)
    if resp.status_code == 200 and len(resp.text) > 50:
        all_content[chunk] = resp.text

all_content["main-ZR7YYZSI.js"] = main_js
print(f"Downloaded {len(all_content)} files total")

# Search for apiUrl contexts in ALL files
print(f"\n{'=' * 80}")
print("SEARCHING FOR apiUrl CONTEXTS (actual API paths)")
print(f"{'=' * 80}")

all_api_paths = set()

for fname, content in sorted(all_content.items()):
    # Find all positions of 'apiUrl' 
    positions = [m.start() for m in re.finditer(r'apiUrl', content)]
    
    if not positions:
        continue
    
    print(f"\n📄 {fname} — {len(positions)} apiUrl references")
    
    for pos in positions:
        # Get a generous window around apiUrl
        window = content[pos:pos+300]
        
        # Extract paths from template literals: `${...apiUrl}/path/here`
        template_paths = re.findall(r'`[^`]*?(/[a-zA-Z][a-zA-Z0-9\-_/${}]*(?:/[a-zA-Z0-9\-_/${}]+)*)', window)
        for p in template_paths:
            # Clean ${} vars
            clean = re.sub(r'\$\{[^}]*\}', '{id}', p)
            if len(clean) > 2:
                all_api_paths.add(clean)
                print(f"  📡 TEMPLATE: {clean}")
        
        # Extract from string concatenation: apiUrl+"/path" or apiUrl,"/path"
        concat_paths = re.findall(r'[+,]\s*["\'](/[a-zA-Z][a-zA-Z0-9\-_/]*)["\']', window)
        for p in concat_paths:
            all_api_paths.add(p)
            print(f"  📡 CONCAT: {p}")
        
        # Extract from full template: `${x.apiUrl}/reception/patients/${id}`
        full_template = re.findall(r'`\$\{[^}]+\}(/[^`]+)`', window)
        for p in full_template:
            clean = re.sub(r'\$\{[^}]*\}', '{id}', p)
            all_api_paths.add(clean)
            print(f"  📡 FULL_TEMPLATE: {clean}")

# Also search for patterns like: this.e.get(`${this.e.apiUrl}/some/path`)
# In minified form: this.x.get(`${this.x.apiUrl}/some/path`)
for fname, content in sorted(all_content.items()):
    # Minified: .get(`${VAR.apiUrl}/path`) or .post(`${VAR.apiUrl}/path`)
    http_templates = re.findall(r'\.(?:get|post|put|delete|patch)\(`\$\{[^}]+\.apiUrl\}(/[^`]+)`', content)
    for p in http_templates:
        clean = re.sub(r'\$\{[^}]*\}', '{id}', p)
        if clean not in all_api_paths:
            all_api_paths.add(clean)
            print(f"  📡 HTTP_CALL in {fname}: {clean}")

# Final summary
print(f"\n{'=' * 80}")
print(f"COMPLETE API PATH MAP: {len(all_api_paths)} unique paths")
print(f"{'=' * 80}")

# Group by first segment
module_map = {}
for p in sorted(all_api_paths):
    segments = [s for s in p.split('/') if s and s != '{id}']
    if segments:
        module = segments[0]
        if module not in module_map:
            module_map[module] = []
        module_map[module].append(p)

for module, paths in sorted(module_map.items()):
    print(f"\n  📦 {module}:")
    for p in sorted(paths):
        print(f"    {p}")

# Save
with open("scratch/final_api_paths.json", "w", encoding="utf-8") as f:
    json.dump({
        "total": len(all_api_paths),
        "paths": sorted(list(all_api_paths)),
        "by_module": {k: sorted(v) for k, v in module_map.items()}
    }, f, ensure_ascii=False, indent=2)

print(f"\nSaved to scratch/final_api_paths.json")
