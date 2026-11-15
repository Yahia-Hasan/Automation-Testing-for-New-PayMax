# محددات عناصر صفحة: تقرير تأكيد طلبات المغادرة (Locators)

- **المسار (Route):** `/reception/leaving-approval-report`
- **المكون (Angular Component):** `<app-leaving-approval-report>`
- **إجمالي عناصر test-id المكتشفة:** `5`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | ملاحظات |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **leaving-approval-report-date-from-input** | `[test-id="leaving-approval-report-date-from-input"]` | `input[data-test-id='leaving-approval-report-date-from-input'], input[test-id='leaving-approval-report-date-from-input']` | `//input[@test-id='leaving-approval-report-date-from-input' or @data-test-id='leaving-approval-report-date-from-input']` | `input (date)` |
| 3 | **leaving-approval-report-date-to-input** | `[test-id="leaving-approval-report-date-to-input"]` | `input[data-test-id='leaving-approval-report-date-to-input'], input[test-id='leaving-approval-report-date-to-input']` | `//input[@test-id='leaving-approval-report-date-to-input' or @data-test-id='leaving-approval-report-date-to-input']` | `input (date)` |
| 4 | **×الكل** | `[test-id="leaving-approval-report-approval-type-select"]` | `ng-select[data-test-id='leaving-approval-report-approval-type-select'], ng-select[test-id='leaving-approval-report-approval-type-select']` | `//ng-select[@test-id='leaving-approval-report-approval-type-select' or @data-test-id='leaving-approval-report-approval-type-select']` | `ng-select ()` |
| 5 | **استعلام** | `[test-id="leaving-approval-report-search-btn"]` | `button[data-test-id='leaving-approval-report-search-btn'], button[test-id='leaving-approval-report-search-btn']` | `//button[@test-id='leaving-approval-report-search-btn' or @data-test-id='leaving-approval-report-search-btn']` | `button ()` |
