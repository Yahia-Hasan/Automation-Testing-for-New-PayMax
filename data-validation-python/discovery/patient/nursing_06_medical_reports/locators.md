# محددات عناصر صفحة: التقارير الطبية للمرضى الداخلي (Locators)

- **المسار (Route):** `/waiting-list/medical-reports`
- **المكون (Angular Component):** `<app-medical-reports>`
- **إجمالي عناصر test-id المكتشفة:** `11`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **medical-reports-from-date-input** | `[test-id="medical-reports-from-date-input"]` | `input[data-test-id='medical-reports-from-date-input'], input[test-id='medical-reports-from-date-input']` | `//input[@test-id='medical-reports-from-date-input' or @data-test-id='medical-reports-from-date-input']` | `input (date)` |
| 3 | **medical-reports-to-date-input** | `[test-id="medical-reports-to-date-input"]` | `input[data-test-id='medical-reports-to-date-input'], input[test-id='medical-reports-to-date-input']` | `//input[@test-id='medical-reports-to-date-input' or @data-test-id='medical-reports-to-date-input']` | `input (date)` |
| 4 | **الكل** | `[test-id="medical-reports-client-select"]` | `ng-select[data-test-id='medical-reports-client-select'], ng-select[test-id='medical-reports-client-select']` | `//ng-select[@test-id='medical-reports-client-select' or @data-test-id='medical-reports-client-select']` | `ng-select ()` |
| 5 | **الكل** | `[test-id="medical-reports-insurance-company-select"]` | `ng-select[data-test-id='medical-reports-insurance-company-select'], ng-select[test-id='medical-reports-insurance-company-select']` | `//ng-select[@test-id='medical-reports-insurance-company-select' or @data-test-id='medical-reports-insurance-company-select']` | `ng-select ()` |
| 6 | **الكلقيد الاستئنافتم الإنهاء** | `[test-id="medical-reports-invoice-status-select"]` | `select[data-test-id='medical-reports-invoice-status-select'], select[test-id='medical-reports-invoice-status-select']` | `//select[@test-id='medical-reports-invoice-status-select' or @data-test-id='medical-reports-invoice-status-select']` | `select ()` |
| 7 | **عرض** | `[test-id="medical-reports-show-btn"]` | `button[data-test-id='medical-reports-show-btn'], button[test-id='medical-reports-show-btn']` | `//button[@test-id='medical-reports-show-btn' or @data-test-id='medical-reports-show-btn']` | `button ()` |
| 8 | **دخول اليوم** | `[test-id="medical-reports-today-in-btn"]` | `button[data-test-id='medical-reports-today-in-btn'], button[test-id='medical-reports-today-in-btn']` | `//button[@test-id='medical-reports-today-in-btn' or @data-test-id='medical-reports-today-in-btn']` | `button ()` |
| 9 | **خروج اليوم** | `[test-id="medical-reports-today-out-btn"]` | `button[data-test-id='medical-reports-today-out-btn'], button[test-id='medical-reports-today-out-btn']` | `//button[@test-id='medical-reports-today-out-btn' or @data-test-id='medical-reports-today-out-btn']` | `button ()` |
| 10 | **المرضى المقيمين** | `[test-id="medical-reports-admitted-btn"]` | `button[data-test-id='medical-reports-admitted-btn'], button[test-id='medical-reports-admitted-btn']` | `//button[@test-id='medical-reports-admitted-btn' or @data-test-id='medical-reports-admitted-btn']` | `button ()` |
| 11 | **بحث بالاسم / الكود / الجهة / الشركة / ال** | `[test-id="medical-reports-search-input"]` | `input[data-test-id='medical-reports-search-input'], input[test-id='medical-reports-search-input']` | `//input[@test-id='medical-reports-search-input' or @data-test-id='medical-reports-search-input']` | `input (text)` |
