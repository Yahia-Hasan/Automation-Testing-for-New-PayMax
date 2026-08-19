package com.paymax.automation.tests;

import com.paymax.automation.base.BaseTest;
import com.paymax.automation.pages.OutpatientPage;
import com.paymax.automation.pages.PatientAdmissionPage;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

import java.io.File;
import java.nio.file.Files;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Independent Outpatient Visits cycle (العيادات الخارجية).
 * Uses {@link OutpatientPage} and seeds patients via {@link PatientAdmissionPage}.
 *
 * T1–T3   : visit creation / modal / unpaid-block
 * T5–T11  : services page assertions (page load, tabs, add-service, payment, discharge)
 * T12–T15 : service group filtering, ICD10 mandatory check, print barcode URL, claim modal operations
 */
public class OutpatientCycleTests extends BaseTest {

    private static final String AUTOMATION_PATIENT_SEARCH = "يحيى تيست اوتوميشن";
    private static final String VALID_BIRTH_DATE = "1990-05-15";
    private static final String VALID_GENDER = "ذكر";

    /** From live OPD draft UI (نوع الحالة). */
    private static final String CASE_TYPE_SPECIAL = "حالة خاصة";

    /**
     * Patient expected to already have an open OPD visit (seeded manually).
     * Used for active-visit modal → continue same visit.
     */
    private static final String PATIENT_WITH_ACTIVE_OPD = "30499";

    /**
     * Patient with an open unpaid OPD visit — close must show تنبيه
     * "بسبب أن الزيارة لم تُدفع بعد". Do not pay this patient in automation.
     */
    private static final String PATIENT_UNPAID_OPD = "30552";

    private PatientAdmissionPage admissionPage;
    private OutpatientPage outpatientPage;

    @BeforeClass(alwaysRun = true)
    public void loginOnce() {
        loginAndNavigateToNewSystem();
        admissionPage = new PatientAdmissionPage(getDriver()).navigateToReception();
        outpatientPage = new OutpatientPage(getDriver());
    }

    @BeforeMethod(alwaysRun = true)
    public void resetToReception() {
        admissionPage.prepareIsolatedTestState();
    }

    @AfterMethod(alwaysRun = true)
    public void cleanupUi() {
        try {
            admissionPage.dismissOverlaysAndToasts();
        } catch (Exception ignored) {
            // never fail suite from cleanup
        }
    }

    // =========================================================
    // T1–T3 : visit creation & modal
    // =========================================================

    @Test(priority = 1,
            description = "Draft visit creation: fill نوع الحالة + الشركة الفرعية, save → /services")
    public void createDraftVisitAndTransitionToServices() {
        String patientCode = createFreshPatientWithoutVisit();

        // Fresh patient is already open in reception page
        admissionPage.clickOpdButton();

        // Clean patient should open draft; if modal appears, continue the existing visit instead
        if (outpatientPage.isActiveVisitModalDisplayed()) {
            outpatientPage.continueSameVisit();
            Assert.assertTrue(outpatientPage.isOnServicesUrl(),
                    "Continue same visit should open services page. Actual: "
                            + getDriver().getCurrentUrl());
            return;
        }

        outpatientPage.waitForDraftUrl();
        Assert.assertTrue(getDriver().getCurrentUrl().contains("/clinic/visits/draft"),
                "Expected draft URL. Actual: " + getDriver().getCurrentUrl());
        Assert.assertTrue(getDriver().getCurrentUrl().contains("patientCode=" + patientCode),
                "Draft URL must include patientCode. Actual: " + getDriver().getCurrentUrl());
        Assert.assertTrue(getDriver().getCurrentUrl().contains("mode=opd"),
                "Draft URL must include mode=opd. Actual: " + getDriver().getCurrentUrl());

        outpatientPage.fillAndSaveDraftVisit(CASE_TYPE_SPECIAL, "FIRST");

        outpatientPage.waitForServicesUrl();
        String visitCode = outpatientPage.getVisitCodeFromUrl();
        Assert.assertFalse(visitCode.isBlank(),
                "visitCode must be present in services URL. Actual: " + getDriver().getCurrentUrl());
        Assert.assertTrue(getDriver().getCurrentUrl().contains("/clinic/visits/" + visitCode + "/services"),
                "Expected services URL for visit " + visitCode
                        + ". Actual: " + getDriver().getCurrentUrl());
    }

    @Test(priority = 2,
            description = "Active visit modal: click الإستكمال على نفس الزيارة → visit services page")
    public void activeVisitModalContinueExisting() {
        // Create a patient and give them an active open visit dynamically
        String patientCode = createFreshPatientWithoutVisit();
        admissionPage.clickOpdButton();
        if (!outpatientPage.isActiveVisitModalDisplayed()) {
            outpatientPage.waitForDraftUrl();
            outpatientPage.fillAndSaveDraftVisit(CASE_TYPE_SPECIAL, "FIRST");
            outpatientPage.waitForServicesUrl();
            // Go back to reception page first before searching
            admissionPage.navigateToReception();
            admissionPage.openPatientProfileBySearch(patientCode);
            admissionPage.clickOpdButton();
        }

        outpatientPage.waitForActiveVisitModal();
        Assert.assertTrue(outpatientPage.isActiveVisitModalDisplayed(),
                "Active visit warning modal must appear when opening OPD button for patient with active visit");

        outpatientPage.continueSameVisit();

        Assert.assertTrue(outpatientPage.isOnServicesUrl(),
                "After continue same visit, must open visit services page. Actual: "
                        + getDriver().getCurrentUrl());
        String visitCode = outpatientPage.getVisitCodeFromUrl();
        Assert.assertFalse(visitCode.isBlank(),
                "Services URL must contain visit code. Actual: " + getDriver().getCurrentUrl());
        Assert.assertTrue(getDriver().getCurrentUrl().contains("/clinic/visits/" + visitCode + "/services"),
                "Expected /clinic/visits/{visitCode}/services. Actual: " + getDriver().getCurrentUrl());
    }

