# محددات عناصر صفحة: قائمة انتظار العيادات (Locators)

- **المسار (Route):** `/clinic/waiting-list`
- **المكون (Angular Component):** `<app-clinic-waiting-list>`
- **إجمالي عناصر test-id المكتشفة:** `6`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **clinic-waiting-list-date-input** | `[test-id="clinic-waiting-list-date-input"]` | `input[data-test-id='clinic-waiting-list-date-input'], input[test-id='clinic-waiting-list-date-input']` | `//input[@test-id='clinic-waiting-list-date-input' or @data-test-id='clinic-waiting-list-date-input']` | `input (date)` |
| 3 | **-- الكل --** | `[test-id="clinic-waiting-list-doctor-select"]` | `ng-select[data-test-id='clinic-waiting-list-doctor-select'], ng-select[test-id='clinic-waiting-list-doctor-select']` | `//ng-select[@test-id='clinic-waiting-list-doctor-select' or @data-test-id='clinic-waiting-list-doctor-select']` | `ng-select ()` |
| 4 | **الكلمدفوعغير مدفوع** | `[test-id="clinic-waiting-list-payment-status-select"]` | `select[data-test-id='clinic-waiting-list-payment-status-select'], select[test-id='clinic-waiting-list-payment-status-select']` | `//select[@test-id='clinic-waiting-list-payment-status-select' or @data-test-id='clinic-waiting-list-payment-status-select']` | `select ()` |
| 5 | **الكلتملم يتم** | `[test-id="clinic-waiting-list-done-status-select"]` | `select[data-test-id='clinic-waiting-list-done-status-select'], select[test-id='clinic-waiting-list-done-status-select']` | `//select[@test-id='clinic-waiting-list-done-status-select' or @data-test-id='clinic-waiting-list-done-status-select']` | `select ()` |
| 6 | **عرض** | `[test-id="clinic-waiting-list-search-btn"]` | `button[data-test-id='clinic-waiting-list-search-btn'], button[test-id='clinic-waiting-list-search-btn']` | `//button[@test-id='clinic-waiting-list-search-btn' or @data-test-id='clinic-waiting-list-search-btn']` | `button ()` |
