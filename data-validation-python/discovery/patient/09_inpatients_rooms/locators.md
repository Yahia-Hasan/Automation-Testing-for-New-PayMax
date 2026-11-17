# محددات عناصر صفحة: المرضى بالغرف (Locators)

- **المسار (Route):** `/reception/inpatients`
- **المكون (Angular Component):** `<app-inpatient-list>`
- **إجمالي عناصر test-id المكتشفة:** `7`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **تحديث** | `[test-id="inpatient-list-refresh-btn"]` | `button[data-test-id='inpatient-list-refresh-btn'], button[test-id='inpatient-list-refresh-btn']` | `//button[@test-id='inpatient-list-refresh-btn' or @data-test-id='inpatient-list-refresh-btn']` | `button ()` |
| 3 | **بحث باسم المريض / كود / طبيب / غرفة...** | `[test-id="inpatient-list-search-input"]` | `input[data-test-id='inpatient-list-search-input'], input[test-id='inpatient-list-search-input']` | `//input[@test-id='inpatient-list-search-input' or @data-test-id='inpatient-list-search-input']` | `input (text)` |
| 4 | **11001Royal Suite1شاغر------شاغر** | `[test-id="inpatient-list-row"]` | `tr[data-test-id='inpatient-list-row'], tr[test-id='inpatient-list-row']` | `//tr[@test-id='inpatient-list-row' or @data-test-id='inpatient-list-row']` | `tr ()` |
| 5 | **inpatient-list-details-btn** | `[test-id="inpatient-list-details-btn"]` | `button[data-test-id='inpatient-list-details-btn'], button[test-id='inpatient-list-details-btn']` | `//button[@test-id='inpatient-list-details-btn' or @data-test-id='inpatient-list-details-btn']` | `button ()` |
| 6 | **inpatient-list-barcode-link** | `[test-id="inpatient-list-barcode-link"]` | `a[data-test-id='inpatient-list-barcode-link'], a[test-id='inpatient-list-barcode-link']` | `//a[@test-id='inpatient-list-barcode-link' or @data-test-id='inpatient-list-barcode-link']` | `a ()` |
| 7 | **inpatient-list-bracelet-link** | `[test-id="inpatient-list-bracelet-link"]` | `a[data-test-id='inpatient-list-bracelet-link'], a[test-id='inpatient-list-bracelet-link']` | `//a[@test-id='inpatient-list-bracelet-link' or @data-test-id='inpatient-list-bracelet-link']` | `a ()` |
