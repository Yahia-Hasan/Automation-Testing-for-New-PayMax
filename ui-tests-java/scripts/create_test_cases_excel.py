# -*- coding: utf-8 -*-
"""
Generate master bilingual test-case registers:
- Paymax Automation Test Cases-Aug16-2026.xlsx
- Paymax_Test_Cases_Register.xlsx
"""

from datetime import date
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUT_EXCEL = str(PROJECT_ROOT / "shared" / "test-data" / "Paymax Automation Test Cases-Aug16-2026.xlsx")

HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
HEADER_FONT = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
ALT_FILL = PatternFill("solid", fgColor="D6EAF8")
THIN = Border(
    left=Side(style="thin", color="B0B0B0"),
    right=Side(style="thin", color="B0B0B0"),
    top=Side(style="thin", color="B0B0B0"),
    bottom=Side(style="thin", color="B0B0B0"),
)
WRAP = Alignment(wrap_text=True, vertical="center", horizontal="left")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")

HEADERS = [
    "TC ID",
    "Module (EN)",
    "Module (AR)",
    "Test Case Name (EN)",
    "Test Case Name (AR)",
    "Description (EN)",
    "Description (AR)",
    "Type",
    "Priority",
    "Automation Status",
    "Method Name",
    "Suite / Class",
    "Date Added",
    "Notes",
]

MODULE_AUTH_EN = "Authentication & Bridge Navigation"
MODULE_AUTH_AR = "تسجيل الدخول والتنقل للنظام الجديد"

MODULE_ADM_EN = "Patient Admission / Medical File (Reception)"
MODULE_ADM_AR = "الملف الطبي / استقبال المريض (مكتب الدخول)"

MODULE_OPD_EN = "Outpatient Visits (OPD Clinics)"
MODULE_OPD_AR = "العيادات الخارجية"

SUITE_LOGIN = "LoginTest"
SUITE_ADMISSION = "PatientAdmissionTests"
SUITE_ACTION_BAR = "PatientActionBarTests"
SUITE_OPD = "OutpatientCycleTests"

TODAY = date.today().isoformat()

