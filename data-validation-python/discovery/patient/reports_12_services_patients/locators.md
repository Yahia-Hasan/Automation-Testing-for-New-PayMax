# محددات عناصر صفحة: خدمات المرضى خلال فترة (Locators)

- **المسار (Route):** `/reports/services-patients`
- **المكون الأساسي (Angular Component):** `<app-services-patients>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-services-patients input` | `//app-services-patients//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-services-patients button` | `//app-services-patients//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-services-patients table, p-table` | `//app-services-patients//table` | `table` |
