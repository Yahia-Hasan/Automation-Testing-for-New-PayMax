# محددات عناصر صفحة: قوائم الأسعار (Locators)

- **المسار (Route):** `/info-desk/price-lists`
- **المكون (Angular Component):** `<app-price-lists>`
- **إجمالي عناصر test-id المكتشفة:** `3`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **اختر الجهة...** | `[test-id="price-lists-client-select"]` | `ng-select[data-test-id='price-lists-client-select'], ng-select[test-id='price-lists-client-select']` | `//ng-select[@test-id='price-lists-client-select' or @data-test-id='price-lists-client-select']` | `ng-select ()` |
| 3 | **عرض** | `[test-id="price-lists-search-btn"]` | `button[data-test-id='price-lists-search-btn'], button[test-id='price-lists-search-btn']` | `//button[@test-id='price-lists-search-btn' or @data-test-id='price-lists-search-btn']` | `button ()` |
