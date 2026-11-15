# محددات عناصر الـ Navbar (Locators Strategy)

تاريخ التحديث: 2026-11-07  
المكون: `TopNavbarComponent` (قائمة مكتب الدخول والقوائم المجاورة)

---

> [!WARNING] تنبيه للمطورين (Missing test-id)
> عناصر الـ Navbar الحالية (الأزرار والروابط المنسدلة) **لا تحتوي على خاصية `test-id` أو `data-test-id`**. تم وضع مقترح واضح لما نطلبه من المطورين لإضافته في العمود الأول، مع توفير أفضل البدائل الحالية (CSS و XPath).

---

## 1. أزرار القوائم الرئيسية (Navbar Dropdown Triggers)

| العنصر | المقترح المطلوب من الـ Devs (`test-id`) | أفضل بديل حالي (CSS Selector) | محدد الـ XPath الاحتياطي | ملاحظات |
| :--- | :--- | :--- | :--- | :--- |
| **شعار PayMax** | `[data-test-id="navbar-brand"]` | `header.top-navbar a.navbar-brand` | `//header[contains(@class,'top-navbar')]//a[contains(@class,'navbar-brand')]` | يعيد المستخدم إلى الـ Landing Page القديمة |
| **زر مكتب الدخول** | `[data-test-id="nav-dropdown-reception-btn"]` | `header.top-navbar .nav-dropdown:nth-child(1) button.nav-group-btn` | `//header//button[contains(@class,'nav-group-btn')][.//span[contains(text(),'مكتب الدخول')]]` | يفتح/يغلق القائمة المنسدلة (لا يفتح بالـ Hover) |
| **زر الاستعلامات** | `[data-test-id="nav-dropdown-info-desk-btn"]` | `header.top-navbar .nav-dropdown:nth-child(2) button.nav-group-btn` | `//header//button[contains(@class,'nav-group-btn')][.//span[contains(text(),'الاستعلامات')]]` | القائمة الثانية من اليمين |
| **زر المرضى المقيمين** | `[data-test-id="nav-dropdown-inpatients-btn"]` | `header.top-navbar .nav-dropdown:nth-child(3) button.nav-group-btn` | `//header//button[contains(@class,'nav-group-btn')][.//span[contains(text(),'المرضى المقيمين')]]` | القائمة الثالثة من اليمين |
| **حاوية القائمة المفتوحة** | `[data-test-id="nav-dropdown-reception-menu"]` | `header.top-navbar .nav-dropdown.open .dropdown-menu` | `//div[contains(@class,'nav-dropdown') and contains(@class,'open')]//div[contains(@class,'dropdown-menu')]` | لا تظهر العناصر إلا عندما يحمل الـ Parent كلاس `.open` |

---

## 2. عناصر قائمة مكتب الدخول (Reception Dropdown Items - 8 DDLs)

| # | الصفحة المستهدفة | المقترح المطلوب (`test-id`) | أفضل بديل حالي (CSS عبر `href`) | محدد الـ XPath الاحتياطي |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **الملف الطبى** | `[data-test-id="nav-link-reception-medical-file"]` | `a.dropdown-item[href="/reception"]` | `//div[contains(@class,'open')]//a[contains(@class,'dropdown-item') and @href='/reception']` |
| **2** | **تقرير إشغال المستشفى** | `[data-test-id="nav-link-occupancy-report"]` | `a.dropdown-item[href="/reception/occupancy-report"]` | `//div[contains(@class,'open')]//a[contains(@class,'dropdown-item') and @href='/reception/occupancy-report']` |
| **3** | **تقرير الدخول والخروج** | `[data-test-id="nav-link-admission-discharge-report"]` | `a.dropdown-item[href="/reception/admission-discharge-report"]` | `//div[contains(@class,'open')]//a[contains(@class,'dropdown-item') and @href='/reception/admission-discharge-report']` |
| **4** | **حجز العمليات** | `[data-test-id="nav-link-surgery-booking"]` | `a.dropdown-item[href="/reception/surgery-booking"]` | `//div[contains(@class,'open')]//a[contains(@class,'dropdown-item') and @href='/reception/surgery-booking']` |
| **5** | **المرضى الداخلي قيد الخروج** | `[data-test-id="nav-link-inpatients-leaving-requests"]` | `a.dropdown-item[href="/waiting-list/leaving-requests"]` | `//div[contains(@class,'open')]//a[contains(@class,'dropdown-item') and @href='/waiting-list/leaving-requests']` |
| **6** | **طلبات خروج المرضى** | `[data-test-id="nav-link-accountant-leaving-requests"]` | `a.dropdown-item[href="/accountant/leaving-requests"]` | `//div[contains(@class,'open')]//a[contains(@class,'dropdown-item') and @href='/accountant/leaving-requests']` |
| **7** | **طلبات تحويل المرضى من الطوارئ** | `[data-test-id="nav-link-emergency-transfers"]` | `a.dropdown-item[href="/reception/emergency-transfers"]` | `//div[contains(@class,'open')]//a[contains(@class,'dropdown-item') and @href='/reception/emergency-transfers']` |
| **8** | **تقرير تأكيد طلبات المغادرة** | `[data-test-id="nav-link-leaving-approval-report"]` | `a.dropdown-item[href="/reception/leaving-approval-report"]` | `//div[contains(@class,'open')]//a[contains(@class,'dropdown-item') and @href='/reception/leaving-approval-report']` |

---

## 3. عناصر الجانب الأيسر (Navbar Actions)

| العنصر | المقترح المطلوب (`test-id`) | أفضل بديل حالي (CSS Selector) | محدد الـ XPath الاحتياطي |
| :--- | :--- | :--- | :--- |
| **زر البحث في الصفحات** | `[data-test-id="nav-search-btn"]` | `button.search-btn` | `//button[contains(@class,'search-btn')]` |
| **زر حساب المستخدم** | `[data-test-id="nav-user-menu-btn"]` | `button.user-menu-btn` | `//button[contains(@class,'user-menu-btn')]` |
| **زر القائمة للموبايل** | `[data-test-id="nav-mobile-toggle-btn"]` | `button.mobile-toggle` | `//button[contains(@class,'mobile-toggle')]` |

