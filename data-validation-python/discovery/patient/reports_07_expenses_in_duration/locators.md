# محددات عناصر صفحة: المصروفات خلال فترة (Locators)

- **المسار (Route):** `/reports/expenses-in-duration`
- **المكون الأساسي (Angular Component):** `<app-expenses-in-duration>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-expenses-in-duration input` | `//app-expenses-in-duration//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-expenses-in-duration button` | `//app-expenses-in-duration//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-expenses-in-duration table, p-table` | `//app-expenses-in-duration//table` | `table` |
