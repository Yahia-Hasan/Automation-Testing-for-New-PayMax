# محددات عناصر صفحة: أجندة العمليات (Locators)

- **المسار (Route):** `/info-desk/surgery-agenda`
- **المكون (Angular Component):** `<app-surgery-agenda>`
- **إجمالي عناصر test-id المكتشفة:** `7`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **surgery-agenda-from-date-input** | `[test-id="surgery-agenda-from-date-input"]` | `input[data-test-id='surgery-agenda-from-date-input'], input[test-id='surgery-agenda-from-date-input']` | `//input[@test-id='surgery-agenda-from-date-input' or @data-test-id='surgery-agenda-from-date-input']` | `input (date)` |
| 3 | **surgery-agenda-to-date-input** | `[test-id="surgery-agenda-to-date-input"]` | `input[data-test-id='surgery-agenda-to-date-input'], input[test-id='surgery-agenda-to-date-input']` | `//input[@test-id='surgery-agenda-to-date-input' or @data-test-id='surgery-agenda-to-date-input']` | `input (date)` |
| 4 | **الكل** | `[test-id="surgery-agenda-doctor-select"]` | `ng-select[data-test-id='surgery-agenda-doctor-select'], ng-select[test-id='surgery-agenda-doctor-select']` | `//ng-select[@test-id='surgery-agenda-doctor-select' or @data-test-id='surgery-agenda-doctor-select']` | `ng-select ()` |
| 5 | **الكل** | `[test-id="surgery-agenda-specialty-select"]` | `ng-select[data-test-id='surgery-agenda-specialty-select'], ng-select[test-id='surgery-agenda-specialty-select']` | `//ng-select[@test-id='surgery-agenda-specialty-select' or @data-test-id='surgery-agenda-specialty-select']` | `ng-select ()` |
| 6 | **الكل** | `[test-id="surgery-agenda-surgery-code-select"]` | `ng-select[data-test-id='surgery-agenda-surgery-code-select'], ng-select[test-id='surgery-agenda-surgery-code-select']` | `//ng-select[@test-id='surgery-agenda-surgery-code-select' or @data-test-id='surgery-agenda-surgery-code-select']` | `ng-select ()` |
| 7 | **استعلام** | `[test-id="surgery-agenda-search-btn"]` | `button[data-test-id='surgery-agenda-search-btn'], button[test-id='surgery-agenda-search-btn']` | `//button[@test-id='surgery-agenda-search-btn' or @data-test-id='surgery-agenda-search-btn']` | `button ()` |
