# محددات عناصر صفحة: قائمة طلبات الأنظمة الغذائية للمرضى (Locators)

- **المسار (Route):** `/waiting-list/patient-diets-list`
- **المكون (Angular Component):** `<app-patient-diets-list>`
- **إجمالي عناصر test-id المكتشفة:** `5`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **الكل** | `[test-id="patient-diets-list-diet-select"]` | `ng-select[data-test-id='patient-diets-list-diet-select'], ng-select[test-id='patient-diets-list-diet-select']` | `//ng-select[@test-id='patient-diets-list-diet-select' or @data-test-id='patient-diets-list-diet-select']` | `ng-select ()` |
| 3 | **عرض** | `[test-id="patient-diets-list-show-btn"]` | `button[data-test-id='patient-diets-list-show-btn'], button[test-id='patient-diets-list-show-btn']` | `//button[@test-id='patient-diets-list-show-btn' or @data-test-id='patient-diets-list-show-btn']` | `button ()` |
| 4 | **Print All Barcodes** | `[test-id="patient-diets-list-print-all-barcodes-btn"]` | `button[data-test-id='patient-diets-list-print-all-barcodes-btn'], button[test-id='patient-diets-list-print-all-barcodes-btn']` | `//button[@test-id='patient-diets-list-print-all-barcodes-btn' or @data-test-id='patient-diets-list-print-all-barcodes-btn']` | `button ()` |
| 5 | **بحث...** | `[test-id="patient-diets-list-search-input"]` | `input[data-test-id='patient-diets-list-search-input'], input[test-id='patient-diets-list-search-input']` | `//input[@test-id='patient-diets-list-search-input' or @data-test-id='patient-diets-list-search-input']` | `input (text)` |
