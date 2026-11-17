# مرجع وتوثيق مشروع الأتمتة الموحد (PROJECT_CONTEXT)
## Hospital Management System (BayMax / PayMax Automation Framework)

> **الغرض من هذا الملف:** يمثل هذا الملف المرجع المعماري والتقني والتشغيلي الموحد لجميع أجزاء منظومة الفحص الآلي للمستشفى (موديول إدارة المرضى / دورة العيادات الخارجية والداخلي والطوارئ). يُلزم الرجوع إليه والالتزام بكافة قواعده عند كتابة أو تعديل أي اختبارات جديدة.

---

## 1. الهيكل المعماري للمشروع الموحد (Framework Architecture)

تم دمج كافة أجزاء المشروع في بنية ثلاثية الطبقات مدعومة بحزمة مشتركة (`shared/`):

```text
Automation Testing Paymax/
│
├── shared/                                # [المكونات المشتركة لجميع الطبقات]
│   ├── config/                            # الإعدادات وبيانات البيئات
│   │   ├── environments.json              # تعريف بيئات التشغيل (URLs, Ports, Timeouts)
│   │   ├── config.properties              # إعدادات Java / Selenium
│   │   ├── .env                           # متغيرات البيئة لبايثون
│   │   └── .env.example                   # نموذج متغيرات البيئة
│   ├── test-data/                         # بيانات الاختبار الموحدة
│   │   ├── patients.json                  # بيانات المرضى، الكودات، والجهات المشتركة
│   │   ├── ui_selectors.json / test_ids   # معرّفات عناصر الـ UI (data-test-id)
│   │   ├── Paymax Automation Test Cases-Aug16-2026.xlsx # مصفوفة اختبارات الـ UI
│   │   ├── BayMax_Testing_Summary_And_Issues.xlsx       # مصفوفة اختبارات الـ APIs
│   │   └── EXECUTIVE_AUDIT_SUMMARY.xlsx   # شيتات تدقيق ومطابقة التقارير
│   └── python-utils/                      # كود بايثون المشترك (DRY)
│       ├── unified_config.py              # محرك قراءة الإعدادات الموحد
│       ├── driver_factory.py              # مصنع تشغيل Chrome الآمن (Bypass SSL & HSTS)
│       ├── auth_manager.py                # جسر تسجيل الدخول القديم وإدارة الـ Token
│       ├── api_client.py                  # عميل اتصالات REST API المعتمد على الـ Bearer
│       └── file_utils.py                  # دوال المسارات والتعامل مع JSON/Excel
│
├── ui-tests-java/                         # [الطبقة الأولى: شاشات الـ UI - Java]
│   ├── pom.xml                            # تبعيات Maven (Selenium, TestNG, Log4j2)
│   ├── testng.xml                         # خطة تنفيذ اختبارات TestNG
│   ├── TEMPORARY_WORKAROUNDS.md           # سجل الـ Workarounds الخاصة بالـ UI
│   ├── scripts/                           # سكربتات مساعدة لتوليد تقارير الإكسيل
│   └── src/test/java/com/paymax/automation/
│       ├── base/                          # BaseTest وإدارة دورة حياة المتصفح
│       ├── config/                        # ConfigReader (يقرأ من shared/config أولاً)
│       ├── helpers/                       # LoginHelper (جسر الدخول)
│       ├── pages/                         # Page Object Model (Reception, Outpatient, ...)
│       └── tests/                         # كلاسات الاختبارات (OutpatientCycle, Admission, ...)
│
├── api-tests-python/                      # [الطبقة الثانية: اختبارات الـ APIs - Python]
│   ├── config.py                          # جسر يوجه إلى shared/python-utils/unified_config
│   ├── conftest.py                        # فيكستشرز pytest وإدارة الـ auth_client
│   ├── client/api_client.py               # عميل الـ API المعتمد على shared
│   ├── selenium_login.py                  # جسر الدخول المعتمد على shared
│   ├── tests/                             # اختبارات الـ API (Smoke, Accounting, Negative, Load)
│   ├── tests_ui/                          # اختبارات الـ UI السريعة والـ Chaos / Buttons
│   ├── locustfile.py                      # اختبارات الحمل والضغط العالي
│   └── docs/                              # تقارير فحص الـ 625 endpoint وتوثيق Postman
│
└── data-validation-python/                # [الطبقة الثالثة: التحقق من الداتا والتقارير - Python]
    ├── config/settings.py                 # موجه إلى shared/python-utils/unified_config
    ├── utils/                             # driver_factory و auth موجهين إلى shared
    ├── compare_opd_live.py                # مطابقة شاشات وتقارير العيادات الخارجية لايف
    ├── reconcile_doctor_reports.py        # تدقيق ومطابقة استحقاقات ونسب الأطباء
    ├── sync_modules.py                    # مزامنة وتدقيق موديولات النظام
    ├── discovery/                         # ملفات JSON المسحوبة من شاشات المبيعات والأقسام
    ├── SYSTEM_AUDIT_REPORT.md             # التقرير التنفيذي لمطابقة البيانات المالية
    └── tests/                             # اختبارات شاشات التقارير والنافبار والاستقبال
```

