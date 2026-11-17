# محددات عناصر صفحة: تقرير الدخول والخروج (Locators)

- **المسار (Route):** `/reception/admission-discharge-report`
- **المكون (Angular Component):** `<app-admission-discharge-report>`
- **إجمالي عناصر test-id المكتشفة:** `8`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | ملاحظات |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **admission-discharge-report-date-from-inp** | `[test-id="admission-discharge-report-date-from-input"]` | `input[data-test-id='admission-discharge-report-date-from-input'], input[test-id='admission-discharge-report-date-from-input']` | `//input[@test-id='admission-discharge-report-date-from-input' or @data-test-id='admission-discharge-report-date-from-input']` | `input (date)` |
| 3 | **admission-discharge-report-date-to-input** | `[test-id="admission-discharge-report-date-to-input"]` | `input[data-test-id='admission-discharge-report-date-to-input'], input[test-id='admission-discharge-report-date-to-input']` | `//input[@test-id='admission-discharge-report-date-to-input' or @data-test-id='admission-discharge-report-date-to-input']` | `input (date)` |
| 4 | **×حالات الدخول** | `[test-id="admission-discharge-report-type-select"]` | `ng-select[data-test-id='admission-discharge-report-type-select'], ng-select[test-id='admission-discharge-report-type-select']` | `//ng-select[@test-id='admission-discharge-report-type-select' or @data-test-id='admission-discharge-report-type-select']` | `ng-select ()` |
| 5 | **الكل** | `[test-id="admission-discharge-report-degree-select"]` | `ng-select[data-test-id='admission-discharge-report-degree-select'], ng-select[test-id='admission-discharge-report-degree-select']` | `//ng-select[@test-id='admission-discharge-report-degree-select' or @data-test-id='admission-discharge-report-degree-select']` | `ng-select ()` |
| 6 | **الكل** | `[test-id="admission-discharge-report-floor-select"]` | `ng-select[data-test-id='admission-discharge-report-floor-select'], ng-select[test-id='admission-discharge-report-floor-select']` | `//ng-select[@test-id='admission-discharge-report-floor-select' or @data-test-id='admission-discharge-report-floor-select']` | `ng-select ()` |
| 7 | **×الكل** | `[test-id="admission-discharge-report-invoice-status-select"]` | `ng-select[data-test-id='admission-discharge-report-invoice-status-select'], ng-select[test-id='admission-discharge-report-invoice-status-select']` | `//ng-select[@test-id='admission-discharge-report-invoice-status-select' or @data-test-id='admission-discharge-report-invoice-status-select']` | `ng-select ()` |
| 8 | **عرض** | `[test-id="admission-discharge-report-search-btn"]` | `button[data-test-id='admission-discharge-report-search-btn'], button[test-id='admission-discharge-report-search-btn']` | `//button[@test-id='admission-discharge-report-search-btn' or @data-test-id='admission-discharge-report-search-btn']` | `button ()` |
