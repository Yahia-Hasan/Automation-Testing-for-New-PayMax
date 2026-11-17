# محددات عناصر صفحة: أتعاب طبيب (Locators)

- **المسار (Route):** `/reports/doctor-fees`
- **المكون الأساسي (Angular Component):** `<app-doctor-fees>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-doctor-fees input` | `//app-doctor-fees//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-doctor-fees button` | `//app-doctor-fees//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-doctor-fees table, p-table` | `//app-doctor-fees//table` | `table` |
