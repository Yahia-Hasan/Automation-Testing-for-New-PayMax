package com.paymax.automation.tests;

import com.paymax.automation.base.BaseTest;
import com.paymax.automation.pages.PatientAdmissionPage;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import java.util.concurrent.ThreadLocalRandom;
import java.util.function.Consumer;

/**
 * Phase-2 coverage for the patient top action bar that appears after a patient
 * is created or selected on Reception.
 * <p>
 * Business rule: عيادات خارجية + الأشعة + التحاليل are one external-visit family.
 * Switching among them must reopen the same visit code. Crossing into دخول or
 * إسعاف (or from those into the external family) must show an ERROR.
 */
public class PatientActionBarTests extends BaseTest {

    /** Distinctive prefix used by admission happy-path patients. */
    private static final String AUTOMATION_PATIENT_SEARCH = "يحيى تيست اوتوميشن";
    private static final String VALID_BIRTH_DATE = "1990-05-15";
    private static final String VALID_GENDER = "ذكر";
    private static final String CLIENT_ID = "52";

    /**
     * Patients already placed in an active visit manually (do not create visits in the test).
     */
    private static final String PATIENT_OPD = "30499";
    private static final String PATIENT_INPATIENT = "30496";
    private static final String PATIENT_EMERGENCY = "30495";
    private static final String PATIENT_RAYS = "30485";
    private static final String PATIENT_LAB = "30456";

    private PatientAdmissionPage page;
    private String knownPatientCode;

    @BeforeClass(alwaysRun = true)
    public void loginAndEnsureAutomationPatient() {
        loginAndNavigateToNewSystem();
        page = new PatientAdmissionPage(getDriver()).navigateToReception();
        knownPatientCode = ensureAutomationPatientExists();
        Assert.assertFalse(knownPatientCode == null || knownPatientCode.isBlank(),
                "Could not resolve a dynamic patientCode for action-bar tests");
    }

    @BeforeMethod(alwaysRun = true)
    public void resetToCleanReception() {
        page.prepareIsolatedTestState();
    }

    @AfterMethod(alwaysRun = true)
    public void cleanupUi() {
        try {
            java.util.Set<String> handles = getDriver().getWindowHandles();
            if (handles.size() > 1) {
                String keep = null;
                for (String handle : handles) {
                    getDriver().switchTo().window(handle);
                    String url = getDriver().getCurrentUrl();
                    if (url != null && url.contains("/reception")) {
                        keep = handle;
                        break;
                    }
                }
                if (keep == null) {
                    keep = handles.iterator().next();
                }
                for (String handle : new java.util.HashSet<>(getDriver().getWindowHandles())) {
                    if (!handle.equals(keep)) {
                        getDriver().switchTo().window(handle);
                        getDriver().close();
                    }
                }
                getDriver().switchTo().window(keep);
            }
            page.dismissOverlaysAndToasts();
        } catch (Exception ignored) {
            // Never fail the suite from cleanup
        }
    }

    @Test(priority = 1,
            description = "Each active top-bar action redirects with the dynamic patientCode")
    public void verifyDynamicActionBarRedirects() {
        assertActionRedirects("دخول",
                PatientAdmissionPage::clickAdmissionButton,
                code -> new String[] {"/reception/patient/" + code + "/admission"});

        assertActionRedirects("عيادات خارجية",
                PatientAdmissionPage::clickOpdButton,
                code -> new String[] {
                        "/clinic/visits/draft",
                        "patientCode=" + code,
                        "clientId=" + CLIENT_ID,
                        "mode=opd"
                });

        assertActionRedirects("الأشعة",
                PatientAdmissionPage::clickRaysButton,
                code -> new String[] {
                        "/clinic/visits/draft",
                        "patientCode=" + code,
                        "clientId=" + CLIENT_ID,
                        "mode=rays"
                });

        assertActionRedirects("تحاليل",
                PatientAdmissionPage::clickTestsButton,
                code -> new String[] {
                        "/clinic/visits/draft",
                        "patientCode=" + code,
                        "clientId=" + CLIENT_ID,
                        "mode=tests"
                });

        assertActionRedirects("إسعاف وطوارئ",
                PatientAdmissionPage::clickEmergencyButton,
                code -> new String[] {
                        "/emergency/cases/draft",
                        "patientCode=" + code,
                        "clientId=" + CLIENT_ID
                });
    }

    @Test(priority = 2, description = "باركود المريض opens a popup with /print/barcode?id={code}")
    public void verifyPatientBarcodePopupWindow() {
        String patientCode = openKnownPatientAndGetCode();
        String popupUrl = page.verifyBarcodeWindow(patientCode);

        Assert.assertTrue(popupUrl.contains("/print/barcode?id="),
                "Barcode popup URL should contain /print/barcode?id=. Actual: " + popupUrl);
        Assert.assertTrue(popupUrl.contains("id=" + patientCode),
                "Barcode popup URL should include patientCode " + patientCode
                        + ". Actual: " + popupUrl);
        Assert.assertTrue(getDriver().getCurrentUrl().contains("/reception/patient/" + patientCode),
                "Driver should be back on the patient profile after closing the barcode popup. "
                        + "Actual: " + getDriver().getCurrentUrl());
    }

