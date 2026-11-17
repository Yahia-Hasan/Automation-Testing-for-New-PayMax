"""
Download the largest chunks and search for ANY string that looks like an API path.
Also get the full app-config.js to understand the base URL pattern.
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

# Get app-config.js fully
resp = session.get(f"{BASE}/app-config.js")
print("=== app-config.js FULL ===")
print(resp.text)
print("=== END ===\n")

# Download the biggest chunks and search for path-like strings
big_chunks = [
    "chunk-YTEK4G3D.js",   # 82KB - biggest
    "chunk-EBZSYVFJ.js",   # 39KB
    "chunk-UMLWSN6Z.js",   # 35KB
    "chunk-56LNTWH5.js",   # 33KB
    "chunk-TYM6UAD4.js",   # 29KB
    "chunk-A6RFFTQ5.js",   # 28KB
    "chunk-YTHKGATR.js",   # 27KB
    "chunk-B5VFHRW4.js",   # 22KB
    "chunk-A77Q2IVI.js",   # 21KB
    "chunk-BSB5NIWT.js",   # 20KB
    "chunk-RQAEDMEV.js",   # 20KB
    "chunk-Y5ZNO3TQ.js",   # 19KB
    "chunk-AXU4MXJK.js",   # 19KB
    "chunk-ZLX3QALP.js",   # 14KB
    "chunk-WYUS65OR.js",   # 13KB
]

all_api_paths = set()

for chunk in big_chunks:
    url = f"{BASE}/{chunk}"
    resp = session.get(url, timeout=30)
    content = resp.text
    print(f"\n{'─' * 60}")
    print(f"Analyzing {chunk} ({len(content)/1024:.0f}KB)")
    print(f"{'─' * 60}")
    
    # Search strategies:
    # 1. Look for quoted strings that contain path-like segments (words with slashes)
    # Common patterns in minified Angular:
    #   - `${this.apiUrl}/reception/patients/search`
    #   - this.apiUrl+"/reception/patients"
    #   - "/reception/patients/search"
    
    # Find ALL quoted strings that contain forward slashes
    # and look like URL paths (not CSS/HTML)
    path_strings = re.findall(r'["\']([a-zA-Z][a-zA-Z0-9\-_/]*(?:/[a-zA-Z0-9\-_{}]+)+)["\']', content)
    
    # Filter for likely API paths (multi-segment, not CSS selectors)
    api_like = set()
    for p in path_strings:
        # Skip obvious non-API paths
        if any(skip in p.lower() for skip in ['assets/', 'node_modules', '.css', '.html', '.js', '.svg', '.png', 'font', 'icon']):
            continue
        segments = p.split("/")
        if len(segments) >= 2 and all(s.isidentifier() or s.startswith("{") or "-" in s for s in segments if s):
            api_like.add(p)
    
    # Also try: look for string concatenation with "apiUrl" nearby
    # Find all strings within 100 chars of 'apiUrl' or 'http' mentions  
    apiUrl_contexts = [m.start() for m in re.finditer(r'apiUrl|baseUrl|apiBase', content)]
    for pos in apiUrl_contexts:
        # Get surrounding context
        window = content[max(0, pos-50):pos+200]
        # Find quoted strings in this window
        local_strings = re.findall(r'["\'/]([a-zA-Z\-_]+(?:/[a-zA-Z\-_{}]+)*)["\'/]', window)
        for s in local_strings:
            if "/" in s and len(s) > 3:
                api_like.add(s)
    
    # Also try: backtick template literals
    templates = re.findall(r'`([^`]*)`', content)
    for t in templates:
        if '/' in t and ('apiUrl' in t or len(t.split('/')) >= 2):
            # Extract the path part
            path_parts = re.findall(r'/([a-zA-Z][a-zA-Z0-9\-_/{}$]+)', t)
            for pp in path_parts:
                if len(pp) > 3:
                    api_like.add(pp)
    
    if api_like:
        print(f"  Found {len(api_like)} potential API paths:")
        for p in sorted(api_like):
            print(f"    📡 {p}")
        all_api_paths.update(api_like)

# Also check the main JS
resp = session.get(f"{BASE}/main-ZR7YYZSI.js")
content = resp.text
print(f"\n{'─' * 60}")
print(f"Analyzing main-ZR7YYZSI.js ({len(content)/1024:.0f}KB)")
print(f"{'─' * 60}")

path_strings = re.findall(r'["\']([a-zA-Z][a-zA-Z0-9\-_/]*(?:/[a-zA-Z0-9\-_{}]+)+)["\']', content)
for p in path_strings:
    if not any(skip in p.lower() for skip in ['assets/', 'node_modules', '.css', '.html', '.svg', '.js', '.png', 'font', 'icon', 'chunk']):
        segments = p.split("/")
        if len(segments) >= 2:
            all_api_paths.add(p)
            print(f"    📡 {p}")

# Summary
print(f"\n{'=' * 80}")
print(f"ALL DISCOVERED PATHS: {len(all_api_paths)}")
print(f"{'=' * 80}")
for p in sorted(all_api_paths):
    print(f"  {p}")

with open("scratch/all_paths_from_js.json", "w", encoding="utf-8") as f:
    json.dump(sorted(list(all_api_paths)), f, ensure_ascii=False, indent=2)