---

## 2. معلومات النظام والبيئات (Target System Specs)

| البند | القيمة / المسار | ملاحظات |
| :--- | :--- | :--- |
| **سيرفر الاستضافة** | `196.218.246.250` | السيرفر متاح عبر الشبكة ويستجيب على المنافذ 80 و 4040. |
| **بوابة الدخول القديمة (Legacy Portal)** | `http://196.218.246.250/sysadmin/login.aspx?macAdd=000000000000` | شاشات ASP.NET WebForms (المنفذ 80 - HTTP). |
| **واجهة النظام الحديث (Angular SPA)** | `https://196.218.246.250:4040` | تطبيق Angular حديث بشهادة أمان Self-Signed (المنفذ 4040 - HTTPS). |
| **واجهات الـ REST API** | `https://196.218.246.250:4040/Patients-Modern-BE` | يحتوي أكثر من 625 مساراً برمجياً في 21 موديولاً. السواجر: `/swagger`. |
| **بيانات تسجيل الدخول** | `sysadmin` / `Ma3an2025` | مستخدم الأدمن العام للنظام. |
| **الفرع الافتراضي** | `Ad Doqi` (فرع الدقي) | Branch ID = `1`, Department ID = `5`, Treasury ID = `0`. |

---

## 3. الحلول التقنية والالتفافية الإلزامية (Critical Workarounds & Fixes)

### 1. جسر تسجيل الدخول (Legacy Login Bridge)
- **المشكلة:** النظام الحديث (`https://...:4040`) لا يمتلك شاشة تسجيل دخول مستقلة حتى الآن، ويعتمد على جلسة النظام القديم (`ASP.NET WebForms`) المنشأة على المنفذ 80.
- **الحل المعتمد:**
  1. التوجه إلى `http://196.218.246.250/sysadmin/login.aspx?macAdd=000000000000`.
  2. النقر على زر اختيار بيئة العمل `btnWorkspaceHospital`.
  3. ملء `txtInvUserName` و `txtInvPassword` ببيانات `sysadmin` / `Ma3an2025` والنقر على `btnLogin`.
  4. فتح كومبوبوكس فرع الدقي في Telerik RadComboBox (`ddlBranches`) واختيار `Ad Doqi` ثم النقر على `btnContinue`.
  5. التأكد من الوصول لـ `frmLandingPage.aspx`.
  6. التوجه فوراً إلى `https://196.218.246.250:4040/home`.
  7. استخراج رمز المصادقة `baymax_token` من `window.localStorage` أو استخدام الكوكيز النشطة.
- **الكود الموحد:** يتم استدعاؤه تلقائياً من `shared/python-utils/auth_manager.py` لكل من بايثون وجافا.

