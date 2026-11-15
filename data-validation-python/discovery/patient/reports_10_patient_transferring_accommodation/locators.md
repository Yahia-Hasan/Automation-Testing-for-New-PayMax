# محددات عناصر صفحة: إقامات المريض داخل المستشفى (Locators)

- **المسار (Route):** `/reports/patient-transferring-accommodation`
- **المكون الأساسي (Angular Component):** `<app-patient-transferring-accommodation>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-patient-transferring-accommodation input` | `//app-patient-transferring-accommodation//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-patient-transferring-accommodation button` | `//app-patient-transferring-accommodation//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-patient-transferring-accommodation table, p-table` | `//app-patient-transferring-accommodation//table` | `table` |
