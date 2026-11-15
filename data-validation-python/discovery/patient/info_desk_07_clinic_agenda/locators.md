# محددات عناصر صفحة: أجندة العيادات (Locators)

- **المسار (Route):** `/info-desk/clinic-agenda`
- **المكون (Angular Component):** `<app-clinic-agenda>`
- **إجمالي عناصر test-id المكتشفة:** `7`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **clinic-agenda-from-date-input** | `[test-id="clinic-agenda-from-date-input"]` | `input[data-test-id='clinic-agenda-from-date-input'], input[test-id='clinic-agenda-from-date-input']` | `//input[@test-id='clinic-agenda-from-date-input' or @data-test-id='clinic-agenda-from-date-input']` | `input (date)` |
| 3 | **clinic-agenda-to-date-input** | `[test-id="clinic-agenda-to-date-input"]` | `input[data-test-id='clinic-agenda-to-date-input'], input[test-id='clinic-agenda-to-date-input']` | `//input[@test-id='clinic-agenda-to-date-input' or @data-test-id='clinic-agenda-to-date-input']` | `input (date)` |
| 4 | **كل الأطباء** | `[test-id="clinic-agenda-doctor-select"]` | `ng-select[data-test-id='clinic-agenda-doctor-select'], ng-select[test-id='clinic-agenda-doctor-select']` | `//ng-select[@test-id='clinic-agenda-doctor-select' or @data-test-id='clinic-agenda-doctor-select']` | `ng-select ()` |
| 5 | **كل المجموعات** | `[test-id="clinic-agenda-service-group-select"]` | `ng-select[data-test-id='clinic-agenda-service-group-select'], ng-select[test-id='clinic-agenda-service-group-select']` | `//ng-select[@test-id='clinic-agenda-service-group-select' or @data-test-id='clinic-agenda-service-group-select']` | `ng-select ()` |
| 6 | **كل الخدمات** | `[test-id="clinic-agenda-service-select"]` | `ng-select[data-test-id='clinic-agenda-service-select'], ng-select[test-id='clinic-agenda-service-select']` | `//ng-select[@test-id='clinic-agenda-service-select' or @data-test-id='clinic-agenda-service-select']` | `ng-select ()` |
| 7 | **بحث** | `[test-id="clinic-agenda-search-btn"]` | `button[data-test-id='clinic-agenda-search-btn'], button[test-id='clinic-agenda-search-btn']` | `//button[@test-id='clinic-agenda-search-btn' or @data-test-id='clinic-agenda-search-btn']` | `button ()` |
