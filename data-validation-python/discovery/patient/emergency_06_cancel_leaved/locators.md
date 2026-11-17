# محددات عناصر صفحة: إلغاء خروج مريض طوارئ تم إغلاقها (Locators)

- **المسار (Route):** `/emergency/cancel-leaved`
- **المكون (Angular Component):** `<app-cancel-leaved-emergency>`
- **إجمالي عناصر test-id المكتشفة:** `4`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **cancel-leaved-emergency-from-date-input** | `[test-id="cancel-leaved-emergency-from-date-input"]` | `input[data-test-id='cancel-leaved-emergency-from-date-input'], input[test-id='cancel-leaved-emergency-from-date-input']` | `//input[@test-id='cancel-leaved-emergency-from-date-input' or @data-test-id='cancel-leaved-emergency-from-date-input']` | `input (date)` |
| 3 | **cancel-leaved-emergency-to-date-input** | `[test-id="cancel-leaved-emergency-to-date-input"]` | `input[data-test-id='cancel-leaved-emergency-to-date-input'], input[test-id='cancel-leaved-emergency-to-date-input']` | `//input[@test-id='cancel-leaved-emergency-to-date-input' or @data-test-id='cancel-leaved-emergency-to-date-input']` | `input (date)` |
| 4 | **عرض** | `[test-id="cancel-leaved-emergency-load-btn"]` | `button[data-test-id='cancel-leaved-emergency-load-btn'], button[test-id='cancel-leaved-emergency-load-btn']` | `//button[@test-id='cancel-leaved-emergency-load-btn' or @data-test-id='cancel-leaved-emergency-load-btn']` | `button ()` |
