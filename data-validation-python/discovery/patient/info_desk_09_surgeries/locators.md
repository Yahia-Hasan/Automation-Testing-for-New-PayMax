# محددات عناصر صفحة: قائمة انتظار العمليات (Locators)

- **المسار (Route):** `/info-desk/surgeries`
- **المكون (Angular Component):** `<app-surgeries-waiting>`
- **إجمالي عناصر test-id المكتشفة:** `4`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **surgeries-waiting-from-date-input** | `[test-id="surgeries-waiting-from-date-input"]` | `input[data-test-id='surgeries-waiting-from-date-input'], input[test-id='surgeries-waiting-from-date-input']` | `//input[@test-id='surgeries-waiting-from-date-input' or @data-test-id='surgeries-waiting-from-date-input']` | `input (date)` |
| 3 | **surgeries-waiting-to-date-input** | `[test-id="surgeries-waiting-to-date-input"]` | `input[data-test-id='surgeries-waiting-to-date-input'], input[test-id='surgeries-waiting-to-date-input']` | `//input[@test-id='surgeries-waiting-to-date-input' or @data-test-id='surgeries-waiting-to-date-input']` | `input (date)` |
| 4 | **عرض** | `[test-id="surgeries-waiting-search-btn"]` | `button[data-test-id='surgeries-waiting-search-btn'], button[test-id='surgeries-waiting-search-btn']` | `//button[@test-id='surgeries-waiting-search-btn' or @data-test-id='surgeries-waiting-search-btn']` | `button ()` |
