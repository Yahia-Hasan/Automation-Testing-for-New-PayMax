# محددات عناصر صفحة: مطالبات خدمات جهة (Locators)

- **المسار (Route):** `/reports/client-obtained-services`
- **المكون الأساسي (Angular Component):** `<app-client-obtained-services>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-client-obtained-services input` | `//app-client-obtained-services//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-client-obtained-services button` | `//app-client-obtained-services//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-client-obtained-services table, p-table` | `//app-client-obtained-services//table` | `table` |
