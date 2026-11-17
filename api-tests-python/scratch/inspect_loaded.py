import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

print("==================== SURGERY BOOKING LOADED ====================")
with open("scratch/surgery_booking_loaded.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

app_surgery = soup.find("app-surgery-booking")
if app_surgery:
    inputs = app_surgery.find_all("input")
    print(f"Inputs ({len(inputs)}):")
    for inp in inputs:
        print(f"  id='{inp.get('id')}', type='{inp.get('type')}', dt='{inp.get('data-test-id')}', name='{inp.get('name')}', ph='{inp.get('placeholder')}', class='{inp.get('class')}'")

    buttons = app_surgery.find_all("button")
    print(f"Buttons ({len(buttons)}):")
    for btn in buttons:
        print(f"  text='{btn.get_text(strip=True)}', dt='{btn.get('data-test-id')}', id='{btn.get('id')}', class='{btn.get('class')}'")

    selects = app_surgery.find_all(["select", "ng-select"])
    print(f"Selects ({len(selects)}):")
    for s in selects:
        print(f"  tag={s.name}, dt='{s.get('data-test-id')}', ph='{s.get('placeholder')}', class='{s.get('class')}'")

    tables = app_surgery.find_all("table")
    print(f"Tables ({len(tables)}):")
    for t in tables:
        th_list = [th.get_text(strip=True) for th in t.find_all("th")]
        print(f"  table headers: {th_list}")

print("\n==================== ADMISSION DISCHARGE LOADED ====================")
with open("scratch/admission_discharge_loaded.html", encoding="utf-8") as f:
    soup2 = BeautifulSoup(f.read(), "html.parser")

app_adm = soup2.find("app-admission-discharge-report")
if app_adm:
    tables = app_adm.find_all("table")
    print(f"Tables ({len(tables)}):")
    for t in tables:
        th_list = [th.get_text(strip=True) for th in t.find_all("th")]
        rows = t.find_all("tr")
        print(f"  table headers: {th_list}, total trs: {len(rows)}")

    cards = app_adm.find_all(class_=lambda c: c and ("card" in c or "kpi" in c or "summary" in c))
    print(f"Cards/Summary ({len(cards)}):")
    for c in cards[:5]:
        print(f"  card: {c.get_text(strip=True)[:80]}")
    
    print("Direct text snippet:", " ".join(app_adm.stripped_strings)[:300])
