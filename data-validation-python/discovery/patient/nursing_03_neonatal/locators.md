# محددات عناصر صفحة: المرضى بالحضانة (تمريض) (Locators)

- **المسار (Route):** `/waiting-list/neonatal`
- **المكون (Angular Component):** `<app-nursing-secretary>`
- **إجمالي عناصر test-id المكتشفة:** `3`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **تحديث** | `[test-id="nursing-secretary-reload-btn"]` | `button[data-test-id='nursing-secretary-reload-btn'], button[test-id='nursing-secretary-reload-btn']` | `//button[@test-id='nursing-secretary-reload-btn' or @data-test-id='nursing-secretary-reload-btn']` | `button ()` |
| 3 | **بحث باسم المريض / كود / طبيب / غرفة...** | `[test-id="nursing-secretary-search-input"]` | `input[data-test-id='nursing-secretary-search-input'], input[test-id='nursing-secretary-search-input']` | `//input[@test-id='nursing-secretary-search-input' or @data-test-id='nursing-secretary-search-input']` | `input (text)` |