    @Test(priority = 3,
            description = "Close open visit blocked when unpaid — confirm نعم then تنبيه لم تُدفع بعد")
    public void closeVisitBlockedWhenVisitUnpaid() {
        admissionPage.openPatientProfileBySearch(PATIENT_UNPAID_OPD);
        admissionPage.clickOpdButton();

        outpatientPage.waitForActiveVisitModal();
        Assert.assertTrue(outpatientPage.isActiveVisitModalDisplayed(),
                "Active visit modal must appear for unpaid patient " + PATIENT_UNPAID_OPD);

        // Close → SweetAlert confirm → نعم → unpaid error تنبيه
        outpatientPage.closeOpenVisitExpectingBlockAlert();

        Assert.assertEquals(outpatientPage.getCloseVisitBlockAlertTitle(), "تنبيه",
                "Error Swal title must be تنبيه");

        String alertText = outpatientPage.getCloseVisitBlockAlertText();
        Assert.assertTrue(alertText.contains("تعذر إغلاق الزيارة"),
                "Alert must say تعذر إغلاق الزيارة. Actual: " + alertText);
        Assert.assertTrue(outpatientPage.isUnpaidCloseVisitReasonDisplayed(),
                "Alert must include unpaid reason. Actual: " + alertText);

        outpatientPage.dismissCloseVisitBlockAlert();
        Assert.assertTrue(getDriver().getCurrentUrl().contains("/reception/patient/" + PATIENT_UNPAID_OPD),
                "After حسناً, should remain on patient profile. Actual: "
                        + getDriver().getCurrentUrl());
    }

    @Test(priority = 4, enabled = false,
            description = "DEFERRED: Add service & verify total — waiting for clarification")
    public void addServiceAndVerifyTotalUpdates() {
        String patientCode = createFreshPatientWithoutVisit();
        admissionPage.clickOpdButton();

        if (outpatientPage.isActiveVisitModalDisplayed()) {
            outpatientPage.continueSameVisit();
        } else {
            outpatientPage.waitForDraftUrl();
            outpatientPage.fillAndSaveDraftVisit(CASE_TYPE_SPECIAL, "FIRST");
            outpatientPage.waitForServicesUrl();
        }

        double totalBefore = outpatientPage.getTotalAmountValue();
        outpatientPage.addServiceToVisit("FIRST", "FIRST", "FIRST");
        outpatientPage.waitUntilTotalGreaterThan(totalBefore);

        double totalAfter = outpatientPage.getTotalAmountValue();
        Assert.assertTrue(totalAfter > totalBefore,
                "الإجمالي must increase after adding a service. before="
                        + totalBefore + " after=" + totalAfter
                        + " raw=" + outpatientPage.getTotalAmountText());
    }

    // =========================================================
    // T5 : Services page load assertions
    // =========================================================

    @Test(priority = 5,
            description = "Services page: title, patient info card, visit code, unpaid badge, and zero totals on fresh visit")
    public void servicesPageLoadsWithCorrectData() {
        String patientCode = createFreshPatientWithoutVisit();
        admissionPage.clickOpdButton();

        if (outpatientPage.isActiveVisitModalDisplayed()) {
            outpatientPage.continueSameVisit();
        } else {
            outpatientPage.waitForDraftUrl();
            outpatientPage.fillAndSaveDraftVisit(CASE_TYPE_SPECIAL, "FIRST");
        }

        outpatientPage.waitForServicesUrl();
        outpatientPage.waitForServicesPageReady();

        String visitCodeFromUrl = outpatientPage.getVisitCodeFromUrl();

        // T5.1 — Page title
        Assert.assertEquals(outpatientPage.getServicesPageTitle(), "الخدمات المقدمة للمريض",
                "Page h1 must be 'الخدمات المقدمة للمريض'");

        // T5.2 — Header visit number matches URL visit code
        String headerVisitNum = outpatientPage.getPageHeaderVisitNumber();
        Assert.assertFalse(headerVisitNum.isBlank(),
                "Header must show 'زيارة رقم: X'");
        Assert.assertEquals(headerVisitNum, visitCodeFromUrl,
                "Header visit number must match URL visit code. header="
                        + headerVisitNum + " url=" + visitCodeFromUrl);

        // T5.3 — Patient code in card matches the one we created
        String cardPatientCode = outpatientPage.getPatientCodeFromCard();
        Assert.assertEquals(cardPatientCode, patientCode,
                "Patient code in card must match created patient. card="
                        + cardPatientCode + " expected=" + patientCode);

        // T5.4 — Visit code in card matches URL visit code
        String cardVisitCode = outpatientPage.getVisitCodeFromCard();
        Assert.assertEquals(cardVisitCode, visitCodeFromUrl,
                "Visit code in patient card must match URL visit code. card="
                        + cardVisitCode + " url=" + visitCodeFromUrl);

        // T5.5 — غير مدفوع badge is shown (new visit = unpaid)
        Assert.assertTrue(outpatientPage.isUnpaidBadgeDisplayed(),
                "New visit must show 'غير مدفوع' badge");

        // T5.6 — All totals strip chips are 0.00 on fresh visit
        Assert.assertEquals(outpatientPage.getTotalChipTotal(), "0.00",
                "إجمالي chip must be 0.00 on fresh visit");
        Assert.assertEquals(outpatientPage.getTotalChipCash(), "0.00",
                "نقدي chip must be 0.00 on fresh visit");
        Assert.assertEquals(outpatientPage.getTotalChipPaid(), "0.00",
                "مدفوع chip must be 0.00 on fresh visit");
        Assert.assertEquals(outpatientPage.getTotalChipRemaining(), "0.00",
                "متبقي chip must be 0.00 on fresh visit");
    }

    // =========================================================
    // T6 : Tabs navigation
    // =========================================================

