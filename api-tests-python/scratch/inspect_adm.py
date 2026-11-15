import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/admission_discharge_loaded.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

adm = soup.find("app-admission-discharge-report")
print("All data-test-id elements in app-admission-discharge-report:")
for tag in adm.find_all(attrs={"data-test-id": True}):
    print(f"  <{tag.name}> data-test-id='{tag.get('data-test-id')}' text='{tag.get_text(strip=True)[:40]}'")

print("\nAll buttons in app-admission-discharge-report:")
for btn in adm.find_all("button"):
    print(f"  <button> data-test-id='{btn.get('data-test-id')}' text='{btn.get_text(strip=True)}' class='{btn.get('class')}'")

print("\nAll links in app-admission-discharge-report:")
for a in adm.find_all("a"):
    print(f"  <a> text='{a.get_text(strip=True)}' class='{a.get('class')}'")
