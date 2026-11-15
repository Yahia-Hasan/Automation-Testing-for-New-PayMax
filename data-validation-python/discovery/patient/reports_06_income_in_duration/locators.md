# محددات عناصر صفحة: حركات الخزينة (Locators)

- **المسار (Route):** `/reports/income-in-duration`
- **المكون الأساسي (Angular Component):** `<app-income-in-duration>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-income-in-duration input` | `//app-income-in-duration//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-income-in-duration button` | `//app-income-in-duration//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-income-in-duration table, p-table` | `//app-income-in-duration//table` | `table` |
