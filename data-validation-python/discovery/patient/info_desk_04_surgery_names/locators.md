# محددات عناصر صفحة: أسماء العمليات (Locators)

- **المسار (Route):** `/info-desk/surgery-names`
- **المكون (Angular Component):** `<app-surgery-names>`
- **إجمالي عناصر test-id المكتشفة:** `3`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **الكل** | `[test-id="surgery-names-specialty-select"]` | `ng-select[data-test-id='surgery-names-specialty-select'], ng-select[test-id='surgery-names-specialty-select']` | `//ng-select[@test-id='surgery-names-specialty-select' or @data-test-id='surgery-names-specialty-select']` | `ng-select ()` |
| 3 | **عرض** | `[test-id="surgery-names-search-btn"]` | `button[data-test-id='surgery-names-search-btn'], button[test-id='surgery-names-search-btn']` | `//button[@test-id='surgery-names-search-btn' or @data-test-id='surgery-names-search-btn']` | `button ()` |
