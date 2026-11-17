# محددات عناصر صفحة: مبيعات العيادات اجمالى (Locators)

- **المسار (Route):** `/reports/opd-sales-report`
- **المكون الأساسي (Angular Component):** `<app-extended-report-page>`

---

> [!NOTE] طبيعة محرك التقارير (Generic Dynamic Report Engine)
> هذه الصفحة تُبنى ديناميكياً عبر مكون التقارير الموحد `<app-extended-report-page>`. الحقول والفلاتر تعتمد على كلاسات مستقرة (`.btn-query`, `.checkbox-multi-trigger`, `.btn-back`). نوصي المطورين بإضافة `data-test-id` مخصص لكل فلتر.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **زر الرجوع للتقارير** | `[data-test-id="report-back-btn"]` | `a.btn-back` | `//a[contains(@class,'btn-back')]` | `link` |
| 2 | **تاريخ البداية (من)** | `[data-test-id="report-date-from"]` | `.filters-grid input[type='date'], .filters-grid input:nth-of-type(1)` | `(//div[contains(@class,'filters-grid')]//input)[1]` | `input (date)` |
| 3 | **تاريخ النهاية (إلى)** | `[data-test-id="report-date-to"]` | `.filters-grid input:nth-of-type(2)` | `(//div[contains(@class,'filters-grid')]//input)[2]` | `input (date)` |
| 4 | **زر استعلام / عرض التقرير** | `[data-test-id="report-query-btn"]` | `button.btn-query` | `//button[contains(@class,'btn-query')]` | `button` |
| 5 | **فلاتر الاختيار المتعدد** | `[data-test-id="report-multi-select"]` | `button.checkbox-multi-trigger` | `//button[contains(@class,'checkbox-multi-trigger')]` | `dropdown trigger` |
| 6 | **القوائم المنسدلة للبحث** | `[data-test-id="report-single-select"]` | `ng-select.ng-select-sm` | `//ng-select[contains(@class,'ng-select-sm')]` | `ng-select` |
| 7 | **جدول نتائج التقرير** | `[data-test-id="report-results-table"]` | `.report-table, p-table, table` | `//table` | `table` |
