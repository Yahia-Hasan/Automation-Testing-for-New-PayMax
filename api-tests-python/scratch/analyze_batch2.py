import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

for key in ["accountant_leaving_requests", "emergency_transfers", "leaving_approval_report"]:
    with open(f"scratch/{key}_page.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    print(f"\n==================== {key} ====================")
    custom_tags = set(tag.name for tag in soup.find_all() if '-' in tag.name)
    print(f"Custom tags: {list(custom_tags)}")
    headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4'])]
    print(f"Headings: {headings}")
    dts = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True})]
    print(f"data-test-ids: {list(dict.fromkeys(dts))}")
