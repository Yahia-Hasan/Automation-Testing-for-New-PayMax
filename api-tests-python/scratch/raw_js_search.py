"""
Raw content search: look for template literals containing API paths.
Angular HttpClient calls use template strings like `${this.apiUrl}/path/to/endpoint`
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

# Get all chunk files
resp = session.get(f"{BASE}/main-ZR7YYZSI.js")
main_js = resp.text
chunk_refs = re.findall(r'"(\./chunk-[A-Z0-9]+\.js)"', main_js)
print(f"Found {len(chunk_refs)} chunks")

all_api_paths = set()
all_files = [("main-ZR7YYZSI.js", main_js)]

for chunk_ref in chunk_refs:
    chunk_name = chunk_ref.lstrip("./")
    resp = session.get(f"{BASE}/{chunk_name}", timeout=15)
    if resp.status_code == 200:
        all_files.append((chunk_name, resp.text))

print(f"Total files to analyze: {len(all_files)}")

for fname, content in all_files:
    # Strategy: find ALL backtick template literals and extract paths
    # In minified JS, template literals are preserved
    backtick_strings = re.findall(r'`([^`]+)`', content)
    
    for bt in backtick_strings:
        # Look for paths containing forward slashes after a ${ expression
        # Pattern: ${...}/some/path/here or ${...}/some-path
        path_after_var = re.findall(r'\$\{[^}]+\}(/[a-zA-Z][a-zA-Z0-9\-_/{}$]*)', bt)
        for p in path_after_var:
            # Clean: remove ${...} parts
            clean = re.sub(r'\$\{[^}]+\}', '*', p)
            if len(clean) > 2 and '/' in clean:
                all_api_paths.add(p)
    
    # Also search for string concatenation patterns like:
    # t.apiUrl+"/reception/patients" 
    # or .apiUrl,"/reception/patients"
    concat_matches = re.findall(r'apiUrl[^"]*"(/[a-zA-Z][a-zA-Z0-9\-_/{}]*)"', content)
    for m in concat_matches:
        all_api_paths.add(m)
    
    # Also check for .get( .post( .put( .delete( patterns with string URLs
    http_calls = re.findall(r'\.(?:get|post|put|delete|patch)\([^)]*"(/[a-zA-Z][a-zA-Z0-9\-_/{}]*)"', content)
    for m in http_calls:
        all_api_paths.add(m)

# Filter and clean
filtered = set()
for p in all_api_paths:
    # Skip obvious non-API
    if any(skip in p.lower() for skip in ['.css', '.html', '.js', '.svg', '.png', 'assets/', 'font', 'node_modules']):
        continue
    # Must have at least one meaningful segment
    segments = [s for s in p.split('/') if s and not s.startswith('$')]
    if len(segments) >= 1:
        filtered.add(p)

print(f"\n{'=' * 80}")
print(f"API PATHS EXTRACTED FROM TEMPLATE LITERALS: {len(filtered)}")
print(f"{'=' * 80}")
for p in sorted(filtered):
    print(f"  📡 {p}")

# Now let's try the ultimate approach: search for ALL strings > 5 chars containing "/" 
# in the largest chunk
print(f"\n{'=' * 80}")
print("EXHAUSTIVE STRING SEARCH in chunk-YTEK4G3D.js (82KB)")
print(f"{'=' * 80}")

for fname, content in all_files:
    if "YTEK4G3D" in fname:
        # Find ALL quoted strings
        all_strings = re.findall(r'"([^"]{5,200})"', content)
        all_strings += re.findall(r"'([^']{5,200})'", content)
        
        path_like = [s for s in all_strings if '/' in s and not s.startswith('http') 
                     and not any(skip in s for skip in ['.css', '.html', '.svg', '.png', 'font', 
                                                         'node_modules', '\\n', '\\t', '<', '>', 
                                                         'xmlns', 'w3.org', 'schemas'])]
        print(f"  Path-like strings found: {len(path_like)}")
        for s in sorted(set(path_like)):
            print(f"    {s}")

# Also search all files for "reception" "clinic" "emergency" "accountant"
# to understand the path naming convention
print(f"\n{'=' * 80}")
print("SEARCHING FOR KNOWN MODULE NAMES IN ALL JS")
print(f"{'=' * 80}")

keywords = ["reception", "clinic", "emergency", "accountant", "inpatient", 
            "waiting-list", "invoice", "patient-accounts", "surgery", "physical-therapy",
            "nursing", "laboratory", "radiology", "pharmacy"]

for keyword in keywords:
    found_in = []
    for fname, content in all_files:
        if keyword in content.lower():
            # Find context around the keyword
            positions = [m.start() for m in re.finditer(re.escape(keyword), content, re.IGNORECASE)]
            contexts = []
            for pos in positions[:3]:
                ctx = content[max(0,pos-30):pos+80]
                ctx = ctx.replace('\n', ' ').strip()
                contexts.append(ctx)
            found_in.append((fname, len(positions), contexts))
    
    if found_in:
        print(f"\n  🔍 '{keyword}' found in:")
        for fname, count, contexts in found_in:
            print(f"    {fname} ({count} occurrences)")
            for ctx in contexts[:2]:
                print(f"      ...{ctx[:120]}...")

with open("scratch/template_literal_paths.json", "w", encoding="utf-8") as f:
    json.dump(sorted(list(filtered)), f, ensure_ascii=False, indent=2)
