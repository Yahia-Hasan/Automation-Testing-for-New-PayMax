# محددات عناصر صفحة: دليل الهاتف (Locators)

- **المسار (Route):** `/info-desk/phone-book`
- **المكون (Angular Component):** `<app-phone-book-info-desk>`
- **إجمالي عناصر test-id المكتشفة:** `2`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **إضافة جديد** | `[test-id="phone-book-add-new-btn"]` | `button[data-test-id='phone-book-add-new-btn'], button[test-id='phone-book-add-new-btn']` | `//button[@test-id='phone-book-add-new-btn' or @data-test-id='phone-book-add-new-btn']` | `button ()` |
