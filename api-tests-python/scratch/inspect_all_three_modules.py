import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from pages.legacy_login_page import LegacyLoginPage

sys.stdout.reconfigure(encoding='utf-8')

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.set_capability("acceptInsecureCerts", True)

driver = webdriver.Chrome(options=options)
driver.set_window_size(1366, 768)

SCREENS = [
    # Emergency (6 screens)
    ("emergency_waiting", "المرضى بالطوارئ", "https://196.218.246.250:4040/emergency/waiting-list"),
    ("emergency_edit_visit", "تعديل زيارة بالطوارئ", "https://196.218.246.250:4040/emergency/edit-visit"),
    ("emergency_adm_disch", "تقرير الدخول والخروج بالطوارئ", "https://196.218.246.250:4040/emergency/admission-discharge-report"),
    ("emergency_medical_reports", "التقارير الطبية للإسعاف والطوارئ", "https://196.218.246.250:4040/emergency/medical-reports"),
    ("emergency_bed_occupancy", "تقرير اشغال أسرة الطوارئ", "https://196.218.246.250:4040/emergency/bed-occupancy"),
    ("emergency_cancel_leaved", "إلغاء خروج مريض طوارئ تم إغلاقها", "https://196.218.246.250:4040/emergency/cancel-leaved"),

    # Clinics (6 screens)
    ("clinic_waiting", "قائمة انتظار العيادات", "https://196.218.246.250:4040/clinic/waiting-list"),
    ("clinic_details_report", "تقرير العيادات التفصيلي", "https://196.218.246.250:4040/clinic/visit-details-report"),
    ("clinic_patients", "المرضى بالعيادات", "https://196.218.246.250:4040/clinic/patients"),
    ("clinic_edit_visit", "تعديل زيارة عيادات", "https://196.218.246.250:4040/clinic/edit-visit"),
    ("clinic_cancel_leaved", "إلغاء خروج مريض عيادات مُغلقة", "https://196.218.246.250:4040/clinic/cancel-leaved-visit"),
    ("clinic_medical_reports", "التقارير الطبية للعيادات الخارجية", "https://196.218.246.250:4040/clinic/medical-reports"),

    # Nursing (6 screens)
    ("nursing_rooms", "المرضى بالغرف", "https://196.218.246.250:4040/waiting-list/accomodation-rooms"),
    ("nursing_icu", "المرضى بالرعاية المركزة", "https://196.218.246.250:4040/waiting-list/icu"),
    ("nursing_neonatal", "المرضى بالحضانة", "https://196.218.246.250:4040/waiting-list/neonatal"),
    ("nursing_patient_diets", "قائمة طلبات الأنظمة الغذائية للمرضي", "https://196.218.246.250:4040/waiting-list/patient-diets-list"),
    ("nursing_attendant_diets", "قائمة طلبات الأنظمة الغذائية للمرافقين", "https://196.218.246.250:4040/waiting-list/attendant-diets"),
    ("nursing_medical_reports", "التقارير الطبية للمرضى الداخلي", "https://196.218.246.250:4040/waiting-list/medical-reports")
]

try:
    print("Logging in...")
    login_page = LegacyLoginPage(driver)
    login_page.login_full_flow()
    time.sleep(2)

    for i, (key, name, url) in enumerate(SCREENS):
        print(f"\n==========================================")
        print(f"[{i+1}/18] Inspecting: {name} ({url})")
        print(f"==========================================")
        driver.get(url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Headings
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4'])]
        print("Headings:", headings[:5])

        # data-test-ids
        dts = [el.get('data-test-id') for el in soup.find_all(attrs={'data-test-id': True}) if el.get('data-test-id') != 'global-toast-stack']
        print(f"data-test-ids ({len(dts)}):", list(dict.fromkeys(dts))[:15])

        # Inputs
        inputs = [(inp.get('name') or inp.get('id') or inp.get('placeholder') or inp.get('type')) for inp in soup.find_all('input')][:5]
        print("Sample inputs:", inputs)

finally:
    driver.quit()
