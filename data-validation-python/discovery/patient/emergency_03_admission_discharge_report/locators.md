# محددات عناصر صفحة: تقرير الدخول والخروج بالطوارئ (Locators)

- **المسار (Route):** `/emergency/admission-discharge-report`
- **المكون (Angular Component):** `<app-emergency-cases-report>`
- **إجمالي عناصر test-id المكتشفة:** `5`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **emergency-cases-report-from-date-input** | `[test-id="emergency-cases-report-from-date-input"]` | `input[data-test-id='emergency-cases-report-from-date-input'], input[test-id='emergency-cases-report-from-date-input']` | `//input[@test-id='emergency-cases-report-from-date-input' or @data-test-id='emergency-cases-report-from-date-input']` | `input (date)` |
| 3 | **emergency-cases-report-to-date-input** | `[test-id="emergency-cases-report-to-date-input"]` | `input[data-test-id='emergency-cases-report-to-date-input'], input[test-id='emergency-cases-report-to-date-input']` | `//input[@test-id='emergency-cases-report-to-date-input' or @data-test-id='emergency-cases-report-to-date-input']` | `input (date)` |
| 4 | **حالات الدخولحالات الخروجحالات محولة لداخ** | `[test-id="emergency-cases-report-report-type-select"]` | `select[data-test-id='emergency-cases-report-report-type-select'], select[test-id='emergency-cases-report-report-type-select']` | `//select[@test-id='emergency-cases-report-report-type-select' or @data-test-id='emergency-cases-report-report-type-select']` | `select ()` |
| 5 | **عرض** | `[test-id="emergency-cases-report-load-btn"]` | `button[data-test-id='emergency-cases-report-load-btn'], button[test-id='emergency-cases-report-load-btn']` | `//button[@test-id='emergency-cases-report-load-btn' or @data-test-id='emergency-cases-report-load-btn']` | `button ()` |
