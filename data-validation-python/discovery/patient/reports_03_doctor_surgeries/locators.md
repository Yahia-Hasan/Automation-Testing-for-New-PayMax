# محددات عناصر صفحة: عمليات طبيب (Locators)

- **المسار (Route):** `/reports/doctor-surgeries`
- **المكون الأساسي (Angular Component):** `<app-doctor-surgeries>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-doctor-surgeries input` | `//app-doctor-surgeries//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-doctor-surgeries button` | `//app-doctor-surgeries//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-doctor-surgeries table, p-table` | `//app-doctor-surgeries//table` | `table` |