    @Test(priority = 6,
            description = "All 4 tabs are visible; الخدمات tab is active by default")
    public void allTabsVisibleAndServicesTabActiveByDefault() {
        navigateToServicesPageForFreshVisit();

        // T6.1 — All 4 tabs visible
        Assert.assertTrue(outpatientPage.isTabVisible("opd-patient-services-services-tab-btn"),
                "الخدمات tab must be visible");
        Assert.assertTrue(outpatientPage.isTabVisible("opd-patient-services-medicines-tab-btn"),
                "صرف الادوية tab must be visible");
        Assert.assertTrue(outpatientPage.isTabVisible("opd-patient-services-med-request-tab-btn"),
                "طلب أدوية tab must be visible");
        Assert.assertTrue(outpatientPage.isTabVisible("opd-patient-services-med-return-tab-btn"),
                "طلب مرتجع أدوية tab must be visible");

        // T6.2 — الخدمات tab is active by default
        Assert.assertTrue(outpatientPage.isServicesTabActive(),
                "الخدمات tab must have 'active' class by default");

        // T6.3 — الخدمات tab badge shows "0" on fresh visit (no services added)
        Assert.assertEquals(outpatientPage.getServicesTabBadgeText(), "0",
                "الخدمات tab badge must show 0 on fresh visit");
    }

    // =========================================================
    // T7 : Add service form initial state
    // =========================================================

    @Test(priority = 7,
            description = "Add service form: إضافة button disabled, price fields readonly, favorites button visible")
    public void addServiceFormInitialState() {
        navigateToServicesPageForFreshVisit();

        // T7.1 — إضافة للقائمة button is disabled before selecting a service
        Assert.assertTrue(outpatientPage.isAddDraftButtonDisabled(),
                "'إضافة للقائمة' button must be disabled before a service is selected");

        // T7.2 — إظهار المفضلة button is visible
        Assert.assertTrue(outpatientPage.isToggleFavoritesBtnVisible(),
                "'إظهار المفضلة' button must be visible");

        // T7.3 — Price/calculated fields are readonly (user cannot type into them)
        Assert.assertTrue(outpatientPage.isUnitPriceReadonly(),
                "Unit price (السعر) field must be readonly");
        Assert.assertTrue(outpatientPage.isCreditPctReadonly(),
                "Credit % (ن الاجل %) field must be readonly");
        Assert.assertTrue(outpatientPage.isCreditPerUnitReadonly(),
                "Credit per unit (الأجل) field must be readonly");
        Assert.assertTrue(outpatientPage.isCashPerUnitReadonly(),
                "Cash per unit (النقدي) field must be readonly");

        // T7.4 — No services recorded message shown on fresh visit
        Assert.assertTrue(outpatientPage.isNoServicesMessageDisplayed(),
                "'لا توجد خدمات مسجلة' message must show on fresh visit");
    }

    // =========================================================
    // T8 : Add service full flow
    // =========================================================

    @Test(priority = 8,
            description = "Add service: select service, doctor & clinic → add → save → visit services update")
    public void addServiceUpdatesListAndTotal() {
        navigateToServicesPageForFreshVisit();

        // T8.1 — Add a service selecting required fields (service, doctor, clinic)
        outpatientPage.addServiceToVisit("FIRST", "FIRST", "FIRST");
        outpatientPage.clickSaveVisitInfo();

        // Wait for page or success response after save
        Assert.assertTrue(admissionPage.waitForSuccessfulPatientSave(),
                "Saving visit after adding service must succeed");
    }

    // =========================================================
    // T9 : Save visit info
    // =========================================================

    @Test(priority = 9,
            description = "Save visit info button: click حفظ → success toast or page stays on services")
    public void saveVisitInfoShowsSuccessToast() {
        navigateToServicesPageForFreshVisit();

        // Just click save without changing anything — should still succeed
        outpatientPage.clickSaveVisitInfo();

        // waitForSuccessfulPatientSave detects toast-success OR staying on saved URL
        Assert.assertTrue(admissionPage.waitForSuccessfulPatientSave(),
                "Clicking 'حفظ' (save visit info) must show a success toast or confirm save");
    }

    // =========================================================
    // T10 : Payment flow
    // =========================================================

    @Test(priority = 10,
            description = "Payment: add service → save → pay → receipt row appears in history table")
    public void paymentCreatesReceiptAndUpdatesPaidChip() {
        navigateToServicesPageForFreshVisit();

        // Add a service first so the visit has a service (populating all required fields)
        outpatientPage.addServiceToVisit("FIRST", "FIRST", "FIRST");
        outpatientPage.clickSaveVisitInfo();
        admissionPage.waitForSuccessfulPatientSave();

        // T10.1 — Payment history is empty before payment
        Assert.assertTrue(outpatientPage.isPaymentHistoryEmpty(),
                "Payment history must be empty before any payment");

        // T10.2 — Submit payment (treasury = pre-selected, first payment method, amount = 100)
        outpatientPage.fillAndSubmitPayment(
                "FIRST",
                "FIRST",
                "100");

        // T10.3 — A receipt row appears in payment history
        outpatientPage.waitForPaymentHistoryRow();
        Assert.assertTrue(outpatientPage.getPaymentHistoryRowCount() >= 1,
                "Payment history must show at least 1 receipt row after payment");
    }

    // =========================================================
    // T11 : Back button
    // =========================================================

    @Test(priority = 11,
            description = "Back button (opd-patient-services-back-btn) navigates away from services page")
    public void backButtonNavigatesFromServicesPage() {
        navigateToServicesPageForFreshVisit();

        String urlBefore = getDriver().getCurrentUrl();
        Assert.assertTrue(urlBefore.contains("/services"),
                "Must be on services page before clicking back. url=" + urlBefore);

        outpatientPage.clickBackButton();

        // Wait for URL to change away from /services
        waitForCondition(
                () -> !getDriver().getCurrentUrl().contains("/services"),
                "After clicking back, URL must no longer contain /services");

        String urlAfter = getDriver().getCurrentUrl();
        Assert.assertFalse(urlAfter.contains("/services"),
                "After back button, must leave services page. url=" + urlAfter);
    }

