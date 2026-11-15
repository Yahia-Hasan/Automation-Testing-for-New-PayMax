import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('occupancy_report_page.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

app = soup.find('app-occupancy-report')
if not app:
    print("No app-occupancy-report found!")
    sys.exit(0)

# Print direct children and sections
for section in app.find_all(recursive=False):
    print(f"Direct child: {section.name} (class={section.get('class')})")

print("\n--- All sections and cards ---")
for el in app.find_all(class_=True):
    classes = " ".join(el.get("class"))
    if any(k in classes for k in ["card", "stat", "floor", "room", "header", "toolbar", "actions", "summary", "empty", "table"]):
        txt = el.get_text(" ", strip=True)
        if len(txt) > 0 and len(txt) < 150:
            print(f"[{classes}] -> {txt}")
