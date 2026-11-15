# BayMax Patients API Automation Framework

إطار عمل مؤتمت لاختبار وفحص واجهات برمجة التطبيقات (**625 Endpoints في 21 موديولاً**) لنظام **BayMax Patients API**.

## الهيكل التنظيمي للمشروع

```
baymax-api-automation/
├── client/
│   ├── __init__.py
│   └── api_client.py       # Wrapper موحد لإدارة الطلبات والـ Bearer Token والـ Logs
├── tests/
│   ├── __init__.py
│   ├── test_smoke.py       # فحص المسار الحرج السريع (Smoke Tests) للخطوات الـ 9 الأساسية
│   └── modules/            # اختبارات الموديولات الـ 21 (Lookups, Flows, Business Logic)
├── docs/
│   └── POSTMAN-API-TEST-GUIDE.md
├── config.py               # الإعدادات العامة (Base URL, Credentials, Timeouts)
├── conftest.py             # Pytest Fixtures المشتركة لإدارة الجلسات والـ Token
├── pytest.ini              # إعدادات تقارير الفحص والـ Logging
└── requirements.txt
```

## طريقة التشغيل

1. **تأكد من تشغيل السيرفر المحلي:**
   ```
   http://localhost:5250
   ```

2. **ضبط بيانات الدخول في متغيرات البيئة (أو تعديل `config.py`):**
   ```powershell
   $env:BAYMAX_BASE_URL="http://localhost:5250"
   $env:BAYMAX_USERNAME="admin"
   $env:BAYMAX_PASSWORD="your_password"
   ```

3. **تشغيل الفحص السريع (Smoke Tests):**
   ```powershell
   pytest tests/test_smoke.py
   ```

4. **عرض التقرير التفاعلي (HTML Report):**
   - بعد انتهاء الفحص، يتم إنشاء ملف `report.html` تلقائياً في المجلد الرئيسي لعرض النتائج وحالة كل Endpoint بالتفصيل.
