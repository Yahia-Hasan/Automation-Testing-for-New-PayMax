package com.paymax.automation.tests;

import com.paymax.automation.base.BaseTest;
import com.paymax.automation.pages.PatientAdmissionPage;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.Locale;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Comprehensive tests for the Patient Admission (Reception) form,
 * covering Egyptian business rules and complex validations.
 */
public class PatientAdmissionTests extends BaseTest {

    private static final String VALID_ENGLISH_NAME = "Automation Test Patient";
    private static final String VALID_BIRTH_DATE = "1990-05-15";
    private static final String VALID_GENDER = "ذكر";

    /** Exact option text in the إثبات الشخصية dropdown. */
    private static final String ID_TYPE_NATIONAL_ID = "رقم قومي";
    private static final String ID_TYPE_PASSPORT = "جواز سفر";
    private static final String CREDIT_COMPANY_NAME = "#@ اليكو";
    private static final String DEFAULT_CLIENT_CASH = "$$نقدي 2019";
    /** Default نوع التعاقد when the field is available / page opens. */
    private static final String CONTRACT_TYPE_MEMBER_SELF = "العضو نفسه";
    private static final String CONTRACT_TYPE_DEPENDENT = "مريض تابع";
    /** Live UI uses a slash separator (not a pipe). */
    private static final String DEFAULT_RELATIVE_SPOUSE = "الزوج/الزوجة";

    private PatientAdmissionPage page;
    /** Name created by the happy-path test — reused by the search test. */
    private String lastCreatedPatientName;
    /** Patient code after happy-path save — preferred search key (TEMPORARY until search UX is confirmed). */
    private String lastCreatedPatientCode;

    // ------------------------------------------------------------------
    // Data generators
    // ------------------------------------------------------------------

    /** Random integer in [1, 10000] used as a unique name suffix. */
    private static int randomNameSuffix() {
        return ThreadLocalRandom.current().nextInt(1, 10_001);
    }

    /**
     * Full 4-word happy-path Arabic name.
     * Format: "يحيى تيست اوتوميشن " + randomNumber (+ time fragment to avoid collisions)
     */
    private static String generateQuadrupleName() {
        return "يحيى تيست اوتوميشن " + randomNameSuffix() + System.currentTimeMillis() % 10_000;
    }

    /** Single-word name that must trigger an ERROR on Save. */
    private static String generateSingleWordName() {
        return "يحيى" + randomNameSuffix() + (System.currentTimeMillis() % 1000);
    }

    /**
     * Two-or-three-word name that should warn on Save but still succeed.
     */
    private static String generateTwoOrThreeWordName() {
        // Randomly pick a double or a triple name
        if (ThreadLocalRandom.current().nextBoolean()) {
            return "يحيى أحمد " + randomNameSuffix();
        }
        return "يحيى أحمد محمد " + randomNameSuffix();
    }

    /**
     * Unique Egyptian mobile (010 + 8 digits). Mixes nanoTime so re-runs and
     * parallel suite executions almost never collide with previously saved patients.
     */
    private static String uniqueMobile() {
        long mixed = Math.abs(System.nanoTime() ^ ThreadLocalRandom.current().nextLong());
        long suffix = mixed % 100_000_000L;
        return "010" + String.format("%08d", suffix);
    }

    /**
     * Generates a unique, structurally valid 14-digit Egyptian National ID
     * for the given birth date (century digit 2 = 1900s, 3 = 2000s).
     */
    private static String nationalIdForBirthDate(LocalDate birthDate) {
        int century = birthDate.getYear() < 2000 ? 2 : 3;
        int gov = ThreadLocalRandom.current().nextInt(1, 28);
        // Include time bits in serial so IDs are not reused across suite runs
        int serial = (int) ((System.nanoTime() + ThreadLocalRandom.current().nextInt(1000, 9999)) % 9000) + 1000;
        int check = ThreadLocalRandom.current().nextInt(1, 10);
        return String.format("%d%02d%02d%02d%02d%04d%d",
                century, birthDate.getYear() % 100,
                birthDate.getMonthValue(), birthDate.getDayOfMonth(),
                gov, serial, check);
    }

