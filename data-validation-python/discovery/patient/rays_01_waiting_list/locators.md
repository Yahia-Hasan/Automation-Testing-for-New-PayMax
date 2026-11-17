# محددات عناصر صفحة: قائمة انتظار الأشعة (Locators)

- **المسار (Route):** `/rays/waiting-list`
- **المكون (Angular Component):** `<app-rays-waiting-list>`
- **إجمالي عناصر test-id المكتشفة:** `13`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **rays-waiting-list-from-date-input** | `[test-id="rays-waiting-list-from-date-input"]` | `input[data-test-id='rays-waiting-list-from-date-input'], input[test-id='rays-waiting-list-from-date-input']` | `//input[@test-id='rays-waiting-list-from-date-input' or @data-test-id='rays-waiting-list-from-date-input']` | `input (date)` |
| 3 | **rays-waiting-list-to-date-input** | `[test-id="rays-waiting-list-to-date-input"]` | `input[data-test-id='rays-waiting-list-to-date-input'], input[test-id='rays-waiting-list-to-date-input']` | `//input[@test-id='rays-waiting-list-to-date-input' or @data-test-id='rays-waiting-list-to-date-input']` | `input (date)` |
| 4 | **الكلتم التنفيذلم ينفذ بعد** | `[test-id="rays-waiting-list-status-select"]` | `select[data-test-id='rays-waiting-list-status-select'], select[test-id='rays-waiting-list-status-select']` | `//select[@test-id='rays-waiting-list-status-select' or @data-test-id='rays-waiting-list-status-select']` | `select ()` |
| 5 | **الكل** | `[test-id="rays-waiting-list-category-select"]` | `ng-select[data-test-id='rays-waiting-list-category-select'], ng-select[test-id='rays-waiting-list-category-select']` | `//ng-select[@test-id='rays-waiting-list-category-select' or @data-test-id='rays-waiting-list-category-select']` | `ng-select ()` |
| 6 | **الكل** | `[test-id="rays-waiting-list-service-select"]` | `ng-select[data-test-id='rays-waiting-list-service-select'], ng-select[test-id='rays-waiting-list-service-select']` | `//ng-select[@test-id='rays-waiting-list-service-select' or @data-test-id='rays-waiting-list-service-select']` | `ng-select ()` |
| 7 | **عرض** | `[test-id="rays-waiting-list-search-btn"]` | `button[data-test-id='rays-waiting-list-search-btn'], button[test-id='rays-waiting-list-search-btn']` | `//button[@test-id='rays-waiting-list-search-btn' or @data-test-id='rays-waiting-list-search-btn']` | `button ()` |
| 8 | **الكل** | `[test-id="rays-waiting-list-dept-all-btn"]` | `button[data-test-id='rays-waiting-list-dept-all-btn'], button[test-id='rays-waiting-list-dept-all-btn']` | `//button[@test-id='rays-waiting-list-dept-all-btn' or @data-test-id='rays-waiting-list-dept-all-btn']` | `button (button)` |
| 9 | **داخلي** | `[test-id="rays-waiting-list-dept-inpatient-btn"]` | `button[data-test-id='rays-waiting-list-dept-inpatient-btn'], button[test-id='rays-waiting-list-dept-inpatient-btn']` | `//button[@test-id='rays-waiting-list-dept-inpatient-btn' or @data-test-id='rays-waiting-list-dept-inpatient-btn']` | `button (button)` |
| 10 | **طوارئ** | `[test-id="rays-waiting-list-dept-emergency-btn"]` | `button[data-test-id='rays-waiting-list-dept-emergency-btn'], button[test-id='rays-waiting-list-dept-emergency-btn']` | `//button[@test-id='rays-waiting-list-dept-emergency-btn' or @data-test-id='rays-waiting-list-dept-emergency-btn']` | `button (button)` |
| 11 | **خارجي** | `[test-id="rays-waiting-list-dept-outpatient-btn"]` | `button[data-test-id='rays-waiting-list-dept-outpatient-btn'], button[test-id='rays-waiting-list-dept-outpatient-btn']` | `//button[@test-id='rays-waiting-list-dept-outpatient-btn' or @data-test-id='rays-waiting-list-dept-outpatient-btn']` | `button (button)` |
| 12 | **بحث باسم / كود / خدمة / كود الطلب...** | `[test-id="rays-waiting-list-search-input"]` | `input[data-test-id='rays-waiting-list-search-input'], input[test-id='rays-waiting-list-search-input']` | `//input[@test-id='rays-waiting-list-search-input' or @data-test-id='rays-waiting-list-search-input']` | `input (text)` |
| 13 | **تصدير إلى إكسيل** | `[test-id="rays-waiting-list-export-excel-btn"]` | `button[data-test-id='rays-waiting-list-export-excel-btn'], button[test-id='rays-waiting-list-export-excel-btn']` | `//button[@test-id='rays-waiting-list-export-excel-btn' or @data-test-id='rays-waiting-list-export-excel-btn']` | `button ()` |
