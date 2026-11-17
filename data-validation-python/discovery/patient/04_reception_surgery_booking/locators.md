# محددات عناصر صفحة: حجز العمليات (Locators)

- **المسار (Route):** `/reception/surgery-booking`
- **المكون (Angular Component):** `<app-surgery-booking>`
- **إجمالي عناصر test-id المكتشفة:** `12`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | ملاحظات |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **surgery-booking-date-input** | `[test-id="surgery-booking-date-input"]` | `input[data-test-id='surgery-booking-date-input'], input[test-id='surgery-booking-date-input']` | `//input[@test-id='surgery-booking-date-input' or @data-test-id='surgery-booking-date-input']` | `input (date)` |
| 3 | **بحث** | `[test-id="surgery-booking-search-btn"]` | `button[data-test-id='surgery-booking-search-btn'], button[test-id='surgery-booking-search-btn']` | `//button[@test-id='surgery-booking-search-btn' or @data-test-id='surgery-booking-search-btn']` | `button ()` |
| 4 | **-- اختر الطبيب --** | `[test-id="surgery-booking-doctor-select"]` | `ng-select[data-test-id='surgery-booking-doctor-select'], ng-select[test-id='surgery-booking-doctor-select']` | `//ng-select[@test-id='surgery-booking-doctor-select' or @data-test-id='surgery-booking-doctor-select']` | `ng-select ()` |
| 5 | **-- اختر التخصص --** | `[test-id="surgery-booking-specialty-select"]` | `ng-select[data-test-id='surgery-booking-specialty-select'], ng-select[test-id='surgery-booking-specialty-select']` | `//ng-select[@test-id='surgery-booking-specialty-select' or @data-test-id='surgery-booking-specialty-select']` | `ng-select ()` |
| 6 | **surgery-booking-short-code-input** | `[test-id="surgery-booking-short-code-input"]` | `input[data-test-id='surgery-booking-short-code-input'], input[test-id='surgery-booking-short-code-input']` | `//input[@test-id='surgery-booking-short-code-input' or @data-test-id='surgery-booking-short-code-input']` | `input (text)` |
| 7 | **-- اختر العملية --** | `[test-id="surgery-booking-surgery-select"]` | `ng-select[data-test-id='surgery-booking-surgery-select'], ng-select[test-id='surgery-booking-surgery-select']` | `//ng-select[@test-id='surgery-booking-surgery-select' or @data-test-id='surgery-booking-surgery-select']` | `ng-select ()` |
| 8 | **surgery-booking-patient-name-input** | `[test-id="surgery-booking-patient-name-input"]` | `input[data-test-id='surgery-booking-patient-name-input'], input[test-id='surgery-booking-patient-name-input']` | `//input[@test-id='surgery-booking-patient-name-input' or @data-test-id='surgery-booking-patient-name-input']` | `input (text)` |
| 9 | **-- غير مرتبط --** | `[test-id="surgery-booking-reservation-select"]` | `ng-select[data-test-id='surgery-booking-reservation-select'], ng-select[test-id='surgery-booking-reservation-select']` | `//ng-select[@test-id='surgery-booking-reservation-select' or @data-test-id='surgery-booking-reservation-select']` | `ng-select ()` |
| 10 | **اضافة** | `[test-id="surgery-booking-add-btn"]` | `button[data-test-id='surgery-booking-add-btn'], button[test-id='surgery-booking-add-btn']` | `//button[@test-id='surgery-booking-add-btn' or @data-test-id='surgery-booking-add-btn']` | `button ()` |
| 11 | **جديد** | `[test-id="surgery-booking-clear-btn"]` | `button[data-test-id='surgery-booking-clear-btn'], button[test-id='surgery-booking-clear-btn']` | `//button[@test-id='surgery-booking-clear-btn' or @data-test-id='surgery-booking-clear-btn']` | `button ()` |
| 12 | **surgery-booking-notes-textarea** | `[test-id="surgery-booking-notes-textarea"]` | `textarea[data-test-id='surgery-booking-notes-textarea'], textarea[test-id='surgery-booking-notes-textarea']` | `//textarea[@test-id='surgery-booking-notes-textarea' or @data-test-id='surgery-booking-notes-textarea']` | `textarea ()` |