    private static String uniqueNationalId() {
        // Spread birth years so generated NIDs stay unique and realistic
        LocalDate randomBirth = LocalDate.of(
                ThreadLocalRandom.current().nextInt(1965, 2005),
                ThreadLocalRandom.current().nextInt(1, 13),
                ThreadLocalRandom.current().nextInt(1, 28));
        return nationalIdForBirthDate(randomBirth);
    }

    /** Asserts a happy-path Save via success toast/alert OR /reception/patient/{code} URL. */
    private void assertPatientSavedSuccessfully() {
        Assert.assertTrue(page.waitForSuccessfulPatientSave(),
                "Happy path save failed: expected a success toast/alert "
                        + "OR URL ending with /reception/patient/{patientCode}. "
                        + "Current URL: " + getDriver().getCurrentUrl());
    }

    /** Converts Arabic-Indic digits (٠١٢...) to ASCII digits for comparisons. */
    private static String normalizeArabicDigits(String text) {
        StringBuilder sb = new StringBuilder(text.length());
        for (char c : text.toCharArray()) {
            if (c >= '\u0660' && c <= '\u0669') {
                sb.append((char) ('0' + (c - '\u0660')));
            } else {
                sb.append(c);
            }
        }
        return sb.toString();
    }

    /**
     * Age years/months as calculated by the Paymax admission UI.
     * <p>
     * Calendar year + month difference only — does <strong>not</strong> borrow a
     * month when {@code today.day < birth.day} (unlike {@code Period.between}).
     * Example on 2026-08-05 for DOB 2000-03-10:
     * Paymax → 26y 5m; {@code Period.between} → 26y 4m.
     */
    private static int[] expectedAgeYearsAndMonths(LocalDate birthDate) {
        return expectedAgeYearsAndMonths(birthDate, LocalDate.now());
    }

    private static int[] expectedAgeYearsAndMonths(LocalDate birthDate, LocalDate today) {
        int years = today.getYear() - birthDate.getYear();
        int months = today.getMonthValue() - birthDate.getMonthValue();
        if (months < 0) {
            years--;
            months += 12;
        }
        return new int[] {years, months};
    }

    private void assertAgeMatchesBirthDate(LocalDate birthDate) {
        String actualYears = page.waitForAgeYearsPopulated();
        int[] expected = expectedAgeYearsAndMonths(birthDate);
        String expectedYears = String.valueOf(expected[0]);
        String expectedMonths = String.valueOf(expected[1]);

        page.waitForAgeMonthsValue(expectedMonths);

        Assert.assertEquals(actualYears, expectedYears,
                "Age years mismatch for DOB " + birthDate
                        + " (UI date field=" + page.getBirthDateValue() + ")");
        Assert.assertEquals(page.getAgeMonthsValue(), expectedMonths,
                "Age months mismatch for DOB " + birthDate
                        + " (UI date field=" + page.getBirthDateValue()
                        + "). Paymax uses calendar month diff without day borrow.");
    }

    // ------------------------------------------------------------------
    // Lifecycle: one login + one navigation, refresh between tests
    // ------------------------------------------------------------------

    @BeforeClass(alwaysRun = true)
    public void loginAndOpenAdmissionPageOnce() {
        loginAndNavigateToNewSystem();
        page = new PatientAdmissionPage(getDriver()).navigateToReception();
    }

    /**
     * Isolates every test: hard-reload exact /reception + click جديد so the
     * form starts clean regardless of what the previous test left behind.
     */
    @BeforeMethod(alwaysRun = true)
    public void resetAdmissionPageBeforeTest() {
        page.prepareIsolatedTestState();
    }