### 2. تجاوز قيود شهادات الأمان و HSTS (SSL & Insecure Certificates)
- **المشكلة:** متصفح Chrome يقوم بترقية الاتصال تلقائياً (HTTPS-First) مما يمنع الدخول على المنفذ 80 القديم، بالإضافة لرفض شهادة السيرفر على المنفذ 4040 لكونها Self-Signed.
- **الحل الإلزامي في إعداد المتصفح:**
  - تفعيل الخيارات: `--ignore-certificate-errors`, `--allow-running-insecure-content`, `acceptInsecureCerts=True`.
  - تعطيل ميزات الترقية التلقائية عبر: `--disable-features=HttpsUpgrades,HttpsFirstModeV2,HttpsFirstBalancedMode,HttpsFirstModeV2ForEngagedSites,AutoupgradeMixedContent`.
  - تشغيل المتصفح ببروفايل مؤقت معزول `tempfile.mkdtemp()` لمنع تراكم كاش الـ HSTS.

### 3. شاشة الاستقبال وعزل حالة الاختبارات (Reception Reload & Isolation)
- **المشكلة:** بعد حفظ المريض بنجاح، يتغير المسار إلى `/reception/patient/{code}` وتحتفظ الحقول ببيانات المريض، والنافبار القديم كان يترك القائمة منسدلة تحجب الأزرار (`click intercepted`).
- **الحل المعتمد بين كل تيست:**
  - لا تعتمد على التنقل عبر النافبار فقط؛ بل قم بعمل Hard Reload للمسار الأصلي: `driver.get("https://...:4040/reception")`.
  - الضغط على زر **جديد** والتأكد من تفريغ حقلي الاسم ورقم الهاتف.
  - **تحذير حاسم:** لا تقم أبداً بمسح `[data-test-id='global-toast-stack']` عبر `innerHTML = ''`، لأن ذلك يعطل محرك Angular Toaster فتبدو الاختبارات التالية فاشلة لعدم ظهور التوست.

### 4. حقل البحث عن المرضى (Patient Search)
- الضغط على `ENTER` في حقل `patient-data-search-input` لا يفتح السجل.
- السلوك الصحيح للأتمتة: بعد كتابة كود المريض أو اسمه، يظهر Dropdown بنتيجة واحدة؛ يجب النقر على السطر لاختيار المريض وتعبئة الشاشة.

### 5. قواعد الأسماء العربية للمرضى (Arabic Name Validation Rules)
- **كلمة واحدة (مثل: "يحيى"):** يظهر **Error Toast** ويمنع الحفظ.
- **كلمتان أو 3 كلمات (مثل: "يحيى تيست"):** يظهر **Warning Toast** ولكن يقبل الحفظ بنجاح (**Warning + Success**).
- **4 كلمات فأكثر (مثل: "يحيى تيست اوتوميشن رباعي"):** حفظ ناجح فوري بنقاء كامل (**Success Toast**).

### 6. دقة مسميات القوائم المنسدلة (Exact Dropdown Values)
- نوع الهوية: يُكتب بالضبط `"رقم قومي"` (وليس `"الرقم القومي"`).
- جهة التأمين الآجل: تُكتب بالضبط `"#@ اليكو"` (شاملة علامات `#@ `).

---

## 4. شروط وقواعد مطابقة التقارير والداتا (Data Reconciliation Rules)

عند كتابة أو تشغيل أي فحص لمخرجات وتقارير السيستم في `data-validation-python/`:

1. **إيرادات الطوارئ (Emergency Revenue):**
   - التطابق تام بنسبة 100% بالقرش بين "تقرير مبيعات الطوارئ التفصيلي" و"تقرير مبيعات طوارئ المستشفى". لا يُقبل أي فارق مالي.
2. **استحقاقات أطباء العمليات (Surgeon Fees):**
   - كشف استحقاقات أطباء العمليات يجب أن يطابق 100% كشف أتعاب الأطباء المجمعة ومسيرات الرواتب.
3. **الخصومات الممنوحة للمرضى (Discounts):**
   - تخضع لمطابقة ثلاثية إجبارية: (إجمالي أذونات الخصم = الخصومات بفواتير خروج المرضى = استقطاعات حصص الأطباء والأقسام).
