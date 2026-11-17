# محددات عناصر صفحة: إلغاء خروج مريض عيادات مُغلقة (Locators)

- **المسار (Route):** `/clinic/cancel-leaved-visit`
- **المكون (Angular Component):** `<app-cancel-leaved-visit>`
- **إجمالي عناصر test-id المكتشفة:** `4`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **cancel-leaved-visit-from-date-input** | `[test-id="cancel-leaved-visit-from-date-input"]` | `input[data-test-id='cancel-leaved-visit-from-date-input'], input[test-id='cancel-leaved-visit-from-date-input']` | `//input[@test-id='cancel-leaved-visit-from-date-input' or @data-test-id='cancel-leaved-visit-from-date-input']` | `input (date)` |
| 3 | **cancel-leaved-visit-to-date-input** | `[test-id="cancel-leaved-visit-to-date-input"]` | `input[data-test-id='cancel-leaved-visit-to-date-input'], input[test-id='cancel-leaved-visit-to-date-input']` | `//input[@test-id='cancel-leaved-visit-to-date-input' or @data-test-id='cancel-leaved-visit-to-date-input']` | `input (date)` |
| 4 | **عرض** | `[test-id="cancel-leaved-visit-search-btn"]` | `button[data-test-id='cancel-leaved-visit-search-btn'], button[test-id='cancel-leaved-visit-search-btn']` | `//button[@test-id='cancel-leaved-visit-search-btn' or @data-test-id='cancel-leaved-visit-search-btn']` | `button ()` |