    /**
     * Safety net after each test (pass/fail/error): close modal / dropdowns /
     * toasts so they cannot block the next hard-reload.
     */
    @AfterMethod(alwaysRun = true)
    public void cleanupAdmissionUiAfterTest() {
        try {
            page.dismissOverlaysAndToasts();
        } catch (Exception e) {
            // Never fail the suite from cleanup
        }
    }

    // ------------------------------------------------------------------
    // 0. Happy path (also seeds data for the search test)
    // ------------------------------------------------------------------

    @Test(priority = 1, description = "Happy path: create a patient with a unique 4-word Arabic name")
    public void createPatientWithMandatoryFields() {
        lastCreatedPatientName = generateQuadrupleName();

        page.fillMandatoryFields(lastCreatedPatientName, uniqueMobile(), VALID_BIRTH_DATE, VALID_GENDER)
                .enterEnglishName(VALID_ENGLISH_NAME + " " + randomNameSuffix())
                .enterNationalId(uniqueNationalId());

        page.clickSave();
        assertPatientSavedSuccessfully();

        lastCreatedPatientCode = page.getPatientCodeValue();
    }

    @Test(priority = 2, description = "Negative: missing Arabic name must show an error message")
    public void savingWithoutMandatoryFieldsShowsValidation() {
        page.enterEnglishName(VALID_ENGLISH_NAME)
                .enterNationalId(uniqueNationalId())
                .setBirthDate(VALID_BIRTH_DATE)
                .selectGender(VALID_GENDER);

        page.clickSave();

        boolean isErrorVisible = page.isSystemMessageDisplayed("error");
        Assert.assertTrue(isErrorVisible, "Negative test failed: Error message was not displayed!");
        Assert.assertTrue(page.isOnReceptionPage(),
                "Should remain on the reception page when validation fails");
    }

    // ------------------------------------------------------------------
    // 1. Mobile number validations
    // ------------------------------------------------------------------

    @Test(priority = 3, description = "Mobile field must completely reject alphabetic input")
    public void mobileFieldRejectsAlphabeticCharacters() {
        page.enterMobile("abcXYZ!@#");

        Assert.assertEquals(page.getMobileValue(), "",
                "Mobile field must stay empty when alphabetic characters are typed");
    }

    @Test(priority = 4, description = "Invalid Egyptian mobile (short / wrong prefix) must block save")
    public void invalidEgyptianMobileIsRejectedOnSave() {
        // 016 is not a valid Egyptian prefix and the number is short
        page.fillMandatoryFields(generateQuadrupleName(), "0161234", VALID_BIRTH_DATE, VALID_GENDER);

        page.clickSave();

        boolean isErrorVisible = page.isSystemMessageDisplayed("error");
        Assert.assertTrue(isErrorVisible, "Negative test failed: Error message was not displayed!");
        Assert.assertTrue(page.isOnReceptionPage(),
                "Save must be blocked for an invalid mobile number");
    }

    // ------------------------------------------------------------------
    // 2. National ID validation + age auto-calculation
    // ------------------------------------------------------------------

    @Test(priority = 5, description = "Invalid National ID pattern must show a validation error on save")
    public void invalidNationalIdIsRejectedOnSave() {
        page.selectIdType(ID_TYPE_NATIONAL_ID);
        page.fillMandatoryFields(generateQuadrupleName(), uniqueMobile(), VALID_BIRTH_DATE, VALID_GENDER)
                .enterNationalId("12345"); // wrong length / pattern

        page.clickSave();

        boolean isErrorVisible = page.isSystemMessageDisplayed("error");
        Assert.assertTrue(isErrorVisible, "Negative test failed: Error message was not displayed!");
        Assert.assertTrue(page.isOnReceptionPage(),
                "Save must be blocked for an invalid National ID");
    }

