import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('reception_page.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

buttons = soup.find_all('button')
print(f"Total buttons found: {len(buttons)}\n")

for i, b in enumerate(buttons, 1):
    test_id = b.get('data-test-id', 'N/A')
    btn_id = b.get('id', 'N/A')
    btn_type = b.get('type', 'button')
    classes = ' '.join(b.get('class', []))
    text = ' '.join(b.text.split())
    disabled = b.has_attr('disabled')
    print(f"[{i:02d}] text='{text}' | test_id='{test_id}' | id='{btn_id}' | type='{btn_type}' | disabled={disabled} | class='{classes}'")