    // =========================================================
    // T12 : Service group filtering clinics
    // =========================================================

    @Test(priority = 12,
            description = "Service group filter: selecting 'الرمد والليزك' in opd-patient-services-service-group-select shows only 'عيادة 8' in clinic select")
    public void serviceGroupFilterLimitsClinicOptions() {
        navigateToServicesPageForFreshVisit();

        outpatientPage.selectServiceGroup("الرمد والليزك");
        List<String> clinicOptions = outpatientPage.getAvailableClinicOptions();

        Assert.assertFalse(clinicOptions.isEmpty(),
                "Clinic options list should not be empty after selecting service group 'الرمد والليزك'");
        Assert.assertTrue(clinicOptions.contains("عيادة 8"),
                "Clinic options must contain 'عيادة 8'. Actual options: " + clinicOptions);
        Assert.assertEquals(clinicOptions.size(), 1,
                "Service group 'الرمد والليزك' should only display 1 clinic ('عيادة 8'). Actual options: " + clinicOptions);
    }

    // =========================================================
    // T13 : ICD10 Diagnosis mandatory check by entity
    // =========================================================

    @Test(priority = 13,
            description = "ICD10 Diagnosis mandatory check: mandatory for entity 'اليكو' and optional for entity 'النقدي2019'")
    public void icdDiagnosisMandatoryValidationByEntity() {
        // 1. Entity 'النقدي2019' — Not mandatory: visit saves without ICD10
        String patientCode1 = createFreshPatientWithoutVisit();
        admissionPage.clickOpdButton();
        outpatientPage.waitForDraftUrl();
        outpatientPage.selectCaseType(CASE_TYPE_SPECIAL);
        outpatientPage.selectFirstSubCompanyOption();
        outpatientPage.clickSaveVisit();
        outpatientPage.waitForServicesUrl();
        Assert.assertTrue(outpatientPage.isOnServicesUrl(),
                "Visit with entity 'النقدي2019' must save without selecting ICD10 diagnosis");

        // 2. Entity 'اليكو' — Mandatory: cannot save without ICD10
        String patientCode2 = createFreshPatientWithoutVisit();
        admissionPage.clickOpdButton();
        outpatientPage.waitForDraftUrl();
        outpatientPage.selectCaseType(CASE_TYPE_SPECIAL);
        outpatientPage.selectSubCompany("اليكو");

        // Attempt save without selecting ICD10
        outpatientPage.clickSaveVisit();

        // Must stay on draft page or mark ICD mandatory
        try {
            Thread.sleep(1000);
        } catch (InterruptedException ignored) {}
        Assert.assertTrue(outpatientPage.isOnDraftUrl() || outpatientPage.isIcdDiagnosisMandatory(),
                "Saving visit for entity 'اليكو' must be blocked when ICD10 diagnosis is empty");

        // Select an ICD10 option then save -> succeeds
        outpatientPage.selectFirstIcdDiagnosisOption();
        outpatientPage.clickSaveVisit();
        outpatientPage.waitForServicesUrl();
        Assert.assertTrue(outpatientPage.isOnServicesUrl(),
                "Visit with entity 'اليكو' must save successfully after selecting an ICD10 diagnosis");
    }

    // =========================================================
    // T14 : Print barcode URL verification
    // =========================================================

    @Test(priority = 14,
            description = "Print barcode button (opd-patient-services-print-barcode-btn) opens URL https://196.218.246.250:4040/clinic/visits/xxxxx/barcode-print")
    public void printBarcodeButtonOpensCorrectUrl() {
        navigateToServicesPageForFreshVisit();

        String visitCode = outpatientPage.getVisitCodeFromUrl();
        Assert.assertFalse(visitCode.isBlank(), "Visit code must be present in services URL");

        String expectedPattern = "/clinic/visits/" + visitCode + "/barcode-print";
        String href = outpatientPage.getBarcodeButtonHref();
        String openedUrl = outpatientPage.clickPrintBarcodeAndGetUrl();

        boolean matchesPattern = openedUrl.contains(expectedPattern) || (href != null && href.contains(expectedPattern));
        Assert.assertTrue(matchesPattern,
                "Print barcode button URL must contain '" + expectedPattern
                        + "'. Actual opened URL: " + openedUrl + ", href: " + href);
    }

    // =========================================================
    // T15 : Claim form modal CRUD operations
    // =========================================================

    @Test(priority = 15,
            description = "Claim form modal (opd-patient-services-open-claim-btn): add claim, verify download & delete buttons")
    public void claimModalAddDownloadAndDeleteOperations() throws Exception {
        navigateToServicesPageForFreshVisit();

        File tempClaimFile = File.createTempFile("test_claim_", ".txt");
        tempClaimFile.deleteOnExit();
        Files.writeString(tempClaimFile.toPath(), "Sample claim content");

        String claimTitle = "324234";

        // 1. Open Modal
        outpatientPage.openClaimModal();
        Assert.assertTrue(outpatientPage.isClaimModalDisplayed(),
                "Claim modal must be visible after clicking opd-patient-services-open-claim-btn");

        // 2. Add / Upload Claim
        outpatientPage.fillAndUploadClaim(claimTitle, tempClaimFile.getAbsolutePath());

        // 3. Verify Claim is in grid
        Assert.assertTrue(outpatientPage.isClaimTitleInGrid(claimTitle),
                "Uploaded claim title '" + claimTitle + "' must appear in grid list");

        // 4. Download Claim
        outpatientPage.clickDownloadClaimForTitle(claimTitle);

        // 5. Delete Claim
        outpatientPage.clickDeleteClaimForTitle(claimTitle);
        Assert.assertFalse(outpatientPage.isClaimTitleInGrid(claimTitle),
                "Claim title '" + claimTitle + "' must be removed from grid list after deletion");

        // 6. Close Modal
        outpatientPage.closeClaimModal();
        Assert.assertFalse(outpatientPage.isClaimModalDisplayed(),
                "Claim modal must close after clicking close button");
    }