    @Test(priority = 6, description = "Valid National ID must auto-populate age years/months")
    public void validNationalIdAutoCalculatesAge() {
        LocalDate birthDate = LocalDate.of(1990, 1, 1);
        String nationalId = nationalIdForBirthDate(birthDate);

        page.selectIdType(ID_TYPE_NATIONAL_ID);
        page.enterNationalId(nationalId);

        assertAgeMatchesBirthDate(birthDate);
    }

    // ------------------------------------------------------------------
    // 3. Date of birth validations
    // ------------------------------------------------------------------

    @Test(priority = 7, description = "Future dates must be blocked by the birth-date picker (max=today)")
    public void futureBirthDatesAreDisabled() {
        String maxAttribute = page.getBirthDateMaxAttribute();
        String today = LocalDate.now().format(DateTimeFormatter.ISO_LOCAL_DATE);

        Assert.assertEquals(maxAttribute, today,
                "Birth-date input must cap selectable dates at today (max attribute)");
    }

    @Test(priority = 8, description = "Picking a birth date manually must recalculate age fields")
    public void manualBirthDateRecalculatesAge() {
        // ISO 2000-03-10 — UI may show 10/03/2000 (day/month), not October 3
        LocalDate birthDate = LocalDate.of(2000, 3, 10);
        page.setBirthDate(birthDate.format(DateTimeFormatter.ISO_LOCAL_DATE));

        assertAgeMatchesBirthDate(birthDate);
    }

    // ------------------------------------------------------------------
    // 4. Conditional credit contract validation (جهة آجل)
    // ------------------------------------------------------------------

    @Test(priority = 9, description = "Credit company (#@ اليكو) makes insurance number + expiry mandatory")
    public void creditCompanyRequiresInsuranceNumberAndExpiry() {
        page.fillMandatoryFields(generateQuadrupleName(), uniqueMobile(), VALID_BIRTH_DATE, VALID_GENDER);
        page.selectClient(CREDIT_COMPANY_NAME);

        // Intentionally leave insurance number + expiration date empty
        page.clickSave();

        boolean isErrorVisible = page.isSystemMessageDisplayed("error");
        Assert.assertTrue(isErrorVisible, "Negative test failed: Error message was not displayed!");
        Assert.assertTrue(page.isOnReceptionPage(),
                "Save must be blocked while insurance number and expiry date are missing");
    }

    // ------------------------------------------------------------------
    // 5. 'New' button reset
    // ------------------------------------------------------------------

    @Test(priority = 10, description = "New (جديد) must clear all inputs and reset dropdowns to -- اختر --")
    public void newButtonClearsInputsAndDropdowns() {
        page.enterArabicName(generateQuadrupleName())
                .enterEnglishName(VALID_ENGLISH_NAME)
                .enterMobile(uniqueMobile())
                .enterNationalId(uniqueNationalId())
                .setBirthDate(VALID_BIRTH_DATE)
                .selectGender(VALID_GENDER);

        page.clickNew();
        page.waitUntilLoaded();

        Assert.assertEquals(page.getArabicNameValue(), "", "Arabic name should be cleared");
        Assert.assertEquals(page.getEnglishNameValue(), "", "English name should be cleared");
        Assert.assertEquals(page.getMobileValue(), "", "Mobile should be cleared");
        Assert.assertEquals(page.getNationalIdValue(), "", "National ID should be cleared");
        Assert.assertEquals(page.getBirthDateValue(), "", "Birth date should be cleared");
        Assert.assertEquals(page.getGenderSelectedText(), "",
                "Gender dropdown should reset to its placeholder (-- اختر --)");
    }

    // ------------------------------------------------------------------
    // 6. Global search
    // ------------------------------------------------------------------

