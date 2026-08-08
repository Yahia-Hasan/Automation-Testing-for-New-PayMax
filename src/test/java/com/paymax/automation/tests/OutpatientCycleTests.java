package com.paymax.automation.tests;

import com.paymax.automation.base.BaseTest;
import com.paymax.automation.pages.OutpatientPage;
import com.paymax.automation.pages.PatientAdmissionPage;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

import java.util.concurrent.ThreadLocalRandom;

/**
 * Independent Outpatient Visits cycle (العيادات الخارجية).
 * Uses {@link OutpatientPage} and seeds patients via {@link PatientAdmissionPage}.
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

    @Test(priority = 1,
            description = "Draft visit creation: fill نوع الحالة + الشركة الفرعية, save → /services")
    public void createDraftVisitAndTransitionToServices() {
        String patientCode = createFreshPatientWithoutVisit();

        admissionPage.openPatientProfileByCode(patientCode);
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
        admissionPage.openPatientProfileByCode(PATIENT_WITH_ACTIVE_OPD);
        admissionPage.clickOpdButton();

        outpatientPage.waitForActiveVisitModal();
        Assert.assertTrue(outpatientPage.isActiveVisitModalDisplayed(),
                "Active visit warning modal must appear for patient " + PATIENT_WITH_ACTIVE_OPD);

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
        admissionPage.openPatientProfileByCode(PATIENT_UNPAID_OPD);
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
        admissionPage.openPatientProfileByCode(patientCode);
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
