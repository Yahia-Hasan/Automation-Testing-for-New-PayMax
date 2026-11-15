# محددات عناصر صفحة: تقرير إشغال المستشفى (Locators)

- **المسار (Route):** `/reception/occupancy-report`
- **المكون (Angular Component):** `<app-occupancy-report>`
- **إجمالي عناصر test-id المكتشفة:** `9`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | ملاحظات |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **تقرير الإشغال بالأدوار** | `[test-id="occupancy-report-by-floor-btn"]` | `button[data-test-id='occupancy-report-by-floor-btn'], button[test-id='occupancy-report-by-floor-btn']` | `//button[@test-id='occupancy-report-by-floor-btn' or @data-test-id='occupancy-report-by-floor-btn']` | `button ()` |
| 3 | **تقرير الإشغال بالغرف** | `[test-id="occupancy-report-by-room-btn"]` | `button[data-test-id='occupancy-report-by-room-btn'], button[test-id='occupancy-report-by-room-btn']` | `//button[@test-id='occupancy-report-by-room-btn' or @data-test-id='occupancy-report-by-room-btn']` | `button ()` |
| 4 | **تقرير قوة المستشفي** | `[test-id="occupancy-report-rates-btn"]` | `button[data-test-id='occupancy-report-rates-btn'], button[test-id='occupancy-report-rates-btn']` | `//button[@test-id='occupancy-report-rates-btn' or @data-test-id='occupancy-report-rates-btn']` | `button ()` |
| 5 | **occupancy-report-empty-only-checkbox** | `[test-id="occupancy-report-empty-only-checkbox"]` | `input[data-test-id='occupancy-report-empty-only-checkbox'], input[test-id='occupancy-report-empty-only-checkbox']` | `//input[@test-id='occupancy-report-empty-only-checkbox' or @data-test-id='occupancy-report-empty-only-checkbox']` | `input (checkbox)` |
| 6 | **occupancy-report-active-rooms-only-check** | `[test-id="occupancy-report-active-rooms-only-checkbox"]` | `input[data-test-id='occupancy-report-active-rooms-only-checkbox'], input[test-id='occupancy-report-active-rooms-only-checkbox']` | `//input[@test-id='occupancy-report-active-rooms-only-checkbox' or @data-test-id='occupancy-report-active-rooms-only-checkbox']` | `input (checkbox)` |
| 7 | **بحث باسم المريض / الكود / الطبيب / الغرف** | `[test-id="occupancy-report-patient-search-input"]` | `input[data-test-id='occupancy-report-patient-search-input'], input[test-id='occupancy-report-patient-search-input']` | `//input[@test-id='occupancy-report-patient-search-input' or @data-test-id='occupancy-report-patient-search-input']` | `input (text)` |
| 8 | **تحديث** | `[test-id="occupancy-report-refresh-btn"]` | `button[data-test-id='occupancy-report-refresh-btn'], button[test-id='occupancy-report-refresh-btn']` | `//button[@test-id='occupancy-report-refresh-btn' or @data-test-id='occupancy-report-refresh-btn']` | `button ()` |
| 9 | **تصدير إلى إكسيل** | `[test-id="occupancy-report-export-excel-btn"]` | `button[data-test-id='occupancy-report-export-excel-btn'], button[test-id='occupancy-report-export-excel-btn']` | `//button[@test-id='occupancy-report-export-excel-btn' or @data-test-id='occupancy-report-export-excel-btn']` | `button ()` |