    @Test(priority = 11, description = "TEMPORARY: search by patient code then click the single dropdown result")
    public void searchPopulatesExistingPatientData() {
        Assert.assertNotNull(lastCreatedPatientName,
                "Happy-path test must run first to create a searchable patient");

        // TEMPORARY: search UX is unclear — ENTER does nothing; a one-item dropdown
        // appears and must be clicked. Prefer patient code when available.
        String searchKey = (lastCreatedPatientCode != null && !lastCreatedPatientCode.isBlank())
                ? lastCreatedPatientCode
                : lastCreatedPatientName;

        page.searchForPatientAndSubmit(searchKey);

        Assert.assertTrue(page.waitForFormPopulated(),
                "Form must auto-populate after selecting the search result");
        Assert.assertTrue(page.getArabicNameValue().contains(lastCreatedPatientName),
                "Arabic name field must contain the searched patient name, but was: "
                        + page.getArabicNameValue());
    }

    // ------------------------------------------------------------------
    // 7. Read-only fields + header date
    // ------------------------------------------------------------------

    @Test(priority = 12, description = "Created-by and created-date fields must be read-only")
    public void createdByAndCreatedDateAreReadOnly() {
        Assert.assertTrue(page.isAddedByReadonly(),
                "'اضافة بواسطة' must be readonly/disabled");
        Assert.assertTrue(page.isAddedDateReadonly(),
                "'تاريخ الإضافة' must be readonly/disabled");
    }

    @Test(priority = 13, description = "Header date must match the actual current local date")
    public void headerDateMatchesCurrentDate() {
        String headerDate = normalizeArabicDigits(page.getHeaderDateText());
        LocalDate today = LocalDate.now();

        String expectedMonthArabic = today.format(
                DateTimeFormatter.ofPattern("MMMM", new Locale("ar")));

        Assert.assertTrue(headerDate.contains(String.valueOf(today.getDayOfMonth())),
                "Header date must contain today's day of month. Header was: " + headerDate);
        Assert.assertTrue(headerDate.contains(String.valueOf(today.getYear())),
                "Header date must contain the current year. Header was: " + headerDate);
        Assert.assertTrue(headerDate.contains(expectedMonthArabic),
                "Header date must contain the current Arabic month name ('"
                        + expectedMonthArabic + "'). Header was: " + headerDate);
    }

    // ------------------------------------------------------------------
    // 8 / 9 / 10. Patient Arabic-name word-count validations
    // ------------------------------------------------------------------

    @Test(priority = 14, description = "TC8: Single-word Arabic name must show ERROR on Save")
    public void singleWordNameShowsErrorOnSave() {
        String singleWordName = generateSingleWordName();

        page.fillMandatoryFields(singleWordName, uniqueMobile(), VALID_BIRTH_DATE, VALID_GENDER)
                .enterEnglishName(VALID_ENGLISH_NAME)
                .enterNationalId(uniqueNationalId());

        page.clickSave();

        boolean isErrorVisible = page.isSystemMessageDisplayed("error");
        Assert.assertTrue(isErrorVisible, "Negative test failed: Error message was not displayed!");
    }

    @Test(priority = 15, description = "TC9: Two/three-word Arabic name shows WARNING + SUCCESS on Save")
    public void twoOrThreeWordNameShowsWarningOnBlur() {
        // Let toasts from earlier tests fully disappear first
        page.waitForPreviousToastsToClear();

        // Explicit unique 2-word name — system allows save but should warn
        String shortName = "يحيى حسن " + randomNameSuffix() + (System.currentTimeMillis() % 1000);

        page.fillMandatoryFields(shortName, uniqueMobile(), VALID_BIRTH_DATE, VALID_GENDER)
                .enterEnglishName(VALID_ENGLISH_NAME + " " + randomNameSuffix())
                .enterNationalId(uniqueNationalId());

        // Arm + click + poll inside one flow so a fast warning toast cannot be missed
        boolean[] signals = page.clickSaveAndObserveWarningAndSuccess(12);
        boolean warningSeen = signals[0];
        boolean savedOk = signals[1];

        Assert.assertTrue(warningSeen,
                "Expected a WARNING toast/alert after saving a 2/3-word Arabic name");
        Assert.assertTrue(savedOk,
                "Expected SUCCESS toast/alert OR /reception/patient/{code} "
                        + "because a 2/3-word name is still allowed to save. URL: "
                        + getDriver().getCurrentUrl());
    }

