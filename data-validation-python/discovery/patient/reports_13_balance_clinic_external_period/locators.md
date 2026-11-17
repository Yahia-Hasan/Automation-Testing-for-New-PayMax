# محددات عناصر صفحة: تحليل الايرادات الطوارئ خلال فترة (Locators)

- **المسار (Route):** `/reports/balance-clinic-external-period`
- **المكون الأساسي (Angular Component):** `<app-balance-clinic-external-period>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-balance-clinic-external-period input` | `//app-balance-clinic-external-period//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-balance-clinic-external-period button` | `//app-balance-clinic-external-period//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-balance-clinic-external-period table, p-table` | `//app-balance-clinic-external-period//table` | `table` |
