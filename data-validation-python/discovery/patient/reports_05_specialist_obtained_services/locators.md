# محددات عناصر صفحة: الخدمات حسب التخصص (Locators)

- **المسار (Route):** `/reports/specialist-obtained-services`
- **المكون الأساسي (Angular Component):** `<app-specialist-obtained-services>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-specialist-obtained-services input` | `//app-specialist-obtained-services//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-specialist-obtained-services button` | `//app-specialist-obtained-services//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-specialist-obtained-services table, p-table` | `//app-specialist-obtained-services//table` | `table` |