    @Test(priority = 16, description = "TC10: Four-word Arabic name is accepted — success toast/alert or patient URL")
    public void quadrupleNameHappyPathShowsSuccessOnly() {
        // Let toasts from earlier tests fully disappear first
        page.waitForPreviousToastsToClear();

        String fullName = generateQuadrupleName();

        page.fillMandatoryFields(fullName, uniqueMobile(), VALID_BIRTH_DATE, VALID_GENDER)
                .enterEnglishName(VALID_ENGLISH_NAME + " " + randomNameSuffix())
                .enterNationalId(uniqueNationalId());

        page.clickSave();
        assertPatientSavedSuccessfully();
    }

    // ------------------------------------------------------------------
    // Full coverage scenarios
    // ------------------------------------------------------------------

    @Test(priority = 17, description = "Full happy path: fill all mandatory + optional fields and save")
    public void fullHappyPathAllFieldsFilled() {
        page.waitForPreviousToastsToClear();

        String arabicName = generateQuadrupleName();
        String mobile = uniqueMobile();
        String nationalId = uniqueNationalId();
        String expiry = LocalDate.now().plusYears(1).format(DateTimeFormatter.ISO_LOCAL_DATE);

        page.fillAllAvailableFields(
                arabicName,
                VALID_ENGLISH_NAME + " " + randomNameSuffix(),
                mobile,
                nationalId,
                VALID_BIRTH_DATE,
                VALID_GENDER,
                "شارع الاختبار رقم " + randomNameSuffix() + System.currentTimeMillis() % 1000,
                "auto" + System.nanoTime() + "@test.com",
                "ملاحظات اوتوميشن " + randomNameSuffix(),
                "INS-" + System.nanoTime(),
                expiry);

        page.clickSave();
        assertPatientSavedSuccessfully();
    }

    @Test(priority = 18, description = "Full form reset: New (جديد) clears all filled inputs and dropdowns")
    public void fullFormResetViaNewButton() {
        String expiry = LocalDate.now().plusYears(1).format(DateTimeFormatter.ISO_LOCAL_DATE);

        page.fillAllAvailableFields(
                generateQuadrupleName(),
                VALID_ENGLISH_NAME,
                uniqueMobile(),
                uniqueNationalId(),
                VALID_BIRTH_DATE,
                VALID_GENDER,
                "عنوان تجريبي",
                "reset@test.com",
                "ملاحظات مؤقتة",
                "INS-RESET",
                expiry);

        page.clickNew();
        page.waitUntilLoaded();

        Assert.assertEquals(page.getArabicNameValue(), "", "Arabic name should be cleared");
        Assert.assertEquals(page.getEnglishNameValue(), "", "English name should be cleared");
        Assert.assertEquals(page.getMobileValue(), "", "Mobile should be cleared");
        Assert.assertEquals(page.getOtherPhoneValue(), "", "Other phone should be cleared");
        Assert.assertEquals(page.getWhatsappValue(), "", "WhatsApp should be cleared");
        Assert.assertEquals(page.getNationalIdValue(), "", "National ID should be cleared");
        Assert.assertEquals(page.getBirthDateValue(), "", "Birth date should be cleared");
        Assert.assertEquals(page.getAddressValue(), "", "Address should be cleared");
        Assert.assertEquals(page.getEmailValue(), "", "Email should be cleared");
        Assert.assertEquals(page.getNotesValue(), "", "Notes should be cleared");
        Assert.assertTrue(page.isGenderAtPlaceholder(),
                "Gender dropdown should reset to -- اختر --");
        Assert.assertTrue(page.isReligionAtPlaceholder(),
                "Religion dropdown should reset to -- اختر --");
        Assert.assertTrue(page.isMaritalStatusAtPlaceholder(),
                "Marital status dropdown should reset to -- اختر --");
        Assert.assertTrue(page.isJobAtPlaceholder(),
                "Job dropdown should reset to -- اختر --");
    }