CASES = [
    # -------------------------------------------------------------
    # Module: Authentication / System Entry
    # -------------------------------------------------------------
    (
        "TC-AUTH-001",
        "Login via legacy bridge and navigate to new Paymax home",
        "تسجيل الدخول عبر النظام القديم والانتقال لواجهة Paymax الجديدة",
        "Authenticate via legacy system login bridge and verify successful navigation to new Paymax home on port 4040 with valid page title.",
        "تسجيل الدخول عبر بوابة النظام القديم والتأكد من فتح الصفحة الرئيسية للنظام الجديد على المنفذ 4040 وعنوان صفحة صحيح.",
        "Smoke",
        "High",
        "Automated",
        "verifyLoginAndNavigateToNewSystem",
    ),

    # -------------------------------------------------------------
    # Module: Patient Admission / Reception (TC-ADM-001 to 027)
    # -------------------------------------------------------------
    (
        "TC-ADM-001",
        "Happy path: create a patient with mandatory fields (unique 4-word Arabic name)",
        "المسار السعيد: إضافة مريض بالبيانات الإجبارية (اسم عربي رباعي فريد)",
        "Create a new patient using all mandatory fields with a unique 4-word Arabic name and verify successful save.",
        "إنشاء مريض جديد بكل الحقول الإجبارية باستخدام اسم عربي رباعي فريد والتحقق من نجاح الحفظ.",
        "Positive",
        "High",
        "Automated",
        "createPatientWithMandatoryFields",
    ),
    (
        "TC-ADM-002",
        "Negative: missing Arabic name must show an error message",
        "سلبي: الحفظ بدون الاسم العربي يظهر رسالة خطأ",
        "Attempt to save without Arabic name and verify that a validation error is displayed.",
        "محاولة الحفظ بدون إدخال الاسم العربي والتحقق من ظهور رسالة خطأ للتحقق.",
        "Negative",
        "High",
        "Automated",
        "savingWithoutMandatoryFieldsShowsValidation",
    ),
    (
        "TC-ADM-003",
        "Mobile field must completely reject alphabetic input",
        "حقل الموبايل يرفض الحروف الأبجدية بالكامل",
        "Enter alphabetic characters in the mobile field and verify they are rejected / not accepted.",
        "إدخال حروف أبجدية في حقل الموبايل والتحقق من رفضها بالكامل.",
        "Negative",
        "Medium",
        "Automated",
        "mobileFieldRejectsAlphabeticCharacters",
    ),
    (
        "TC-ADM-004",
        "Invalid Egyptian mobile (short / wrong prefix) must block save",
        "موبايل مصري غير صحيح (قصير / بادئة غلط) يمنع الحفظ",
        "Enter an invalid Egyptian mobile number and verify that save is blocked with an error.",
        "إدخال رقم موبايل مصري غير صحيح والتحقق من منع الحفظ وظهور خطأ.",
        "Negative",
        "High",
        "Automated",
        "invalidEgyptianMobileIsRejectedOnSave",
    ),
    (
        "TC-ADM-005",
        "Invalid National ID pattern must show a validation error on save",
        "الرقم القومي غير الصحيح يظهر خطأ تحقق عند الحفظ",
        "Enter an invalid National ID pattern and verify a validation error appears on save.",
        "إدخال رقم قومي غير مطابق للنمط الصحيح والتحقق من ظهور خطأ عند الحفظ.",
        "Negative",
        "High",
        "Automated",
        "invalidNationalIdIsRejectedOnSave",
    ),
    (
        "TC-ADM-006",
        "Valid National ID must auto-populate age years/months",
        "الرقم القومي الصحيح يحسب السن تلقائيًا (سنين/شهور)",
        "Enter a valid National ID and verify that age years and months are auto-calculated.",
        "إدخال رقم قومي صحيح والتحقق من حساب السن تلقائيًا بالسنين والشهور.",
        "Positive",
        "High",
        "Automated",
        "validNationalIdAutoCalculatesAge",
    ),
    (
        "TC-ADM-007",
        "Future dates must be blocked by the birth-date picker (max=today)",
        "التواريخ المستقبلية ممنوعة في تاريخ الميلاد (أقصى تاريخ = اليوم)",
        "Verify that the birth-date picker blocks future dates (maximum selectable date is today).",
        "التحقق من أن منتقي تاريخ الميلاد يمنع اختيار تواريخ مستقبلية (أقصى تاريخ = اليوم).",
        "Negative",
        "Medium",
        "Automated",
        "futureBirthDatesAreDisabled",
    ),
    (
        "TC-ADM-008",
        "Picking a birth date manually must recalculate age fields",
        "اختيار تاريخ الميلاد يدويًا يعيد حساب حقول السن",
        "Select a birth date manually and verify that age fields are recalculated correctly.",
        "اختيار تاريخ ميلاد يدويًا والتحقق من إعادة حساب حقول السن بشكل صحيح.",
        "Positive",
        "Medium",
        "Automated",
        "manualBirthDateRecalculatesAge",
    ),
    (
        "TC-ADM-009",
        "Credit company (#@ اليكو) makes insurance number + expiry mandatory",
        "اختيار جهة الائتمان (#@ اليكو) يجعل رقم التأمين وتاريخ الانتهاء إجباريين",
        "Select credit company #@ اليكو and verify insurance number and expiry become mandatory.",
        "اختيار جهة الائتمان #@ اليكو والتحقق من أن رقم التأمين وتاريخ الانتهاء أصبحا إجباريين.",
        "Negative",
        "High",
        "Automated",
        "creditCompanyRequiresInsuranceNumberAndExpiry",
    ),
    (
        "TC-ADM-010",
        "New (جديد) must clear all inputs and reset dropdowns",
        "زرار جديد يفرغ كل الحقول ويعيد ضبط القوائم المنسدلة",
        "Click New (جديد) and verify all inputs are cleared and dropdowns reset to default.",
        "الضغط على جديد والتحقق من تفريغ كافة الحقول وإعادة ضبط القوائم المنسدلة للوضع الافتراضي.",
        "Positive",
        "High",
        "Automated",
        "newButtonClearsInputsAndDropdowns",
    ),
    (
        "TC-ADM-011",
        "Search by patient code then open the matching result (temporary)",
        "البحث بكود المريض وفتح النتيجة المطابقة (مؤقت)",
        "Search by patient code, click the matching dropdown result, and verify fields populate.",
        "البحث بكود المريض والضغط على النتيجة من القائمة والتحقق من ملء بيانات المريض في الحقول.",
        "Positive",
        "High",
        "Automated",
        "searchPopulatesExistingPatientData",
    ),
    (
        "TC-ADM-012",
        "Created-by and created-date fields must be read-only",
        "حقول المنشئ وتاريخ الإنشاء للقراءة فقط",
        "Verify that created-by and created-date fields are read-only and reject manual input.",
        "التحقق من أن حقول المنشئ وتاريخ الإنشاء محمية ولا تقبل الكتابة اليدوية.",
        "Negative",
        "Low",
        "Automated",
        "createdByAndCreatedDateAreReadOnly",
    ),
    (
        "TC-ADM-013",
        "Header date must match the actual current local date",
        "تاريخ الهيدر يطابق التاريخ الحالي الفعلي",
        "Verify the date displayed in the reception header matches today's local system date.",
        "التحقق من أن التاريخ المعروض في أعلى الصفحة يطابق التاريخ المحلي لجهاز المستخدم اليوم.",
        "Positive",
        "Low",
        "Automated",
        "headerDateMatchesCurrentDate",
    ),
    (
        "TC-ADM-014",
        "TC8: Single-word Arabic name must show ERROR on Save",
        "TC8: اسم عربي أحادي يظهر خطأ عند الحفظ",
        "Enter a single-word Arabic name and attempt to save; verify an error message is displayed.",
        "إدخال اسم عربي من كلمة واحدة ومحاولة الحفظ، والتحقق من ظهور رسالة خطأ.",
        "Negative",
        "Medium",
        "Automated",
        "singleWordNameShowsErrorOnSave",
    ),
    (
        "TC-ADM-015",
        "TC9: Two/three-word Arabic name shows WARNING + SUCCESS on Save",
        "TC9: اسم عربي ثنائي أو ثلاثي يظهر تحذير ويحفظ بنجاح",
        "Enter a 2 or 3 word Arabic name; verify warning appears and save succeeds.",
        "إدخال اسم عربي ثنائي أو ثلاثي والتحقق من ظهور تحذير مع إمكانية الحفظ بنجاح.",
        "Positive",
        "Medium",
        "Automated",
        "twoOrThreeWordNameShowsWarningOnBlur",
    ),
    (
        "TC-ADM-016",
        "TC10: Four-word Arabic name is accepted (Success)",
        "TC10: اسم عربي رباعي يقبل بنجاح وبدون تحذيرات",
        "Enter a complete 4-word Arabic name and verify save succeeds without warnings.",
        "إدخال اسم عربي رباعي كامل والتحقق من قبول الحفظ بنجاح بدون تحذيرات على الاسم.",
        "Positive",
        "High",
        "Automated",
        "quadrupleNameHappyPathShowsSuccessOnly",
    ),
    (
        "TC-ADM-017",
        "Full happy path: fill all mandatory + optional fields and save",
        "المسار السعيد الكامل: ملء كافة الحقول الإجبارية والاختيارية والحفظ",
        "Fill every available field (mandatory + optional) and verify patient is saved cleanly.",
        "ملء كل الحقول المتاحة في شاشة الدخول (الإجبارية والاختيارية) والتحقق من حفظ المريض بالكامل.",
        "Positive",
        "High",
        "Automated",
        "fullHappyPathAllFieldsFilled",
    ),
    (
        "TC-ADM-018",
        "Full form reset: New clears all filled inputs and dropdowns",
        "إعادة ضبط كاملة: جديد يفرغ كل الحقول والقوائم المنسدلة",
        "Fill all fields, click New (جديد), and verify every single input is cleared and dropdown reset.",
        "ملء جميع حقول الشاشة ثم الضغط على جديد والتأكد من تصفير كل الحقول والقوائم بدون استثناء.",
        "Positive",
        "Medium",
        "Automated",
        "fullFormResetViaNewButton",
    ),
    (
        "TC-ADM-019",
        "Age years auto-calculate to 10 when DOB is exactly 10 years ago",
        "حساب السن تلقائيًا 10 سنوات عند إدخال تاريخ ميلاد قبل 10 سنوات",
        "Set date of birth to exactly 10 years ago and verify age years field auto-populates 10.",
        "إدخال تاريخ ميلاد قبل 10 سنوات بدقة والتحقق من حساب خانة السن تلقائيًا بـ 10 سنوات.",
        "Positive",
        "Medium",
        "Automated",
        "ageAutoCalculatesFromDateOfBirthTenYearsAgo",
    ),
    (
        "TC-ADM-020",
        "Credit company requires insurance number + expiry on Save (error when empty)",
        "جهة الائتمان تطلب رقم التأمين وتاريخ الانتهاء عند الحفظ (خطأ عند تركها فارغة)",
        "Select a credit entity and leave insurance fields empty; verify save is blocked with validation.",
        "اختيار جهة ائتمان وترك حقول التأمين فارغة ثم الضغط على حفظ والتحقق من ظهور رسائل المنع.",
        "Negative",
        "High",
        "Automated",
        "creditCompanyMandatoryFieldsShowErrorWhenEmpty",
    ),
    (
        "TC-ADM-021",
        "Created-by and created-date are readonly and reject typing",
        "حقول المنشئ وتاريخ الإنشاء للقراءة فقط وترفض الكتابة",
        "Attempt to type into created-by and created-date fields; verify input is rejected.",
        "محاولة الكتابة داخل حقول المنشئ وتاريخ الإنشاء والتأكد من رفض الإدخال تمامًا.",
        "Negative",
        "Low",
        "Automated",
        "readOnlyFieldsRejectModification",
    ),
    (
        "TC-ADM-022",
        "Unknown patient modal: auto-generated patient code is read-only",
        "نافذة مريض غير معلوم: كود المريض المنشأ تلقائيًا للقراءة فقط",
        "Open the unknown patient modal and verify patient-code input is disabled/readonly.",
        "فتح نافذة تسجيل مريض غير معلوم والتحقق من أن حقل كود المريض محمي ولا يمكن تعديله.",
        "Negative",
        "Medium",
        "Automated",
        "unknownPatientCodeIsReadOnly",
    ),
    (
        "TC-ADM-023",
        "Unknown patient modal: happy path save shows a success message",
        "نافذة مريض غير معلوم: الحفظ بنجاح يظهر رسالة تأكيد",
        "Fill unknown patient form with required data, click save, and verify success message.",
        "ملء بيانات مريض غير معلوم والضغط على حفظ والتحقق من ظهور رسالة النجاح وإغلاق النافذة.",
        "Positive",
        "High",
        "Automated",
        "saveUnknownPatientHappyPath",
    ),
    (
        "TC-ADM-024",
        "Unknown patient modal: X button closes the modal",
        "نافذة مريض غير معلوم: زرار الإغلاق (X) يغلق النافذة",
        "Open unknown patient modal, click the close (X) button, and verify modal disappears.",
        "فتح نافذة مريض غير معلوم والضغط على زرار الإغلاق X والتأكد من اختفاء النافذة تمامًا.",
        "Positive",
        "Low",
        "Automated",
        "closeUnknownPatientModal",
    ),
    (
        "TC-ADM-025",
        "Default الجهة value is $$نقدي 2019 on a fresh admission page",
        "القيمة الافتراضية للجهة هي $$نقدي 2019 عند فتح شاشة الدخول",
        "Open a fresh admission page and verify the client (الجهة) dropdown defaults to $$نقدي 2019.",
        "فتح شاشة دخول جديدة والتأكد من أن القيمة المختارة تلقائيًا في حقل الجهة هي $$نقدي 2019.",
        "Positive",
        "Medium",
        "Automated",
        "defaultClientDropdownValueIsCash2019",
    ),
    (
        "TC-ADM-026",
        "Identity type selection updates the adjacent ID-number field label",
        "اختيار نوع إثبات الشخصية يحدث عنوان حقل رقم الإثبات المجاور",
        "Change identity type (e.g. جواز سفر) and verify the adjacent ID input label changes dynamically.",
        "تغيير نوع إثبات الشخصية (مثل جواز سفر) والتحقق من تحديث التسمية التوضيحية لحقل الرقم المجاور.",
        "Positive",
        "Medium",
        "Automated",
        "identityTypeUpdatesAdjacentFieldLabel",
    ),
    (
        "TC-ADM-027",
        "نوع التعاقد defaults to العضو نفسه; DDL has العضو نفسه/مريض تابع; dependent defaults درجة القرابة",
        "نوع التعاقد يبدأ بالعضو نفسه؛ القائمة تحتوي (العضو نفسه/مريض تابع)؛ مريض تابع يحدد درجة القرابة",
        "Select credit entity, verify contract type enables with default العضو نفسه and options; choose مريض تابع and verify relative degree opens.",
        "اختيار جهة آجل والتحقق من فتح نوع التعاقد بالافتراضي 'العضو نفسه'، واختيار 'مريض تابع' والتحقق من ظهور درجة القرابة الزوج/الزوجة.",
        "Positive",
        "High",
        "Automated",
        "cascadingContractAndDependentPatientRules",
    ),

    # -------------------------------------------------------------
    # Module: Top Action Bar (TC-ADM-028 to 032)
    # -------------------------------------------------------------
    (
        "TC-ADM-028",
        "Top action bar: each active button redirects with dynamic patientCode",
        "شريط الإجراءات العلوي: كل زرار نشط يوجه للرابط المطلوب مع كود المريض",
        "Open a patient and click each top action button (عيادات، داخلي، طوارئ، أشعة، معامل، أسنان، عمليات، علاج طبيعي) and verify URL structure.",
        "فتح ملف مريض والضغط على أزرار شريط الإجراءات والتحقق من التوجيه للرابط المناسب حاملاً كود المريض.",
        "Positive",
        "High",
        "Automated",
        "verifyDynamicActionBarRedirects",
    ),
    (
        "TC-ADM-029",
        "Top action bar: Patient Barcode opens popup with /print/barcode?id={code}",
        "شريط الإجراءات العلوي: باركود المريض يفتح نافذة منبثقة برابط الطباعة",
        "Click the barcode button on action bar, verify a popup opens with /print/barcode?id={code}, and close it safely.",
        "الضغط على زرار باركود المريض والتحقق من فتح نافذة طباعة بالرابط الصحيح ثم إغلاقها بنجاح.",
        "Positive",
        "Medium",
        "Automated",
        "verifyPatientBarcodePopupWindow",
    ),
    (
        "TC-ADM-030",
        "Top action bar: under-development buttons stay inactive / do not break the app",
        "شريط الإجراءات العلوي: الأزرار تحت التطوير تظل غير مفعلة ولا تكسر التطبيق",
        "Verify placeholder action buttons (قسطرة، غسيل كلى، المناظير، الأرشيف) do not cause application crash or incorrect navigation.",
        "التحقق من أن الأزرار غير المكتملة لا تسبب أخطاء في التطبيق وتظل في وضع الخمول بأمان.",
        "Positive",
        "Low",
        "Automated",
        "verifyUnderDevelopmentActionButtonsDoNotBreakApp",
    ),
    (
        "TC-ADM-031",
        "External visit family (OPD/Rays/Lab): switching modes keeps the same visit code",
        "عائلة الزيارات الخارجية: التنقل بين العيادات والأشعة والمعامل يحتفظ بنفس كود الزيارة",
        "Open a patient with an active OPD visit and switch between Rays/Lab; verify the system maintains the same visit code.",
        "فتح مريض لديه زيارة عيادات والتنقل للأشعة أو المعامل والتحقق من الاحتفاظ بنفس كود الزيارة المفتوحة.",
        "Positive",
        "High",
        "Automated",
        "verifyExternalVisitFamilyKeepsSameVisitCode",
    ),
    (
        "TC-ADM-032",
        "Incompatible active visit: switching visit type shows ERROR and stays on profile",
        "الزيارة النشطة غير المتوافقة: محاولة التحويل تظهر رسالة خطأ وتبقى في صفحة المريض",
        "Attempt to open an incompatible visit mode (e.g. Inpatient when OPD open) and verify error alert blocks transition.",
        "محاولة فتح نوع زيارة غير متوافق (مثل داخلي أثناء وجود زيارة خارجية) والتحقق من ظهور رسالة خطأ تمنع التحويل.",
        "Negative",
        "High",
        "Automated",
        "verifyIncompatibleVisitSwitchShowsError",
    ),

    # -------------------------------------------------------------
    # Module: Reception Navigation & Agenda (TC-ADM-033 to 036)
    # -------------------------------------------------------------
    (
        "TC-ADM-033",
        "Refresh on selected patient (/reception/patient/{code}) redirects to /reception",
        "إعادة تحميل الصفحة على مريض محدد توجه تلقائيًا إلى /reception",
        "Navigate to a saved patient URL and refresh browser; verify URL cleans up and redirects to base /reception route.",
        "فتح رابط مريض محفوظ وعمل Refresh للمتصفح والتأكد من إعادة التوجيه للرابط الرئيسي /reception.",
        "Positive",
        "Medium",
        "Automated",
        "refreshOnPatientProfileRedirectsToReception",
    ),
    (
        "TC-ADM-034",
        "New (جديد) on selected patient navigates to exact /reception",
        "الضغط على جديد في شاشة مريض محدد ينتقل إلى /reception مباشرة",
        "On an open patient profile, click New (جديد) and verify navigation to exact /reception URL and form reset.",
        "أثناء فتح بيانات مريض محدد، الضغط على جديد والتأكد من الانتقال إلى الرابط /reception وتفريغ الشاشة لمريض جديد.",
        "Positive",
        "Medium",
        "Automated",
        "newButtonOnPatientProfileNavigatesToReception",
    ),
    (
        "TC-ADM-035",
        "Reservation Agenda modal opens with current dates (from/to)",
        "نافذة أجندة الحجوزات تفتح بالتواريخ الحالية تلقائيًا (من / إلى = اليوم)",
        "Click the reservation agenda button and verify modal opens with From and To date fields defaulting to today's date.",
        "الضغط على زرار أجندة الحجوزات والتحقق من فتح النافذة وتعيين حقول تاريخ 'من' و 'إلى' على تاريخ اليوم الحالي.",
        "Positive",
        "High",
        "Automated",
        "verifyReservationAgendaModalOpensWithCurrentDates",
    ),
    (
        "TC-ADM-036",
        "Reservation Agenda search by specific date returns matching results",
        "البحث في أجندة الحجوزات بتاريخ محدد يرجع الحجوزات المطابقة",
        "Set date filters in reservation agenda modal to a specific target date (2026-08-08), click show, and verify grid row results.",
        "تحديد تاريخ محدد (2026-08-08) في فلتر نافذة الأجندة والضغط على عرض والتأكد من ظهور نتيجة الحجز في الجدول.",
        "Positive",
        "High",
        "Automated",
        "verifyReservationSearchBySpecificDate",
    ),

    # -------------------------------------------------------------
    # Module: Outpatient Visits (OPD) — Cycle & Core (TC-OPD-001 to 011)
    # -------------------------------------------------------------
    (
        "TC-OPD-001",
        "Draft OPD visit creation: fill case type + sub-company, save -> /services",
        "إنشاء زيارة عيادات خارجية مسودة: ملء نوع الحالة والشركة الفرعية والحفظ -> صفحة الخدمات",
        "Start an OPD visit from reception, fill required draft fields (نوع الحالة, الشركة الفرعية), click save and verify redirection to /clinic/visits/{code}/services.",
        "بدء زيارة خارجية من الاستقبال وملء الحقول الإجبارية للمسودة وحفظها والتأكد من الانتقال لصفحة خدمات الزيارة.",
        "Positive",
        "High",
        "Automated",
        "createDraftVisitAndTransitionToServices",
    ),
    (
        "TC-OPD-002",
        "Active visit modal: continue same visit opens services page",
        "نافذة الزيارة المفتوحة: اختيار الاستكمال على نفس الزيارة يفتح صفحة الخدمات",
        "When attempting to open OPD for a patient with an existing active visit, click 'الاستكمال على نفس الزيارة' and verify services page opens.",
        "عند فتح زيارة لمريض لديه زيارة مفتوحة بالفعل، اختيار زر الاستكمال على نفس الزيارة والتأكد من فتح صفحة الخدمات مباشرة.",
        "Positive",
        "High",
        "Automated",
        "activeVisitModalContinueExisting",
    ),
    (
        "TC-OPD-003",
        "Close unpaid visit is blocked with warning message",
        "إغلاق زيارة غير مسددة ممنوع وتظهر رسالة تنبيه بعدم السداد",
        "Attempt to close an unpaid active visit, confirm in SweetAlert modal, and verify the system blocks closure with alert 'بسبب أن الزيارة لم تُدفع بعد'.",
        "محاولة إغلاق زيارة لم تسدد خدماتها وتأكيد الإغلاق والتحقق من منع النظام للإغلاق وظهور تنبيه بعدم السداد.",
        "Negative",
        "High",
        "Automated",
        "closeVisitBlockedWhenVisitUnpaid",
    ),
    (
        "TC-OPD-004",
        "Add service to visit and verify total amount updates correctly",
        "إضافة خدمة للزيارة والتحقق من تحديث الإجمالي بشكل صحيح",
        "Add a billable service to an open OPD visit and verify that total amount chip and services grid reflect the added cost.",
        "إضافة خدمة بقيمة مالية للزيارة والتحقق من تحديث إجمالي الزيارة وجدول الخدمات المحسوبة.",
        "Positive",
        "High",
        "Planned",
        "addServiceAndVerifyTotalUpdates",
    ),
    (
        "TC-OPD-005",
        "Services page header title and summary chips verification",
        "التحقق من هيدر صفحة الخدمات وبطاقات الملخص (الإجمالي، المدفوع، نسبة التحمل، المتبقي، عدد الخدمات)",
        "Open OPD services page and verify visit header, patient info card, visit code, unpaid status badge, and financial summary chips.",
        "فتح صفحة خدمات العيادات والتحقق من كارت بيانات المريض وكود الزيارة وشارة حالة السداد وبطاقات الإجمالي والمدفوع والمتبقي.",
        "Positive",
        "High",
        "Automated",
        "servicesPageLoadsWithCorrectData",
    ),
    (
        "TC-OPD-006",
        "Services tabs active state and badge counts",
        "حالة تبويبات صفحة الخدمات وشارات العدادات (الخدمات، الأشعة، التحاليل، صرف الأدوية)",
        "Verify all 4 OPD tabs are visible, 'الخدمات' tab is active by default, and tab badges reflect correct service counts.",
        "التحقق من ظهور التبويبات الأربعة واختيار تبويب الخدمات افتراضيًا ومطابقة عدادات التبويبات للبيانات.",
        "Positive",
        "Medium",
        "Automated",
        "allTabsVisibleAndServicesTabActiveByDefault",
    ),
    (
        "TC-OPD-007",
        "Add service form initial state and price field restrictions",
        "الحالة الأولية لفورم إضافة خدمة وحماية حقول الأسعار",
        "Verify 'إضافة' button is disabled before selecting service, price fields are read-only, and favorites button is visible.",
        "التحقق من تعطيل زر الإضافة قبل اختيار الخدمة وحماية حقول الأسعار من التعديل اليدوي وظهور زر المفضلة.",
        "Positive",
        "Medium",
        "Automated",
        "addServiceFormInitialState",
    ),
    (
        "TC-OPD-008",
        "Add service to visit and save visit info",
        "إضافة خدمة للزيارة وحفظ بيانات الزيارة",
        "Select service group, service, doctor, clinic, click add to draft list, and click save visit info.",
        "اختيار مجموعة الخدمات والخدمة والطبيب والعيادة وإضافتها للقائمة ثم حفظ بيانات الزيارة بنجاح.",
        "Positive",
        "High",
        "Automated",
        "addServiceUpdatesListAndTotal",
    ),
    (
        "TC-OPD-009",
        "Save visit info button success toast notification",
        "زرار حفظ بيانات الزيارة يظهر إشعار نجاح",
        "Click 'حفظ بيانات الزيارة' and verify toast notification confirms successful save and page remains on services.",
        "الضغط على زرار حفظ بيانات الزيارة والتحقق من ظهور إشعار Toast بنجاح الحفظ وبقاء المستخدم في صفحة الخدمات.",
        "Positive",
        "Medium",
        "Automated",
        "saveVisitInfoShowsSuccessToast",
    ),
    (
        "TC-OPD-010",
        "OPD visit payment flow (receipt created and added to history table)",
        "دورة سداد زيارة العيادات (إنشاء إيصال السداد وإضافته لجدول سجل المدفوعات)",
        "Submit payment for visit services and verify a new receipt row appears in the payment history table.",
        "تنفيذ سداد خدمات الزيارة والتحقق من إضافة صف إيصال جديد في جدول سجل الإيصالات.",
        "Positive",
        "High",
        "Automated",
        "paymentCreatesReceiptAndUpdatesPaidChip",
    ),
    (
        "TC-OPD-011",
        "Services page back button navigates to previous page",
        "زرار العودة بصفحة الخدمات يرجع للصفحة السابقة",
        "Click opd-patient-services-back-btn button and verify navigation away from services page.",
        "الضغط على زرار العودة (رجوع) في صفحة الخدمات والتحقق من مغادرة الصفحة بنجاح.",
        "Positive",
        "Medium",
        "Automated",
        "backButtonNavigatesFromServicesPage",
    ),

    # -------------------------------------------------------------
    # Module: Outpatient Visits (OPD) — Advanced Validation (TC-OPD-012 to 018)
    # -------------------------------------------------------------
    (
        "TC-OPD-012",
        "Service group filter limits available clinics",
        "فلترة مجموعة الخدمات تحدد العيادات المتاحة",
        "Select service group الرمد والليزك in opd-patient-services-service-group-select and verify clinic dropdown displays only عيادة 8.",
        "اختيار مجموعة الخدمات الرمد والليزك والتحقق أن قائمة العيادات المتاحة تحتوي فقط على عيادة 8.",
        "Positive",
        "High",
        "Automated",
        "serviceGroupFilterLimitsClinicOptions",
    ),
    (
        "TC-OPD-013",
        "ICD10 Diagnosis mandatory validation by entity (optional for النقدي2019, mandatory for اليكو)",
        "التحقق من إلزامية تشخيص ICD10 حسب الجهة (اختياري للنقدي2019 وإجباري لاليكو)",
        "Verify OPD visit with entity النقدي2019 saves without ICD10 diagnosis, while entity اليكو blocks save until ICD10 diagnosis is selected.",
        "التحقق أن الزيارة مع جهة النقدي2019 تحفظ بدون تشخيص ICD10، بينما تمنع جهة اليكو الحفظ إلا بعد اختيار تشخيص ICD10.",
        "Positive",
        "High",
        "Automated",
        "icdDiagnosisMandatoryValidationByEntity",
    ),
    (
        "TC-OPD-014",
        "Print barcode button opens correct barcode URL",
        "زرار طباعة الباركود يفتح الرابط الصحيح للباركود",
        "Click opd-patient-services-print-barcode-btn button and verify opened URL matches /clinic/visits/{visitCode}/barcode-print.",
        "الضغط على زرار طباعة الباركود والتحقق أن الرابط المفتوح يطابق /clinic/visits/{كود الزيارة}/barcode-print.",
        "Positive",
        "Medium",
        "Automated",
        "printBarcodeButtonOpensCorrectUrl",
    ),
    (
        "TC-OPD-015",
        "Claim form modal CRUD operations (add, download, delete claim file)",
        "عمليات نموذج المطالبة (إضافة، تحميل، حذف ملف المطالبة)",
        "Open claim modal via opd-patient-services-open-claim-btn, upload claim title and file, verify in grid, test download and delete buttons.",
        "فتح بوب أب المطالبة، رفع عنوان وملف المطالبة، التأكد من التواجد في الجدول، وتجربة أزرار التحميل والحذف.",
        "Positive",
        "Medium",
        "Automated",
        "claimModalAddDownloadAndDeleteOperations",
    ),
    (
        "TC-OPD-016",
        "Service short code lookup (valid code 4444 populates data, invalid code 91238128 triggers error message)",
        "التحقق من الكود المختصر للخدمة (الكود الصحيح 4444 يجيب البيانات، والكود الخاطئ 91238128 يظهر خطأ)",
        "Type short code 4444 + ENTER to verify service and price auto-populate. Type invalid code 91238128 + ENTER to verify error message كود الخدمة غير صحيح.",
        "إدخال الكود المختصر 4444 والضغط على ENTER والتحقق من تعبئة الخدمة والسعر تلقائيًا. إدخال الكود الخاطئ 91238128 والضغط على ENTER والتحقق من ظهور رسالة الخطأ كود الخدمة غير صحيح.",
        "Positive",
        "High",
        "Automated",
        "serviceShortCodeValidAndInvalidVerification",
    ),
    (
        "TC-OPD-017",
        "Approval number field state toggle (closed by default, enabled for service 444)",
        "حالة حقل رقم الموافقة (معطل افتراضيًا ويفتح للخدمة 444 التي تطلب موافقة)",
        "Verify approval number field is closed/disabled by default, and becomes enabled/open when service 444 is selected.",
        "التحقق أن حقل رقم الموافقة معطل/مغلق افتراضيًا للخدمات العادية، ويفتح للإدخال عند اختيار الخدمة 444.",
        "Positive",
        "High",
        "Automated",
        "approvalNumberFieldToggleVerification",
    ),
    (
        "TC-OPD-018",
        "Complete outpatient service draft and save cycle (group -> service 444 -> doctor -> clinic -> approval no -> draft list -> saved grid)",
        "السايكل الكاملة للخدمات الخارجية (مجموعة الخدمات -> الخدمة 444 -> الطبيب -> العيادة -> رقم الموافقة -> قائمة الانتظار -> الحفظ في الجريد)",
        "Execute full OPD service cycle: select service group, service 444, doctor, clinic, approval number 324, click add to list (Draft), then click save drafts and verify transfer to saved services grid.",
        "تنفيذ سايكل إضافة الخدمة بالكامل: اختيار مجموعة الخدمات والخدمة 444 والطبيب والعيادة ورقم الموافقة 324 والضغط على إضافة للقائمة لتنزل في خدمات في الانتظار ثم حفظ الخدمات والتحقق من انتقالها لجدول الخدمات المحفوظة.",
        "Positive",
        "High",
        "Automated",
        "completeServicesDraftAndSaveCycle",
    ),

    # -------------------------------------------------------------
    # Module: Outpatient Visits (OPD) — Rules & Medicines Tab (TC-OPD-019 to 029)
    # -------------------------------------------------------------
    (
        "TC-OPD-019",
        "Service quantity field rules (min 1; locked for non-countable vs custom for countable)",
        "قواعد حقل العدد للخدمة (يجب أن يكون >= 1؛ مغلق للخدمات غير القابلة للعد ومفتوح للخدمات القابلة للعد)",
        "Verify that quantity defaults to 1 and is locked for non-countable service ('خدمة الظهر الشاملة الكاملة 1'), while countable service ('مفاصل الظهر') allows entering custom quantity.",
        "التحقق من أن العدد يبدأ بـ 1 ويكون مغلقاً للخدمة غير القابلة للعد، ومفتوحاً لإدخال العدد للخدمة القابلة للعد.",
        "Functional",
        "High",
        "Automated",
        "verifyServiceQuantityFieldRules",
    ),
    (
        "TC-OPD-020",
        "Approval number mandatory validation rules",
        "قواعد إجبارية رقم الموافقة للخدمات التي تتطلب موافقة",
        "Verify that adding a service requiring approval number without entering approval number displays validation error 'برجاء إدخال رقم الموافقة', while service not requiring approval does not mandate it.",
        "التحقق من أن إضافة خدمة تطلب موافقة بدون إدخال رقم الموافقة يظهر رسالة تحذير، بينما الخدمة التي لا تطلب موافقة لا تشترط ذلك.",
        "Negative",
        "High",
        "Automated",
        "verifyApprovalNumberRules",
    ),
    (
        "TC-OPD-021",
        "Doctor selection mandatory rules by service configuration",
        "قواعد إجبارية الطبيب حسب إعدادات الخدمة",
        "Verify adding service not requiring doctor ('كشف ظهر كامل') succeeds without doctor, while service requiring doctor ('كشف ظهر') displays doctor selection validation error.",
        "التحقق من أن الخدمة التي لا تطلب طبيباً تنزل للقائمة بدون طبيب، بينما الخدمة التي تتطلب طبيباً تظهر رسالة خطأ عند عدم اختياره.",
        "Functional",
        "High",
        "Automated",
        "verifyDoctorMandatoryRules",
    ),
    (
        "TC-OPD-022",
        "Service unit price editability rules (fixed vs editable)",
        "قواعد تعديل سعر وحدة الخدمة (سعر ثابت مغلق مقابل سعر قابل للتعديل)",
        "Verify price field is locked/readonly for fixed-price service ('خدمة الظهر الشاملة الكاملة 1') and editable for variable-price service.",
        "التحقق من أن سعر الخدمة الثابتة يكون مغلقاً ومحدداً مسبقاً، وسعر الخدمة القابلة للتعديل يكون مفتوحاً للكتابة.",
        "Functional",
        "Medium",
        "Automated",
        "verifyServicePriceEditableRules",
    ),
    (
        "TC-OPD-023",
        "Discount giver mandatory rules when discount percentage is applied",
        "قواعد مانح الخصم عند إدخال نسبة خصم على الخدمة",
        "Verify discount giver DDL is disabled by default, opens when discount % is entered, and mandates selecting discount giver before adding service.",
        "التحقق من أن مانح الخصم يكون مغلقاً افتراضياً ويفتح عند إدخال نسبة خصم، وتشترط الصفحة اختياره قبل إضافة الخدمة.",
        "Negative",
        "High",
        "Automated",
        "verifyDiscountGiverMandatoryRules",
    ),
    (
        "TC-OPD-024",
        "Discount percentage upper limit (>100%) and negative value validation",
        "حدود نسبة الخصم (عدم تجاوز 100% والرفض للقيم السالبة)",
        "Verify entering discount > 100% displays error 'نسبة الخصم يجب ألا تزيد عن 100%' and clears field, and negative % displays validation error.",
        "التحقق من إظهار تنبيه عند إدخال نسبة خصم أكبر من 100% وتفريغ الفيلد، وإظهار خطأ عند إدخال قيمة سالبة.",
        "Negative",
        "Medium",
        "Automated",
        "verifyDiscountPercentageLimits",
    ),
    (
        "TC-OPD-025",
        "Favorites list toggle, favorite menu selection ('اليكو 2026') and item checkboxes",
        "إظهار قائمة المفضلة واختيار قائمة 'اليكو 2026' وظهور خيارات الخدمات والأشعة والتحاليل",
        "Verify clicking 'إظهار المفضلة' opens favorite menu dropdown, selecting favorite menu 'اليكو 2026' displays favorite item checkboxes.",
        "التحقق من أن زرار 'إظهار المفضلة' يفتح DDL القوائم المفضلة، واختيار قائمة 'اليكو 2026' يظهر عناصر الـ Checkboxes الخاصة بالخدمات والأشعة والتحاليل.",
        "Positive",
        "High",
        "Automated",
        "favoritesListToggleAndItemSelection",
    ),
    (
        "TC-OPD-026",
        "Medicines tab initial empty state for Store/Doctor and '+' batch button toggle",
        "الحالة الأولى لتاب صرف الأدوية (اختر المخزن، اختر الطبيب) وظهور علامة الـ + بعد اختيار المخزن والطبيب",
        "Verify store and doctor DDLs default to 'اختر المخزن' and 'اختر الطبيب', '+' button is hidden initially and becomes visible after selecting store 'main store' and doctor 'Ahmed Badawi'.",
        "التحقق من أن DDL المخزن والطبيب يبدءان بدون اختيار، وعلامة الـ + لا تظهر إلا بعد اختيار مخزن 'main store' والطبيب 'Ahmed Badawi'.",
        "Positive",
        "High",
        "Automated",
        "medicinesTabInitialStateAndStoreDoctorSelection",
    ),
    (
        "TC-OPD-027",
        "Medicines tab item & unit selection, batch dialog '+', and 'جديد' clear button",
        "اختيار صنف 'يورانيوم مشع' والوحدة 'حبيبات' وعلامة الـ + وزرار 'جديد' لتفريغ البيانات",
        "Select item 'يورانيوم مشع', unit 'حبيبات', click '+' batch button, click 'جديد' (clear button) and verify store, doctor, and item selections are cleared.",
        "اختيار صنف 'يورانيوم مشع' والوحدة 'حبيبات' والضغط على علامة الـ + ثم الضغط على 'جديد' والتأكد من تفريغ داتا المخزن والطبيب والأصناف.",
        "Positive",
        "High",
        "Automated",
        "medicinesTabItemSelectionBatchAndClearData",
    ),
    (
        "TC-OPD-028",
        "Medicines tab credit percentage field (نسبة التحمل) locked/readonly for Cash entity",
        "فيلد نسبة التحمل في تاب صرف الأدوية (مغلق ومحمي للجهات النقدي)",
        "Verify credit percentage field is locked/readonly for cash entity visits.",
        "التحقق من أن فيلد نسبة التحمل يكون مغلقاً وغير قابل للتعديل في حالة جهة المريض نقدي.",
        "Functional",
        "High",
        "Automated",
        "medicinesTabCreditPctReadonlyForCashEntity",
    ),
    (
        "TC-OPD-029",
        "Medicines tab credit percentage field (نسبة التحمل) enabled/editable (0-100%) for Credit entity",
        "فيلد نسبة التحمل في تاب صرف الأدوية (مفتوح وقابل لإدخال 0-100% للجهات الآجل)",
        "Verify credit percentage field is enabled and editable (0-100%) for credit entity visits ('اليكو').",
        "التحقق من أن فيلد نسبة التحمل يكون مفتوحاً ويقبل نسب من 0 إلى 100% في حالة جهة المريض آجل ('اليكو').",
        "Functional",
        "High",
        "Automated",
        "medicinesTabCreditPctEditableForCreditEntity",
    ),
]