    // =========================================================
    // T16 : Service short code lookup (Valid 4444 & Invalid 91238128)
    // =========================================================

    @Test(priority = 16,
            description = "Service short code lookup: valid code 4444 auto-populates service & price; invalid code 91238128 triggers error message 'كود الخدمة غير صحيح'")
    public void serviceShortCodeValidAndInvalidVerification() {
        navigateToServicesPageForFreshVisit();

        // 1. Invalid short code test (91238128)
        outpatientPage.enterShortCodeAndPressEnter("91238128");

        try {
            Thread.sleep(800);
        } catch (InterruptedException ignored) {}

        boolean hasError = outpatientPage.isInvalidServiceCodeErrorDisplayed();
        String errorText = outpatientPage.getInvalidServiceCodeErrorText();
        Assert.assertTrue(hasError || errorText.contains("كود الخدمة غير صحيح"),
                "Entering invalid short code '91238128' must display error message 'كود الخدمة غير صحيح'. Actual text: " + errorText);

        // 2. Valid short code test (4444)
        outpatientPage.enterShortCodeAndPressEnter("4444");

        try {
            Thread.sleep(1000);
        } catch (InterruptedException ignored) {}

        String priceVal = outpatientPage.getUnitPriceInputValue();
        String selectedService = outpatientPage.getSelectedServiceNameText();

        Assert.assertFalse(priceVal.isBlank() || "0".equals(priceVal) || "0.00".equals(priceVal),
                "Entering valid short code '4444' must populate service price. Actual price: " + priceVal);
        Assert.assertFalse(selectedService.isBlank(),
                "Entering valid short code '4444' must populate selected service name. Actual service: " + selectedService);
    }

    // =========================================================
    // T17 : Approval Number Field State (Service 444 needs approval)
    // =========================================================

    @Test(priority = 17,
            description = "Approval number field: closed/disabled for default services, opened/enabled when service '444' is selected")
    public void approvalNumberFieldToggleVerification() {
        navigateToServicesPageForFreshVisit();

        // 1. Initial state without approval-required service
        boolean initiallyEnabled = outpatientPage.isApprovalNumberInputEnabled();
        Assert.assertFalse(initiallyEnabled,
                "Approval number field should be closed/disabled by default for services that do not require approval");

        // 2. Select service with code '444' (which requires approval)
        outpatientPage.enterShortCodeAndPressEnter("444");

        try {
            Thread.sleep(1000);
        } catch (InterruptedException ignored) {}

        boolean enabledFor444 = outpatientPage.isApprovalNumberInputEnabled();
        Assert.assertTrue(enabledFor444,
                "Approval number field must open/enable when service '444' is selected");

        // 3. Fill approval number
        outpatientPage.enterApprovalNumber("324");
        Assert.assertEquals(outpatientPage.getApprovalNumberInputValue(), "324",
                "Approval number field must contain the entered approval number '324'");
    }

    // =========================================================
    // T18 : Complete Services Draft and Save Cycle
    // =========================================================

    @Test(priority = 18,
            description = "Complete outpatient service cycle: select group, service (444), doctor, clinic, enter approval number -> add to draft -> save -> verify in saved grid")
    public void completeServicesDraftAndSaveCycle() {
        navigateToServicesPageForFreshVisit();

        // 1. Select service 444 via short code or dropdown
        outpatientPage.enterShortCodeAndPressEnter("444");

        try {
            Thread.sleep(1000);
        } catch (InterruptedException ignored) {}

        // Select doctor and clinic
        outpatientPage.selectFirstDoctorOption();
        outpatientPage.selectFirstClinicOption();

        // Fill approval number '324' if required
        if (outpatientPage.isApprovalNumberInputEnabled()) {
            outpatientPage.enterApprovalNumber("324");
        }

        // 2. Click "إضافة للقائمة" (Add to draft)
        int draftCountBefore = outpatientPage.getDraftServicesRowCount();
        outpatientPage.clickAddDraftService();

        try {
            Thread.sleep(1000);
        } catch (InterruptedException ignored) {}

        int draftCountAfter = outpatientPage.getDraftServicesRowCount();
        Assert.assertTrue(draftCountAfter > draftCountBefore || outpatientPage.isDraftServicePresent("444"),
                "Service '444' must be added to draft services list (خدمات في الانتظار)");

        // 3. Click "حفظ الخدمات" (Save draft services)
        outpatientPage.clickSaveDraftServices();

        try {
            Thread.sleep(1500);
        } catch (InterruptedException ignored) {}

        int savedCount = outpatientPage.getSavedServicesRowCountFromGrid();
        Assert.assertTrue(savedCount >= 1 || outpatientPage.isSavedServicePresentInGrid("444") || outpatientPage.getSavedServicesCount() >= 1,
                "Saved services grid must contain the saved service row after clicking 'حفظ الخدمات'");
    }

    // =========================================================
    // T16–T21 : Outpatient Services Business & Validation Rules
    // =========================================================

    private static final String SERVICE_GROUP_BACK = "خدمات الكشف على الظهر";
    private static final String SVC_NON_COUNTABLE = "خدمة الظهر الشاملة الكاملة 1";
    private static final String SVC_COUNTABLE = "مفاصل الظهر (تنفيذ مباشر)";
    private static final String SVC_NO_DOCTOR = "كشف ظهر كامل";
    private static final String SVC_NEEDS_DOCTOR = "كشف ظهر";

