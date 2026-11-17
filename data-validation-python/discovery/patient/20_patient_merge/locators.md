# محددات عناصر صفحة: دمج بين المرضى (Locators)

- **المسار (Route):** `/patient-accounts/merge-patients`
- **المكون (Angular Component):** `<app-merge-patients>`
- **إجمالي عناصر test-id المكتشفة:** `4`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **أدخل كود المريض المصدر** | `[test-id="merge-patients-code-from-input"]` | `input[data-test-id='merge-patients-code-from-input'], input[test-id='merge-patients-code-from-input']` | `//input[@test-id='merge-patients-code-from-input' or @data-test-id='merge-patients-code-from-input']` | `input (number)` |
| 3 | **أدخل كود المريض الهدف** | `[test-id="merge-patients-code-to-input"]` | `input[data-test-id='merge-patients-code-to-input'], input[test-id='merge-patients-code-to-input']` | `//input[@test-id='merge-patients-code-to-input' or @data-test-id='merge-patients-code-to-input']` | `input (number)` |
| 4 | **تنفيذ الدمج** | `[test-id="merge-patients-merge-btn"]` | `button[data-test-id='merge-patients-merge-btn'], button[test-id='merge-patients-merge-btn']` | `//button[@test-id='merge-patients-merge-btn' or @data-test-id='merge-patients-merge-btn']` | `button ()` |
