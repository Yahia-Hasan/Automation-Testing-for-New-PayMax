# محددات عناصر صفحة: أسعار العمليات (Locators)

- **المسار (Route):** `/info-desk/surgery-prices`
- **المكون (Angular Component):** `<app-surgery-prices>`
- **إجمالي عناصر test-id المكتشفة:** `5`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **اختر الجهة** | `[test-id="surgery-prices-client-select"]` | `ng-select[data-test-id='surgery-prices-client-select'], ng-select[test-id='surgery-prices-client-select']` | `//ng-select[@test-id='surgery-prices-client-select' or @data-test-id='surgery-prices-client-select']` | `ng-select ()` |
| 3 | **الكل** | `[test-id="surgery-prices-specialty-select"]` | `ng-select[data-test-id='surgery-prices-specialty-select'], ng-select[test-id='surgery-prices-specialty-select']` | `//ng-select[@test-id='surgery-prices-specialty-select' or @data-test-id='surgery-prices-specialty-select']` | `ng-select ()` |
| 4 | **اختر العملية** | `[test-id="surgery-prices-surgery-select"]` | `ng-select[data-test-id='surgery-prices-surgery-select'], ng-select[test-id='surgery-prices-surgery-select']` | `//ng-select[@test-id='surgery-prices-surgery-select' or @data-test-id='surgery-prices-surgery-select']` | `ng-select ()` |
| 5 | **عرض** | `[test-id="surgery-prices-search-btn"]` | `button[data-test-id='surgery-prices-search-btn'], button[test-id='surgery-prices-search-btn']` | `//button[@test-id='surgery-prices-search-btn' or @data-test-id='surgery-prices-search-btn']` | `button ()` |
