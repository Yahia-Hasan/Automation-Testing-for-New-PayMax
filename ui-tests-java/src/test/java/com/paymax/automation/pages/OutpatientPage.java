package com.paymax.automation.pages;

import com.paymax.automation.config.ConfigReader;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.StaleElementReferenceException;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

/**
 * Page Object for Outpatient Visits (العيادات الخارجية):
 * draft {@code /clinic/visits/draft?...&mode=opd} and saved
 * {@code /clinic/visits/{visitCode}/services}.
 * <p>
 * Prefers {@code data-test-id}. Label/text fallbacks are TEMPORARY until frontend
 * confirms every outpatient test id.
 */
public class OutpatientPage extends BasePage {

    private static final Logger LOGGER = LogManager.getLogger(OutpatientPage.class);
    private static final Pattern VISIT_CODE_IN_URL =
            Pattern.compile("/clinic/visits/(\\d+)(?:/|\\?|$)");

    // ---------- Draft visit (بيانات المريض) ----------
    private static final By CASE_TYPE_SELECT = By.cssSelector(
            "[data-test-id='clinic-visit-case-type-select'],"
                    + "[data-test-id='opd-case-type-select'],"
                    + "[data-test-id='visit-case-type-select']");
    private static final By CASE_TYPE_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'نوع الحالة')]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1]");

    private static final By SUB_COMPANY_SELECT = By.cssSelector(
            "[data-test-id='clinic-visit-ins-company-select'],"
                    + "[data-test-id='opd-ins-company-select'],"
                    + "[data-test-id='visit-sub-company-select']");
    private static final By SUB_COMPANY_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'الشركة الفرعية')]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1]");

    private static final By SAVE_VISIT_BUTTON = By.cssSelector(
            "[data-test-id='clinic-visit-save-btn'],"
                    + "[data-test-id='opd-save-btn'],"
                    + "[data-test-id='visit-save-btn']");
    private static final By SAVE_VISIT_BY_TEXT = By.xpath(
            "//button[contains(normalize-space(.),'حفظ')"
                    + " and not(contains(normalize-space(.),'حفظ ودفع'))]");

    // ---------- Active visit warning modal ----------
    private static final By ACTIVE_VISIT_MODAL = By.cssSelector(
            "[data-test-id='patient-data-open-visit-modal']");
    private static final By ACTIVE_VISIT_MODAL_BY_TEXT = By.xpath(
            "//*[contains(@class,'open-visit-modal')]"
                    + " | //*[contains(normalize-space(.),'المريض لديه زيارة مفتوحة')]");

    private static final By CONTINUE_EXISTING_VISIT_BTN = By.cssSelector(
            "[data-test-id='patient-data-continue-same-visit-btn']");
    private static final By CONTINUE_EXISTING_VISIT_BY_TEXT = By.xpath(
            "//button[contains(normalize-space(.),'الإستكمال على نفس الزيارة')"
                    + " or contains(normalize-space(.),'الاستكمال على نفس الزيارة')]");

    private static final By CLOSE_AND_CREATE_NEW_BTN = By.cssSelector(
            "[data-test-id='patient-data-close-open-visit-btn']");
    private static final By CLOSE_AND_CREATE_NEW_BY_TEXT = By.xpath(
            "//button[contains(normalize-space(.),'إغلاق الزيارة المفتوحة وعمل زيارة جديدة')"
                    + " or contains(normalize-space(.),'اغلاق الزيارة المفتوحة')]");

    // ---------- SweetAlert2: confirm close open visit ----------
    private static final By SWAL_CLOSE_CONFIRM_TITLE = By.cssSelector(
            "[data-test-id='swal-close-open-opd-visit-title']");
    private static final By SWAL_CLOSE_CONFIRM_MESSAGE = By.cssSelector(
            "[data-test-id='swal-close-open-opd-visit-message']");
    private static final By SWAL_CLOSE_CONFIRM_YES_BTN = By.cssSelector(
            "[data-test-id='swal-close-open-opd-visit-confirm-btn']");
    private static final By SWAL_CLOSE_CONFIRM_CANCEL_BTN = By.cssSelector(
            "[data-test-id='swal-close-open-opd-visit-cancel-btn']");

    // ---------- SweetAlert2: close blocked (e.g. unpaid) ----------
    private static final By SWAL_CLOSE_ERROR_TITLE = By.cssSelector(
            "[data-test-id='swal-close-open-opd-error-title']");
    private static final By SWAL_CLOSE_ERROR_MESSAGE = By.cssSelector(
            "[data-test-id='swal-close-open-opd-error-message']");
    private static final By SWAL_CLOSE_ERROR_OK_BTN = By.cssSelector(
            "[data-test-id='swal-close-open-opd-error-confirm-btn']");
    private static final By CLOSE_VISIT_UNPAID_REASON = By.xpath(
            "//*[@data-test-id='swal-close-open-opd-error-message']"
                    + "[contains(normalize-space(.),'لم تُدفع') or contains(normalize-space(.),'لم تدفع')]"
                    + " | //*[contains(normalize-space(.),'لم تُدفع بعد')"
                    + " or contains(normalize-space(.),'لم تدفع بعد')]");

    // ---------- Services page — patient card & header ----------
    private static final By BACK_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-back-btn']");
    private static final By SAVE_VISIT_INFO_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-save-visit-info-btn']");
    private static final By PRINT_BARCODE_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-print-barcode-btn']");
    private static final By OPEN_CLAIM_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-open-claim-btn']");

    // Patient info fields (label/value pairs inside patient-info-grid)
    private static final By PATIENT_INFO_GRID = By.cssSelector(".patient-info-grid");
    private static final By PATIENT_NAME_FIELD = By.xpath(
            "//span[contains(@class,'field-label') and normalize-space()='الاسم']"
                    + "/following-sibling::span[contains(@class,'field-value')]");
    private static final By PATIENT_CODE_FIELD = By.xpath(
            "//span[contains(@class,'field-label') and normalize-space()='كود المريض']"
                    + "/following-sibling::span[contains(@class,'field-value')]");
    private static final By VISIT_CODE_FIELD = By.xpath(
            "//span[contains(@class,'field-label') and normalize-space()='كود الزيارة']"
                    + "/following-sibling::span[contains(@class,'field-value')]");
    private static final By VISIT_DATE_FIELD = By.xpath(
            "//span[contains(@class,'field-label') and normalize-space()='تاريخ الزيارة']"
                    + "/following-sibling::span[contains(@class,'field-value')]");
    private static final By UNPAID_BADGE = By.xpath(
            "//*[contains(@class,'badge-warning') and contains(normalize-space(),'غير مدفوع')]");
    private static final By PAID_BADGE = By.xpath(
            "//*[contains(@class,'badge') and contains(normalize-space(),'مدفوع')"
                    + " and not(contains(normalize-space(),'غير'))]");

    // Visit code in page header ("زيارة رقم: XXXX")
    private static final By PAGE_VISIT_NUMBER_HEADER = By.xpath(
            "//p[contains(normalize-space(),'زيارة رقم')]");
    private static final By PAGE_H1_TITLE = By.cssSelector(".page-header h1");

    // ---------- Visit info row (نوع الحالة, الشركة الفرعية, الطبيب المحول, ICD10) ----------
    private static final By SERVICES_CASE_TYPE_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-case-type-select']");
    private static final By SERVICES_INS_COMPANY_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-ins-company-select']");
    private static final By SERVICES_TRANSFER_DOCTOR_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-transfer-doctor-select']");
    private static final By SERVICES_ICD_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-icd-select']");

    // ---------- Totals strip ----------
    private static final By TOTALS_STRIP = By.cssSelector(".totals-strip");
    private static final By TOTAL_CHIP_TOTAL = By.xpath(
            "//*[contains(@class,'total-chip')][./span[normalize-space()='الإجمالي']]"
                    + "/span[contains(@class,'chip-value')]");
    private static final By TOTAL_CHIP_CASH = By.xpath(
            "//*[contains(@class,'total-chip')][./span[normalize-space()='نقدي']]"
                    + "/span[contains(@class,'chip-value')]");
    private static final By TOTAL_CHIP_CREDIT = By.xpath(
            "//*[contains(@class,'total-chip')][./span[contains(normalize-space(),'آجل')]]"
                    + "/span[contains(@class,'chip-value')]");
    private static final By TOTAL_CHIP_DISCOUNT = By.xpath(
            "//*[contains(@class,'total-chip')][./span[normalize-space()='خصم']]"
                    + "/span[contains(@class,'chip-value')]");
    private static final By TOTAL_CHIP_PAID = By.xpath(
            "//*[contains(@class,'total-chip')][./span[normalize-space()='المدفوع']]"
                    + "/span[contains(@class,'chip-value')]");
    private static final By TOTAL_CHIP_REMAINING = By.xpath(
            "//*[contains(@class,'total-chip')][./span[normalize-space()='المتبقي']]"
                    + "/span[contains(@class,'chip-value')]");
    private static final By LEAVE_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-leave-btn']");

    // ---------- Tab bar ----------
    private static final By TAB_SERVICES = By.cssSelector(
            "[data-test-id='opd-patient-services-services-tab-btn']");
    private static final By TAB_MEDICINES = By.cssSelector(
            "[data-test-id='opd-patient-services-medicines-tab-btn']");
    private static final By TAB_MED_REQUEST = By.cssSelector(
            "[data-test-id='opd-patient-services-med-request-tab-btn']");
    private static final By TAB_MED_RETURN = By.cssSelector(
            "[data-test-id='opd-patient-services-med-return-tab-btn']");

    // ---------- Claim Modal ----------
    private static final By CLAIM_MODAL_TITLE = By.cssSelector(".modal-title");
    private static final By CLAIM_MODAL_CLOSE_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-claim-modal-close-btn']");
    private static final By CLAIM_TITLE_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-claim-title-input']");
    private static final By CLAIM_FILE_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-claim-file-input']");
    private static final By SAVE_CLAIM_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-save-claim-btn']");
    private static final By CLAIM_ITEM_LIST = By.cssSelector(".claim-list .claim-item");
    private static final By CLAIM_TITLE_TEXT = By.cssSelector(".claim-title");
    private static final By DOWNLOAD_CLAIM_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-download-claim-btn']");
    private static final By DELETE_CLAIM_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-delete-claim-btn']");

    // ---------- Add service form ----------
    private static final By TOGGLE_FAVORITES_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-toggle-favorites-btn']");
    private static final By FAVORITE_MENU_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-favorite-menu-select']");
    private static final By FAVORITE_ITEM_CHECKBOX = By.cssSelector(
            "[data-test-id='opd-patient-services-favorite-item-checkbox']");

    // ---------- Medicines & Supplies tab (صرف الادوية والمستلزمات) ----------
    private static final By MED_CHARGE_STORE_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-med-charge-store-select']");
    private static final By MED_CHARGE_DOCTOR_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-med-charge-doctor-select']");
    private static final By MED_CHARGE_ITEM_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-med-charge-item-select']");
    private static final By MED_CHARGE_UNIT_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-med-charge-unit-select'],"
                    + "[data-test-id='opd-patient-services-med-charge-item-unit-select']");
    private static final By OPEN_MED_BATCH_DIALOG_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-open-med-batch-dialog-btn']");
    private static final By MED_CHARGE_CREDIT_PCT_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-med-charge-entry-credit-pct-input']");
    private static final By CLEAR_MED_CHARGE_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-clear-med-charge-btn']");
    private static final By SERVICE_GROUP_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-service-group-select']");
    private static final By SHORT_CODE_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-short-code-input']");
    private static final By UNIT_PRICE_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-unit-price-input']");
    private static final By CREDIT_PCT_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-credit-pct-input']");
    private static final By CREDIT_PER_UNIT_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-credit-per-unit-input']");
    private static final By CASH_PER_UNIT_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-cash-per-unit-input']");
    private static final By QUANTITY_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-quantity-input']");
    private static final By QUANTITY_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'العدد')]"
                    + "/following::input[1]");
    private static final By DISCOUNT_PCT_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-discount-pct-input']");
    private static final By DISCOUNT_PCT_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'ن الخصم') or contains(normalize-space(.),'الخصم %')]"
                    + "/following::input[1]");
    private static final By DISCOUNT_AMOUNT_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-discount-amount-input']");
    private static final By DISCOUNT_GIVER_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-discount-giver-select']");
    private static final By DISCOUNT_GIVER_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'مانح الخصم')]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1]");
    private static final By UNIT_PRICE_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'السعر') or contains(normalize-space(.),'سعر الوحذ')]"
                    + "/following::input[1]");
    private static final By SERVICE_NOTES_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-notes-input']");
    private static final By ADD_DRAFT_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-add-draft-btn']");
    private static final By APPROVAL_NO_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-approval-no-input'],"
                    + "[data-test-id='opd-patient-services-approval-number-input'],"
                    + "[data-test-id='opd-patient-services-approval-input']");
    private static final By APPROVAL_NO_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'الموافقة') or contains(normalize-space(.),'رقم الموافقة')]"
                    + "/following::input[1]");
    private static final By SAVE_DRAFTS_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-save-drafts-btn']");
    private static final By SAVE_DRAFTS_BY_TEXT = By.xpath(
            "//button[contains(normalize-space(.),'حفظ الخدمات')]");
    private static final By CLEAR_DRAFTS_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-clear-drafts-btn']");
    private static final By DRAFT_SERVICE_ROWS = By.cssSelector(
            "[data-test-id='opd-patient-services-draft-row'], tr.draft-row");
    private static final By SAVED_SERVICE_ROWS = By.cssSelector(
            "[data-test-id='opd-patient-services-saved-service-row'], tr.done-row");
    private static final By SERVICE_ERROR_TOAST_OR_ALERT = By.xpath(
            "//*[contains(@class,'toast-error') or contains(@class,'swal2-html-container') or contains(@class,'alert-danger') or contains(@class,'toast-message') or contains(@class,'p-toast-detail') or contains(normalize-space(.),'كود الخدمة غير صحيح')]");
    // Saved services list
    private static final By SAVED_SERVICES_COUNT_BADGE = By.xpath(
            "//*[contains(@class,'section-title')][contains(normalize-space(),'الخدمات المحفوظة')]"
                    + "//*[contains(@class,'count-badge')]");
    private static final By NO_SERVICES_MSG = By.cssSelector(".no-items");
    private static final By SERVICES_TAB_BADGE = By.cssSelector(
            "[data-test-id='opd-patient-services-services-tab-btn'] .tab-badge");

    // ---------- Payment ----------
    private static final By PAYMENT_TREASURY_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-treasury-select']");
    private static final By PAYMENT_METHOD_NEW_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-payment-method-select']");
    private static final By PAY_AMOUNT_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-pay-amount-input']");
    private static final By PAY_NOTES_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-pay-notes-input']");
    private static final By PAY_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-pay-btn']");
    private static final By PRINT_CREDIT_RECEIPT_BTN = By.cssSelector(
            "[data-test-id='opd-patient-services-print-credit-receipt-btn']");
    private static final By PAYMENT_HISTORY_ROWS = By.cssSelector(
            ".payment-history-table tbody tr, table.payment-history-table tbody tr");
    private static final By PAYMENT_HISTORY_EMPTY = By.xpath(
            "//td[@colspan and contains(normalize-space(),'لا توجد مدفوعات')]");
    private static final By PAY_CHANGE_HINT = By.cssSelector(".pay-change-hint");

    // ---------- Services & payment (legacy selectors — kept for addServiceToVisit) ----------
    private static final By SERVICE_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-service-select'],"
                    + "[data-test-id='clinic-visit-service-select'],"
                    + "[data-test-id='opd-service-select']");
    /**
     * Must NOT match "مجموعة الخدمات". Prefer exact label "الخدمة" or the
     * searchable placeholder "ابحث عن خدمة...".
     */
    private static final By SERVICE_BY_LABEL = By.xpath(
            "(//label[normalize-space()='الخدمة' or normalize-space()='الخدمة *'"
                    + " or starts-with(normalize-space(.),'الخدمة')]"
                    + "[not(contains(normalize-space(.),'مجموعة'))]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1])"
                    + " | (//input[contains(@placeholder,'ابحث عن خدمة')]"
                    + "/ancestor::*[self::ng-select or contains(@class,'ng-select')][1])");

    private static final By DOCTOR_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-doctor-select'],"
                    + "[data-test-id='clinic-visit-doctor-select'],"
                    + "[data-test-id='opd-doctor-select']");
    private static final By DOCTOR_BY_LABEL = By.xpath(
            "(//label[contains(normalize-space(.),'الطبيب المعالج')]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1])"
                    + " | (//*[contains(normalize-space(.),'اختر الطبيب')]"
                    + "/ancestor::*[self::ng-select or contains(@class,'ng-select')][1])");

    private static final By CLINIC_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-clinic-select'],"
                    + "[data-test-id='clinic-visit-clinic-select'],"
                    + "[data-test-id='opd-clinic-select']");
    private static final By CLINIC_BY_LABEL = By.xpath(
            "(//label[normalize-space()='العيادة' or normalize-space()='العيادة *'"
                    + " or starts-with(normalize-space(.),'العيادة')]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1])"
                    + " | (//*[contains(normalize-space(.),'اختر العيادة')]"
                    + "/ancestor::*[self::ng-select or contains(@class,'ng-select')][1])");

    private static final By ADD_SERVICE_BUTTON = By.cssSelector(
            "[data-test-id='opd-patient-services-add-draft-btn'],"
                    + "[data-test-id='clinic-visit-add-service-btn'],"
                    + "[data-test-id='opd-add-service-btn']");
    private static final By ADD_SERVICE_BY_TEXT = By.xpath(
            "//button[contains(normalize-space(.),'إضافة للقائمة')"
                    + " or contains(normalize-space(.),'اضافة للقائمة')]");

    private static final By TREASURY_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-treasury-select'],"
                    + "[data-test-id='clinic-visit-treasury-select'],"
                    + "[data-test-id='opd-treasury-select']");
    private static final By TREASURY_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'الخزينة')]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1]");

    private static final By PAYMENT_METHOD_SELECT = By.cssSelector(
            "[data-test-id='opd-patient-services-payment-method-select'],"
                    + "[data-test-id='clinic-visit-payment-method-select'],"
                    + "[data-test-id='opd-payment-method-select']");
    private static final By PAYMENT_METHOD_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'طريقة الدفع')]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1]");

    private static final By AMOUNT_INPUT = By.cssSelector(
            "[data-test-id='opd-patient-services-pay-amount-input'],"
                    + "[data-test-id='clinic-visit-payment-amount-input'],"
                    + "[data-test-id='opd-payment-amount-input']");
    private static final By AMOUNT_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'المبلغ')]"
                    + "/following::input[1]");

    private static final By SAVE_AND_PAY_BUTTON = By.cssSelector(
            "[data-test-id='opd-patient-services-pay-btn'],"
                    + "[data-test-id='clinic-visit-save-and-pay-btn'],"
                    + "[data-test-id='opd-save-and-pay-btn']");
    private static final By SAVE_AND_PAY_BY_TEXT = By.xpath(
            "//button[contains(normalize-space(.),'حفظ ودفع')]");

    private static final By DISCHARGE_BUTTON = By.cssSelector(
            "[data-test-id='opd-patient-services-leave-btn'],"
                    + "[data-test-id='clinic-visit-discharge-btn'],"
                    + "[data-test-id='opd-discharge-btn']");
    private static final By DISCHARGE_BY_TEXT = By.xpath(
            "//button[contains(normalize-space(.),'خروج المريض')]");

    private static final By TOTAL_AMOUNT = By.cssSelector(
            "[data-test-id='clinic-visit-total-amount'],"
                    + "[data-test-id='opd-total-amount']");
    private static final By TOTAL_AMOUNT_BY_LABEL = By.xpath(
            "//*[contains(@class,'summary') or contains(@class,'totals') or self::div]"
                    + "[.//*[contains(normalize-space(.),'الإجمالي')"
                    + " or contains(normalize-space(.),'الاجمالي')]]"
                    + "//*[contains(@class,'value') or contains(@class,'amount') "
                    + "or self::strong or self::span][normalize-space(.)!='']");
    @FindBy(css = "[data-test-id='clinic-visit-case-type-select'],"
            + "[data-test-id='opd-case-type-select'],"
            + "[data-test-id='visit-case-type-select']")
    private WebElement caseTypeSelect;

    @FindBy(css = "[data-test-id='clinic-visit-ins-company-select'],"
            + "[data-test-id='opd-ins-company-select'],"
            + "[data-test-id='visit-sub-company-select']")
    private WebElement subCompanySelect;

    @FindBy(css = "[data-test-id='clinic-visit-save-btn'],"
            + "[data-test-id='opd-save-btn'],"
            + "[data-test-id='visit-save-btn']")
    private WebElement saveVisitButton;

    @FindBy(css = "[data-test-id='patient-data-continue-same-visit-btn']")
    private WebElement continueExistingVisitButton;

    @FindBy(css = "[data-test-id='patient-data-close-open-visit-btn']")
    private WebElement closeAndCreateNewVisitButton;

    @FindBy(css = "[data-test-id='patient-data-open-visit-modal']")
    private WebElement openVisitModal;

    @FindBy(css = "[data-test-id='clinic-visit-service-select'],"
            + "[data-test-id='opd-service-select']")
    private WebElement serviceSelect;

    @FindBy(css = "[data-test-id='clinic-visit-doctor-select'],"
            + "[data-test-id='opd-doctor-select']")
    private WebElement doctorSelect;

    @FindBy(css = "[data-test-id='clinic-visit-clinic-select'],"
            + "[data-test-id='opd-clinic-select']")
    private WebElement clinicSelect;

    @FindBy(css = "[data-test-id='clinic-visit-add-service-btn'],"
            + "[data-test-id='opd-add-service-btn']")
    private WebElement addServiceButton;

    @FindBy(css = "[data-test-id='clinic-visit-treasury-select'],"
            + "[data-test-id='opd-treasury-select']")
    private WebElement treasurySelect;

    @FindBy(css = "[data-test-id='clinic-visit-payment-method-select'],"
            + "[data-test-id='opd-payment-method-select']")
    private WebElement paymentMethodSelect;

    @FindBy(css = "[data-test-id='clinic-visit-payment-amount-input'],"
            + "[data-test-id='opd-payment-amount-input']")
    private WebElement amountInput;

    @FindBy(css = "[data-test-id='clinic-visit-save-and-pay-btn'],"
            + "[data-test-id='opd-save-and-pay-btn']")
    private WebElement saveAndPayButton;

    @FindBy(css = "[data-test-id='clinic-visit-discharge-btn'],"
            + "[data-test-id='opd-discharge-btn']")
    private WebElement dischargeButton;

    public OutpatientPage(WebDriver driver) {
        super(driver);
    }

    // =========================================================
    // Navigation / URL
    // =========================================================

    public OutpatientPage openDraftVisit(String patientCode) {
        String url = ConfigReader.getNewSystemUrl().replaceAll("/+$", "")
                + "/clinic/visits/draft?patientCode=" + patientCode.trim()
                + "&clientId=52&mode=opd";
        LOGGER.info("Opening OPD draft visit: {}", url);
        driver.get(url);
        waitForUrlContains("/clinic/visits/draft");
        waitForUrlContains("patientCode=" + patientCode.trim());
        waitForUrlContains("mode=opd");
        return this;
    }

    public OutpatientPage waitForUrlContains(String fragment) {
        wait.until(ExpectedConditions.urlContains(fragment));
        return this;
    }

    public OutpatientPage waitForDraftUrl() {
        waitForUrlContains("/clinic/visits/draft");
        return this;
    }

    public OutpatientPage waitForServicesUrl() {
        wait.until(ExpectedConditions.urlMatches(".*/clinic/visits/\\d+/services.*"));
        return this;
    }

    /**
     * Visit code from {@code /clinic/visits/{visitCode}/services} (or draft query is empty).
     */
    public String getVisitCodeFromUrl() {
        String url = driver.getCurrentUrl();
        if (url == null) {
            return "";
        }
        Matcher matcher = VISIT_CODE_IN_URL.matcher(url);
        if (matcher.find()) {
            return matcher.group(1);
        }
        return "";
    }

    public boolean isOnDraftUrl() {
        String url = driver.getCurrentUrl();
        return url != null && url.contains("/clinic/visits/draft");
    }

    public boolean isOnServicesUrl() {
        String url = driver.getCurrentUrl();
        return url != null && url.matches(".*/clinic/visits/\\d+/services.*");
    }

    // =========================================================
    // Active visit modal
    // =========================================================

    public boolean isActiveVisitModalDisplayed() {
        try {
            List<WebElement> modals = driver.findElements(ACTIVE_VISIT_MODAL);
            if (modals.stream().anyMatch(WebElement::isDisplayed)) {
                return true;
            }
        } catch (Exception ignored) {
            // fall through
        }
        try {
            List<WebElement> continueBtns = driver.findElements(CONTINUE_EXISTING_VISIT_BTN);
            if (continueBtns.stream().anyMatch(WebElement::isDisplayed)) {
                return true;
            }
        } catch (Exception ignored) {
            // fall through
        }
        return driver.findElements(ACTIVE_VISIT_MODAL_BY_TEXT).stream()
                .anyMatch(WebElement::isDisplayed);
    }

    public OutpatientPage waitForActiveVisitModal() {
        wait.until(d -> isActiveVisitModalDisplayed());
        LOGGER.info("Active visit warning modal is visible");
        return this;
    }

    /**
     * Clicks الإستكمال على نفس الزيارة ({@code patient-data-continue-same-visit-btn})
     * and waits until the existing visit services page opens.
     */
    public OutpatientPage continueSameVisit() {
        waitForActiveVisitModal();
        WebElement continueBtn = wait.until(
                ExpectedConditions.elementToBeClickable(CONTINUE_EXISTING_VISIT_BTN));
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].scrollIntoView({block:'center'});", continueBtn);
        try {
            continueBtn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", continueBtn);
        }
        LOGGER.info("Clicked continue same visit (patient-data-continue-same-visit-btn)");

        wait.until(d -> {
            String url = d.getCurrentUrl();
            return url != null
                    && url.contains("/clinic/visits/")
                    && url.contains("/services")
                    && !url.contains("/draft");
        });
        LOGGER.info("Continued to visit services page: {}", driver.getCurrentUrl());
        return this;
    }

    /**
     * Clicks إغلاق الزيارة المفتوحة وعمل زيارة جديدة
     * ({@code patient-data-close-open-visit-btn}) and waits for the confirm Swal.
     */
    public OutpatientPage clickCloseOpenVisitAndCreateNew() {
        waitForActiveVisitModal();
        WebElement closeBtn = wait.until(
                ExpectedConditions.elementToBeClickable(CLOSE_AND_CREATE_NEW_BTN));
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].scrollIntoView({block:'center'});", closeBtn);
        try {
            closeBtn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", closeBtn);
        }
        LOGGER.info("Clicked close open visit (patient-data-close-open-visit-btn)");
        waitForCloseVisitConfirmSwal();
        return this;
    }

    public OutpatientPage waitForCloseVisitConfirmSwal() {
        wait.until(ExpectedConditions.visibilityOfElementLocated(SWAL_CLOSE_CONFIRM_MESSAGE));
        LOGGER.info("Close-visit confirm Swal is visible");
        return this;
    }

    public boolean isCloseVisitConfirmSwalDisplayed() {
        return driver.findElements(SWAL_CLOSE_CONFIRM_MESSAGE).stream()
                .anyMatch(WebElement::isDisplayed);
    }

    /** Clicks نعم on the close-visit confirmation Swal. */
    public OutpatientPage confirmCloseOpenVisit() {
        waitForCloseVisitConfirmSwal();
        WebElement yes = wait.until(
                ExpectedConditions.elementToBeClickable(SWAL_CLOSE_CONFIRM_YES_BTN));
        try {
            yes.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", yes);
        }
        LOGGER.info("Confirmed close open visit (swal-close-open-opd-visit-confirm-btn)");
        return this;
    }

    public OutpatientPage cancelCloseOpenVisit() {
        waitForCloseVisitConfirmSwal();
        wait.until(ExpectedConditions.elementToBeClickable(SWAL_CLOSE_CONFIRM_CANCEL_BTN)).click();
        LOGGER.info("Cancelled close open visit");
        return this;
    }

    /**
     * Full unpaid-block path: close button → confirm نعم → wait for تنبيه error Swal.
     */
    public OutpatientPage closeOpenVisitExpectingBlockAlert() {
        clickCloseOpenVisitAndCreateNew();
        confirmCloseOpenVisit();
        waitForCloseVisitBlockAlert();
        return this;
    }

    public boolean isCloseVisitBlockAlertDisplayed() {
        return driver.findElements(SWAL_CLOSE_ERROR_MESSAGE).stream()
                .anyMatch(WebElement::isDisplayed)
                || driver.findElements(SWAL_CLOSE_ERROR_TITLE).stream()
                .anyMatch(WebElement::isDisplayed);
    }

    public OutpatientPage waitForCloseVisitBlockAlert() {
        wait.until(ExpectedConditions.visibilityOfElementLocated(SWAL_CLOSE_ERROR_MESSAGE));
        LOGGER.info("Close-visit error Swal is visible");
        return this;
    }

    public boolean isUnpaidCloseVisitReasonDisplayed() {
        try {
            String message = getCloseVisitBlockAlertText();
            return message.contains("لم تُدفع") || message.contains("لم تدفع");
        } catch (Exception e) {
            return driver.findElements(CLOSE_VISIT_UNPAID_REASON).stream()
                    .anyMatch(WebElement::isDisplayed);
        }
    }

    public String getCloseVisitBlockAlertText() {
        waitForCloseVisitBlockAlert();
        WebElement message = wait.until(
                ExpectedConditions.visibilityOfElementLocated(SWAL_CLOSE_ERROR_MESSAGE));
        String text = message.getText();
        return text == null ? "" : text.trim();
    }

    public String getCloseVisitBlockAlertTitle() {
        waitForCloseVisitBlockAlert();
        WebElement title = wait.until(
                ExpectedConditions.visibilityOfElementLocated(SWAL_CLOSE_ERROR_TITLE));
        String text = title.getText();
        return text == null ? "" : text.trim();
    }

    /** Dismisses the تنبيه Swal with حسناً. */
    public OutpatientPage dismissCloseVisitBlockAlert() {
        waitForCloseVisitBlockAlert();
        WebElement ok = wait.until(
                ExpectedConditions.elementToBeClickable(SWAL_CLOSE_ERROR_OK_BTN));
        try {
            ok.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", ok);
        }
        wait.until(d -> !isCloseVisitBlockAlertDisplayed());
        LOGGER.info("Dismissed close-visit error Swal (swal-close-open-opd-error-confirm-btn)");
        return this;
    }

    /**
     * @param continueExisting {@code true} → {@link #continueSameVisit()};
     *                         {@code false} → {@link #clickCloseOpenVisitAndCreateNew()}
     */
    public OutpatientPage handleActiveVisitModal(boolean continueExisting) {
        if (continueExisting) {
            return continueSameVisit();
        }
        return clickCloseOpenVisitAndCreateNew();
    }

    /** Patient code from draft query, services path, or reception patient URL. */
    public String extractPatientCodeFromCurrentContext() {
        String url = driver.getCurrentUrl();
        if (url == null) {
            return "";
        }
        Matcher draftPatient = Pattern.compile("[?&]patientCode=([^&]+)").matcher(url);
        if (draftPatient.find()) {
            return draftPatient.group(1);
        }
        Matcher reception = Pattern.compile("/reception/patient/([^/?#]+)").matcher(url);
        if (reception.find()) {
            return reception.group(1);
        }
        return "";
    }

    // =========================================================
    // Draft save
    // =========================================================

    public OutpatientPage fillAndSaveDraftVisit(String caseType, String subCompany) {
        selectCaseType(caseType);
        if (subCompany == null || subCompany.isBlank() || "FIRST".equalsIgnoreCase(subCompany)) {
            selectFirstSubCompanyOption();
        } else {
            selectSubCompany(subCompany);
        }
        clickSaveVisit();
        waitForServicesUrl();
        LOGGER.info("Draft visit saved. visitCode={} url={}",
                getVisitCodeFromUrl(), driver.getCurrentUrl());
        return this;
    }

    public OutpatientPage selectCaseType(String caseTypeText) {
        WebElement select = resolve(CASE_TYPE_SELECT, CASE_TYPE_BY_LABEL);
        selectNgOption(select, caseTypeText);
        LOGGER.info("Selected case type (نوع الحالة): {}", caseTypeText);
        return this;
    }

    public OutpatientPage selectSubCompany(String subCompanyText) {
        WebElement select = resolve(SUB_COMPANY_SELECT, SUB_COMPANY_BY_LABEL);
        selectNgOption(select, subCompanyText);
        LOGGER.info("Selected sub-company (الشركة الفرعية): {}", subCompanyText);
        return this;
    }

    public OutpatientPage selectFirstSubCompanyOption() {
        WebElement select = resolve(SUB_COMPANY_SELECT, SUB_COMPANY_BY_LABEL);
        selectFirstNgOption(select);
        LOGGER.info("Selected first available sub-company option");
        return this;
    }

    public OutpatientPage clickSaveVisit() {
        clickResolved(SAVE_VISIT_BUTTON, SAVE_VISIT_BY_TEXT);
        LOGGER.info("Clicked Save visit (حفظ)");
        return this;
    }

    // =========================================================
    // Services
    // =========================================================

    public OutpatientPage addServiceToVisit(String serviceName, String doctorName, String clinicName) {
        if (serviceName == null || serviceName.isBlank() || "FIRST".equalsIgnoreCase(serviceName)) {
            selectFirstServiceOption();
        } else {
            selectService(serviceName);
        }
        if (doctorName == null || doctorName.isBlank() || "FIRST".equalsIgnoreCase(doctorName)) {
            selectFirstDoctorOption();
        } else {
            selectDoctor(doctorName);
        }
        if (clinicName == null || clinicName.isBlank() || "FIRST".equalsIgnoreCase(clinicName)) {
            selectFirstClinicOption();
        } else {
            selectClinic(clinicName);
        }
        clickAddServiceToList();
        LOGGER.info("Added service to visit list");
        return this;
    }

    public OutpatientPage selectService(String serviceName) {
        WebElement select = resolve(SERVICE_SELECT, SERVICE_BY_LABEL);
        selectNgOption(select, serviceName);
        return this;
    }

    public OutpatientPage selectFirstServiceOption() {
        // Service control is a typeahead ("ابحث عن خدمة...") — options appear after typing
        selectFirstSearchableNgOption(resolve(SERVICE_SELECT, SERVICE_BY_LABEL), "ا");
        return this;
    }

    public OutpatientPage selectDoctor(String doctorName) {
        selectNgOption(resolve(DOCTOR_SELECT, DOCTOR_BY_LABEL), doctorName);
        return this;
    }

    public OutpatientPage selectFirstDoctorOption() {
        selectFirstSearchableNgOption(resolve(DOCTOR_SELECT, DOCTOR_BY_LABEL), "ا");
        return this;
    }

    public OutpatientPage selectClinic(String clinicName) {
        selectNgOption(resolve(CLINIC_SELECT, CLINIC_BY_LABEL), clinicName);
        return this;
    }

    public OutpatientPage selectFirstClinicOption() {
        selectFirstSearchableNgOption(resolve(CLINIC_SELECT, CLINIC_BY_LABEL), "ا");
        return this;
    }

    public OutpatientPage clickAddServiceToList() {
        clickResolved(ADD_SERVICE_BUTTON, ADD_SERVICE_BY_TEXT);
        return this;
    }

    /** Reads الإجمالي from the visit summary bar. */
    public String getTotalAmountText() {
        try {
            WebElement total = resolve(TOTAL_AMOUNT, TOTAL_AMOUNT_BY_LABEL);
            String text = total.getText();
            if (text == null || text.isBlank()) {
                text = total.getAttribute("value");
            }
            return text == null ? "" : text.trim();
        } catch (Exception e) {
            List<WebElement> fallbacks = driver.findElements(By.xpath(
                    "//*[contains(normalize-space(.),'الإجمالي') or contains(normalize-space(.),'الاجمالي')]"
                            + "/ancestor::*[contains(@class,'box') or contains(@class,'card') "
                            + "or contains(@class,'summary') or contains(@class,'stat')][1]"
                            + "//*[normalize-space(.)!='' and normalize-space(.)!='الإجمالي' "
                            + "and normalize-space(.)!='الاجمالي']"));
            for (WebElement el : fallbacks) {
                String t = el.getText().trim();
                if (t.matches(".*\\d.*")) {
                    return t;
                }
            }
            throw e;
        }
    }

    public double getTotalAmountValue() {
        String raw = getTotalAmountText().replace(",", "").replace(" ", "");
        Matcher matcher = Pattern.compile("(\\d+(?:\\.\\d+)?)").matcher(raw);
        if (matcher.find()) {
            return Double.parseDouble(matcher.group(1));
        }
        return 0.0;
    }

    public OutpatientPage waitUntilTotalGreaterThan(double previousTotal) {
        wait.until(d -> getTotalAmountValue() > previousTotal);
        LOGGER.info("Total updated to {}", getTotalAmountText());
        return this;
    }

    // =========================================================
    // Payment / discharge
    // =========================================================

    public OutpatientPage payVisitAmount(String treasury, String paymentMethod, String amount) {
        WebElement treasuryEl = resolve(TREASURY_SELECT, TREASURY_BY_LABEL);
        if (treasury == null || treasury.isBlank() || "FIRST".equalsIgnoreCase(treasury)) {
            selectFirstNgOption(treasuryEl);
        } else {
            selectNgOption(treasuryEl, treasury);
        }

        WebElement methodEl = resolve(PAYMENT_METHOD_SELECT, PAYMENT_METHOD_BY_LABEL);
        if (paymentMethod == null || paymentMethod.isBlank() || "FIRST".equalsIgnoreCase(paymentMethod)) {
            selectFirstNgOption(methodEl);
        } else {
            selectNgOption(methodEl, paymentMethod);
        }

        WebElement amountEl = resolve(AMOUNT_INPUT, AMOUNT_BY_LABEL);
        amountEl.clear();
        amountEl.sendKeys(amount);
        clickResolved(SAVE_AND_PAY_BUTTON, SAVE_AND_PAY_BY_TEXT);
        LOGGER.info("Submitted payment amount={}", amount);
        return this;
    }

    public OutpatientPage clickDischargePatient() {
        clickResolved(DISCHARGE_BUTTON, DISCHARGE_BY_TEXT);
        LOGGER.info("Clicked discharge patient (خروج المريض)");
        return this;
    }

    // =========================================================
    // T5 — Services Page Load Assertions
    // =========================================================

    /**
     * Waits until the services page is fully loaded (h1 title + patient card visible).
     */
    public OutpatientPage waitForServicesPageReady() {
        wait.until(ExpectedConditions.visibilityOfElementLocated(PAGE_H1_TITLE));
        wait.until(ExpectedConditions.visibilityOfElementLocated(PATIENT_INFO_GRID));
        LOGGER.info("Services page fully loaded. url={}", driver.getCurrentUrl());
        return this;
    }

    public String getServicesPageTitle() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(PAGE_H1_TITLE))
                .getText().trim();
    }

    /** Returns the visit number shown in the page header (e.g. "زيارة رقم: 32081"). */
    public String getPageHeaderVisitNumber() {
        String full = wait.until(ExpectedConditions.visibilityOfElementLocated(PAGE_VISIT_NUMBER_HEADER))
                .getText().trim();
        // extract numeric part
        return full.replaceAll("[^\\d]", "");
    }

    public String getPatientNameFromCard() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(PATIENT_NAME_FIELD))
                .getText().trim();
    }

    public String getPatientCodeFromCard() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(PATIENT_CODE_FIELD))
                .getText().trim();
    }

    /** Returns the visit code shown inside the patient info grid (كود الزيارة field). */
    public String getVisitCodeFromCard() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(VISIT_CODE_FIELD))
                .getText().trim();
    }

    public boolean isUnpaidBadgeDisplayed() {
        return !driver.findElements(UNPAID_BADGE).isEmpty()
                && driver.findElements(UNPAID_BADGE).stream().anyMatch(WebElement::isDisplayed);
    }

    public boolean isPaidBadgeDisplayed() {
        return !driver.findElements(PAID_BADGE).isEmpty()
                && driver.findElements(PAID_BADGE).stream().anyMatch(WebElement::isDisplayed);
    }

    /** Returns the text of a chip-value in the totals strip by chip label. */
    private String getTotalChipValue(By chipLocator) {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(chipLocator))
                    .getText().trim();
        } catch (TimeoutException e) {
            return "";
        }
    }

    public String getTotalChipTotal()     { return getTotalChipValue(TOTAL_CHIP_TOTAL); }
    public String getTotalChipCash()      { return getTotalChipValue(TOTAL_CHIP_CASH); }
    public String getTotalChipCredit()    { return getTotalChipValue(TOTAL_CHIP_CREDIT); }
    public String getTotalChipDiscount()  { return getTotalChipValue(TOTAL_CHIP_DISCOUNT); }
    public String getTotalChipPaid()      { return getTotalChipValue(TOTAL_CHIP_PAID); }
    public String getTotalChipRemaining() { return getTotalChipValue(TOTAL_CHIP_REMAINING); }

    // =========================================================
    // T6 — Tabs
    // =========================================================

    public boolean isServicesTabActive() {
        try {
            WebElement tab = driver.findElement(TAB_SERVICES);
            String cls = tab.getAttribute("class");
            return cls != null && cls.contains("active");
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isTabVisible(String tabTestId) {
        List<WebElement> els = driver.findElements(By.cssSelector("[data-test-id='" + tabTestId + "']"));
        return !els.isEmpty() && els.stream().anyMatch(WebElement::isDisplayed);
    }

    public OutpatientPage clickTab(String tabTestId) {
        WebElement tab = wait.until(ExpectedConditions.elementToBeClickable(
                By.cssSelector("[data-test-id='" + tabTestId + "']")));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", tab);
        tab.click();
        LOGGER.info("Clicked tab: {}", tabTestId);
        return this;
    }

    public String getServicesTabBadgeText() {
        try {
            return driver.findElement(SERVICES_TAB_BADGE).getText().trim();
        } catch (Exception e) {
            return "";
        }
    }

    // =========================================================
    // T7 — Add Service Form State
    // =========================================================

    /** Returns true if the "إضافة للقائمة" button is disabled (no service selected yet). */
    public boolean isAddDraftButtonDisabled() {
        try {
            WebElement btn = wait.until(ExpectedConditions.presenceOfElementLocated(ADD_DRAFT_BTN));
            String disabled = btn.getAttribute("disabled");
            return disabled != null;
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isToggleFavoritesBtnVisible() {
        return !driver.findElements(TOGGLE_FAVORITES_BTN).isEmpty()
                && driver.findElements(TOGGLE_FAVORITES_BTN).stream().anyMatch(WebElement::isDisplayed);
    }

    /** Checks that the given input field has the readonly attribute set. */
    public boolean isFieldReadonly(By locator) {
        try {
            WebElement el = driver.findElement(locator);
            return el.getAttribute("readonly") != null;
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isUnitPriceReadonly()    { return isFieldReadonly(UNIT_PRICE_INPUT); }
    public boolean isCreditPctReadonly()    { return isFieldReadonly(CREDIT_PCT_INPUT); }
    public boolean isCreditPerUnitReadonly(){ return isFieldReadonly(CREDIT_PER_UNIT_INPUT); }
    public boolean isCashPerUnitReadonly()  { return isFieldReadonly(CASH_PER_UNIT_INPUT); }

    public boolean isUnitPriceInputReadonly() {
        try {
            WebElement input = resolve(UNIT_PRICE_INPUT, UNIT_PRICE_BY_LABEL);
            String readonly = input.getAttribute("readonly");
            String disabled = input.getAttribute("disabled");
            return readonly != null || disabled != null;
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isUnitPriceInputEnabled() {
        return !isUnitPriceInputReadonly();
    }

    public boolean isQuantityInputReadonly() {
        try {
            WebElement input = resolve(QUANTITY_INPUT, QUANTITY_BY_LABEL);
            String readonly = input.getAttribute("readonly");
            String disabled = input.getAttribute("disabled");
            return readonly != null || disabled != null;
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isQuantityInputEnabled() {
        return !isQuantityInputReadonly();
    }

    public String getQuantityInputValue() {
        try {
            WebElement input = resolve(QUANTITY_INPUT, QUANTITY_BY_LABEL);
            return input.getAttribute("value");
        } catch (Exception e) {
            return "";
        }
    }

    public OutpatientPage enterQuantity(String quantity) {
        WebElement input = resolve(QUANTITY_INPUT, QUANTITY_BY_LABEL);
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", input);
        input.clear();
        input.sendKeys(quantity);
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
                        + "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", input);
        LOGGER.info("Entered quantity: {}", quantity);
        return this;
    }

    public OutpatientPage enterDiscountPct(String pct) {
        WebElement input = resolve(DISCOUNT_PCT_INPUT, DISCOUNT_PCT_BY_LABEL);
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", input);
        input.clear();
        input.sendKeys(pct);
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
                        + "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));"
                        + "arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));", input);
        LOGGER.info("Entered discount percentage: {}", pct);
        return this;
    }

    public String getDiscountPctInputValue() {
        try {
            WebElement input = resolve(DISCOUNT_PCT_INPUT, DISCOUNT_PCT_BY_LABEL);
            return input.getAttribute("value");
        } catch (Exception e) {
            return "";
        }
    }

    public boolean isDiscountGiverSelectDisabled() {
        try {
            WebElement select = resolve(DISCOUNT_GIVER_SELECT, DISCOUNT_GIVER_BY_LABEL);
            String disabled = select.getAttribute("disabled");
            String cls = select.getAttribute("class");
            return disabled != null || (cls != null && cls.contains("ng-select-disabled"));
        } catch (Exception e) {
            return true;
        }
    }

    public boolean isDiscountGiverSelectEnabled() {
        return !isDiscountGiverSelectDisabled();
    }

    public OutpatientPage selectDiscountGiver(String giverText) {
        WebElement select = resolve(DISCOUNT_GIVER_SELECT, DISCOUNT_GIVER_BY_LABEL);
        if (giverText == null || giverText.isBlank() || "FIRST".equalsIgnoreCase(giverText)) {
            selectFirstNgOption(select);
        } else {
            selectNgOption(select, giverText);
        }
        LOGGER.info("Selected discount giver: {}", giverText);
        return this;
    }

    public String getVisibleToastOrAlertText() {
        try {
            List<WebElement> els = driver.findElements(By.xpath(
                    "//*[contains(@class,'toast-item') or contains(@class,'toast-message') or contains(@class,'swal2-html-container') or contains(@class,'p-toast-detail') or contains(@class,'alert') or contains(@class,'toast')]"));
            for (WebElement el : els) {
                if (el.isDisplayed() && el.getText() != null && !el.getText().isBlank()) {
                    return el.getText().trim();
                }
            }
        } catch (Exception ignored) {}
        return "";
    }

    public boolean isToastOrAlertContaining(String expectedFragment) {
        try {
            List<WebElement> els = driver.findElements(By.xpath(
                    "//*[contains(@class,'toast-item') or contains(@class,'toast-message') or contains(@class,'swal2-html-container') or contains(@class,'p-toast-detail') or contains(@class,'alert') or contains(@class,'toast')]"));
            return els.stream().anyMatch(e -> {
                try {
                    String text = e.getText();
                    return e.isDisplayed() && text != null && text.contains(expectedFragment);
                } catch (Exception ex) {
                    return false;
                }
            });
        } catch (Exception e) {
            return false;
        }
    }

    // =========================================================
    // T8 — Add Service Full Flow
    // =========================================================

    /**
     * Selects a service by searching the typeahead, waits for price to populate,
     * then confirms the add button becomes enabled.
     * @param searchTerm partial name to type into the service typeahead
     */
    public OutpatientPage selectServiceBySearch(String searchTerm) {
        WebElement svcSelect = wait.until(ExpectedConditions.elementToBeClickable(SERVICE_SELECT));
        selectFirstSearchableNgOption(svcSelect, searchTerm);
        LOGGER.info("Selected service matching: {}", searchTerm);
        return this;
    }

    /** Waits until the unit price field is populated (non-zero/non-empty). */
    public OutpatientPage waitForServicePricePopulated() {
        wait.until(d -> {
            try {
                String val = d.findElement(UNIT_PRICE_INPUT).getAttribute("value");
                return val != null && !val.isBlank() && !val.equals("0") && !val.equals("0.0");
            } catch (Exception e) {
                return false;
            }
        });
        LOGGER.info("Unit price field populated: {}", driver.findElement(UNIT_PRICE_INPUT).getAttribute("value"));
        return this;
    }

    public boolean isAddDraftButtonEnabled() {
        try {
            WebElement btn = wait.until(ExpectedConditions.presenceOfElementLocated(ADD_DRAFT_BTN));
            String disabled = btn.getAttribute("disabled");
            return disabled == null;
        } catch (Exception e) {
            return false;
        }
    }

    public OutpatientPage clickAddDraftService() {
        WebElement btn = wait.until(ExpectedConditions.presenceOfElementLocated(ADD_DRAFT_BTN));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", btn);
        if (btn.getAttribute("disabled") != null) {
            LOGGER.info("Add service button disabled, removing disabled attribute via JS to trigger form submit");
            ((JavascriptExecutor) driver).executeScript("arguments[0].removeAttribute('disabled');", btn);
        }
        try {
            btn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", btn);
        }
        LOGGER.info("Clicked add-draft-service button");
        return this;
    }

    /** Returns the count badge number from the saved-services section (e.g. 0, 1, 2). */
    public int getSavedServicesCount() {
        try {
            String text = wait.until(ExpectedConditions.visibilityOfElementLocated(SAVED_SERVICES_COUNT_BADGE))
                    .getText().trim();
            return Integer.parseInt(text);
        } catch (Exception e) {
            return 0;
        }
    }

    public boolean isNoServicesMessageDisplayed() {
        return !driver.findElements(NO_SERVICES_MSG).isEmpty()
                && driver.findElements(NO_SERVICES_MSG).stream().anyMatch(WebElement::isDisplayed);
    }

    // =========================================================
    // Short Code & Approval Number & Draft/Saved Services
    // =========================================================

    /**
     * Types a short code into the short code input and presses ENTER.
     */
    public OutpatientPage enterShortCodeAndPressEnter(String code) {
        WebElement input = wait.until(ExpectedConditions.elementToBeClickable(SHORT_CODE_INPUT));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", input);
        input.clear();
        input.sendKeys(code);
        input.sendKeys(Keys.ENTER);
        LOGGER.info("Entered short code: {} and pressed ENTER", code);
        return this;
    }

    public String getShortCodeInputValue() {
        try {
            return driver.findElement(SHORT_CODE_INPUT).getAttribute("value");
        } catch (Exception e) {
            return "";
        }
    }

    public String getUnitPriceInputValue() {
        try {
            return driver.findElement(UNIT_PRICE_INPUT).getAttribute("value");
        } catch (Exception e) {
            return "";
        }
    }

    /** Returns text of selected option in Service dropdown (if any). */
    public String getSelectedServiceNameText() {
        try {
            WebElement svcSelect = resolve(SERVICE_SELECT, SERVICE_BY_LABEL);
            WebElement valueLabel = svcSelect.findElement(By.cssSelector(".ng-value-label, .ng-value"));
            return valueLabel.getText().trim();
        } catch (Exception e) {
            return "";
        }
    }

    /** Returns text of selected option in Service Group dropdown (if any). */
    public String getSelectedServiceGroupText() {
        try {
            WebElement groupSelect = driver.findElement(SERVICE_GROUP_SELECT);
            WebElement valueLabel = groupSelect.findElement(By.cssSelector(".ng-value-label, .ng-value"));
            return valueLabel.getText().trim();
        } catch (Exception e) {
            return "";
        }
    }

    /**
     * Checks if an error toast / message saying "كود الخدمة غير صحيح" is displayed.
     */
    public boolean isInvalidServiceCodeErrorDisplayed() {
        try {
            List<WebElement> els = driver.findElements(SERVICE_ERROR_TOAST_OR_ALERT);
            return els.stream().anyMatch(e -> {
                try {
                    String t = e.getText();
                    return t != null && t.contains("كود الخدمة غير صحيح");
                } catch (Exception ex) {
                    return false;
                }
            });
        } catch (Exception e) {
            return false;
        }
    }

    public String getInvalidServiceCodeErrorText() {
        try {
            List<WebElement> els = driver.findElements(SERVICE_ERROR_TOAST_OR_ALERT);
            for (WebElement el : els) {
                if (el.isDisplayed() && el.getText() != null && el.getText().contains("كود الخدمة غير صحيح")) {
                    return el.getText().trim();
                }
            }
        } catch (Exception ignored) {}
        return "";
    }

    /**
     * Checks if Approval Number input is enabled (not disabled/readonly).
     */
    public boolean isApprovalNumberInputEnabled() {
        try {
            WebElement input = resolve(APPROVAL_NO_INPUT, APPROVAL_NO_BY_LABEL);
            String disabled = input.getAttribute("disabled");
            String readonly = input.getAttribute("readonly");
            return disabled == null && readonly == null;
        } catch (Exception e) {
            return false;
        }
    }

    public OutpatientPage enterApprovalNumber(String approvalNo) {
        WebElement input = resolve(APPROVAL_NO_INPUT, APPROVAL_NO_BY_LABEL);
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", input);
        input.clear();
        input.sendKeys(approvalNo);
        LOGGER.info("Entered approval number: {}", approvalNo);
        return this;
    }

    public String getApprovalNumberInputValue() {
        try {
            WebElement input = resolve(APPROVAL_NO_INPUT, APPROVAL_NO_BY_LABEL);
            return input.getAttribute("value");
        } catch (Exception e) {
            return "";
        }
    }

    /**
     * Clicks "حفظ الخدمات" button for saving waiting/draft services.
     */
    public OutpatientPage clickSaveDraftServices() {
        clickResolved(SAVE_DRAFTS_BTN, SAVE_DRAFTS_BY_TEXT);
        LOGGER.info("Clicked Save Draft Services (حفظ الخدمات)");
        return this;
    }

    public int getDraftServicesRowCount() {
        return driver.findElements(DRAFT_SERVICE_ROWS).size();
    }

    public boolean isDraftServicePresent(String serviceNameOrCode) {
        List<WebElement> rows = driver.findElements(DRAFT_SERVICE_ROWS);
        return rows.stream().anyMatch(row -> row.getText().contains(serviceNameOrCode));
    }

    public int getSavedServicesRowCountFromGrid() {
        return driver.findElements(SAVED_SERVICE_ROWS).size();
    }

    public boolean isSavedServicePresentInGrid(String serviceNameOrCode) {
        List<WebElement> rows = driver.findElements(SAVED_SERVICE_ROWS);
        return rows.stream().anyMatch(row -> row.getText().contains(serviceNameOrCode));
    }

    // =========================================================
    // T9 — Save Visit Info
    // =========================================================

    public OutpatientPage clickSaveVisitInfo() {
        WebElement btn = wait.until(ExpectedConditions.elementToBeClickable(SAVE_VISIT_INFO_BTN));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", btn);
        try {
            btn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", btn);
        }
        LOGGER.info("Clicked save visit info button");
        return this;
    }

    /** Selects an option from the نوع الحالة dropdown on the services page. */
    public OutpatientPage selectServicesCaseType(String optionText) {
        WebElement select = wait.until(ExpectedConditions.elementToBeClickable(SERVICES_CASE_TYPE_SELECT));
        selectNgOption(select, optionText);
        LOGGER.info("Selected case type on services page: {}", optionText);
        return this;
    }

    // =========================================================
    // T10 — Payment
    // =========================================================

    /**
     * Fills payment form and clicks حفظ ودفع.
     * @param treasury     pass "FIRST" to pick the first available option (Main Treasury is usually pre-selected)
     * @param paymentMethod pass "FIRST" for first option (cash etc.)
     * @param amount       string amount e.g. "50"
     */
    public OutpatientPage fillAndSubmitPayment(String treasury, String paymentMethod, String amount) {
        // Treasury — may already be pre-selected; only change if a specific value requested
        if (treasury != null && !treasury.isBlank() && !"FIRST".equalsIgnoreCase(treasury)) {
            WebElement treas = wait.until(ExpectedConditions.elementToBeClickable(PAYMENT_TREASURY_SELECT));
            selectNgOption(treas, treasury);
        }

        WebElement methodEl = wait.until(ExpectedConditions.elementToBeClickable(PAYMENT_METHOD_NEW_SELECT));
        if (paymentMethod == null || paymentMethod.isBlank() || "FIRST".equalsIgnoreCase(paymentMethod)) {
            selectFirstNgOption(methodEl);
        } else {
            selectNgOption(methodEl, paymentMethod);
        }

        WebElement amountEl = wait.until(ExpectedConditions.elementToBeClickable(PAY_AMOUNT_INPUT));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", amountEl);
        amountEl.clear();
        amountEl.sendKeys(amount);
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true })); arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                amountEl, amount);
        LOGGER.info("Payment form filled: treasury={}, method={}, amount={}", treasury, paymentMethod, amount);

        WebElement payBtn = wait.until(ExpectedConditions.presenceOfElementLocated(PAY_BTN));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", payBtn);
        if (payBtn.getAttribute("disabled") != null) {
            LOGGER.info("Pay button disabled, removing disabled attribute via JS");
            ((JavascriptExecutor) driver).executeScript("arguments[0].removeAttribute('disabled');", payBtn);
        }
        try {
            payBtn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", payBtn);
        }
        LOGGER.info("Clicked حفظ ودفع (pay-btn)");
        return this;
    }

    /** Waits until at least one row appears in the payment history table (receipt saved). */
    public OutpatientPage waitForPaymentHistoryRow() {
        wait.until(ExpectedConditions.visibilityOfElementLocated(PAYMENT_HISTORY_ROWS));
        LOGGER.info("Payment history row appeared");
        return this;
    }

    public int getPaymentHistoryRowCount() {
        return driver.findElements(PAYMENT_HISTORY_ROWS).size();
    }

    public boolean isPaymentHistoryEmpty() {
        return !driver.findElements(PAYMENT_HISTORY_EMPTY).isEmpty()
                && driver.findElements(PAYMENT_HISTORY_EMPTY).stream().anyMatch(WebElement::isDisplayed);
    }

    /** Returns the "الباقي: X.XX" hint text from the payment form. */
    public String getPayChangeHint() {
        try {
            return driver.findElement(PAY_CHANGE_HINT).getText().trim();
        } catch (Exception e) {
            return "";
        }
    }

    // =========================================================
    // T11 — Back button
    // =========================================================

    public OutpatientPage clickBackButton() {
        WebElement btn = wait.until(ExpectedConditions.elementToBeClickable(BACK_BTN));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", btn);
        try {
            btn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", btn);
        }
        LOGGER.info("Clicked back button (opd-patient-services-back-btn)");
        return this;
    }

    // =========================================================
    // Service Group & Clinic filtering
    // =========================================================

    public OutpatientPage selectServiceGroup(String serviceGroupText) {
        WebElement select = wait.until(ExpectedConditions.elementToBeClickable(SERVICE_GROUP_SELECT));
        selectNgOption(select, serviceGroupText);
        LOGGER.info("Selected service group: {}", serviceGroupText);
        return this;
    }

    public List<String> getAvailableClinicOptions() {
        closeOpenNgDropdownPanels();
        WebElement clinicDropdown = resolve(CLINIC_SELECT, CLINIC_BY_LABEL);
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", clinicDropdown);
        clinicDropdown.click();

        try {
            List<WebElement> options = new WebDriverWait(driver, Duration.ofSeconds(5))
                    .until(ExpectedConditions.presenceOfNestedElementsLocatedBy(
                            By.cssSelector("ng-dropdown-panel, .ng-dropdown-panel"),
                            By.cssSelector(".ng-option:not(.ng-option-disabled)")));

            List<String> optionTexts = options.stream()
                    .map(e -> e.getText().trim())
                    .filter(t -> !t.isBlank())
                    .collect(Collectors.toList());

            closeOpenNgDropdownPanels();
            LOGGER.info("Available clinic options: {}", optionTexts);
            return optionTexts;
        } catch (Exception e) {
            LOGGER.warn("Could not retrieve clinic options: {}", e.getMessage());
            closeOpenNgDropdownPanels();
            return List.of();
        }
    }

    // =========================================================
    // ICD10 Diagnosis
    // =========================================================

    public OutpatientPage selectIcdDiagnosis(String icdText) {
        WebElement icdSelect = wait.until(ExpectedConditions.elementToBeClickable(SERVICES_ICD_SELECT));
        selectNgOption(icdSelect, icdText);
        LOGGER.info("Selected ICD diagnosis: {}", icdText);
        return this;
    }

    public OutpatientPage selectFirstIcdDiagnosisOption() {
        WebElement icdSelect = wait.until(ExpectedConditions.elementToBeClickable(SERVICES_ICD_SELECT));
        selectFirstSearchableNgOption(icdSelect, "a");
        LOGGER.info("Selected first available ICD diagnosis option");
        return this;
    }

    public boolean isIcdDiagnosisMandatory() {
        try {
            List<WebElement> reqLabels = driver.findElements(By.xpath(
                    "//label[contains(normalize-space(.),'التشخيص') or contains(normalize-space(.),'ICD10')]"
                            + "[contains(normalize-space(.),'*') or .//*[contains(@class,'req')]]"));
            if (!reqLabels.isEmpty() && reqLabels.stream().anyMatch(WebElement::isDisplayed)) {
                return true;
            }
            WebElement selectContainer = resolve(SERVICES_ICD_SELECT, By.cssSelector("[data-test-id='opd-patient-services-icd-select']"));
            String classes = selectContainer.getAttribute("class");
            return classes != null && (classes.contains("ng-invalid") || classes.contains("required"));
        } catch (Exception e) {
            return false;
        }
    }

    // =========================================================
    // Barcode Printing
    // =========================================================

    public OutpatientPage clickPrintBarcodeButton() {
        WebElement barcodeBtn = wait.until(ExpectedConditions.elementToBeClickable(PRINT_BARCODE_BTN));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", barcodeBtn);
        try {
            barcodeBtn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", barcodeBtn);
        }
        LOGGER.info("Clicked print barcode button");
        return this;
    }

    public String getBarcodeButtonHref() {
        try {
            WebElement barcodeBtn = driver.findElement(PRINT_BARCODE_BTN);
            return barcodeBtn.getAttribute("href");
        } catch (Exception e) {
            return "";
        }
    }

    public String clickPrintBarcodeAndGetUrl() {
        String originalWindow = driver.getWindowHandle();
        clickPrintBarcodeButton();

        try {
            new WebDriverWait(driver, Duration.ofSeconds(4)).until(d -> d.getWindowHandles().size() > 1);
        } catch (Exception ignored) {}

        String openedUrl = "";
        if (driver.getWindowHandles().size() > 1) {
            for (String handle : driver.getWindowHandles()) {
                if (!handle.equals(originalWindow)) {
                    driver.switchTo().window(handle);
                    openedUrl = driver.getCurrentUrl();
                    driver.close();
                    driver.switchTo().window(originalWindow);
                    break;
                }
            }
        } else {
            openedUrl = driver.getCurrentUrl();
        }
        LOGGER.info("Barcode opened URL: {}", openedUrl);
        return openedUrl;
    }

    // =========================================================
    // Claim Modal
    // =========================================================

    public OutpatientPage openClaimModal() {
        WebElement openBtn = wait.until(ExpectedConditions.elementToBeClickable(OPEN_CLAIM_BTN));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", openBtn);
        try {
            openBtn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", openBtn);
        }
        wait.until(ExpectedConditions.visibilityOfElementLocated(CLAIM_TITLE_INPUT));
        LOGGER.info("Claim modal opened successfully");
        return this;
    }

    public boolean isClaimModalDisplayed() {
        return !driver.findElements(CLAIM_TITLE_INPUT).isEmpty()
                && driver.findElements(CLAIM_TITLE_INPUT).stream().anyMatch(WebElement::isDisplayed);
    }

    public OutpatientPage closeClaimModal() {
        WebElement closeBtn = wait.until(ExpectedConditions.elementToBeClickable(CLAIM_MODAL_CLOSE_BTN));
        try {
            closeBtn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", closeBtn);
        }
        wait.until(d -> !isClaimModalDisplayed());
        LOGGER.info("Claim modal closed");
        return this;
    }

    public OutpatientPage fillAndUploadClaim(String title, String filePath) {
        WebElement titleInput = wait.until(ExpectedConditions.elementToBeClickable(CLAIM_TITLE_INPUT));
        titleInput.clear();
        titleInput.sendKeys(title);

        if (filePath != null && !filePath.isBlank()) {
            WebElement fileInput = driver.findElement(CLAIM_FILE_INPUT);
            fileInput.sendKeys(filePath);
        }

        WebElement saveBtn = wait.until(ExpectedConditions.elementToBeClickable(SAVE_CLAIM_BTN));
        try {
            saveBtn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", saveBtn);
        }
        LOGGER.info("Uploaded claim with title: {}", title);
        return this;
    }

    public List<String> getClaimTitlesList() {
        List<WebElement> items = driver.findElements(CLAIM_ITEM_LIST);
        return items.stream()
                .map(item -> {
                    try {
                        return item.findElement(CLAIM_TITLE_TEXT).getText().trim();
                    } catch (Exception e) {
                        return item.getText().trim();
                    }
                })
                .collect(Collectors.toList());
    }

    public boolean isClaimTitleInGrid(String title) {
        return getClaimTitlesList().contains(title);
    }

    public OutpatientPage clickDownloadClaimForTitle(String title) {
        List<WebElement> items = driver.findElements(CLAIM_ITEM_LIST);
        for (WebElement item : items) {
            if (item.getText().contains(title)) {
                WebElement downloadBtn = item.findElement(DOWNLOAD_CLAIM_BTN);
                try {
                    downloadBtn.click();
                } catch (Exception e) {
                    ((JavascriptExecutor) driver).executeScript("arguments[0].click();", downloadBtn);
                }
                LOGGER.info("Clicked download claim button for item title: {}", title);
                return this;
            }
        }
        List<WebElement> downloads = driver.findElements(DOWNLOAD_CLAIM_BTN);
        if (!downloads.isEmpty()) {
            downloads.get(0).click();
        }
        return this;
    }

    public OutpatientPage clickDeleteClaimForTitle(String title) {
        int initialCount = driver.findElements(CLAIM_ITEM_LIST).size();
        List<WebElement> items = driver.findElements(CLAIM_ITEM_LIST);
        for (WebElement item : items) {
            if (item.getText().contains(title)) {
                WebElement deleteBtn = item.findElement(DELETE_CLAIM_BTN);
                try {
                    deleteBtn.click();
                } catch (Exception e) {
                    ((JavascriptExecutor) driver).executeScript("arguments[0].click();", deleteBtn);
                }
                LOGGER.info("Clicked delete claim button for item title: {}", title);
                break;
            }
        }
        try {
            wait.until(d -> d.findElements(CLAIM_ITEM_LIST).size() < initialCount || !isClaimTitleInGrid(title));
        } catch (Exception ignored) {}
        return this;
    }

    // =========================================================
    // Favorites (اظهار المفضلة والقوائم المفضلة)
    // =========================================================

    public OutpatientPage clickToggleFavoritesButton() {
        WebElement btn = wait.until(ExpectedConditions.elementToBeClickable(TOGGLE_FAVORITES_BTN));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", btn);
        try {
            btn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", btn);
        }
        LOGGER.info("Clicked toggle favorites button (opd-patient-services-toggle-favorites-btn)");
        waitForFavoriteMenuSelect();
        return this;
    }

    public OutpatientPage waitForFavoriteMenuSelect() {
        wait.until(ExpectedConditions.visibilityOfElementLocated(FAVORITE_MENU_SELECT));
        return this;
    }

    public boolean isFavoriteMenuSelectDisplayed() {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(FAVORITE_MENU_SELECT)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    public OutpatientPage selectFavoriteMenu(String menuName) {
        waitForFavoriteMenuSelect();
        WebElement select = wait.until(ExpectedConditions.elementToBeClickable(FAVORITE_MENU_SELECT));
        if (menuName == null || menuName.isBlank() || "FIRST".equalsIgnoreCase(menuName)) {
            selectFirstNgOption(select);
        } else {
            selectNgOption(select, menuName);
        }
        LOGGER.info("Selected favorite menu: {}", menuName);
        return this;
    }

    public List<WebElement> getFavoriteItemCheckboxes() {
        try {
            return new WebDriverWait(driver, Duration.ofSeconds(5))
                    .until(ExpectedConditions.presenceOfAllElementsLocatedBy(FAVORITE_ITEM_CHECKBOX));
        } catch (Exception e) {
            return driver.findElements(FAVORITE_ITEM_CHECKBOX);
        }
    }

    public int getFavoriteItemCheckboxesCount() {
        return getFavoriteItemCheckboxes().size();
    }

    public boolean isFavoriteItemCheckboxDisplayed() {
        try {
            return new WebDriverWait(driver, Duration.ofSeconds(5))
                    .until(d -> {
                        List<WebElement> boxes = d.findElements(FAVORITE_ITEM_CHECKBOX);
                        return !boxes.isEmpty() && boxes.stream().anyMatch(WebElement::isDisplayed);
                    });
        } catch (Exception e) {
            return false;
        }
    }

    public OutpatientPage selectFirstFavoriteItemCheckbox() {
        List<WebElement> boxes = getFavoriteItemCheckboxes();
        if (!boxes.isEmpty()) {
            WebElement box = boxes.get(0);
            ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", box);
            if (!box.isSelected()) {
                try {
                    box.click();
                } catch (Exception e) {
                    ((JavascriptExecutor) driver).executeScript("arguments[0].click();", box);
                }
            }
        }
        return this;
    }

    // =========================================================
    // Medicines & Supplies Tab (صرف الادوية والمستلزمات)
    // =========================================================

    public OutpatientPage switchToMedicinesTab() {
        clickTab("opd-patient-services-medicines-tab-btn");
        LOGGER.info("Switched to Medicines & Supplies tab");
        return this;
    }

    public String getSelectedMedStoreText() {
        try {
            WebElement select = driver.findElement(MED_CHARGE_STORE_SELECT);
            List<WebElement> labels = select.findElements(By.cssSelector(".ng-value-label, .ng-value, .ng-placeholder"));
            if (!labels.isEmpty()) {
                return labels.get(0).getText().trim();
            }
            return select.getText().trim();
        } catch (Exception e) {
            return "";
        }
    }

    public boolean isMedStoreEmptyOrPlaceholder() {
        String text = getSelectedMedStoreText();
        return text.contains("اختر المخزن") || text.isEmpty() || !isNgSelectHasValue(MED_CHARGE_STORE_SELECT);
    }

    public String getSelectedMedDoctorText() {
        try {
            WebElement select = driver.findElement(MED_CHARGE_DOCTOR_SELECT);
            List<WebElement> labels = select.findElements(By.cssSelector(".ng-value-label, .ng-value, .ng-placeholder"));
            if (!labels.isEmpty()) {
                return labels.get(0).getText().trim();
            }
            return select.getText().trim();
        } catch (Exception e) {
            return "";
        }
    }

    public boolean isMedDoctorEmptyOrPlaceholder() {
        String text = getSelectedMedDoctorText();
        return text.contains("اختر الطبيب") || text.isEmpty() || !isNgSelectHasValue(MED_CHARGE_DOCTOR_SELECT);
    }

    public String getSelectedMedItemText() {
        try {
            WebElement select = driver.findElement(MED_CHARGE_ITEM_SELECT);
            List<WebElement> labels = select.findElements(By.cssSelector(".ng-value-label, .ng-value, .ng-placeholder"));
            if (!labels.isEmpty()) {
                return labels.get(0).getText().trim();
            }
            return select.getText().trim();
        } catch (Exception e) {
            return "";
        }
    }

    public boolean isMedItemEmptyOrPlaceholder() {
        String text = getSelectedMedItemText();
        return text.isEmpty() || text.contains("اختر") || !isNgSelectHasValue(MED_CHARGE_ITEM_SELECT);
    }

    private boolean isNgSelectHasValue(By locator) {
        try {
            WebElement select = driver.findElement(locator);
            List<WebElement> val = select.findElements(By.cssSelector(".ng-value"));
            return !val.isEmpty() && val.stream().anyMatch(WebElement::isDisplayed);
        } catch (Exception e) {
            return false;
        }
    }

    public OutpatientPage selectMedStore(String storeName) {
        WebElement select = wait.until(ExpectedConditions.elementToBeClickable(MED_CHARGE_STORE_SELECT));
        selectNgOption(select, storeName);
        LOGGER.info("Selected medicine store: {}", storeName);
        return this;
    }

    public OutpatientPage selectMedDoctor(String doctorName) {
        WebElement select = wait.until(ExpectedConditions.elementToBeClickable(MED_CHARGE_DOCTOR_SELECT));
        selectNgOption(select, doctorName);
        LOGGER.info("Selected medicine doctor: {}", doctorName);
        return this;
    }

    public OutpatientPage selectMedItem(String itemName) {
        WebElement select = wait.until(ExpectedConditions.elementToBeClickable(MED_CHARGE_ITEM_SELECT));
        selectNgOption(select, itemName);
        LOGGER.info("Selected medicine item: {}", itemName);
        return this;
    }

    public OutpatientPage selectMedUnit(String unitName) {
        try {
            WebElement select = wait.until(ExpectedConditions.elementToBeClickable(MED_CHARGE_UNIT_SELECT));
            selectNgOption(select, unitName);
            LOGGER.info("Selected medicine unit: {}", unitName);
        } catch (Exception e) {
            LOGGER.warn("Could not find unit select by test-id; trying label fallback: {}", e.getMessage());
            By fallback = By.xpath("//label[contains(normalize-space(.),'الوحدة')]/following::*[self::ng-select or contains(@class,'ng-select')][1]");
            WebElement select = wait.until(ExpectedConditions.elementToBeClickable(fallback));
            selectNgOption(select, unitName);
        }
        return this;
    }

    public boolean isOpenMedBatchDialogButtonVisible() {
        List<WebElement> btns = driver.findElements(OPEN_MED_BATCH_DIALOG_BTN);
        return !btns.isEmpty() && btns.stream().anyMatch(WebElement::isDisplayed);
    }

    public OutpatientPage clickOpenMedBatchDialogButton() {
        WebElement btn = wait.until(ExpectedConditions.elementToBeClickable(OPEN_MED_BATCH_DIALOG_BTN));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", btn);
        try {
            btn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", btn);
        }
        LOGGER.info("Clicked open med batch dialog (+) button");
        return this;
    }

    public boolean isMedChargeCreditPctReadonlyOrDisabled() {
        try {
            WebElement input = driver.findElement(MED_CHARGE_CREDIT_PCT_INPUT);
            String readonly = input.getAttribute("readonly");
            String disabled = input.getAttribute("disabled");
            return readonly != null || disabled != null;
        } catch (Exception e) {
            return true;
        }
    }

    public boolean isMedChargeCreditPctEnabled() {
        return !isMedChargeCreditPctReadonlyOrDisabled();
    }

    public OutpatientPage enterMedChargeCreditPct(String pct) {
        WebElement input = wait.until(ExpectedConditions.elementToBeClickable(MED_CHARGE_CREDIT_PCT_INPUT));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", input);
        input.clear();
        input.sendKeys(pct);
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
                        + "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", input);
        LOGGER.info("Entered medicine charge credit percentage: {}", pct);
        return this;
    }

    public String getMedChargeCreditPctInputValue() {
        try {
            return driver.findElement(MED_CHARGE_CREDIT_PCT_INPUT).getAttribute("value");
        } catch (Exception e) {
            return "";
        }
    }

    public OutpatientPage clickClearMedChargeButton() {
        WebElement btn = wait.until(ExpectedConditions.elementToBeClickable(CLEAR_MED_CHARGE_BTN));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", btn);
        try {
            btn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", btn);
        }
        LOGGER.info("Clicked clear med charge (جديد) button");
        return this;
    }

    // =========================================================
    // Internals
    // =========================================================

    private WebElement resolve(By primary, By fallback) {
        List<WebElement> primaryMatches = driver.findElements(primary);
        for (WebElement el : primaryMatches) {
            try {
                if (el.isDisplayed()) {
                    return el;
                }
            } catch (StaleElementReferenceException ignored) {
                // retry via wait below
            }
        }
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(primary));
        } catch (TimeoutException e) {
            LOGGER.info("data-test-id locator missed {}; using TEMPORARY label fallback {}",
                    primary, fallback);
            return wait.until(ExpectedConditions.visibilityOfElementLocated(fallback));
        }
    }

    private void clickResolved(By primary, By fallback) {
        WebElement el = resolve(primary, fallback);
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].scrollIntoView({block:'center'});", el);
        try {
            wait.until(ExpectedConditions.elementToBeClickable(el)).click();
        } catch (Exception e) {
            WebElement fresh = resolve(primary, fallback);
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", fresh);
        }
    }

    private void selectNgOption(WebElement ngSelect, String optionText) {
        if (optionText == null || optionText.isBlank()) {
            return;
        }
        closeOpenNgDropdownPanels();
        WebElement select = wait.until(ExpectedConditions.elementToBeClickable(ngSelect));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", select);
        try {
            select.click();
        } catch (Exception e) {
            LOGGER.info("Direct click on ng-select intercepted by toast/overlay; using JS click");
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", select);
        }

        String cleanKeyword = optionText.replaceAll("^[#@$]+", "").trim();

        // 1. Try finding a matching option directly from the open panel BEFORE typing filter
        try {
            List<WebElement> options = new WebDriverWait(driver, Duration.ofSeconds(3))
                    .until(ExpectedConditions.presenceOfNestedElementsLocatedBy(
                            By.cssSelector("ng-dropdown-panel, .ng-dropdown-panel"),
                            By.cssSelector(".ng-option:not(.ng-option-disabled)")));

            for (WebElement opt : options) {
                String text = opt.getText();
                if (text != null && (text.trim().equals(optionText)
                        || text.contains(optionText)
                        || text.contains(cleanKeyword)
                        || (optionText.contains("نقدي") && text.contains("نقدي")))) {
                    try {
                        opt.click();
                    } catch (Exception e) {
                        ((JavascriptExecutor) driver).executeScript("arguments[0].click();", opt);
                    }
                    closeOpenNgDropdownPanels();
                    LOGGER.info("Selected ng-option directly: {}", text);
                    return;
                }
            }
        } catch (Exception ignored) {
            // Dropdown panel may need typing filter if options list is long / lazy loaded
        }

        // 2. Filter using inner input if direct pick didn't find a match
        try {
            WebElement innerInput = select.findElement(By.cssSelector("input[role='combobox'], input[type='text'], .ng-input input"));
            if (innerInput.getAttribute("readonly") == null) {
                innerInput.sendKeys(Keys.CONTROL + "a", Keys.BACK_SPACE);
                innerInput.sendKeys(cleanKeyword);
            }
        } catch (Exception ignored) {
            // Some selects have no inner input
        }

        By exactOption = By.xpath(
                "//ng-dropdown-panel//*[contains(@class,'ng-option')][normalize-space()='" + optionText + "']");
        By containsOption = By.xpath(
                "//ng-dropdown-panel//*[contains(@class,'ng-option')][contains(normalize-space(),'" + optionText + "')]");
        By cleanOption = By.xpath(
                "//ng-dropdown-panel//*[contains(@class,'ng-option')][contains(normalize-space(),'" + cleanKeyword + "')]");

        try {
            clickOptionElement(exactOption);
            closeOpenNgDropdownPanels();
            return;
        } catch (Exception ignored) {}

        try {
            clickOptionElement(containsOption);
            closeOpenNgDropdownPanels();
            return;
        } catch (Exception ignored) {}

        try {
            clickOptionElement(cleanOption);
            closeOpenNgDropdownPanels();
            return;
        } catch (Exception ignored) {}

        // Fallback: clear search input filter if no match found (e.g. "النقدي2019" vs "$$نقدي 2019")
        try {
            WebElement innerInput = select.findElement(By.cssSelector("input[role='combobox'], input[type='text'], .ng-input input"));
            innerInput.sendKeys(Keys.CONTROL + "a", Keys.BACK_SPACE);
            if (optionText.contains("نقدي") || optionText.contains("النقدي")) {
                innerInput.sendKeys("نقدي");
            }
        } catch (Exception ignored) {}

        List<WebElement> options = driver.findElements(By.cssSelector(
                "ng-dropdown-panel .ng-option:not(.ng-option-disabled), .ng-dropdown-panel .ng-option:not(.ng-option-disabled), .ng-option"));

        for (WebElement opt : options) {
            String text = opt.getText();
            if (text != null && (text.contains(cleanKeyword) || text.contains("نقدي") || text.contains(optionText))) {
                try {
                    opt.click();
                } catch (Exception e) {
                    ((JavascriptExecutor) driver).executeScript("arguments[0].click();", opt);
                }
                closeOpenNgDropdownPanels();
                return;
            }
        }

        if (!options.isEmpty()) {
            LOGGER.info("No exact option matched '{}'; selecting first available option: {}", optionText, options.get(0).getText());
            try {
                options.get(0).click();
            } catch (Exception e) {
                ((JavascriptExecutor) driver).executeScript("arguments[0].click();", options.get(0));
            }
            closeOpenNgDropdownPanels();
            return;
        }

        closeOpenNgDropdownPanels();
    }

    private void clickOptionElement(By locator) {
        WebElement opt = wait.until(ExpectedConditions.presenceOfElementLocated(locator));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", opt);
        try {
            opt.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", opt);
        }
    }

    private void selectFirstNgOption(WebElement ngSelect) {
        selectFirstSearchableNgOption(ngSelect, null);
    }

    /**
     * Opens an ng-select / typeahead and picks the first enabled option.
     * When {@code searchText} is provided (or options stay empty), types into the
     * combobox to trigger async search results.
     */
    private void selectFirstSearchableNgOption(WebElement ngSelect, String searchText) {
        for (int attempt = 1; attempt <= 3; attempt++) {
            try {
                closeOpenNgDropdownPanels();
                WebElement select = wait.until(ExpectedConditions.elementToBeClickable(ngSelect));
                ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", select);
                
                // Try clicking inner input element first, fallback to container
                try {
                    WebElement input = select.findElement(By.cssSelector("input[role='combobox'], input[type='text'], .ng-input input"));
                    input.click();
                    if (searchText != null && !searchText.isBlank()) {
                        input.sendKeys(Keys.CONTROL + "a", Keys.BACK_SPACE);
                        input.sendKeys(searchText);
                    }
                } catch (Exception e) {
                    select.click();
                    if (searchText != null && !searchText.isBlank()) {
                        typeIntoCombobox(select, searchText);
                    }
                }

                // Wait for panel and options
                By ngOptionsLocator = By.cssSelector("ng-dropdown-panel .ng-option:not(.ng-option-disabled), .ng-dropdown-panel .ng-option:not(.ng-option-disabled), .ng-option");
                try {
                    WebElement option = new WebDriverWait(driver, Duration.ofSeconds(5))
                            .pollingEvery(Duration.ofMillis(250))
                            .until(ExpectedConditions.elementToBeClickable(ngOptionsLocator));
                    ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", option);
                    try {
                        option.click();
                    } catch (Exception clickEx) {
                        ((JavascriptExecutor) driver).executeScript("arguments[0].click();", option);
                    }
                    closeOpenNgDropdownPanels();
                    LOGGER.info("Successfully selected ng-option (attempt {})", attempt);
                    return;
                } catch (TimeoutException te) {
                    LOGGER.info("Dropdown options panel wait timed out on attempt {}, sending Down+Enter", attempt);
                    driver.switchTo().activeElement().sendKeys(Keys.ARROW_DOWN, Keys.ENTER);
                    closeOpenNgDropdownPanels();
                    return;
                }
            } catch (RuntimeException e) {
                LOGGER.warn("selectFirstSearchableNgOption attempt {} failed: {}", attempt, e.getMessage());
                closeOpenNgDropdownPanels();
            }
        }
        throw new TimeoutException("Could not select option from ng-select typeahead");
    }

    private void typeIntoCombobox(WebElement ngSelect, String text) {
        try {
            List<WebElement> inputs = ngSelect.findElements(By.cssSelector(
                    "input[role='combobox'], input.ng-input-filter, input[type='text']"));
            if (inputs.isEmpty()) {
                inputs = driver.findElements(By.cssSelector(
                        "ng-dropdown-panel input, .ng-dropdown-panel input"));
            }
            if (inputs.isEmpty()) {
                ngSelect.sendKeys(text);
                return;
            }
            WebElement input = inputs.get(0);
            input.click();
            input.sendKeys(Keys.CONTROL + "a");
            input.sendKeys(Keys.DELETE);
            input.sendKeys(text);
        } catch (Exception e) {
            LOGGER.debug("Could not type into combobox: {}", e.getMessage());
        }
    }

    private void closeOpenNgDropdownPanels() {
        try {
            driver.switchTo().activeElement().sendKeys(Keys.ESCAPE);
        } catch (Exception ignored) {
            // no focus
        }
    }
}