# Suite / Class mapping
SUITE_BY_ID = {
    "TC-AUTH-001": SUITE_LOGIN,
    "TC-ADM-028": SUITE_ACTION_BAR,
    "TC-ADM-029": SUITE_ACTION_BAR,
    "TC-ADM-030": SUITE_ACTION_BAR,
    "TC-ADM-031": SUITE_ACTION_BAR,
    "TC-ADM-032": SUITE_ACTION_BAR,
}
for i in range(1, 30):
    SUITE_BY_ID[f"TC-OPD-{i:03d}"] = SUITE_OPD

# Module mapping
MODULE_BY_ID = {
    "TC-AUTH-001": (MODULE_AUTH_EN, MODULE_AUTH_AR),
}
for i in range(1, 30):
    MODULE_BY_ID[f"TC-OPD-{i:03d}"] = (MODULE_OPD_EN, MODULE_OPD_AR)

# Date Added mapping
DATE_BY_ID = {
    "TC-AUTH-001": "2026-08-08",
    "TC-ADM-001": "2026-08-16",
    "TC-ADM-002": "2026-08-16",
    "TC-ADM-003": "2026-08-16",
    "TC-ADM-004": "2026-08-16",
    "TC-ADM-005": "2026-08-16",
    "TC-ADM-006": "2026-08-16",
    "TC-ADM-007": "2026-08-16",
    "TC-ADM-008": "2026-08-16",
    "TC-ADM-009": "2026-08-16",
    "TC-ADM-010": "2026-08-16",
    "TC-ADM-011": "2026-08-16",
    "TC-ADM-012": "2026-08-16",
    "TC-ADM-013": "2026-08-16",
    "TC-ADM-014": "2026-08-16",
    "TC-ADM-015": "2026-08-16",
    "TC-ADM-016": "2026-08-16",
    "TC-ADM-017": "2026-08-16",
    "TC-ADM-018": "2026-08-16",
    "TC-ADM-019": "2026-08-16",
    "TC-ADM-020": "2026-08-16",
    "TC-ADM-021": "2026-08-16",
    "TC-ADM-022": "2026-07-25",
    "TC-ADM-023": "2026-07-25",
    "TC-ADM-024": "2026-07-25",
    "TC-ADM-025": "2026-07-25",
    "TC-ADM-026": "2026-07-25",
    "TC-ADM-027": "2026-07-25",
    "TC-ADM-028": "2026-07-28",
    "TC-ADM-029": "2026-07-28",
    "TC-ADM-030": "2026-07-28",
    "TC-ADM-031": "2026-07-28",
    "TC-ADM-032": "2026-07-28",
    "TC-ADM-033": "2026-08-08",
    "TC-ADM-034": "2026-08-08",
    "TC-ADM-035": "2026-08-10",
    "TC-ADM-036": "2026-08-10",
    "TC-OPD-001": "2026-08-07",
    "TC-OPD-002": "2026-08-07",
    "TC-OPD-003": "2026-08-07",
    "TC-OPD-004": "2026-08-07",
    "TC-OPD-005": "2026-08-10",
    "TC-OPD-006": "2026-08-10",
    "TC-OPD-007": "2026-08-10",
    "TC-OPD-008": "2026-08-10",
    "TC-OPD-009": "2026-08-10",
    "TC-OPD-010": "2026-08-10",
    "TC-OPD-011": "2026-08-10",
    "TC-OPD-012": "2026-08-16",
    "TC-OPD-013": "2026-08-16",
    "TC-OPD-014": "2026-08-16",
    "TC-OPD-015": "2026-08-16",
    "TC-OPD-016": "2026-08-16",
    "TC-OPD-017": "2026-08-16",
    "TC-OPD-018": "2026-08-16",
    "TC-OPD-019": "2026-08-19",
    "TC-OPD-020": "2026-08-19",
    "TC-OPD-021": "2026-08-19",
    "TC-OPD-022": "2026-08-19",
    "TC-OPD-023": "2026-08-19",
    "TC-OPD-024": "2026-08-19",
    "TC-OPD-025": "2026-08-19",
    "TC-OPD-026": "2026-08-19",
    "TC-OPD-027": "2026-08-19",
    "TC-OPD-028": "2026-08-19",
    "TC-OPD-029": "2026-08-19",
}

