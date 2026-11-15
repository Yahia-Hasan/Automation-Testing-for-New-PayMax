import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

for key in ['admission_discharge', 'surgery_booking', 'leaving_requests']:
    with open(f'scratch/{key}_page.html', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    print(f"\n==================== {key} ====================")
    # Find all elements inside router-outlet or main layout
    layout = soup.find('app-baymax-layout')
    if layout:
        # Find inner router-outlet or content container
        content = layout.find('main') or layout.find(class_='main-content') or layout
        # Print child tags inside layout
        sub_comps = [c.name for c in layout.find_all(recursive=False)]
        print(f"Layout direct children: {sub_comps}")
        # Look for custom angular components (tags with hyphens)
        custom_tags = set(tag.name for tag in layout.find_all() if '-' in tag.name)
        print(f"Custom tags in layout: {list(custom_tags)}")
    
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
    print(f"Headings: {[h.get_text(strip=True) for h in headings]}")

    # Inspect buttons or special elements
    data_test_ids = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True})]
    print(f"data-test-ids ({len(data_test_ids)}): {data_test_ids[:15]}")
