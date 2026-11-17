# محددات عناصر صفحة: تسويات الأطباء (Locators)

- **المسار (Route):** `/reports/doctors-settlements`
- **المكون الأساسي (Angular Component):** `<app-doctors-settlements>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-doctors-settlements input` | `//app-doctors-settlements//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-doctors-settlements button` | `//app-doctors-settlements//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-doctors-settlements table, p-table` | `//app-doctors-settlements//table` | `table` |
