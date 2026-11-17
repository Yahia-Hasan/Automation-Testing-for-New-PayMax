# محددات عناصر صفحة: طلبات تحويل المرضى من الطوارئ للداخلي (Locators)

- **المسار (Route):** `/reception/emergency-transfers`
- **المكون (Angular Component):** `<app-emergency-transfers>`
- **إجمالي عناصر test-id المكتشفة:** `4`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | ملاحظات |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **emergency-transfers-date-from-input** | `[test-id="emergency-transfers-date-from-input"]` | `input[data-test-id='emergency-transfers-date-from-input'], input[test-id='emergency-transfers-date-from-input']` | `//input[@test-id='emergency-transfers-date-from-input' or @data-test-id='emergency-transfers-date-from-input']` | `input (date)` |
| 3 | **emergency-transfers-date-to-input** | `[test-id="emergency-transfers-date-to-input"]` | `input[data-test-id='emergency-transfers-date-to-input'], input[test-id='emergency-transfers-date-to-input']` | `//input[@test-id='emergency-transfers-date-to-input' or @data-test-id='emergency-transfers-date-to-input']` | `input (date)` |
| 4 | **عرض** | `[test-id="emergency-transfers-search-btn"]` | `button[data-test-id='emergency-transfers-search-btn'], button[test-id='emergency-transfers-search-btn']` | `//button[@test-id='emergency-transfers-search-btn' or @data-test-id='emergency-transfers-search-btn']` | `button ()` |
