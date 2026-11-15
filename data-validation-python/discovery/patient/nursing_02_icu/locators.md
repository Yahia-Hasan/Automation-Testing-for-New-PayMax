# محددات عناصر صفحة: المرضى بالرعاية المركزة (تمريض) (Locators)

- **المسار (Route):** `/waiting-list/icu`
- **المكون (Angular Component):** `<app-nursing-secretary>`
- **إجمالي عناصر test-id المكتشفة:** `7`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **تحديث** | `[test-id="nursing-secretary-reload-btn"]` | `button[data-test-id='nursing-secretary-reload-btn'], button[test-id='nursing-secretary-reload-btn']` | `//button[@test-id='nursing-secretary-reload-btn' or @data-test-id='nursing-secretary-reload-btn']` | `button ()` |
| 3 | **بحث باسم المريض / كود / طبيب / غرفة...** | `[test-id="nursing-secretary-search-input"]` | `input[data-test-id='nursing-secretary-search-input'], input[test-id='nursing-secretary-search-input']` | `//input[@test-id='nursing-secretary-search-input' or @data-test-id='nursing-secretary-search-input']` | `input (text)` |
| 4 | **nursing-secretary-bed-actions-btn** | `[test-id="nursing-secretary-bed-actions-btn"]` | `button[data-test-id='nursing-secretary-bed-actions-btn'], button[test-id='nursing-secretary-bed-actions-btn']` | `//button[@test-id='nursing-secretary-bed-actions-btn' or @data-test-id='nursing-secretary-bed-actions-btn']` | `button (button)` |
| 5 | **nursing-secretary-vip-checkbox** | `[test-id="nursing-secretary-vip-checkbox"]` | `input[data-test-id='nursing-secretary-vip-checkbox'], input[test-id='nursing-secretary-vip-checkbox']` | `//input[@test-id='nursing-secretary-vip-checkbox' or @data-test-id='nursing-secretary-vip-checkbox']` | `input (checkbox)` |
| 6 | **nursing-secretary-can-visit-checkbox** | `[test-id="nursing-secretary-can-visit-checkbox"]` | `input[data-test-id='nursing-secretary-can-visit-checkbox'], input[test-id='nursing-secretary-can-visit-checkbox']` | `//input[@test-id='nursing-secretary-can-visit-checkbox' or @data-test-id='nursing-secretary-can-visit-checkbox']` | `input (checkbox)` |
| 7 | **اشعار بالخروج** | `[test-id="nursing-secretary-inform-exit-btn"]` | `button[data-test-id='nursing-secretary-inform-exit-btn'], button[test-id='nursing-secretary-inform-exit-btn']` | `//button[@test-id='nursing-secretary-inform-exit-btn' or @data-test-id='nursing-secretary-inform-exit-btn']` | `button ()` |