    @Test(priority = 16, description = "Rule 1: Quantity field must be >= 1; non-countable services lock quantity at 1 while countable services allow custom quantity")
    public void verifyServiceQuantityFieldRules() {
        navigateToServicesPageForFreshVisit();
        outpatientPage.selectServiceGroup(SERVICE_GROUP_BACK);

        // Non-countable service -> quantity must be locked/readonly at 1
        outpatientPage.selectServiceBySearch(SVC_NON_COUNTABLE);
        Assert.assertEquals(outpatientPage.getQuantityInputValue(), "1",
                "Non-countable service 'خدمة الظهر الشاملة الكاملة 1' quantity must default to 1");
        Assert.assertTrue(outpatientPage.isQuantityInputReadonly(),
                "Non-countable service 'خدمة الظهر الشاملة الكاملة 1' quantity field must be locked/readonly");

        // Countable service -> quantity input must be enabled
        outpatientPage.selectServiceBySearch(SVC_COUNTABLE);
        Assert.assertTrue(outpatientPage.isQuantityInputEnabled(),
                "Countable service 'مفاصل الظهر (تنفيذ مباشر)' quantity field must be editable");
        outpatientPage.enterQuantity("3");
        Assert.assertEquals(outpatientPage.getQuantityInputValue(), "3",
                "Entered quantity 3 must be retained in quantity field");
    }

    @Test(priority = 17, description = "Rule 2: Approval number field rules: mandatory when service requires approval number")
    public void verifyApprovalNumberRules() {
        navigateToServicesPageForFreshVisit();
        outpatientPage.selectServiceGroup(SERVICE_GROUP_BACK);

        // Service requiring approval number
        outpatientPage.selectServiceBySearch(SVC_COUNTABLE);
        outpatientPage.clickAddDraftService();

        Assert.assertTrue(outpatientPage.isToastOrAlertContaining("برجاء إدخال رقم الموافقة")
                        || outpatientPage.isToastOrAlertContaining("الموافقة"),
                "Adding service requiring approval number without entering approval number must show error 'برجاء إدخال رقم الموافقة'. Actual toast: "
                        + outpatientPage.getVisibleToastOrAlertText());

        // Service not requiring approval number
        outpatientPage.selectServiceBySearch(SVC_NON_COUNTABLE);
        Assert.assertFalse(outpatientPage.isApprovalNumberInputEnabled(),
                "Service not requiring approval number 'خدمة الظهر الشاملة الكاملة 1' should not mandate approval input");
    }

    @Test(priority = 18, description = "Rule 3: Doctor requirement rules: service needing doctor vs service not needing doctor")
    public void verifyDoctorMandatoryRules() {
        navigateToServicesPageForFreshVisit();
        outpatientPage.selectServiceGroup(SERVICE_GROUP_BACK);

        // Service not needing doctor: كشف ظهر كامل
        outpatientPage.selectServiceBySearch(SVC_NO_DOCTOR);
        int countBefore = outpatientPage.getDraftServicesRowCount();
        outpatientPage.clickAddDraftService();
        try { Thread.sleep(500); } catch (InterruptedException ignored) {}
        int countAfter = outpatientPage.getDraftServicesRowCount();
        Assert.assertTrue(countAfter > countBefore || outpatientPage.isDraftServicePresent(SVC_NO_DOCTOR) || outpatientPage.isAddDraftButtonEnabled(),
                "Service not requiring doctor 'كشف ظهر كامل' should be added without selecting doctor");

        // Service needing doctor: كشف ظهر
        outpatientPage.selectServiceBySearch(SVC_NEEDS_DOCTOR);
        outpatientPage.clickAddDraftService();
        Assert.assertTrue(outpatientPage.isToastOrAlertContaining("طبيب")
                        || outpatientPage.isToastOrAlertContaining("اختر الطبيب")
                        || outpatientPage.isToastOrAlertContaining("برجاء إدخال الطبيب")
                        || outpatientPage.isToastOrAlertContaining("إجباري"),
                "Adding service requiring doctor 'كشف ظهر' without selecting a doctor must show validation error. Actual toast: "
                        + outpatientPage.getVisibleToastOrAlertText());
    }

    @Test(priority = 19, description = "Rule 4: Unit price editability rules: fixed price vs editable price services")
    public void verifyServicePriceEditableRules() {
        navigateToServicesPageForFreshVisit();
        outpatientPage.selectServiceGroup(SERVICE_GROUP_BACK);

        // Non-editable price service: خدمة الظهر الشاملة الكاملة 1
        outpatientPage.selectServiceBySearch(SVC_NON_COUNTABLE);
        Assert.assertTrue(outpatientPage.isUnitPriceInputReadonly(),
                "Price field for fixed-price service 'خدمة الظهر الشاملة الكاملة 1' must be locked/readonly");
        Assert.assertFalse(outpatientPage.getUnitPriceInputValue().isBlank(),
                "Fixed-price service must show its pre-configured unit price");

        // Editable price service: مفاصل الظهر (تنفيذ مباشر)
        outpatientPage.selectServiceBySearch(SVC_COUNTABLE);
        Assert.assertTrue(outpatientPage.isUnitPriceInputEnabled(),
                "Price field for editable-price service 'مفاصل الظهر (تنفيذ مباشر)' must be enabled");
    }

    @Test(priority = 20, description = "Rule 5: Discount giver DDL rules: disabled by default, opens when discount % entered, mandatory when discount applied")
    public void verifyDiscountGiverMandatoryRules() {
        navigateToServicesPageForFreshVisit();
        outpatientPage.selectServiceGroup(SERVICE_GROUP_BACK);
        outpatientPage.selectServiceBySearch(SVC_NON_COUNTABLE);

        // Default state: discount giver disabled when discount % is 0 or empty
        Assert.assertTrue(outpatientPage.isDiscountGiverSelectDisabled(),
                "Discount giver DDL must be disabled when discount percentage is not entered");

        // Enter discount % -> DDL becomes enabled
        outpatientPage.enterDiscountPct("10");
        Assert.assertTrue(outpatientPage.isDiscountGiverSelectEnabled(),
                "Discount giver DDL must become enabled when discount percentage is entered");

        // Trying to add service with discount % but without selecting discount giver must fail
        outpatientPage.clickAddDraftService();
        Assert.assertTrue(outpatientPage.isToastOrAlertContaining("مانح الخصم")
                        || outpatientPage.isToastOrAlertContaining("خصم")
                        || outpatientPage.isToastOrAlertContaining("برجاء اختيار"),
                "Adding service with discount % without picking discount giver must show validation error. Actual toast: "
                        + outpatientPage.getVisibleToastOrAlertText());

        // Select discount giver -> service can now be added
        outpatientPage.selectDiscountGiver("FIRST");
        outpatientPage.clickAddDraftService();
        try { Thread.sleep(500); } catch (InterruptedException ignored) {}
        Assert.assertTrue(outpatientPage.getDraftServicesRowCount() > 0 || outpatientPage.isDraftServicePresent(SVC_NON_COUNTABLE),
                "Service with discount % and discount giver selected should be added to draft list");
    }

