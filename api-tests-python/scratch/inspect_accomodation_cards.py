import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.legacy_login_page import LegacyLoginPage

sys.stdout.reconfigure(encoding='utf-8')
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.set_capability('acceptInsecureCerts', True)
driver = webdriver.Chrome(options=options)
driver.set_window_size(1440, 1000)

try:
    LegacyLoginPage(driver).login_full_flow()
    driver.get('https://196.218.246.250:4040/waiting-list/accomodation-rooms')
    time.sleep(5)
    driver.save_screenshot('scratch/accomodation_rooms_cards.png')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Save the page html to analyze
    with open('scratch/accomodation_rooms_page.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
        
    print("Page Title:", driver.title)
    # find all buttons or links on the page
    action_btns = [(b.get('title') or b.get_text(strip=True), b.get('class'), b.get('onclick'), b.get('href')) for b in soup.find_all(['button', 'a'])]
    print("All buttons/links:", action_btns[:30])

finally:
    driver.quit()
