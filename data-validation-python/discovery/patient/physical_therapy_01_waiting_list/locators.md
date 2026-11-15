# محددات عناصر صفحة: قائمة انتظار العلاج الطبيعي (Locators)

- **المسار (Route):** `/physical-therapy/waiting-list`
- **المكون (Angular Component):** `<app-pt-waiting-list>`
- **إجمالي عناصر test-id المكتشفة:** `10`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **pt-waiting-list-from-date-input** | `[test-id="pt-waiting-list-from-date-input"]` | `input[data-test-id='pt-waiting-list-from-date-input'], input[test-id='pt-waiting-list-from-date-input']` | `//input[@test-id='pt-waiting-list-from-date-input' or @data-test-id='pt-waiting-list-from-date-input']` | `input (date)` |
| 3 | **pt-waiting-list-to-date-input** | `[test-id="pt-waiting-list-to-date-input"]` | `input[data-test-id='pt-waiting-list-to-date-input'], input[test-id='pt-waiting-list-to-date-input']` | `//input[@test-id='pt-waiting-list-to-date-input' or @data-test-id='pt-waiting-list-to-date-input']` | `input (date)` |
| 4 | **الكل** | `[test-id="pt-waiting-list-service-select"]` | `ng-select[data-test-id='pt-waiting-list-service-select'], ng-select[test-id='pt-waiting-list-service-select']` | `//ng-select[@test-id='pt-waiting-list-service-select' or @data-test-id='pt-waiting-list-service-select']` | `ng-select ()` |
| 5 | **الكلداخليخارجيطوارئ** | `[test-id="pt-waiting-list-patient-type-select"]` | `select[data-test-id='pt-waiting-list-patient-type-select'], select[test-id='pt-waiting-list-patient-type-select']` | `//select[@test-id='pt-waiting-list-patient-type-select' or @data-test-id='pt-waiting-list-patient-type-select']` | `select ()` |
| 6 | **الكلقيد التنفيذتم التنفيذ** | `[test-id="pt-waiting-list-status-select"]` | `select[data-test-id='pt-waiting-list-status-select'], select[test-id='pt-waiting-list-status-select']` | `//select[@test-id='pt-waiting-list-status-select' or @data-test-id='pt-waiting-list-status-select']` | `select ()` |
| 7 | **الكل** | `[test-id="pt-waiting-list-patient-select"]` | `ng-select[data-test-id='pt-waiting-list-patient-select'], ng-select[test-id='pt-waiting-list-patient-select']` | `//ng-select[@test-id='pt-waiting-list-patient-select' or @data-test-id='pt-waiting-list-patient-select']` | `ng-select ()` |
| 8 | **استعلام** | `[test-id="pt-waiting-list-search-btn"]` | `button[data-test-id='pt-waiting-list-search-btn'], button[test-id='pt-waiting-list-search-btn']` | `//button[@test-id='pt-waiting-list-search-btn' or @data-test-id='pt-waiting-list-search-btn']` | `button ()` |
| 9 | **بحث...** | `[test-id="pt-waiting-list-search-input"]` | `input[data-test-id='pt-waiting-list-search-input'], input[test-id='pt-waiting-list-search-input']` | `//input[@test-id='pt-waiting-list-search-input' or @data-test-id='pt-waiting-list-search-input']` | `input (text)` |
| 10 | **تصدير إلى إكسيل** | `[test-id="pt-waiting-list-export-excel-btn"]` | `button[data-test-id='pt-waiting-list-export-excel-btn'], button[test-id='pt-waiting-list-export-excel-btn']` | `//button[@test-id='pt-waiting-list-export-excel-btn' or @data-test-id='pt-waiting-list-export-excel-btn']` | `button ()` |