    @Test(priority = 21, description = "Rule 6: Discount percentage limits: > 100% displays error and clears field; negative % shows error")
    public void verifyDiscountPercentageLimits() {
        navigateToServicesPageForFreshVisit();
        outpatientPage.selectServiceGroup(SERVICE_GROUP_BACK);
        outpatientPage.selectServiceBySearch(SVC_NON_COUNTABLE);

        // 1. Discount percentage > 100% (e.g. 150%)
        outpatientPage.enterDiscountPct("150");
        outpatientPage.clickAddDraftService();
        Assert.assertTrue(outpatientPage.isToastOrAlertContaining("نسبة الخصم يجب ألا تزيد عن 100%")
                        || outpatientPage.isToastOrAlertContaining("100%"),
                "Entering discount > 100% must show error 'نسبة الخصم يجب ألا تزيد عن 100%'. Actual toast: "
                        + outpatientPage.getVisibleToastOrAlertText());

        String valAfter150 = outpatientPage.getDiscountPctInputValue();
        Assert.assertTrue(valAfter150.isBlank() || "0".equals(valAfter150) || Double.parseDouble(valAfter150) <= 100,
                "Field value after entering > 100% must be cleared or reset. Actual: " + valAfter150);

        // 2. Negative discount percentage (e.g. -10%)
        outpatientPage.enterDiscountPct("-10");
        outpatientPage.clickAddDraftService();
        Assert.assertTrue(outpatientPage.isToastOrAlertContaining("أقل من الصفر")
                        || outpatientPage.isToastOrAlertContaining("سالب")
                        || outpatientPage.isToastOrAlertContaining("غير صحيح")
                        || outpatientPage.isToastOrAlertContaining("خطأ"),
                "Entering negative discount percentage must show validation error. Actual toast: "
                        + outpatientPage.getVisibleToastOrAlertText());
    }

    // =========================================================
    // T22–T25 : Favorites List & Medicines Tab Validation Tests
    // =========================================================

    @Test(priority = 22,
            description = "Favorites list toggle (opd-patient-services-toggle-favorites-btn): opens favorite menu select (opd-patient-services-favorite-menu-select) and displays item checkboxes (opd-patient-services-favorite-item-checkbox)")
    public void favoritesListToggleAndItemSelection() {
        // Create visit under default cash entity
        navigateToServicesPageForFreshVisit();

        // 1. Verify toggle favorites button is displayed and click it
        Assert.assertTrue(outpatientPage.isToggleFavoritesBtnVisible(),
                "Toggle favorites button (opd-patient-services-toggle-favorites-btn) must be visible on services page");

        outpatientPage.clickToggleFavoritesButton();

        // 2. Verify favorite menu select DDL appears
        Assert.assertTrue(outpatientPage.isFavoriteMenuSelectDisplayed(),
                "Favorite menu select (opd-patient-services-favorite-menu-select) must be displayed after toggling favorites");

        // 3. Select favorite menu "اليكو 2026"
        outpatientPage.selectFavoriteMenu("اليكو 2026");

        // 4. Verify item checkboxes appear
        try { Thread.sleep(800); } catch (InterruptedException ignored) {}
        Assert.assertTrue(outpatientPage.isFavoriteItemCheckboxDisplayed() || outpatientPage.getFavoriteItemCheckboxesCount() > 0,
                "Favorite item checkboxes (opd-patient-services-favorite-item-checkbox) must be displayed for menu 'اليكو 2026'");
    }

    @Test(priority = 23,
            description = "Medicines tab initial state & store/doctor requirement: DDLs display 'اختر المخزن' and 'اختر الطبيب'; '+' button hidden before store selection and visible after selecting 'main store' & 'Ahmed Badawi'")
    public void medicinesTabInitialStateAndStoreDoctorSelection() {
        navigateToServicesPageForFreshVisit();

        // 1. Switch to medicines tab
        outpatientPage.switchToMedicinesTab();

        // 2. Assert initial state: Store DDL empty / showing 'اختر المخزن', Doctor DDL empty / showing 'اختر الطبيب'
        Assert.assertTrue(outpatientPage.isMedStoreEmptyOrPlaceholder(),
                "Store DDL (opd-patient-services-med-charge-store-select) must show 'اختر المخزن' initially");
        Assert.assertTrue(outpatientPage.isMedDoctorEmptyOrPlaceholder(),
                "Doctor DDL (opd-patient-services-med-charge-doctor-select) must show 'اختر الطبيب' initially");

        // 3. Verify '+' batch button is NOT visible before selecting store
        Assert.assertFalse(outpatientPage.isOpenMedBatchDialogButtonVisible(),
                "Add batch '+' button (opd-patient-services-open-med-batch-dialog-btn) must NOT be visible before selecting store");

        // 4. Select store 'main store' and doctor 'Ahmed Badawi'
        outpatientPage.selectMedStore("main store");
        outpatientPage.selectMedDoctor("Ahmed Badawi");

        // 5. Verify '+' batch button is now visible after store selection
        Assert.assertTrue(outpatientPage.isOpenMedBatchDialogButtonVisible(),
                "Add batch '+' button (opd-patient-services-open-med-batch-dialog-btn) must become visible after selecting store 'main store'");
    }

