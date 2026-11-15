# محددات عناصر صفحة: موقف تنفيذ حالات الأشعة وطباعة الاستيكر (Locators)

- **المسار (Route):** `/rays/status`
- **المكون (Angular Component):** `<app-rays-status>`
- **إجمالي عناصر test-id المكتشفة:** `10`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **rays-status-from-date-input** | `[test-id="rays-status-from-date-input"]` | `input[data-test-id='rays-status-from-date-input'], input[test-id='rays-status-from-date-input']` | `//input[@test-id='rays-status-from-date-input' or @data-test-id='rays-status-from-date-input']` | `input (date)` |
| 3 | **rays-status-to-date-input** | `[test-id="rays-status-to-date-input"]` | `input[data-test-id='rays-status-to-date-input'], input[test-id='rays-status-to-date-input']` | `//input[@test-id='rays-status-to-date-input' or @data-test-id='rays-status-to-date-input']` | `input (date)` |
| 4 | **الكلداخليطوارئخارجي** | `[test-id="rays-status-patient-type-select"]` | `select[data-test-id='rays-status-patient-type-select'], select[test-id='rays-status-patient-type-select']` | `//select[@test-id='rays-status-patient-type-select' or @data-test-id='rays-status-patient-type-select']` | `select ()` |
| 5 | **الكلتم التنفيذلم ينفذ** | `[test-id="rays-status-status-select"]` | `select[data-test-id='rays-status-status-select'], select[test-id='rays-status-status-select']` | `//select[@test-id='rays-status-status-select' or @data-test-id='rays-status-status-select']` | `select ()` |
| 6 | **أشعةتحاليل** | `[test-id="rays-status-service-group-select"]` | `select[data-test-id='rays-status-service-group-select'], select[test-id='rays-status-service-group-select']` | `//select[@test-id='rays-status-service-group-select' or @data-test-id='rays-status-service-group-select']` | `select ()` |
| 7 | **عرض** | `[test-id="rays-status-search-btn"]` | `button[data-test-id='rays-status-search-btn'], button[test-id='rays-status-search-btn']` | `//button[@test-id='rays-status-search-btn' or @data-test-id='rays-status-search-btn']` | `button ()` |
| 8 | **طباعة** | `[test-id="rays-status-print-btn"]` | `button[data-test-id='rays-status-print-btn'], button[test-id='rays-status-print-btn']` | `//button[@test-id='rays-status-print-btn' or @data-test-id='rays-status-print-btn']` | `button ()` |
| 9 | **بحث...** | `[test-id="rays-status-search-input"]` | `input[data-test-id='rays-status-search-input'], input[test-id='rays-status-search-input']` | `//input[@test-id='rays-status-search-input' or @data-test-id='rays-status-search-input']` | `input (text)` |
| 10 | **تصدير إلى إكسيل** | `[test-id="rays-status-export-excel-btn"]` | `button[data-test-id='rays-status-export-excel-btn'], button[test-id='rays-status-export-excel-btn']` | `//button[@test-id='rays-status-export-excel-btn' or @data-test-id='rays-status-export-excel-btn']` | `button ()` |
