import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load the token
with open("session.json", "r", encoding="utf-8") as f:
    session_data = json.load(f)

token = session_data.get("token")
print(f"Loaded Token: {token[:40]}... (len={len(token) if token else 0})")

# Test endpoints on port 4040 and port 5250 (if on remote server)
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

candidate_bases = [
    "https://196.218.246.250:4040",
    "http://196.218.246.250:5250",
    "https://196.218.246.250:5250",
    "http://196.218.246.250"
]

for base in candidate_bases:
    url = f"{base}/api/auth/me"
    print(f"\nTesting: {url}")
    try:
        res = requests.get(url, headers=headers, verify=False, timeout=5)
        print(f"  --> Status: {res.status_code}")
        print(f"  --> Body: {res.text[:200]}")
    except Exception as e:
        print(f"  --> Error: {e}")