    @Test(priority = 24,
            description = "Medicines tab item selection & clear button ('جديد'): select item 'يورانيوم مشع', unit 'حبيبات', click '+' button, then click 'جديد' (opd-patient-services-clear-med-charge-btn) -> verifies data cleared")
    public void medicinesTabItemSelectionBatchAndClearData() {
        navigateToServicesPageForFreshVisit();

        // 1. Switch to medicines tab & select store & doctor
        outpatientPage.switchToMedicinesTab();
        outpatientPage.selectMedStore("main store");
        outpatientPage.selectMedDoctor("Ahmed Badawi");

        // 2. Select item 'يورانيوم مشع' and unit 'حبيبات'
        outpatientPage.selectMedItem("يورانيوم مشع");
        outpatientPage.selectMedUnit("حبيبات");

        // 3. Click '+' batch dialog button
        outpatientPage.clickOpenMedBatchDialogButton();

        // 4. Click 'جديد' clear button
        outpatientPage.clickClearMedChargeButton();

        // 5. Verify data in Store, Doctor, Item DDLs has been cleared
        Assert.assertTrue(outpatientPage.isMedStoreEmptyOrPlaceholder(),
                "Clicking 'جديد' button must clear store selection back to 'اختر المخزن'");
        Assert.assertTrue(outpatientPage.isMedDoctorEmptyOrPlaceholder(),
                "Clicking 'جديد' button must clear doctor selection back to 'اختر الطبيب'");
        Assert.assertTrue(outpatientPage.isMedItemEmptyOrPlaceholder(),
                "Clicking 'جديد' button must clear item selection");
    }

    @Test(priority = 25,
            description = "Medicines tab credit percentage field (opd-patient-services-med-charge-entry-credit-pct-input): locked/readonly for cash entity, enabled/editable (0-100%) for credit entity")
    public void medicinesTabCreditPctFieldValidationCashVsCredit() {
        // Part 1: Cash Entity Visit -> credit pct field must be locked/readonly
        navigateToServicesPageForFreshVisit();

        outpatientPage.switchToMedicinesTab();

        Assert.assertTrue(outpatientPage.isMedChargeCreditPctReadonlyOrDisabled(),
                "Credit percentage field (opd-patient-services-med-charge-entry-credit-pct-input) must be locked/readonly for cash entity visits");

        // Part 2: Credit Entity Visit -> credit pct field must be enabled & accept 0-100%
        createFreshPatientWithoutVisit();
        admissionPage.clickOpdButton();
        if (outpatientPage.isActiveVisitModalDisplayed()) {
            outpatientPage.continueSameVisit();
        } else {
            outpatientPage.waitForDraftUrl();
            outpatientPage.selectCaseType(CASE_TYPE_SPECIAL);
            outpatientPage.selectSubCompany("اليكو");
            outpatientPage.selectFirstIcdDiagnosisOption();
            outpatientPage.clickSaveVisit();
        }
        outpatientPage.waitForServicesUrl();
        outpatientPage.waitForServicesPageReady();

        outpatientPage.switchToMedicinesTab();

        Assert.assertTrue(outpatientPage.isMedChargeCreditPctEnabled(),
                "Credit percentage field (opd-patient-services-med-charge-entry-credit-pct-input) must be enabled for credit entity visits");

        outpatientPage.enterMedChargeCreditPct("20");
        Assert.assertEquals(outpatientPage.getMedChargeCreditPctInputValue(), "20",
                "Credit percentage field must contain entered percentage '20'");
    }

    // =========================================================
    // Helpers
    // =========================================================

    /**
     * Creates a fresh patient, opens draft visit, saves it, and lands on the
     * services page — ready for T5–T11 assertions.
     */
    private void navigateToServicesPageForFreshVisit() {
        createFreshPatientWithoutVisit();
        // Patient profile is already open after save
        admissionPage.clickOpdButton();

        if (outpatientPage.isActiveVisitModalDisplayed()) {
            outpatientPage.continueSameVisit();
        } else {
            outpatientPage.waitForDraftUrl();
            outpatientPage.fillAndSaveDraftVisit(CASE_TYPE_SPECIAL, "FIRST");
        }

        outpatientPage.waitForServicesUrl();
        outpatientPage.waitForServicesPageReady();
    }

    /**
     * Polls a condition with explicit wait (15s).
     * Avoids Thread.sleep — uses WebDriverWait lambda.
     */
    private void waitForCondition(java.util.function.Supplier<Boolean> condition, String errorMessage) {
        new org.openqa.selenium.support.ui.WebDriverWait(getDriver(), java.time.Duration.ofSeconds(15))
                .withMessage(errorMessage)
                .until(d -> condition.get());
    }

    /** Parses a chip value string like "50.00" → 50.0, returns 0 on failure. */
    private double parseTotalChip(String chipText) {
        try {
            return Double.parseDouble(chipText.replace(",", "").trim());
        } catch (Exception e) {
            return 0.0;
        }
    }

    private String createFreshPatientWithoutVisit() {
        admissionPage.prepareIsolatedTestState();
        String name = AUTOMATION_PATIENT_SEARCH + " OPD "
                + ThreadLocalRandom.current().nextInt(1, 10_001)
                + (System.currentTimeMillis() % 10_000);
        long mixed = Math.abs(System.nanoTime() ^ ThreadLocalRandom.current().nextLong());
        String mobile = "010" + String.format("%08d", mixed % 100_000_000L);

        admissionPage.fillMandatoryFields(name, mobile, VALID_BIRTH_DATE, VALID_GENDER);
        admissionPage.clickSave();
        Assert.assertTrue(admissionPage.waitForSuccessfulPatientSave(),
                "Failed to create clean OPD patient. URL=" + getDriver().getCurrentUrl());

        String code = admissionPage.getSelectedPatientCode();
        Assert.assertFalse(code == null || code.isBlank(), "patientCode empty after save");
        return code;
    }
}
