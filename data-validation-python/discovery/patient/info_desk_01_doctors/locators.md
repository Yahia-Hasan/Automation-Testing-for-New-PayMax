# محددات عناصر صفحة: بيانات الأطباء (Locators)

- **المسار (Route):** `/info-desk/doctors`
- **المكون (Angular Component):** `<app-doctors-list>`
- **إجمالي عناصر test-id المكتشفة:** `4`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **تصدير إلى إكسيل** | `[test-id="doctors-list-export-excel-btn"]` | `button[data-test-id='doctors-list-export-excel-btn'], button[test-id='doctors-list-export-excel-btn']` | `//button[@test-id='doctors-list-export-excel-btn' or @data-test-id='doctors-list-export-excel-btn']` | `button ()` |
| 3 | **ابحث باسم الطبيب أو التخصص...** | `[test-id="doctors-list-search-input"]` | `input[data-test-id='doctors-list-search-input'], input[test-id='doctors-list-search-input']` | `//input[@test-id='doctors-list-search-input' or @data-test-id='doctors-list-search-input']` | `input (text)` |
| 4 | **doctors-list-active-only-checkbox** | `[test-id="doctors-list-active-only-checkbox"]` | `input[data-test-id='doctors-list-active-only-checkbox'], input[test-id='doctors-list-active-only-checkbox']` | `//input[@test-id='doctors-list-active-only-checkbox' or @data-test-id='doctors-list-active-only-checkbox']` | `input (checkbox)` |