    @Test(priority = 3, description = "Under-development action buttons stay inactive / do not break the app")
    public void verifyUnderDevelopmentActionButtonsDoNotBreakApp() {
        openKnownPatientAndGetCode();

        assertUnderDevSafe(page.catheterButtonLocator(), "قسطرة");
        assertUnderDevSafe(page.dialysisButtonLocator(), "غسيل كلى");
        assertUnderDevSafe(page.endoscopyButtonLocator(), "المناظير");
        assertUnderDevSafe(page.archiveButtonLocator(), "الأرشيف");
    }

    /**
     * External-visit family: OPD / Rays / Lab share one visit.
     * Each seed patient opens its own mode first, then the other two modes,
     * and كود الزيارة must stay the same.
     */
    @DataProvider(name = "externalVisitFamilyPatients")
    public Object[][] externalVisitFamilyPatients() {
        return new Object[][] {
                {"خارجي (OPD)", PATIENT_OPD, "opd",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickOpdButton},
                {"أشعة", PATIENT_RAYS, "rays",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickRaysButton},
                {"تحاليل", PATIENT_LAB, "tests",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickTestsButton},
        };
    }

    @Test(priority = 4, dataProvider = "externalVisitFamilyPatients",
            description = "OPD/Rays/Lab are one external visit — switching modes keeps the same visit code")
    public void verifyExternalVisitFamilyKeepsSameVisitCode(
            String activeVisitLabel,
            String patientCode,
            String seedMode,
            Consumer<PatientAdmissionPage> openSeedMode) {

        page.openPatientProfileByCode(patientCode);
        Assert.assertEquals(page.getSelectedPatientCode(), patientCode,
                "Opened wrong patient for external-visit family (" + activeVisitLabel + ")");

        openSeedMode.accept(page);
        page.waitForUrlContains("/clinic/visits/");
        page.waitForUrlContains("patientCode=" + patientCode);
        page.waitForUrlContains("mode=" + seedMode);
        String baselineVisitCode = page.getVisitCodeFromVisitPage();
        Assert.assertFalse(baselineVisitCode == null || baselineVisitCode.isBlank(),
                "Could not read كود الزيارة for patient " + patientCode
                        + " (" + activeVisitLabel + "). URL=" + getDriver().getCurrentUrl());

        assertExternalModeKeepsVisitCode(patientCode, baselineVisitCode, "opd",
                PatientAdmissionPage::clickOpdButton);
        assertExternalModeKeepsVisitCode(patientCode, baselineVisitCode, "rays",
                PatientAdmissionPage::clickRaysButton);
        assertExternalModeKeepsVisitCode(patientCode, baselineVisitCode, "tests",
                PatientAdmissionPage::clickTestsButton);
    }

    /**
     * Crossing out of / into incompatible visit types must ERROR.
     * OPD/Rays/Lab must NOT block each other (covered by the family test above).
     */
    @DataProvider(name = "incompatibleActiveVisitSwitches")
    public Object[][] incompatibleActiveVisitSwitches() {
        return new Object[][] {
                {"خارجي (OPD)", PATIENT_OPD, "دخول",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickAdmissionButton},
                {"خارجي (OPD)", PATIENT_OPD, "إسعاف وطوارئ",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickEmergencyButton},
                {"أشعة", PATIENT_RAYS, "دخول",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickAdmissionButton},
                {"أشعة", PATIENT_RAYS, "إسعاف وطوارئ",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickEmergencyButton},
                {"تحاليل", PATIENT_LAB, "دخول",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickAdmissionButton},
                {"تحاليل", PATIENT_LAB, "إسعاف وطوارئ",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickEmergencyButton},
                {"داخلي (Admission)", PATIENT_INPATIENT, "عيادات خارجية",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickOpdButton},
                {"داخلي (Admission)", PATIENT_INPATIENT, "الأشعة",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickRaysButton},
                {"داخلي (Admission)", PATIENT_INPATIENT, "تحاليل",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickTestsButton},
                {"داخلي (Admission)", PATIENT_INPATIENT, "إسعاف وطوارئ",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickEmergencyButton},
                {"طوارئ", PATIENT_EMERGENCY, "عيادات خارجية",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickOpdButton},
                {"طوارئ", PATIENT_EMERGENCY, "الأشعة",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickRaysButton},
                {"طوارئ", PATIENT_EMERGENCY, "تحاليل",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickTestsButton},
                {"طوارئ", PATIENT_EMERGENCY, "دخول",
                        (Consumer<PatientAdmissionPage>) PatientAdmissionPage::clickAdmissionButton},
        };
    }

