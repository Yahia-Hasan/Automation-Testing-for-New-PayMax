# محددات عناصر صفحة: تعديل زيارة بالطوارئ (Locators)

- **المسار (Route):** `/emergency/edit-visit`
- **المكون (Angular Component):** `<app-edit-emergency-visit>`
- **إجمالي عناصر test-id المكتشفة:** `4`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **edit-emergency-visit-from-date-input** | `[test-id="edit-emergency-visit-from-date-input"]` | `input[data-test-id='edit-emergency-visit-from-date-input'], input[test-id='edit-emergency-visit-from-date-input']` | `//input[@test-id='edit-emergency-visit-from-date-input' or @data-test-id='edit-emergency-visit-from-date-input']` | `input (date)` |
| 3 | **edit-emergency-visit-to-date-input** | `[test-id="edit-emergency-visit-to-date-input"]` | `input[data-test-id='edit-emergency-visit-to-date-input'], input[test-id='edit-emergency-visit-to-date-input']` | `//input[@test-id='edit-emergency-visit-to-date-input' or @data-test-id='edit-emergency-visit-to-date-input']` | `input (date)` |
| 4 | **عرض** | `[test-id="edit-emergency-visit-load-btn"]` | `button[data-test-id='edit-emergency-visit-load-btn'], button[test-id='edit-emergency-visit-load-btn']` | `//button[@test-id='edit-emergency-visit-load-btn' or @data-test-id='edit-emergency-visit-load-btn']` | `button ()` |
