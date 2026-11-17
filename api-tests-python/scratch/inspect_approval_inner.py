import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
with open('scratch/leaving_approval_report_page.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

comp = soup.find('app-leaving-approval-report')
print("Direct children in app-leaving-approval-report:")
for child in comp.find_all(recursive=False):
    print(" ", child.name, child.get("class"))

print("\nAll elements with text in app-leaving-approval-report:")
for el in comp.find_all():
    # if element has direct text
    txt = el.get_text(strip=True)
    if el.name in ['h1', 'h2', 'h3', 'h4', 'span', 'p', 'label', 'div', 'button'] and txt and len(txt) < 50:
        print(f"  <{el.name}> class={el.get('class')}: '{txt}'")
