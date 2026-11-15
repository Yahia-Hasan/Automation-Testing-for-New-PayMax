# محددات عناصر صفحة: كل التقارير التحليلية (Locators)

- **المسار (Route):** `/reports/analytical`
- **المكون الأساسي (Angular Component):** `<app-analytical-reports>`

---

> [!NOTE] حالة الـ test-id ومحرك التقارير
> شاشة مخصصة ضمن قسم التقارير التحليلية. تم رصد 0 عنصر يحمل `test-id` صريح.

| # | العنصر | المقترح المطلوب (`test-id`) | أفضل محدد حالي (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **حقل البحث في التقارير التحليلية** | `analytical-search-input` | `input.search-input, input[type='search'], .p-inputtext` | `//input[contains(@class,'search-input') or contains(@class,'p-inputtext')]` | `input` |
| 2 | **بطاقات التقارير التحليلية** | `analytical-report-card` | `.report-card, .card-item, a.report-link` | `//div[contains(@class,'card')]//a` | `card / link` |
