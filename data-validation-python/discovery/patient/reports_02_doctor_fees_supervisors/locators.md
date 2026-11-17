# محددات عناصر صفحة: أتعاب مرور الاستشاريين (Locators)

- **المسار (Route):** `/reports/doctor-fees-supervisors`
- **المكون الأساسي (Angular Component):** `<app-doctor-fees-supervisors>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-doctor-fees-supervisors input` | `//app-doctor-fees-supervisors//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-doctor-fees-supervisors button` | `//app-doctor-fees-supervisors//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-doctor-fees-supervisors table, p-table` | `//app-doctor-fees-supervisors//table` | `table` |
