# محددات عناصر صفحة: إدارة الغرف (Locators)

- **المسار (Route):** `/reception/room-management`
- **المكون (Angular Component):** `<app-room-management>`
- **إجمالي عناصر test-id المكتشفة:** `7`

---

| # | اسم العنصر | الأولوية الأولى (`test-id`) | أفضل بديل (CSS Selector) | محدد XPath الاحتياطي | نوع الحقل |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **global-toast-stack** | `[test-id="global-toast-stack"]` | `div[data-test-id='global-toast-stack'], div[test-id='global-toast-stack']` | `//div[@test-id='global-toast-stack' or @data-test-id='global-toast-stack']` | `div ()` |
| 2 | **الإقامة** | `[test-id="room-management-rooms-tab-btn"]` | `button[data-test-id='room-management-rooms-tab-btn'], button[test-id='room-management-rooms-tab-btn']` | `//button[@test-id='room-management-rooms-tab-btn' or @data-test-id='room-management-rooms-tab-btn']` | `button ()` |
| 3 | **الرعاية المركزة** | `[test-id="room-management-icu-tab-btn"]` | `button[data-test-id='room-management-icu-tab-btn'], button[test-id='room-management-icu-tab-btn']` | `//button[@test-id='room-management-icu-tab-btn' or @data-test-id='room-management-icu-tab-btn']` | `button ()` |
| 4 | **الحضانة** | `[test-id="room-management-neonatal-tab-btn"]` | `button[data-test-id='room-management-neonatal-tab-btn'], button[test-id='room-management-neonatal-tab-btn']` | `//button[@test-id='room-management-neonatal-tab-btn' or @data-test-id='room-management-neonatal-tab-btn']` | `button ()` |
| 5 | **بحث بالغرفة أو الدور أو الدرجة...** | `[test-id="room-management-search-input"]` | `input[data-test-id='room-management-search-input'], input[test-id='room-management-search-input']` | `//input[@test-id='room-management-search-input' or @data-test-id='room-management-search-input']` | `input (text)` |
| 6 | **BasementB01POST Cath CCUمتاحةعرض** | `[test-id="room-management-row"]` | `tr[data-test-id='room-management-row'], tr[test-id='room-management-row']` | `//tr[@test-id='room-management-row' or @data-test-id='room-management-row']` | `tr ()` |
| 7 | **عرض** | `[test-id="room-management-show-details-btn"]` | `button[data-test-id='room-management-show-details-btn'], button[test-id='room-management-show-details-btn']` | `//button[@test-id='room-management-show-details-btn' or @data-test-id='room-management-show-details-btn']` | `button ()` |
