"""
Generates an executive, clean, and concise Excel report showing:
1. Executive Summary & KPIs
2. Issues Log & Status (Resolved vs In Progress vs Documented)
3. Testing Scope & Completed Work Log
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# Define styles & colors
FONT_FAMILY = "Segoe UI"
HEADER_BG = "1E293B"       # Slate Navy
HEADER_FG = "FFFFFF"
ROW_BG_ALT = "F8FAFC"      # Light slate tint
BORDER_COLOR = "CBD5E1"    # Slate border

font_title = Font(name=FONT_FAMILY, size=16, bold=True, color="0F172A")
font_subtitle = Font(name=FONT_FAMILY, size=11, italic=True, color="64748B")
font_section = Font(name=FONT_FAMILY, size=12, bold=True, color="1E293B")
font_header = Font(name=FONT_FAMILY, size=11, bold=True, color=HEADER_FG)
font_data = Font(name=FONT_FAMILY, size=10, color="0F172A")
font_bold = Font(name=FONT_FAMILY, size=10, bold=True, color="0F172A")

fill_header = PatternFill(start_color=HEADER_BG, end_color=HEADER_BG, fill_type="solid")
fill_alt = PatternFill(start_color=ROW_BG_ALT, end_color=ROW_BG_ALT, fill_type="solid")

# Status styles
fill_resolved = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid") # Soft emerald
font_resolved = Font(name=FONT_FAMILY, size=10, bold=True, color="065F46")

fill_inprogress = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # Soft amber
font_inprogress = Font(name=FONT_FAMILY, size=10, bold=True, color="92400E")

fill_reported = PatternFill(start_color="FFE4E6", end_color="FFE4E6", fill_type="solid") # Soft rose
font_reported = Font(name=FONT_FAMILY, size=10, bold=True, color="9F1239")

fill_verified = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid") # Soft blue
font_verified = Font(name=FONT_FAMILY, size=10, bold=True, color="1E40AF")

thin_border = Border(
    left=Side(style='thin', color=BORDER_COLOR),
    right=Side(style='thin', color=BORDER_COLOR),
    top=Side(style='thin', color=BORDER_COLOR),
    bottom=Side(style='thin', color=BORDER_COLOR)
)

card_border = Border(
    left=Side(style='medium', color="94A3B8"),
    right=Side(style='medium', color="94A3B8"),
    top=Side(style='medium', color="94A3B8"),
    bottom=Side(style='medium', color="94A3B8")
)

# ==============================================================================
# SHEET 1: ملخص الإنجاز (Executive Overview)
# ==============================================================================
ws_summary = wb.active
ws_summary.title = "ملخص الإنجاز"
ws_summary.views.sheetView[0].rightToLeft = True

# Title block
ws_summary["A2"] = "تقرير إنجاز الاختبارات ومتابعة المشاكل — نظام BayMax"
ws_summary["A2"].font = font_title
ws_summary["A3"] = "ملخص شامل وموجز لنتائج اختبارات الـ UI والـ APIs وحالة المشاكل المكتشفة"
ws_summary["A3"].font = font_subtitle

# KPI Cards
kpi_data = [
    ("إجمالي الشاشات المفحوصة (UI)", "27 شاشة", "E0F2FE", "0369A1"),
    ("إجمالي الـ APIs المفحوصة", "625 Endpoint", "F0FDF4", "15803D"),
    ("فواتير تم تدقيقها حسابياً", "3,119 فاتورة", "FEF3C7", "B45309"),
    ("مشاكل تم حلها / قيد الإغلاق", "4 مشاكل ✅", "D1FAE5", "065F46"),
    ("مشاكل تم رصدها وتسليمها", "6 مشاكل ⚠️", "FFE4E6", "BE123C"),
]

for idx, (title, value, bg, fg) in enumerate(kpi_data):
    col = chr(ord('A') + idx)
    ws_summary[f"{col}5"] = title
    ws_summary[f"{col}5"].font = Font(name=FONT_FAMILY, size=9, bold=True, color="475569")
    ws_summary[f"{col}5"].alignment = Alignment(horizontal="center", vertical="center")
    ws_summary[f"{col}5"].fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
    ws_summary[f"{col}5"].border = card_border

    ws_summary[f"{col}6"] = value
    ws_summary[f"{col}6"].font = Font(name=FONT_FAMILY, size=14, bold=True, color=fg)
    ws_summary[f"{col}6"].alignment = Alignment(horizontal="center", vertical="center")
    ws_summary[f"{col}6"].fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
    ws_summary[f"{col}6"].border = card_border

ws_summary.row_dimensions[5].height = 24
ws_summary.row_dimensions[6].height = 36

# Work Streams Table
ws_summary["A9"] = "مجالات العمل التي تم إنجازها (Work Streams Summary)"
ws_summary["A9"].font = font_section

headers_summary = ["م", "مجال الفحص", "نطاق العمل المنجز", "عدد الحالات / العناصر", "الحالة العامة"]
for col_num, h in enumerate(headers_summary, 1):
    cell = ws_summary.cell(row=10, column=col_num)
    cell.value = h
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border
ws_summary.row_dimensions[10].height = 26

summary_rows = [
    (1, "أتمتة واجهات المستخدم (UI Automation)", "فحص 27 شاشة (استقبال، عيادات، طوارئ، إقامة، فواتير، تمريض)", "27 شاشة رئيسية", "مكتمل بنجاح"),
    (2, "فحص الـ APIs الأساسية (Smoke Suite)", "التحقق من دورة عمل المريض (تسجيل دخول، بحث، حوافظ، فواتير)", "625 Endpoint (21 موديول)", "مكتمل بنجاح"),
    (3, "فحص الأمان والمدخلات الشاذة (Security & Negative)", "اختبارات التوكن، التواريخ الحدية، SQLi، وسقوط السيرفر", "9 اختبارات رئيسية", "تم رصد 3 ثغرات"),
    (4, "فحص الحسابات والتدقيق المالي (Financial Deep Audit)", "تدقيق شامل لـ 3,119 فاتورة، مراجعة العمليات الحسابية والقيم السالبة", "3,119 فاتورة حية", "تم رصد أخطاء محاسبية"),
    (5, "اختبارات الضغط والتزامن (Concurrency & Load)", "إرسال طلبات متزامنة في نفس اللحظة لفحص ثبات DbContext", "15 طلب متزامن", "مستقر (Passed)"),
]

for row_idx, row_data in enumerate(summary_rows, 11):
    fill_row = fill_alt if row_idx % 2 == 0 else PatternFill(fill_type=None)
    for col_idx, val in enumerate(row_data, 1):
        cell = ws_summary.cell(row=row_idx, column=col_idx)
        cell.value = val
        cell.font = font_data
        cell.border = thin_border
        cell.fill = fill_row
        if col_idx in [1, 4, 5]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if col_idx == 5:
                cell.font = font_bold
        else:
            cell.alignment = Alignment(horizontal="right", vertical="center")
    ws_summary.row_dimensions[row_idx].height = 24

# ==============================================================================
# SHEET 2: المشاكل وحالتها (Issues & Status)
# ==============================================================================
ws_issues = wb.create_sheet(title="سجل المشاكل وحالتها")
ws_issues.views.sheetView[0].rightToLeft = True

ws_issues["A2"] = "سجل المشاكل المكتشفة وحالة الحل (Issues & Resolutions)"
ws_issues["A2"].font = font_title
ws_issues["A3"] = "بيان بالمشاكل التي تم حلها بالفعل، والمشاكل قيد التعديل، والمشاكل الموثقة للديفلوبرز"
ws_issues["A3"].font = font_subtitle

headers_issues = [
    "كود",
    "الموديول / الشاشة",
    "وصف المشكلة بإيجاز",
    "الأثر / الخطورة",
    "الحالة الحالية",
    "الإجراء المتخذ / تفاصيل الحل"
]

for col_num, h in enumerate(headers_issues, 1):
    cell = ws_issues.cell(row=5, column=col_num)
    cell.value = h
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border
ws_issues.row_dimensions[5].height = 28

issues_data = [
    (
        "ISS-01",
        "الاستقبال (Reception)",
        "تعطل الفاليديشن في حقل تاريخ الميلاد وقبول تواريخ شاذة",
        "متوسطة",
        "تم الحل والإغلاق",
        "تم تحديث الحقل وإصلاح الفاليديشن لمنع إدخال التواريخ غير المنطقية وتم استبعاده من المشاكل الحالية.",
        "resolved"
    ),
    (
        "ISS-02",
        "واجهات مختلفة (UI)",
        "أزرار معطلة أو لا تستجيب في بعض شاشات التمريض والإقامة",
        "متوسطة",
        "قيد التعديل والتحديث",
        "تم حصر الأزرار المعطلة ورفعها لفريق التطوير وجاري إنهاء التعديلات عليها برمجياً.",
        "inprogress"
    ),
    (
        "ISS-03",
        "المصادقة (Auth API)",
        "صعوبة الربط مع آلية التوكن والـ Auto-Login عبر الأتمتة",
        "عالية",
        "تم الحل والإغلاق",
        "تم بناء Selenium Auth Bridge واستخراج JWT Token آلياً وحفظه بالجلسة ليعمل 100% في كافة الاختبارات.",
        "resolved"
    ),
    (
        "ISS-04",
        "قاعدة البيانات (Concurrency)",
        "مخاوف من تصادم استعلامات DbContext عند تزامن الطلبات",
        "حرجة",
        "تم التحقق والاستقرار",
        "تم إطلاق 15 طلباً متزامناً في نفس الجزء من الثانية على الفواتير وقوائم الانتظار وصمد السيرفر بنجاح كامل.",
        "verified"
    ),
    (
        "ISS-05",
        "الحسابات (Invoices API)",
        "قبول أيام إقامة سالبة نتج عنه فاتورة وإجماليات سالبة (Invoice #58128)",
        "حرجة جداً",
        "تم الرصد والتسليم للديفلوبر",
        "رصد حجز به 'daysCount': -1 أنتج فاتورة بـ -5,576 ج.م. المطلوب: إضافة Validation بالسيرفر (days >= 1).",
        "reported"
    ),
    (
        "ISS-06",
        "الحسابات (Invoices API)",
        "تضارب رياضي بين الإجمالي ومجموع الكاش والآجل (Invoice #47887)",
        "حرجة",
        "تم الرصد والتسليم للديفلوبر",
        "رصد فارق 14,400 ج.م بين الإجمالي والكاش بالفاتورة. المطلوب: مراجعة كود تجميع عناصر الفاتورة.",
        "reported"
    ),
    (
        "ISS-07",
        "فلاتر التاريخ (Accountant API)",
        "سقوط السيرفر بخطأ 500 عند إدخال تاريخ حدي 0001-01-01",
        "عالية",
        "تم الرصد والتسليم للديفلوبر",
        "انهيار بسبب SqlDateTime overflow. المطلوب: التحقق من التاريخ بالسيرفر وإرجاع 400 Bad Request بدلاً من 500.",
        "reported"
    ),
    (
        "ISS-08",
        "العلاج الطبيعي (PT API)",
        "سقوط السيرفر بخطأ 500 في قائمة الانتظار لغياب فلاتر التاريخ",
        "عالية",
        "تم الرصد والتسليم للديفلوبر",
        "المسار ينهار بـ NullReferenceException عند طلبه بدون بارامترات. المطلوب: ضبط التاريخ الافتراضي لليوم الحالي.",
        "reported"
    ),
    (
        "ISS-09",
        "التقارير (Date Filters)",
        "قبول التواريخ المعكوسة بصمت (تاريخ البدء بعد تاريخ الانتهاء)",
        "متوسطة",
        "تم الرصد والتسليم للديفلوبر",
        "الـ API والواجهة يرجعان جدولاً فارغاً 200 OK دون تنبيه للمستخدم. المطلوب: إضافة شرط تحقق fromDate <= toDate.",
        "reported"
    ),
    (
        "ISS-10",
        "العيادات (Clinics API)",
        "انعكاس وسوم السكربتات XSS في رسالة خطأ التحقق من التاريخ",
        "أمان",
        "تم التوثيق (مؤجلة حالياً)",
        "السيرفر يعكس وسم script كما هو داخل تفاصيل الخطأ. تم توثيقها لعمل Sanitization للمدخلات لاحقاً.",
        "reported"
    ),
]

for row_idx, item in enumerate(issues_data, 6):
    code, module, desc, impact, status, action, status_type = item
    
    ws_issues.cell(row=row_idx, column=1, value=code).alignment = Alignment(horizontal="center", vertical="center")
    ws_issues.cell(row=row_idx, column=2, value=module).alignment = Alignment(horizontal="right", vertical="center")
    ws_issues.cell(row=row_idx, column=3, value=desc).alignment = Alignment(horizontal="right", vertical="center")
    ws_issues.cell(row=row_idx, column=4, value=impact).alignment = Alignment(horizontal="center", vertical="center")
    
    # Status cell with colored badge
    cell_status = ws_issues.cell(row=row_idx, column=5, value=status)
    cell_status.alignment = Alignment(horizontal="center", vertical="center")
    if status_type == "resolved":
        cell_status.fill = fill_resolved
        cell_status.font = font_resolved
    elif status_type == "inprogress":
        cell_status.fill = fill_inprogress
        cell_status.font = font_inprogress
    elif status_type == "verified":
        cell_status.fill = fill_verified
        cell_status.font = font_verified
    else:
        cell_status.fill = fill_reported
        cell_status.font = font_reported

    ws_issues.cell(row=row_idx, column=6, value=action).alignment = Alignment(horizontal="right", vertical="center")

    # Borders & fonts
    for c in range(1, 7):
        curr_cell = ws_issues.cell(row=row_idx, column=c)
        curr_cell.border = thin_border
        if c != 5:
            curr_cell.font = font_data

    ws_issues.row_dimensions[row_idx].height = 28

# ==============================================================================
# SHEET 3: تفاصيل ما تم إنجازه (Completed Work Log)
# ==============================================================================
ws_work = wb.create_sheet(title="سجل العمل المنجز")
ws_work.views.sheetView[0].rightToLeft = True

ws_work["A2"] = "سجل الأعمال المنفذة ومخرجات الاختبار (Test Execution Log)"
ws_work["A2"].font = font_title
ws_work["A3"] = "بيان بالملفات، السكريبتات، والتقارير المكتملة خلال فترة العمل"
ws_work["A3"].font = font_subtitle

headers_work = ["م", "البند / النشاط", "التفاصيل وما تم إنجازه", "الملف / التقرير المولد", "النتيجة النهائية"]
for col_num, h in enumerate(headers_work, 1):
    cell = ws_work.cell(row=5, column=col_num)
    cell.value = h
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border
ws_work.row_dimensions[5].height = 26

work_log = [
    (1, "بناء خريطة الـ APIs الشاملة", "حصر وتوثيق 625 مساراً برمجياً في 21 موديولاً للنظام مع المتغيرات", "POSTMAN-API-TEST-GUIDE.md", "جاهز للاستخدام"),
    (2, "فحص الشاشات آلياً (UI Automation)", "كتابة سكريبتات Selenium وتغطية 27 شاشة وفحص استجابة الأزرار والحقول", "tests_ui / pages", "تم رصد أخطاء الشاشات"),
    (3, "اختبارات الدخان الآلية (Smoke Suite)", "التحقق من صحة المسارات الحيوية (تسجيل، استقبال، عيادات، طوارئ، فواتير)", "test_smoke.py / report.html", "ناجح (Passed)"),
    (4, "اختبارات التخريب والأمان (Destructive API)", "فحص تزوير التوكن، والمدخلات الضخمة، والـ SQLi، والتزامن", "test_api_negative_and_destructive.py", "مكتمل بنجاح"),
    (5, "التدقيق المالي العميق (Financial API)", "سحب وتحليل 3,119 فاتورة من الـ DB وكشف الفواتير السالبة وفروق الحسابات", "test_api_accounting_deep.py", "تم توثيق 5 عيوب حرجة"),
    (6, "تقرير الـ HTML التفاعلي للحسابات", "توليد تقرير رسمي تفاعلي لنتائج فحص الفواتير والتواريخ وتزامن السيرفر", "report_api_accounting_deep.html", "مكتمل ومتاح للفتح"),
]

for row_idx, row_data in enumerate(work_log, 6):
    fill_row = fill_alt if row_idx % 2 == 0 else PatternFill(fill_type=None)
    for col_idx, val in enumerate(row_data, 1):
        cell = ws_work.cell(row=row_idx, column=col_idx)
        cell.value = val
        cell.font = font_data
        cell.border = thin_border
        cell.fill = fill_row
        if col_idx in [1, 5]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if col_idx == 5:
                cell.font = font_bold
        elif col_idx == 4:
            cell.alignment = Alignment(horizontal="left", vertical="center")
            cell.font = Font(name="Consolas", size=9, color="0369A1")
        else:
            cell.alignment = Alignment(horizontal="right", vertical="center")
    ws_work.row_dimensions[row_idx].height = 24

# ==============================================================================
# Auto-adjust column widths
# ==============================================================================
for sheet in wb.worksheets:
    for col in sheet.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            # Skip title rows
            if cell.row in [2, 3]:
                continue
            val_str = str(cell.value or "")
            # Estimate width (Arabic characters count roughly 1.3)
            val_len = sum(1.3 if ord(c) > 127 else 1.0 for c in val_str)
            if val_len > max_len:
                max_len = val_len
        sheet.column_dimensions[col_letter].width = max(max_len + 4, 12)

# Specific custom widths for best visual balance
ws_summary.column_dimensions['A'].width = 8
ws_summary.column_dimensions['B'].width = 38
ws_summary.column_dimensions['C'].width = 65
ws_summary.column_dimensions['D'].width = 24
ws_summary.column_dimensions['E'].width = 20

ws_issues.column_dimensions['A'].width = 12
ws_issues.column_dimensions['B'].width = 24
ws_issues.column_dimensions['C'].width = 52
ws_issues.column_dimensions['D'].width = 16
ws_issues.column_dimensions['E'].width = 25
ws_issues.column_dimensions['F'].width = 65

ws_work.column_dimensions['A'].width = 8
ws_work.column_dimensions['B'].width = 34
ws_work.column_dimensions['C'].width = 65
ws_work.column_dimensions['D'].width = 35
ws_work.column_dimensions['E'].width = 24

output_filename = "BayMax_Testing_Summary_And_Issues.xlsx"
wb.save(output_filename)
print(f"Excel workbook created successfully: {output_filename}")
