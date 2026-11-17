import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
with open('scratch/surgery_booking_page.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
booking = soup.find('app-surgery-booking')
if booking:
    print(booking.prettify())
else:
    print("app-surgery-booking tag not found")
