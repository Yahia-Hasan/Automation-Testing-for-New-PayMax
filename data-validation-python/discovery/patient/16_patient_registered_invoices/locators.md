# محددات عناصر صفحة: فواتير المرضى (Locators)

- **المسار (Route):** `/patient-accounts/registered-invoices`
- **المكون (Angular Component):** `<app-registered-invoices>`
- **إجمالي عناصر test-id المكتشفة:** `11`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **registered-invoices-from-date-input** | `[test-id="registered-invoices-from-date-input"]` | `input[data-test-id='registered-invoices-from-date-input'], input[test-id='registered-invoices-from-date-input']` | `//input[@test-id='registered-invoices-from-date-input' or @data-test-id='registered-invoices-from-date-input']` | `input (date)` |
| 3 | **registered-invoices-to-date-input** | `[test-id="registered-invoices-to-date-input"]` | `input[data-test-id='registered-invoices-to-date-input'], input[test-id='registered-invoices-to-date-input']` | `//input[@test-id='registered-invoices-to-date-input' or @data-test-id='registered-invoices-to-date-input']` | `input (date)` |
| 4 | **-- الكل --** | `[test-id="registered-invoices-client-select"]` | `ng-select[data-test-id='registered-invoices-client-select'], ng-select[test-id='registered-invoices-client-select']` | `//ng-select[@test-id='registered-invoices-client-select' or @data-test-id='registered-invoices-client-select']` | `ng-select ()` |
| 5 | **-- الكل --** | `[test-id="registered-invoices-ins-company-select"]` | `ng-select[data-test-id='registered-invoices-ins-company-select'], ng-select[test-id='registered-invoices-ins-company-select']` | `//ng-select[@test-id='registered-invoices-ins-company-select' or @data-test-id='registered-invoices-ins-company-select']` | `ng-select ()` |
| 6 | **-- الكل --** | `[test-id="registered-invoices-acc-types-select"]` | `ng-select[data-test-id='registered-invoices-acc-types-select'], ng-select[test-id='registered-invoices-acc-types-select']` | `//ng-select[@test-id='registered-invoices-acc-types-select' or @data-test-id='registered-invoices-acc-types-select']` | `ng-select ()` |
| 7 | **AllIPDCATH** | `[test-id="registered-invoices-hospital-section-select"]` | `select[data-test-id='registered-invoices-hospital-section-select'], select[test-id='registered-invoices-hospital-section-select']` | `//select[@test-id='registered-invoices-hospital-section-select' or @data-test-id='registered-invoices-hospital-section-select']` | `select ()` |
| 8 | **بحث** | `[test-id="registered-invoices-search-btn"]` | `button[data-test-id='registered-invoices-search-btn'], button[test-id='registered-invoices-search-btn']` | `//button[@test-id='registered-invoices-search-btn' or @data-test-id='registered-invoices-search-btn']` | `button ()` |
| 9 | **خروج اليوم** | `[test-id="registered-invoices-today-exit-btn"]` | `button[data-test-id='registered-invoices-today-exit-btn'], button[test-id='registered-invoices-today-exit-btn']` | `//button[@test-id='registered-invoices-today-exit-btn' or @data-test-id='registered-invoices-today-exit-btn']` | `button ()` |
| 10 | **بحث...** | `[test-id="registered-invoices-search-input"]` | `input[data-test-id='registered-invoices-search-input'], input[test-id='registered-invoices-search-input']` | `//input[@test-id='registered-invoices-search-input' or @data-test-id='registered-invoices-search-input']` | `input (text)` |
| 11 | **تصدير إلى إكسيل** | `[test-id="registered-invoices-export-excel-btn"]` | `button[data-test-id='registered-invoices-export-excel-btn'], button[test-id='registered-invoices-export-excel-btn']` | `//button[@test-id='registered-invoices-export-excel-btn' or @data-test-id='registered-invoices-export-excel-btn']` | `button ()` |
