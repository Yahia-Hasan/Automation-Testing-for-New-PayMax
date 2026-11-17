# محددات عناصر صفحة: المرضى بالحضانة (Locators)

- **المسار (Route):** `/reception/neonatal`
- **المكون (Angular Component):** `<app-inpatient-list>`
- **إجمالي عناصر test-id المكتشفة:** `3`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **تحديث** | `[test-id="inpatient-list-refresh-btn"]` | `button[data-test-id='inpatient-list-refresh-btn'], button[test-id='inpatient-list-refresh-btn']` | `//button[@test-id='inpatient-list-refresh-btn' or @data-test-id='inpatient-list-refresh-btn']` | `button ()` |
| 3 | **بحث باسم المريض / كود / طبيب / غرفة...** | `[test-id="inpatient-list-search-input"]` | `input[data-test-id='inpatient-list-search-input'], input[test-id='inpatient-list-search-input']` | `//input[@test-id='inpatient-list-search-input' or @data-test-id='inpatient-list-search-input']` | `input (text)` |
