# محددات عناصر صفحة: مديونيات المرضى (Locators)

- **المسار (Route):** `/patient-accounts/patient-settlements`
- **المكون (Angular Component):** `<app-patient-settlements>`
- **إجمالي عناصر test-id المكتشفة:** `8`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **patient-settlements-from-date-input** | `[test-id="patient-settlements-from-date-input"]` | `input[data-test-id='patient-settlements-from-date-input'], input[test-id='patient-settlements-from-date-input']` | `//input[@test-id='patient-settlements-from-date-input' or @data-test-id='patient-settlements-from-date-input']` | `input (date)` |
| 3 | **patient-settlements-to-date-input** | `[test-id="patient-settlements-to-date-input"]` | `input[data-test-id='patient-settlements-to-date-input'], input[test-id='patient-settlements-to-date-input']` | `//input[@test-id='patient-settlements-to-date-input' or @data-test-id='patient-settlements-to-date-input']` | `input (date)` |
| 4 | **أدخل كود المريض** | `[test-id="patient-settlements-patient-code-input"]` | `input[data-test-id='patient-settlements-patient-code-input'], input[test-id='patient-settlements-patient-code-input']` | `//input[@test-id='patient-settlements-patient-code-input' or @data-test-id='patient-settlements-patient-code-input']` | `input (number)` |
| 5 | **الكلمسددغير مسددجزئي** | `[test-id="patient-settlements-search-type-select"]` | `select[data-test-id='patient-settlements-search-type-select'], select[test-id='patient-settlements-search-type-select']` | `//select[@test-id='patient-settlements-search-type-select' or @data-test-id='patient-settlements-search-type-select']` | `select ()` |
| 6 | **بحث** | `[test-id="patient-settlements-search-btn"]` | `button[data-test-id='patient-settlements-search-btn'], button[test-id='patient-settlements-search-btn']` | `//button[@test-id='patient-settlements-search-btn' or @data-test-id='patient-settlements-search-btn']` | `button ()` |
| 7 | **بحث...** | `[test-id="patient-settlements-search-input"]` | `input[data-test-id='patient-settlements-search-input'], input[test-id='patient-settlements-search-input']` | `//input[@test-id='patient-settlements-search-input' or @data-test-id='patient-settlements-search-input']` | `input (text)` |
| 8 | **تصدير إلى إكسيل** | `[test-id="patient-settlements-export-excel-btn"]` | `button[data-test-id='patient-settlements-export-excel-btn'], button[test-id='patient-settlements-export-excel-btn']` | `//button[@test-id='patient-settlements-export-excel-btn' or @data-test-id='patient-settlements-export-excel-btn']` | `button ()` |
