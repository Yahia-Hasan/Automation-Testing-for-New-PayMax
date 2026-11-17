# محددات عناصر صفحة: استعلام عن بنك الدم (Locators)

- **المسار (Route):** `/lab/blood-bank-status`
- **المكون (Angular Component):** `<app-blood-bank-status>`
- **إجمالي عناصر test-id المكتشفة:** `8`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **الكلما تم حجزهما تم صرفهلم يتم الحجز ولم** | `[test-id="blood-bank-status-status-select"]` | `select[data-test-id='blood-bank-status-status-select'], select[test-id='blood-bank-status-status-select']` | `//select[@test-id='blood-bank-status-status-select' or @data-test-id='blood-bank-status-status-select']` | `select ()` |
| 3 | **الكل** | `[test-id="blood-bank-status-client-select"]` | `ng-select[data-test-id='blood-bank-status-client-select'], ng-select[test-id='blood-bank-status-client-select']` | `//ng-select[@test-id='blood-bank-status-client-select' or @data-test-id='blood-bank-status-client-select']` | `ng-select ()` |
| 4 | **blood-bank-status-from-date-input** | `[test-id="blood-bank-status-from-date-input"]` | `input[data-test-id='blood-bank-status-from-date-input'], input[test-id='blood-bank-status-from-date-input']` | `//input[@test-id='blood-bank-status-from-date-input' or @data-test-id='blood-bank-status-from-date-input']` | `input (date)` |
| 5 | **blood-bank-status-to-date-input** | `[test-id="blood-bank-status-to-date-input"]` | `input[data-test-id='blood-bank-status-to-date-input'], input[test-id='blood-bank-status-to-date-input']` | `//input[@test-id='blood-bank-status-to-date-input' or @data-test-id='blood-bank-status-to-date-input']` | `input (date)` |
| 6 | **استعلام** | `[test-id="blood-bank-status-search-btn"]` | `button[data-test-id='blood-bank-status-search-btn'], button[test-id='blood-bank-status-search-btn']` | `//button[@test-id='blood-bank-status-search-btn' or @data-test-id='blood-bank-status-search-btn']` | `button ()` |
| 7 | **تصدير إلى إكسيل** | `[test-id="blood-bank-status-export-btn"]` | `button[data-test-id='blood-bank-status-export-btn'], button[test-id='blood-bank-status-export-btn']` | `//button[@test-id='blood-bank-status-export-btn' or @data-test-id='blood-bank-status-export-btn']` | `button ()` |
| 8 | **بحث...** | `[test-id="blood-bank-status-search-input"]` | `input[data-test-id='blood-bank-status-search-input'], input[test-id='blood-bank-status-search-input']` | `//input[@test-id='blood-bank-status-search-input' or @data-test-id='blood-bank-status-search-input']` | `input (text)` |
