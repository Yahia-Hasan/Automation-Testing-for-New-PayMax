# محددات عناصر صفحة: الإقامة خلال فترة (Locators)

- **المسار (Route):** `/reports/accommodation-in-duration`
- **المكون الأساسي (Angular Component):** `<app-accommodation-in-duration>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير العام
> شاشة مخصصة ضمن قسم التقارير العامة. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقول إدخال المعايير** | `report-input` | `app-accommodation-in-duration input` | `//app-accommodation-in-duration//input` | `input` |
| 2 | **أزرار الإجراءات والاستعلام** | `report-action-btn` | `app-accommodation-in-duration button` | `//app-accommodation-in-duration//button` | `button` |
| 3 | **جدول عرض البيانات** | `report-table` | `app-accommodation-in-duration table, p-table` | `//app-accommodation-in-duration//table` | `table` |