    @Test(priority = 19, description = "Age years auto-calculate to 10 when DOB is exactly 10 years ago")
    public void ageAutoCalculatesFromDateOfBirthTenYearsAgo() {
        LocalDate tenYearsAgo = LocalDate.now().minusYears(10);
        page.setBirthDate(tenYearsAgo.format(DateTimeFormatter.ISO_LOCAL_DATE));

        String actualYears = page.waitForAgeYearsPopulated();
        Assert.assertEquals(actualYears, "10",
                "Years field must auto-update to 10 for a DOB exactly 10 years ago");
    }

    @Test(priority = 20, description = "Credit company (#@ اليكو) requires insurance number + expiry on Save")
    public void creditCompanyMandatoryFieldsShowErrorWhenEmpty() {
        page.waitForPreviousToastsToClear();

        page.fillMandatoryFields(generateQuadrupleName(), uniqueMobile(), VALID_BIRTH_DATE, VALID_GENDER);
        page.selectClient(CREDIT_COMPANY_NAME);
        // Intentionally leave Insurance Number and Expiry Date blank

        page.clickSave();

        boolean isErrorVisible = page.isSystemMessageDisplayed("error");
        Assert.assertTrue(isErrorVisible, "Negative test failed: Error message was not displayed!");
    }

    @Test(priority = 21, description = "Created-by and created-date are readonly and reject typing")
    public void readOnlyFieldsRejectModification() {
        Assert.assertTrue(page.isAddedByReadonly(),
                "'اضافة بواسطة' must expose readonly/disabled attribute");
        Assert.assertTrue(page.isAddedDateReadonly(),
                "'تاريخ الإضافة' must expose readonly/disabled attribute");

        Assert.assertTrue(page.tryTypeIntoAddedBy("HACKED USER"),
                "'اضافة بواسطة' must not accept typed changes");
        Assert.assertTrue(page.tryTypeIntoAddedDate("01/01/1999"),
                "'تاريخ الإضافة' must not accept typed changes");
    }

    // ------------------------------------------------------------------
    // Unknown patient (مريض غير معروف) modal
    // ------------------------------------------------------------------

    @Test(priority = 22, description = "Unknown patient modal: auto-generated code is read-only")
    public void unknownPatientCodeIsReadOnly() {
        page.openUnknownPatientModal();

        Assert.assertTrue(page.isUnknownPatientCodeInputDisplayed(),
                "'كود المريض' input must be visible inside the unknown-patient modal");
        Assert.assertTrue(page.isUnknownPatientCodeInputNotEditable(),
                "'كود المريض' must be readonly or disabled — it is generated by the system. "
                        + "Current value: " + page.getUnknownPatientCodeValue());
    }

    @Test(priority = 23, description = "Unknown patient modal: happy path save shows a success message")
    public void saveUnknownPatientHappyPath() {
        page.waitForPreviousToastsToClear();
        page.openUnknownPatientModal();

        String visitDate = LocalDate.now().format(DateTimeFormatter.ISO_LOCAL_DATE);
        String visitTime = LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm"));

        page.fillUnknownPatientForm(VALID_GENDER, visitDate, visitTime,
                "مريض غير معروف - اوتوميشن " + randomNameSuffix());

        page.clickSaveUnknownPatient();

        Assert.assertTrue(page.isSystemMessageDisplayed("success"),
                "Saving an unknown patient should show a SUCCESS message");
    }