# Notes mapping
NOTES_BY_ID = {
    "TC-AUTH-001": "Initial suite — Legacy system login & Angular redirect",
    "TC-ADM-022": "Added 2026-07-25 — Unknown Patient modal",
    "TC-ADM-023": "Added 2026-07-25 — Unknown Patient modal",
    "TC-ADM-024": "Added 2026-07-25 — Unknown Patient modal",
    "TC-ADM-025": "Added 2026-07-25 — Dynamic UI / default جهة",
    "TC-ADM-026": "Added 2026-07-25 — Dynamic label (إثبات الشخصية)",
    "TC-ADM-027": "Updated 2026-08-05 — نوع التعاقد default العضو نفسه + DDL options + درجة القرابة",
    "TC-ADM-028": "Added 2026-07-28 — Top action bar redirects",
    "TC-ADM-029": "Added 2026-07-28 — Barcode popup window",
    "TC-ADM-030": "Added 2026-07-28 — Under-dev action buttons",
    "TC-ADM-031": "Added 2026-07-28 — External visit family (same visit code)",
    "TC-ADM-032": "Added 2026-07-28 — Incompatible visit ERROR",
    "TC-ADM-033": "Added 2026-08-08 — Refresh patient profile -> /reception",
    "TC-ADM-034": "Added 2026-08-08 — جديد on patient profile -> /reception",
    "TC-ADM-035": "Added 2026-08-10 — Reservation Agenda modal current dates",
    "TC-ADM-036": "Added 2026-08-10 — Reservation Agenda search by specific date",
    "TC-OPD-001": "Added 2026-08-07 — OPD draft -> services",
    "TC-OPD-002": "Added 2026-08-07 — Continue same visit (patient-data-continue-same-visit-btn)",
    "TC-OPD-003": "Added 2026-08-07 — Close unpaid visit blocked (Swal confirm + تنبيه)",
    "TC-OPD-004": "Added 2026-08-07 — Deferred (enabled=false) until clarified",
    "TC-OPD-005": "Added 2026-08-10 — OPD services page header & summary chips",
    "TC-OPD-006": "Added 2026-08-10 — OPD services page tabs & badge counts",
    "TC-OPD-007": "Added 2026-08-10 — Add service form initial state & price field restrictions",
    "TC-OPD-008": "Added 2026-08-10 — Add service full flow & save visit info",
    "TC-OPD-009": "Added 2026-08-10 — Save visit info button success toast",
    "TC-OPD-010": "Added 2026-08-10 — OPD payment flow & receipt history table",
    "TC-OPD-011": "Added 2026-08-10 — OPD services page back button navigation",
    "TC-OPD-012": "Added 2026-08-16 — Service group clinic filter",
    "TC-OPD-013": "Added 2026-08-16 — ICD10 mandatory check by entity",
    "TC-OPD-014": "Added 2026-08-16 — Print barcode button URL",
    "TC-OPD-015": "Added 2026-08-16 — Claim modal operations",
    "TC-OPD-016": "Added 2026-08-16 — Short code lookup (valid 4444 & invalid 91238128 error)",
    "TC-OPD-017": "Added 2026-08-16 — Approval number field state toggle (service 444)",
    "TC-OPD-018": "Added 2026-08-16 — Complete OPD service draft & save cycle",
    "TC-OPD-019": "Added 2026-08-19 — Rule 1: Service quantity rules (min 1, non-countable vs countable)",
    "TC-OPD-020": "Added 2026-08-19 — Rule 2: Approval number mandatory validation",
    "TC-OPD-021": "Added 2026-08-19 — Rule 3: Doctor requirement validation",
    "TC-OPD-022": "Added 2026-08-19 — Rule 4: Service price editability rules",
    "TC-OPD-023": "Added 2026-08-19 — Rule 5: Discount giver DDL validation",
    "TC-OPD-024": "Added 2026-08-19 — Rule 6: Discount percentage limits (>100% and negative)",
    "TC-OPD-025": "Added 2026-08-19 — Favorites list toggle and 'اليكو 2026' item selection",
    "TC-OPD-026": "Added 2026-08-19 — Medicines tab initial state & Store/Doctor requirement",
    "TC-OPD-027": "Added 2026-08-19 — Medicines tab item batch '+' and 'جديد' clear",
    "TC-OPD-028": "Added 2026-08-19 — Medicines tab credit percentage locked for Cash entity",
    "TC-OPD-029": "Added 2026-08-19 — Medicines tab credit percentage editable for Credit entity",
}


