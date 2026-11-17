# محددات عناصر صفحة: قائمة انتظار بنك الدم (Locators)

- **المسار (Route):** `/lab/blood-waiting-list`
- **المكون (Angular Component):** `<app-blood-waiting-list>`
- **إجمالي عناصر test-id المكتشفة:** `10`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **كل المرضي** | `[test-id="blood-waiting-list-patient-select"]` | `ng-select[data-test-id='blood-waiting-list-patient-select'], ng-select[test-id='blood-waiting-list-patient-select']` | `//ng-select[@test-id='blood-waiting-list-patient-select' or @data-test-id='blood-waiting-list-patient-select']` | `ng-select ()` |
| 3 | **عرض** | `[test-id="blood-waiting-list-search-btn"]` | `button[data-test-id='blood-waiting-list-search-btn'], button[test-id='blood-waiting-list-search-btn']` | `//button[@test-id='blood-waiting-list-search-btn' or @data-test-id='blood-waiting-list-search-btn']` | `button ()` |
| 4 | **بحث...** | `[test-id="blood-waiting-list-search-input"]` | `input[data-test-id='blood-waiting-list-search-input'], input[test-id='blood-waiting-list-search-input']` | `//input[@test-id='blood-waiting-list-search-input' or @data-test-id='blood-waiting-list-search-input']` | `input (text)` |
| 5 | **1522447716عبدالرحيم بن مدني بن عبدالرحيم** | `[test-id="blood-waiting-list-row"]` | `tr[data-test-id='blood-waiting-list-row'], tr[test-id='blood-waiting-list-row']` | `//tr[@test-id='blood-waiting-list-row' or @data-test-id='blood-waiting-list-row']` | `tr ()` |
| 6 | **التفاصيل** | `[test-id="blood-waiting-list-open-details-btn"]` | `button[data-test-id='blood-waiting-list-open-details-btn'], button[test-id='blood-waiting-list-open-details-btn']` | `//button[@test-id='blood-waiting-list-open-details-btn' or @data-test-id='blood-waiting-list-open-details-btn']` | `button ()` |
| 7 | **«** | `[test-id="blood-waiting-list-first-page-btn"]` | `button[data-test-id='blood-waiting-list-first-page-btn'], button[test-id='blood-waiting-list-first-page-btn']` | `//button[@test-id='blood-waiting-list-first-page-btn' or @data-test-id='blood-waiting-list-first-page-btn']` | `button ()` |
| 8 | **‹** | `[test-id="blood-waiting-list-prev-page-btn"]` | `button[data-test-id='blood-waiting-list-prev-page-btn'], button[test-id='blood-waiting-list-prev-page-btn']` | `//button[@test-id='blood-waiting-list-prev-page-btn' or @data-test-id='blood-waiting-list-prev-page-btn']` | `button ()` |
| 9 | **›** | `[test-id="blood-waiting-list-next-page-btn"]` | `button[data-test-id='blood-waiting-list-next-page-btn'], button[test-id='blood-waiting-list-next-page-btn']` | `//button[@test-id='blood-waiting-list-next-page-btn' or @data-test-id='blood-waiting-list-next-page-btn']` | `button ()` |
| 10 | **»** | `[test-id="blood-waiting-list-last-page-btn"]` | `button[data-test-id='blood-waiting-list-last-page-btn'], button[test-id='blood-waiting-list-last-page-btn']` | `//button[@test-id='blood-waiting-list-last-page-btn' or @data-test-id='blood-waiting-list-last-page-btn']` | `button ()` |
