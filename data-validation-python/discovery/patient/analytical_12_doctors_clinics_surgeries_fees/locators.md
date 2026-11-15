# محددات عناصر صفحة: أتعاب الأطباء (عيادات + عمليات) (Locators)

- **المسار (Route):** `/reports/doctors-clinics-surgeries-fees`
- **المكون الأساسي (Angular Component):** `<app-extended-report-page>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير
> تعتمد هذه الصفحة على محرك التقارير الديناميكي الموحد Extended Report Engine. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **زر الرجوع للتقارير التحليلية** | `report-back-btn` | `a.btn-back` | `//a[contains(@class,'btn-back')]` | `link` |
| 2 | **تاريخ البداية (من)** | `report-date-from` | `.filters-grid input[type='date'], .filters-grid input:nth-of-type(1)` | `(//div[contains(@class,'filters-grid')]//input)[1]` | `input (date)` |
| 3 | **تاريخ النهاية (إلى)** | `report-date-to` | `.filters-grid input:nth-of-type(2)` | `(//div[contains(@class,'filters-grid')]//input)[2]` | `input (date)` |
| 4 | **زر استعلام / عرض التقرير** | `report-query-btn` | `button.btn-query` | `//button[contains(@class,'btn-query')]` | `button` |
| 5 | **فلاتر الاختيار المتعدد (الأقسام/الجهات)** | `report-multi-select` | `button.checkbox-multi-trigger` | `//button[contains(@class,'checkbox-multi-trigger')]` | `dropdown trigger` |
| 6 | **القوائم المنسدلة للبحث (الأطباء/العيادات)** | `report-single-select` | `ng-select.ng-select-sm` | `//ng-select[contains(@class,'ng-select-sm')]` | `ng-select` |
| 7 | **جدول نتائج التقرير** | `report-results-table` | `.report-table, p-table, table` | `//table` | `table` |