def style_header(ws):
    for col, header in enumerate(HEADERS, 1):
        cell = ws.cell(1, col, header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = CENTER
        cell.border = THIN
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{chr(ord('A') + len(HEADERS) - 1)}1"


def build_workbook():
    wb = Workbook()

    # ---- Sheet 1: Instructions ----
    ws_how = wb.active
    ws_how.title = "How to use"
    ws_how["A1"] = "Paymax Automation — Test Case Register"
    ws_how["A1"].font = Font(bold=True, size=16, color="1F4E79")
    ws_how["A3"] = "Purpose / الغرض"
    ws_how["A3"].font = Font(bold=True, size=12)
    ws_how["A4"] = (
        "This workbook is the master list of all automated (and planned) test cases for Paymax."
    )
    ws_how["A5"] = (
        "هذا الملف هو السجل الرئيسي لكل التست كيسز اللي اتعملت أو هتتعمل على نظام Paymax."
    )
    ws_how["A7"] = "How to add a new test case / إضافة تيست كيس جديد"
    ws_how["A7"].font = Font(bold=True, size=12)
    steps = [
        '1. Open the "Test Cases" sheet.',
        "2. Add a new row at the bottom.",
        "3. Fill TC ID using the next number (example: TC-ADM-037 or TC-OPD-030).",
        "4. Fill English + Arabic name and description.",
        "5. Choose Type / Priority / Automation Status from the dropdowns.",
        '6. Put the Java method name in "Method Name" when it is automated.',
        "",
        "1. افتح شيت Test Cases.",
        "2. أضف صف جديد في آخر الجدول.",
        "3. اكتب TC ID بالرقم التالي (مثال: TC-ADM-037 أو TC-OPD-030).",
        "4. املأ الاسم والوصف بالعربي والإنجليزي.",
        "5. اختَر Type / Priority / Automation Status من القوائم.",
        "6. لما التيست يبقى Automated، حط اسم الميثود في Method Name.",
    ]
    for i, text in enumerate(steps):
        ws_how.cell(8 + i, 1, text)

    automated = sum(1 for c in CASES if c[7] == "Automated")
    planned = sum(1 for c in CASES if c[7] == "Planned")

    ws_how["A23"] = "Current coverage / التغطية الحالية"
    ws_how["A23"].font = Font(bold=True, size=12)
    ws_how["A24"] = "Modules: Authentication (AUTH) + Admission (ADM) + Outpatient (OPD)"
    ws_how["A25"] = f"Total test cases: {len(CASES)} | Automated: {automated} | Planned: {planned}"
    ws_how["A26"] = f"Classes: {SUITE_LOGIN} + {SUITE_ADMISSION} + {SUITE_ACTION_BAR} + {SUITE_OPD}"
    ws_how["A27"] = f"Last updated: {TODAY}"

    change_log = [
        ("A29", "Added on 2026-07-25 / اللي اتضاف يوم 25-07 (Unknown Patient & Dynamic UI)"),
        ("A30", "TC-ADM-022 → Unknown patient: code is read-only"),
        ("A31", "TC-ADM-023 → Unknown patient: happy path save (Success)"),
        ("A32", "TC-ADM-024 → Unknown patient: close modal (X)"),
        ("A33", "TC-ADM-025 → Default الجهة = $$نقدي 2019"),
        ("A34", "TC-ADM-026 → إثبات الشخصية updates ID field label (e.g. جواز سفر)"),
        ("A35", "TC-ADM-027 → نوع التعاقد default العضو نفسه; DDL: العضو نفسه|مريض تابع; مريض تابع → درجة القرابة الزوج/الزوجة"),
        ("A37", "Added on 2026-07-28 / اللي اتضاف يوم 28-07 (Top Action Bar)"),
        ("A38", "TC-ADM-028 → Action bar redirects with dynamic patientCode"),
        ("A39", "TC-ADM-029 → Barcode popup (/print/barcode?id=) + close print window"),
        ("A40", "TC-ADM-030 → Under-dev buttons: قسطرة / غسيل كلى / المناظير / الأرشيف"),
        ("A41", "TC-ADM-031 → External visit family (OPD/Rays/Lab) keeps same كود الزيارة"),
        ("A42", "TC-ADM-032 → Incompatible visit switch shows ERROR (Inpatient/Emergency vs others)"),
        ("A44", "Added on 2026-08-07 / اللي اتضاف يوم 07-08 (Outpatient cycle)"),
        ("A45", "TC-OPD-001 → Draft OPD visit save → /clinic/visits/{code}/services"),
        ("A46", "TC-OPD-002 → Continue same visit (patient-data-continue-same-visit-btn)"),
        ("A47", "TC-OPD-003 → Close unpaid visit blocked (confirm نعم → تنبيه لم تُدفع بعد)"),
        ("A48", "TC-OPD-004 → Add service & total (Planned / enabled=false)"),
        ("A50", "Added on 2026-08-08 / اللي اتضاف يوم 08-08 (Auth Bridge & Reception URL reset)"),
        ("A51", "TC-AUTH-001 → Legacy login bridge lands on new Paymax home (port 4040)"),
        ("A52", "TC-ADM-033 → Refresh on /reception/patient/{code} redirects to /reception"),
        ("A53", "TC-ADM-034 → جديد on selected patient navigates to /reception"),
        ("A55", "Added on 2026-08-10 / اللي اتضاف يوم 10-08 (Reservation Agenda & OPD Services/Payments)"),
        ("A56", "TC-ADM-035 → Reservation Agenda modal opens with current dates (from/to = today)"),
        ("A57", "TC-ADM-036 → Reservation Agenda search by specific date (2026-08-08) returns matching results"),
        ("A58", "TC-OPD-005 → OPD services page header title and summary chips (total, paid, insurance %, remaining, count)"),
        ("A59", "TC-OPD-006 → OPD services page tabs active state & badge counts"),
        ("A60", "TC-OPD-007 → Add service form initial state & price field restrictions (readonly)"),
        ("A61", "TC-OPD-008 → Add service to visit & save visit info"),
        ("A62", "TC-OPD-009 → Save visit info button success toast notification"),
        ("A63", "TC-OPD-010 → OPD visit payment flow (receipt created & added to history table)"),
        ("A64", "TC-OPD-011 → Services page back button navigation"),
        ("A66", "Added on 2026-08-16 / اللي اتضاف يوم 16-08 (OPD Advanced Service Validations & Claim)"),
        ("A67", "TC-OPD-012 → Service group clinic filter ('الرمد والليزك' -> 'عيادة 8')"),
        ("A68", "TC-OPD-013 → ICD10 mandatory check by entity (النقدي2019 optional, اليكو mandatory)"),
        ("A69", "TC-OPD-014 → Print barcode button URL"),
        ("A70", "TC-OPD-015 → Claim modal CRUD operations (add, download, delete)"),
        ("A71", "TC-OPD-016 → Short code lookup (valid 4444 & invalid 91238128 error)"),
        ("A72", "TC-OPD-017 → Approval number field state toggle (service 444)"),
        ("A73", "TC-OPD-018 → Complete OPD service draft & save cycle"),
        ("A75", "Added on 2026-08-19 / اللي اتضاف يوم 19-08 (OPD Rules & Medicines Tab)"),
        ("A76", "TC-OPD-019 → Service quantity field rules (min 1, non-countable lock 1, countable custom)"),
        ("A77", "TC-OPD-020 → Approval number mandatory validation rules"),
        ("A78", "TC-OPD-021 → Doctor selection mandatory rules by service configuration"),
        ("A79", "TC-OPD-022 → Service unit price editability rules (fixed vs editable)"),
        ("A80", "TC-OPD-023 → Discount giver mandatory rules when discount percentage applied"),
        ("A81", "TC-OPD-024 → Discount percentage limits (>100% and negative value)"),
        ("A82", "TC-OPD-025 → Favorites list toggle and item selection ('اليكو 2026')"),
        ("A83", "TC-OPD-026 → Medicines tab initial state & Store/Doctor requirement"),
        ("A84", "TC-OPD-027 → Medicines tab item & unit selection, batch '+', and 'جديد' clear"),
        ("A85", "TC-OPD-028 → Medicines tab credit percentage locked for Cash entity"),
        ("A86", "TC-OPD-029 → Medicines tab credit percentage editable for Credit entity"),
        ("A88", "Seed patients (manual setup):"),
        ("A89", "OPD active 30499 | Unpaid OPD 30552 | Inpatient 30496 | Emergency 30495 | Rays 30485 | Lab 30456"),
        ("A91", "Suggested ID prefixes:"),
        ("A92", "ADM = Patient Admission | OPD = Outpatient | BILL = Billing | LAB = Lab | PHARM = Pharmacy | AUTH = Login/Auth"),
    ]
    for cell_ref, text in change_log:
        ws_how[cell_ref] = text
        if text.startswith("Added on") or text.startswith("Seed patients") or text.startswith("Suggested ID"):
            ws_how[cell_ref].font = Font(bold=True, size=12)

    ws_how.column_dimensions["A"].width = 120

    # ---- Sheet 2: Test Cases ----
    ws = wb.create_sheet("Test Cases")
    style_header(ws)

    for i, case in enumerate(CASES, 1):
        tc_id, name_en, name_ar, desc_en, desc_ar, ttype, prio, status, method = case
        module_en, module_ar = MODULE_BY_ID.get(tc_id, (MODULE_ADM_EN, MODULE_ADM_AR))
        row = [
            tc_id,
            module_en,
            module_ar,
            name_en,
            name_ar,
            desc_en,
            desc_ar,
            ttype,
            prio,
            status,
            method,
            SUITE_BY_ID.get(tc_id, SUITE_ADMISSION),
            DATE_BY_ID.get(tc_id, TODAY),
            NOTES_BY_ID.get(tc_id, ""),
        ]
        for col, val in enumerate(row, 1):
            cell = ws.cell(i + 1, col, val)
            cell.border = THIN
            cell.alignment = CENTER if col in (1, 8, 9, 10, 13) else WRAP
            if i % 2 == 0:
                cell.fill = ALT_FILL
        ws.row_dimensions[i + 1].height = 48

    widths = {
        "A": 14,
        "B": 38,
        "C": 34,
        "D": 55,
        "E": 50,
        "F": 55,
        "G": 50,
        "H": 12,
        "I": 10,
        "J": 16,
        "K": 44,
        "L": 24,
        "M": 12,
        "N": 32,
    }
    for col, width in widths.items():
        ws.column_dimensions[col].width = width

    dv_type = DataValidation(
        type="list",
        formula1='"Positive,Negative,Boundary,Smoke,Regression,Functional"',
        allow_blank=True,
    )
    dv_prio = DataValidation(
        type="list", formula1='"High,Medium,Low"', allow_blank=True
    )
    dv_status = DataValidation(
        type="list",
        formula1='"Automated,In Progress,Planned,Blocked,Manual Only"',
        allow_blank=True,
    )
    for dv, rng in (
        (dv_type, "H2:H500"),
        (dv_prio, "I2:I500"),
        (dv_status, "J2:J500"),
    ):
        dv.add(rng)
        ws.add_data_validation(dv)

    # ---- Sheet 3: Summary ----
    ws_sum = wb.create_sheet("Summary")
    summary_headers = [
        "Module (EN)",
        "Module (AR)",
        "Total TCs",
        "Automated",
        "In Progress",
        "Planned",
    ]
    for col, header in enumerate(summary_headers, 1):
        cell = ws_sum.cell(1, col, header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.border = THIN
        cell.alignment = CENTER

    auth_cases = [c for c in CASES if c[0].startswith("TC-AUTH-")]
    adm_cases = [c for c in CASES if c[0].startswith("TC-ADM-")]
    opd_cases = [c for c in CASES if c[0].startswith("TC-OPD-")]

    def write_summary_row(row_idx, module_en, module_ar, cases):
        ws_sum.cell(row_idx, 1, module_en)
        ws_sum.cell(row_idx, 2, module_ar)
        ws_sum.cell(row_idx, 3, len(cases))
        ws_sum.cell(row_idx, 4, sum(1 for c in cases if c[7] == "Automated"))
        ws_sum.cell(row_idx, 5, sum(1 for c in cases if c[7] == "In Progress"))
        ws_sum.cell(row_idx, 6, sum(1 for c in cases if c[7] == "Planned"))
        for col in range(1, 7):
            ws_sum.cell(row_idx, col).border = THIN
            ws_sum.cell(row_idx, col).alignment = CENTER if col >= 3 else WRAP

    write_summary_row(2, MODULE_AUTH_EN, MODULE_AUTH_AR, auth_cases)
    write_summary_row(3, MODULE_ADM_EN, MODULE_ADM_AR, adm_cases)
    write_summary_row(4, MODULE_OPD_EN, MODULE_OPD_AR, opd_cases)

    # Total row
    ws_sum.cell(5, 1, "Total")
    ws_sum.cell(5, 2, "الإجمالي")
    ws_sum.cell(5, 3, len(CASES))
    ws_sum.cell(5, 4, sum(1 for c in CASES if c[7] == "Automated"))
    ws_sum.cell(5, 5, sum(1 for c in CASES if c[7] == "In Progress"))
    ws_sum.cell(5, 6, sum(1 for c in CASES if c[7] == "Planned"))
    for col in range(1, 7):
        ws_sum.cell(5, col).border = THIN
        ws_sum.cell(5, col).font = Font(bold=True)
        ws_sum.cell(5, col).alignment = CENTER if col >= 3 else WRAP

    for col, width in zip("ABCDEF", [42, 38, 12, 12, 12, 12]):
        ws_sum.column_dimensions[col].width = width

    return wb


def main():
    wb = build_workbook()
    wb.save(OUT_EXCEL)
    print(f"Successfully generated: {OUT_EXCEL}")
    print(f"Total test cases: {len(CASES)}")


if __name__ == "__main__":
    main()
