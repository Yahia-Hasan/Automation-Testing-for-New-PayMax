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

    // ---------- Services & payment ----------
    private static final By SERVICE_SELECT = By.cssSelector(
            "[data-test-id='clinic-visit-service-select'],"
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
            "[data-test-id='clinic-visit-doctor-select'],"
                    + "[data-test-id='opd-doctor-select']");
    private static final By DOCTOR_BY_LABEL = By.xpath(
            "(//label[contains(normalize-space(.),'الطبيب المعالج')]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1])"
                    + " | (//*[contains(normalize-space(.),'اختر الطبيب')]"
                    + "/ancestor::*[self::ng-select or contains(@class,'ng-select')][1])");

    private static final By CLINIC_SELECT = By.cssSelector(
            "[data-test-id='clinic-visit-clinic-select'],"
                    + "[data-test-id='opd-clinic-select']");
    private static final By CLINIC_BY_LABEL = By.xpath(
            "(//label[normalize-space()='العيادة' or normalize-space()='العيادة *'"
                    + " or starts-with(normalize-space(.),'العيادة')]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1])"
                    + " | (//*[contains(normalize-space(.),'اختر العيادة')]"
                    + "/ancestor::*[self::ng-select or contains(@class,'ng-select')][1])");

    private static final By ADD_SERVICE_BUTTON = By.cssSelector(
            "[data-test-id='clinic-visit-add-service-btn'],"
                    + "[data-test-id='opd-add-service-btn']");
    private static final By ADD_SERVICE_BY_TEXT = By.xpath(
            "//button[contains(normalize-space(.),'إضافة للقائمة')"
                    + " or contains(normalize-space(.),'اضافة للقائمة')]");

    private static final By TREASURY_SELECT = By.cssSelector(
            "[data-test-id='clinic-visit-treasury-select'],"
                    + "[data-test-id='opd-treasury-select']");
    private static final By TREASURY_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'الخزينة')]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1]");

    private static final By PAYMENT_METHOD_SELECT = By.cssSelector(
            "[data-test-id='clinic-visit-payment-method-select'],"
                    + "[data-test-id='opd-payment-method-select']");
    private static final By PAYMENT_METHOD_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'طريقة الدفع')]"
                    + "/following::*[self::ng-select or contains(@class,'ng-select')][1]");

    private static final By AMOUNT_INPUT = By.cssSelector(
            "[data-test-id='clinic-visit-payment-amount-input'],"
                    + "[data-test-id='opd-payment-amount-input']");
    private static final By AMOUNT_BY_LABEL = By.xpath(
            "//label[contains(normalize-space(.),'المبلغ')]"
                    + "/following::input[1]");

    private static final By SAVE_AND_PAY_BUTTON = By.cssSelector(
            "[data-test-id='clinic-visit-save-and-pay-btn'],"
                    + "[data-test-id='opd-save-and-pay-btn']");
    private static final By SAVE_AND_PAY_BY_TEXT = By.xpath(
            "//button[contains(normalize-space(.),'حفظ ودفع')]");

    private static final By DISCHARGE_BUTTON = By.cssSelector(
            "[data-test-id='clinic-visit-discharge-btn'],"
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
        closeOpenNgDropdownPanels();
        WebElement select = wait.until(ExpectedConditions.elementToBeClickable(ngSelect));
        select.click();

        try {
            WebElement innerInput = select.findElement(By.cssSelector("input[role='combobox']"));
            if (innerInput.getAttribute("readonly") == null) {
                innerInput.clear();
                innerInput.sendKeys(optionText);
            }
        } catch (Exception ignored) {
            // Some selects have no inner input
        }

        By option = By.xpath(
                "//ng-dropdown-panel//*[contains(@class,'ng-option')]"
                        + "[normalize-space()='" + optionText + "']");
        By optionFallback = By.xpath(
                "//ng-dropdown-panel//*[contains(@class,'ng-option')]"
                        + "[contains(normalize-space(),'" + optionText + "')]");
        try {
            wait.until(ExpectedConditions.elementToBeClickable(option)).click();
        } catch (Exception e) {
            wait.until(ExpectedConditions.elementToBeClickable(optionFallback)).click();
        }
        closeOpenNgDropdownPanels();
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
        By[] optionLocators = new By[] {
                By.cssSelector("ng-dropdown-panel .ng-option:not(.ng-option-disabled)"),
                By.cssSelector(".ng-dropdown-panel .ng-option:not(.ng-option-disabled)"),
                By.cssSelector("[role='listbox'] [role='option']"),
                By.cssSelector(".p-autocomplete-panel .p-autocomplete-item")
        };
        RuntimeException lastError = null;
        String[] probes = searchText == null
                ? new String[] {null, "ا", "م", "a"}
                : new String[] {searchText, "ا", "م", null};

        for (int attempt = 1; attempt <= 5; attempt++) {
            try {
                closeOpenNgDropdownPanels();
                WebElement select = wait.until(ExpectedConditions.elementToBeClickable(ngSelect));
                select.click();

                String probe = probes[Math.min(attempt - 1, probes.length - 1)];
                if (probe != null) {
                    typeIntoCombobox(select, probe);
                }

                WebElement option = null;
                TimeoutException lastOptionError = null;
                for (By optionLocator : optionLocators) {
                    try {
                        option = new WebDriverWait(driver, Duration.ofSeconds(4))
                                .pollingEvery(Duration.ofMillis(200))
                                .until(ExpectedConditions.elementToBeClickable(optionLocator));
                        break;
                    } catch (TimeoutException e) {
                        lastOptionError = e;
                    }
                }
                if (option == null) {
                    throw lastOptionError != null
                            ? lastOptionError
                            : new TimeoutException("No dropdown options appeared");
                }
                option.click();
                closeOpenNgDropdownPanels();
                LOGGER.info("Selected first searchable ng-option (attempt {}, probe={})",
                        attempt, probe);
                return;
            } catch (RuntimeException e) {
                lastError = e;
                LOGGER.warn("selectFirstSearchableNgOption attempt {} failed: {}",
                        attempt, e.getMessage());
                closeOpenNgDropdownPanels();
                try {
                    Thread.sleep(350L * attempt);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
        throw lastError != null
                ? lastError
                : new TimeoutException("Could not select first searchable ng-select option");
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
        try {
            ((JavascriptExecutor) driver).executeScript(
                    "document.querySelectorAll('ng-dropdown-panel').forEach(p => p.remove());");
        } catch (Exception ignored) {
            // best-effort
        }
    }
}
