import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/accomodation_rooms_page.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

buttons = soup.find_all(['button', 'a'])
print(f"Total buttons and links found in accomodation_rooms: {len(buttons)}\n")

for i, b in enumerate(buttons, 1):
    test_id = b.get('data-test-id', 'N/A')
    tag = b.name
    classes = ' '.join(b.get('class', []))
    text = ' '.join(b.text.split())
    disabled = b.has_attr('disabled')
    href = b.get('href', 'N/A')
    if text or test_id != 'N/A' or 'btn' in classes:
        print(f"[{i:02d}] tag={tag} | text='{text}' | test_id='{test_id}' | href='{href}' | disabled={disabled} | class='{classes}'")