    @Test(priority = 24, description = "Unknown patient modal: X button closes the modal")
    public void closeUnknownPatientModal() {
        page.openUnknownPatientModal();
        Assert.assertTrue(page.isUnknownPatientModalDisplayed(),
                "Modal must be visible before closing it");

        page.closeUnknownPatientModal();

        Assert.assertFalse(page.isUnknownPatientModalDisplayed(),
                "Modal must disappear after clicking the close (X) button");
    }

    // ------------------------------------------------------------------
    // Dynamic UI / conditional contract logic
    // ------------------------------------------------------------------

    @Test(priority = 25, description = "الجهة defaults to $$نقدي 2019 on a fresh admission page")
    public void defaultClientDropdownValueIsCash2019() {
        // clickNew() clears defaults — reload the blank page to read the real default
        page.reloadAndWaitForDefaultClient(DEFAULT_CLIENT_CASH);

        Assert.assertEquals(page.getClientSelectedText(), DEFAULT_CLIENT_CASH,
                "Default selected الجهة must be $$نقدي 2019");
    }

    @Test(priority = 26, description = "إثبات الشخصية updates the adjacent identity-number field label")
    public void identityTypeUpdatesAdjacentFieldLabel() {
        page.selectIdTypeAndWaitForLabel(ID_TYPE_PASSPORT, ID_TYPE_PASSPORT);

        Assert.assertEquals(page.getIdNumberFieldLabelText(), ID_TYPE_PASSPORT,
                "Identity-number field label must update to match the selected إثبات الشخصية");
    }

    @Test(priority = 27,
            description = "نوع التعاقد defaults to العضو نفسه; DDL offers العضو نفسه/مريض تابع; "
                    + "مريض تابع defaults درجة القرابة to الزوج/الزوجة")
    public void cascadingContractAndDependentPatientRules() {
        // Credit جهة unlocks contract cascading (cash keeps نوع التعاقد disabled)
        page.selectClient(CREDIT_COMPANY_NAME);
        page.selectFirstInsCompanyOption();

        page.waitUntilContractTypeEnabled();
        Assert.assertTrue(page.isContractTypeEnabled(),
                "نوع التعاقد must become enabled after selecting جهة + شركة فرعية");

        Assert.assertEquals(page.getContractTypeSelectedText(), CONTRACT_TYPE_MEMBER_SELF,
                "نوع التعاقد default selection must be العضو نفسه");

        java.util.List<String> contractOptions = page.getContractTypeOptionTexts();
        Assert.assertTrue(contractOptions.contains(CONTRACT_TYPE_MEMBER_SELF),
                "نوع التعاقد DDL must include العضو نفسه. Options=" + contractOptions);
        Assert.assertTrue(contractOptions.contains(CONTRACT_TYPE_DEPENDENT),
                "نوع التعاقد DDL must include مريض تابع. Options=" + contractOptions);
        Assert.assertEquals(contractOptions.size(), 2,
                "نوع التعاقد DDL must offer exactly two choices after جهة آجل. Options="
                        + contractOptions);

        // Default stays العضو نفسه — درجة القرابة should not be required/enabled yet
        Assert.assertFalse(page.isRelativeDegreeEnabled(),
                "درجة القرابة must stay disabled while نوع التعاقد is العضو نفسه");

        page.selectContractType(CONTRACT_TYPE_DEPENDENT);

        page.waitUntilRelativeDegreeEnabled();
        Assert.assertTrue(page.isRelativeDegreeDisplayed(),
                "درجة القرابة must be visible after selecting مريض تابع");
        Assert.assertTrue(page.isRelativeDegreeEnabled(),
                "درجة القرابة must become enabled after selecting مريض تابع");

        String relative = page.getRelativeDegreeDefaultValue();
        Assert.assertEquals(relative, DEFAULT_RELATIVE_SPOUSE,
                "درجة القرابة default must be الزوج/الزوجة after selecting مريض تابع");

        Assert.assertTrue(page.isRelativeDegreeInputReadOnly(),
                "درجة القرابة combobox must be read-only (no free typing / searching)");
    }
}
