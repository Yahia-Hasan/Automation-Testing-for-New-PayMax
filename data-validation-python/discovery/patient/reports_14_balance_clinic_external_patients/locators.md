# محددات عناصر صفحة: تحليل الايرادات الخارجي خلال فترة (Locators)

- **المسار (Route):** `/reports/balance-clinic-external-patients`
- **المكون الأساسي (Angular Component):** `<app-balance-clinic-external-patients>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-balance-clinic-external-patients input` | `//app-balance-clinic-external-patients//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-balance-clinic-external-patients button` | `//app-balance-clinic-external-patients//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-balance-clinic-external-patients table, p-table` | `//app-balance-clinic-external-patients//table` | `table` |
