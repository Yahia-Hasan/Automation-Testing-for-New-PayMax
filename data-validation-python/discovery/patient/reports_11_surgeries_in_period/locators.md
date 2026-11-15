# محددات عناصر صفحة: تقرير بالعمليات خلال فترة (Locators)

- **المسار (Route):** `/reports/surgeries-in-period`
- **المكون الأساسي (Angular Component):** `<app-surgeries-in-period>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-surgeries-in-period input` | `//app-surgeries-in-period//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-surgeries-in-period button` | `//app-surgeries-in-period//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-surgeries-in-period table, p-table` | `//app-surgeries-in-period//table` | `table` |
