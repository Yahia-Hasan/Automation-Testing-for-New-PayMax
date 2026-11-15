import sys
import time
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/accountant_leaving_requests_searched.png", "rb") as f:
    pass # file exists

for key in ["accountant_leaving_requests", "emergency_transfers", "leaving_approval_report"]:
    with open(f"scratch/{key}_page.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    print(f"\n==================== {key} ====================")
    # find direct child tags of the main component
    comp = soup.find(["app-accom-leaving-wl", "app-emergency-transfers", "app-leaving-approval-report"])
    if comp:
        print("Component tag:", comp.name)
        card = comp.find(class_=lambda c: c and ("card" in c or "container" in c or "box" in c))
        if card:
            print("Card classes:", card.get("class"))
        # find any text inside component
        print("Direct strings:", list(comp.stripped_strings))
