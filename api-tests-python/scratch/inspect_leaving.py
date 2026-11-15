import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/leaving_requests_page.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

lr = soup.find("app-leaving-requests")
print("All data-test-id in app-leaving-requests:")
dt_counts = {}
for tag in lr.find_all(attrs={"data-test-id": True}):
    dt = tag.get('data-test-id')
    dt_counts[dt] = dt_counts.get(dt, 0) + 1
for dt, c in dt_counts.items():
    print(f"  dt: '{dt}' (count: {c})")

print("\nTable columns:")
for th in lr.find_all("th"):
    print(f"  TH: {th.get_text(strip=True)}")

print("\nFirst row sample:")
first_row = lr.find("tr", attrs={"data-test-id": "leaving-requests-row"})
if first_row:
    tds = [td.get_text(strip=True) for td in first_row.find_all("td")]
    print(f"  TDs: {tds}")
