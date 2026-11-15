# محددات عناصر صفحة: طلبات خروج المرضى (قسم الحسابات) (Locators)

- **المسار (Route):** `/accountant/leaving-requests`
- **المكون (Angular Component):** `<app-accom-leaving-wl>`
- **إجمالي عناصر test-id المكتشفة:** `7`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | ملاحظات |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **accom-leaving-wl-from-date-input** | `[test-id="accom-leaving-wl-from-date-input"]` | `input[data-test-id='accom-leaving-wl-from-date-input'], input[test-id='accom-leaving-wl-from-date-input']` | `//input[@test-id='accom-leaving-wl-from-date-input' or @data-test-id='accom-leaving-wl-from-date-input']` | `input (date)` |
| 3 | **accom-leaving-wl-to-date-input** | `[test-id="accom-leaving-wl-to-date-input"]` | `input[data-test-id='accom-leaving-wl-to-date-input'], input[test-id='accom-leaving-wl-to-date-input']` | `//input[@test-id='accom-leaving-wl-to-date-input' or @data-test-id='accom-leaving-wl-to-date-input']` | `input (date)` |
| 4 | **الكل** | `[test-id="accom-leaving-wl-client-select"]` | `ng-select[data-test-id='accom-leaving-wl-client-select'], ng-select[test-id='accom-leaving-wl-client-select']` | `//ng-select[@test-id='accom-leaving-wl-client-select' or @data-test-id='accom-leaving-wl-client-select']` | `ng-select ()` |
| 5 | **الكل** | `[test-id="accom-leaving-wl-accom-type-select"]` | `ng-select[data-test-id='accom-leaving-wl-accom-type-select'], ng-select[test-id='accom-leaving-wl-accom-type-select']` | `//ng-select[@test-id='accom-leaving-wl-accom-type-select' or @data-test-id='accom-leaving-wl-accom-type-select']` | `ng-select ()` |
| 6 | **الكل** | `[test-id="accom-leaving-wl-room-select"]` | `ng-select[data-test-id='accom-leaving-wl-room-select'], ng-select[test-id='accom-leaving-wl-room-select']` | `//ng-select[@test-id='accom-leaving-wl-room-select' or @data-test-id='accom-leaving-wl-room-select']` | `ng-select ()` |
| 7 | **عرض** | `[test-id="accom-leaving-wl-search-btn"]` | `button[data-test-id='accom-leaving-wl-search-btn'], button[test-id='accom-leaving-wl-search-btn']` | `//button[@test-id='accom-leaving-wl-search-btn' or @data-test-id='accom-leaving-wl-search-btn']` | `button ()` |
