# محددات عناصر صفحة: حسابات المرضى الداخلي (Locators)

- **المسار (Route):** `/patient-accounts/patient-checkups`
- **المكون (Angular Component):** `<app-patient-checkups>`
- **إجمالي عناصر test-id المكتشفة:** `6`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **patient-checkups-from-date-input** | `[test-id="patient-checkups-from-date-input"]` | `input[data-test-id='patient-checkups-from-date-input'], input[test-id='patient-checkups-from-date-input']` | `//input[@test-id='patient-checkups-from-date-input' or @data-test-id='patient-checkups-from-date-input']` | `input (date)` |
| 3 | **patient-checkups-to-date-input** | `[test-id="patient-checkups-to-date-input"]` | `input[data-test-id='patient-checkups-to-date-input'], input[test-id='patient-checkups-to-date-input']` | `//input[@test-id='patient-checkups-to-date-input' or @data-test-id='patient-checkups-to-date-input']` | `input (date)` |
| 4 | **بحث** | `[test-id="patient-checkups-search-btn"]` | `button[data-test-id='patient-checkups-search-btn'], button[test-id='patient-checkups-search-btn']` | `//button[@test-id='patient-checkups-search-btn' or @data-test-id='patient-checkups-search-btn']` | `button ()` |
| 5 | **بحث...** | `[test-id="patient-checkups-search-input"]` | `input[data-test-id='patient-checkups-search-input'], input[test-id='patient-checkups-search-input']` | `//input[@test-id='patient-checkups-search-input' or @data-test-id='patient-checkups-search-input']` | `input (text)` |
| 6 | **تصدير إلى إكسيل** | `[test-id="patient-checkups-export-excel-btn"]` | `button[data-test-id='patient-checkups-export-excel-btn'], button[test-id='patient-checkups-export-excel-btn']` | `//button[@test-id='patient-checkups-export-excel-btn' or @data-test-id='patient-checkups-export-excel-btn']` | `button ()` |