    @Test(priority = 5, dataProvider = "incompatibleActiveVisitSwitches",
            description = "Incompatible visit types must show ERROR and stay on patient profile")
    public void verifyIncompatibleVisitSwitchShowsError(
            String activeVisitLabel,
            String patientCode,
            String conflictingActionLabel,
            Consumer<PatientAdmissionPage> clickConflictingAction) {

        page.openPatientProfileByCode(patientCode);
        Assert.assertEquals(page.getSelectedPatientCode(), patientCode,
                "Opened wrong patient for incompatible-visit restriction (" + activeVisitLabel + ")");
        page.dismissOverlaysAndToasts();

        String urlBefore = getDriver().getCurrentUrl();
        clickConflictingAction.accept(page);

        Assert.assertTrue(page.isSystemMessageDisplayed("error", 8),
                "Patient " + patientCode + " (" + activeVisitLabel + ") already has an active visit; "
                        + "clicking '" + conflictingActionLabel + "' must show an ERROR toast. URL="
                        + getDriver().getCurrentUrl());

        String urlAfter = getDriver().getCurrentUrl();
        boolean stayedOnProfile = urlAfter != null
                && urlAfter.contains("/reception/patient/" + patientCode)
                && !urlAfter.contains("/clinic/visits/")
                && !urlAfter.contains("/emergency/");
        Assert.assertTrue(stayedOnProfile,
                "Patient " + patientCode + " should remain on profile after blocked '"
                        + conflictingActionLabel + "'. Before=" + urlBefore + " After=" + urlAfter);
    }

    private void assertExternalModeKeepsVisitCode(
            String patientCode,
            String baselineVisitCode,
            String mode,
            Consumer<PatientAdmissionPage> clickMode) {

        page.openPatientProfileByCode(patientCode);
        page.dismissOverlaysAndToasts();
        clickMode.accept(page);
        page.waitForUrlContains("/clinic/visits/");
        page.waitForUrlContains("patientCode=" + patientCode);
        page.waitForUrlContains("mode=" + mode);

        String visitCode = page.getVisitCodeFromVisitPage();
        Assert.assertEquals(visitCode, baselineVisitCode,
                "External-visit family must keep the same كود الزيارة when opening mode="
                        + mode + " for patient " + patientCode
                        + ". URL=" + getDriver().getCurrentUrl());
    }

    private void assertActionRedirects(
            String actionLabel,
            Consumer<PatientAdmissionPage> clickAction,
            java.util.function.Function<String, String[]> expectedFragmentsFn) {

        // Fresh patient per redirect so a previous visit cannot block another type
        page.prepareIsolatedTestState();
        String patientCode = createFreshAutomationPatient();
        clickAction.accept(page);

        for (String fragment : expectedFragmentsFn.apply(patientCode)) {
            page.waitForUrlContains(fragment);
            Assert.assertTrue(getDriver().getCurrentUrl().contains(fragment),
                    "After '" + actionLabel + "', URL should contain '" + fragment
                            + "'. Actual: " + getDriver().getCurrentUrl());
        }
    }

    private String openKnownPatientAndGetCode() {
        page.openPatientProfileBySearch(AUTOMATION_PATIENT_SEARCH);
        String code = page.getSelectedPatientCode();
        Assert.assertFalse(code == null || code.isBlank(),
                "patientCode was empty after opening '" + AUTOMATION_PATIENT_SEARCH + "'");
        Assert.assertTrue(page.isTopActionBarVisible(),
                "Top action bar should be visible after opening the patient profile");
        knownPatientCode = code;
        return code;
    }

    private String ensureAutomationPatientExists() {
        try {
            page.openPatientProfileBySearch(AUTOMATION_PATIENT_SEARCH);
            String code = page.getSelectedPatientCode();
            if (code != null && !code.isBlank()) {
                return code;
            }
        } catch (Exception ignored) {
            // Create a fresh patient below
        }
        return createFreshAutomationPatient();
    }

    private String createFreshAutomationPatient() {
        page.prepareIsolatedTestState();
        String name = AUTOMATION_PATIENT_SEARCH + " "
                + ThreadLocalRandom.current().nextInt(1, 10_001)
                + (System.currentTimeMillis() % 10_000);
        long mixed = Math.abs(System.nanoTime() ^ ThreadLocalRandom.current().nextLong());
        String mobile = "010" + String.format("%08d", mixed % 100_000_000L);

        page.fillMandatoryFields(name, mobile, VALID_BIRTH_DATE, VALID_GENDER);
        page.clickSave();
        Assert.assertTrue(page.waitForSuccessfulPatientSave(),
                "Failed to seed automation patient for action-bar tests. URL="
                        + getDriver().getCurrentUrl());
        String code = page.getSelectedPatientCode();
        knownPatientCode = code;
        return code;
    }

    private void assertUnderDevSafe(By buttonLocator, String label) {
        boolean inactive = page.isActionButtonInactive(buttonLocator);
        boolean stayed = page.clickUnderDevelopmentActionStaysOnPatientProfile(buttonLocator);
        Assert.assertTrue(inactive || stayed,
                "Under-development button '" + label
                        + "' should be inactive or leave the patient profile intact. URL="
                        + getDriver().getCurrentUrl());
    }
}