4. **تعداد المرضى (Patient Census):**
   - مجموع دفاتر دخول الأقسام (عيادات + طوارئ + داخلي) يجب أن يساوي تماماً الرقم النهائي بالتقرير الإحصائي العام للمستشفى.
5. **مبيعات الداخلي اليومية vs فواتير الخروج:**
   - تقرير مبيعات الداخلي اليومي أعلى بكثير من فواتير الخروج (لأنه يسجل إقامة كافة المرضى الحاليين)، بينما فواتير الخروج تسجل فقط من تم شفاؤهم وخرجوا رسمياً. هذا سلوك تشغيلي طبيعي.
6. **فصل إيراد المعمل عن العيادات:**
   - شاشة مبيعات العيادات تسجل كامل الفاتورة باسم العيادة، بينما شاشة إحصائيات الإيراد تفصل كشوفات التحاليل وتحيلها لقسم المعامل. الإجمالي المالي صحيح، والفارق تصنيفي فقط.
7. **تقفيل الخزائن ومواعيد الشيفتات:**
   - وجود فارق بين إيرادات اليوم وحركة المقبوضات ناتج عن فارق ساعتين في توقيت الخادم بين إقفال 10 مساءً و 12 منتصف الليل (إيصالات وردية السهرة).

---

## 5. دليل التشغيل السريع (How to Run)

### تشغيل اختبارات واجهة المستخدم (UI Layer - Java):
```powershell
cd "c:\Users\Ma3n\Desktop\Automation  Testing Paymax\ui-tests-java"
mvn test
# أو لتشغيل كلاس محدد:
mvn test -Dtest=PatientAdmissionTests
```

### تشغيل اختبارات واجهات البرمجة (API Layer - Python):
```powershell
cd "c:\Users\Ma3n\Desktop\Automation  Testing Paymax"
# فحص الـ Smoke السريع للـ APIs
python -m pytest "api-tests-python/tests/test_smoke.py" -v

# فحص اختبارات الـ UI والـ Chaos السريعة
python -m pytest "api-tests-python/tests_ui" -v
```

### تشغيل مطابقة التقارير والداتا (Data Validation - Python):
```powershell
cd "c:\Users\Ma3n\Desktop\Automation  Testing Paymax"
# اختبارات مطابقة شاشات ونافبار الاستقبال
python -m pytest "data-validation-python/tests" -v

# تشغيل سكربت المقارنة الحية لتقارير العيادات
python "data-validation-python/compare_opd_live.py"

# تشغيل سكربت تدقيق أتعاب ونسب الأطباء
python "data-validation-python/reconcile_doctor_reports.py"
```

---

## 6. إرشادات إلزامية عند إضافة أي تيست كيس جديدة (Golden Rules)

1. **الاستيراد من الحزمة المشتركة دائماً:**
   - في بايثون: استخدم دائماً `from shared.python_utils import ...` أو استورد من `unified_config`, `driver_factory`, `auth_manager`. لا تكتب كود تسجيل دخول أو فتح متصفح من الصفر مطلقاً.
   - في جافا: اعتمد على `ConfigReader` و `BaseTest`.
2. **استخدام معرّفات الاختبار الموحدة:**
   - راجع `shared/test-data/test_ids.txt` و `shared/test-data/patients.json` للحصول على أسماء الحقول و `data-test-id` الدقيقة.
3. **عدم استخدام أوقات انتظار ثابتة (Explicit Waits Only):**
   - تجنب `Thread.sleep` أو `time.sleep` الطويلة؛ اعتمد دائماً على `WebDriverWait` لمراقبة اختفاء مؤشرات التحميل وظهور التوست أو الجداول.
4. **تسجيل النتائج في ملفات التدقيق:**
   - أي فحص جديد للتقارير يجب أن يسجل مخرجاته في مصفوفة المقارنة لضمان استمرار مطابقة الحسابات بالقرش.
