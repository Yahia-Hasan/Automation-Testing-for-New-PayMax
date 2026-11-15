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

/**
 * Page Object for the Patient Admission (Reception) page:
 * https://196.218.246.250:4040/reception
 * <p>
 * All form locators rely strictly on data-test-id attributes via CSS selectors.
 */
public class PatientAdmissionPage extends BasePage {

    private static final Logger LOGGER = LogManager.getLogger(PatientAdmissionPage.class);

    private static final By SAVE_BUTTON =
            By.cssSelector("[data-test-id='patient-data-save-btn']");
    private static final By NEW_BUTTON =
            By.cssSelector("[data-test-id='patient-data-new-btn']");
    private static final By RECEPTION_NAV_LINK = By.cssSelector("a[href='/reception']");
    private static final By RECEPTION_NAV_GROUP = By.xpath(
            "//a[@href='/reception']/ancestor::div[contains(@class,'nav-dropdown')]/button");
    private static final By HEADER_DATE = By.cssSelector(".navbar-date span");
    /** Stable locator from frontend: data-test-id on the global toaster stack. */
    private static final By TOAST_STACK =
            By.cssSelector("[data-test-id='global-toast-stack']");
    /** Fallback if the data-test-id is missing on an older build. */
    private static final By TOAST_STACK_FALLBACK =
            By.cssSelector("app-global-toaster .toast-stack");

    // ---------- Unknown patient modal ----------
    private static final By UNKNOWN_PATIENT_OPEN_BUTTON =
            By.cssSelector("[data-test-id='patient-data-unknown-patient-btn']");
    private static final By UNKNOWN_PATIENT_MODAL =
            By.cssSelector("[data-test-id='patient-data-unknown-modal']");
    private static final By UNKNOWN_PATIENT_CLOSE_BUTTON =
            By.cssSelector("[data-test-id='patient-data-unknown-modal-close-btn']");
    private static final By UNKNOWN_PATIENT_CODE_INPUT =
            By.cssSelector("[data-test-id='patient-data-unknown-code-input']");
    private static final By UNKNOWN_PATIENT_SAVE_BUTTON =
            By.cssSelector("[data-test-id='patient-data-save-unknown-btn']");

    // ---------- Reservation Agenda Modal ----------
    private static final By RESERVATION_AGENDA_BTN =
            By.cssSelector("[data-test-id='patient-data-reservation-agenda-btn']");
    private static final By RESERVATION_MODAL_BACKDROP =
            By.cssSelector("[data-test-id='patient-data-reservation-modal-backdrop']");
    private static final By RESERVATION_MODAL =
            By.cssSelector("[data-test-id='patient-data-reservation-modal']");
    private static final By RESERVATION_CLOSE_BTN =
            By.cssSelector("[data-test-id='patient-data-reservation-modal-close-btn']");
    private static final By RESERVATION_FROM_DATE_INPUT =
            By.cssSelector("[data-test-id='patient-data-reservation-modal'] .reservation-filters div.fg:nth-child(1) input[type='date']");
    private static final By RESERVATION_TO_DATE_INPUT =
            By.cssSelector("[data-test-id='patient-data-reservation-modal'] .reservation-filters div.fg:nth-child(2) input[type='date']");
    private static final By RESERVATION_SHOW_BTN =
            By.cssSelector("[data-test-id='patient-data-reservation-show-btn']");
    private static final By RESERVATION_TABLE_ROWS =
            By.cssSelector("[data-test-id='patient-data-reservation-modal'] table.tbl tbody tr");


    // ---------- Search ----------
    @FindBy(css = "[data-test-id='patient-data-search-input']")
    private WebElement searchInput;

    // ---------- Mandatory fields ----------
    @FindBy(css = "[data-test-id='patient-data-patient-name-input']")
    private WebElement arabicNameInput;

    @FindBy(css = "[data-test-id='patient-data-mobile-phone-input']")
    private WebElement mobileInput;

    @FindBy(css = "[data-test-id='patient-data-birth-date-input']")
    private WebElement birthDateInput;

    @FindBy(css = "[data-test-id='patient-data-gender-select']")
    private WebElement genderSelect;

    // ---------- Other key fields ----------
    @FindBy(css = "[data-test-id='patient-data-patient-name-en-input']")
    private WebElement englishNameInput;

    @FindBy(css = "[data-test-id='patient-data-home-phone-input']")
    private WebElement otherPhoneInput;

    @FindBy(css = "[data-test-id='patient-data-whatsapp-input']")
    private WebElement whatsappInput;

    @FindBy(css = "[data-test-id='patient-data-id-type-select']")
    private WebElement idTypeSelect;

    @FindBy(css = "[data-test-id='patient-data-id-number-input']")
    private WebElement nationalIdInput;

    @FindBy(css = "[data-test-id='patient-data-age-years-input']")
    private WebElement ageYearsInput;

    @FindBy(css = "[data-test-id='patient-data-age-months-input']")
    private WebElement ageMonthsInput;

    @FindBy(css = "[data-test-id='patient-data-religion-select']")
    private WebElement religionSelect;

    @FindBy(css = "[data-test-id='patient-data-marital-status-select']")
    private WebElement maritalStatusSelect;

    @FindBy(css = "[data-test-id='patient-data-address-input']")
    private WebElement addressInput;

    @FindBy(css = "[data-test-id='patient-data-email-input']")
    private WebElement emailInput;

    @FindBy(css = "[data-test-id='patient-data-job-select']")
    private WebElement jobSelect;

    @FindBy(css = "[data-test-id='patient-data-notes-textarea']")
    private WebElement notesTextarea;

    @FindBy(css = "[data-test-id='patient-data-client-select']")
    private WebElement clientSelect;

    @FindBy(css = "[data-test-id='patient-data-ins-company-select']")
    private WebElement insCompanySelect;

    @FindBy(css = "[data-test-id='patient-data-patient-type-select']")
    private WebElement contractTypeSelect;

    @FindBy(css = "[data-test-id='patient-data-patient-relative-select']")
    private WebElement relativeDegreeSelect;

    @FindBy(css = "[data-test-id='patient-data-medical-number-input']")
    private WebElement insuranceNumberInput;

    @FindBy(css = "[data-test-id='patient-data-expiration-date-input']")
    private WebElement expirationDateInput;

    // ---------- Read-only fields ----------
    @FindBy(css = "[data-test-id='patient-data-added-by-input']")
    private WebElement addedByInput;

    @FindBy(css = "[data-test-id='patient-data-added-date-input']")
    private WebElement addedDateInput;

    // ---------- Unknown patient (مريض غير معروف) modal ----------
    @FindBy(css = "[data-test-id='patient-data-unknown-patient-btn']")
    private WebElement unknownPatientOpenButton;

    @FindBy(css = "[data-test-id='patient-data-unknown-modal']")
    private WebElement unknownPatientModal;

    @FindBy(css = "[data-test-id='patient-data-unknown-modal-close-btn']")
    private WebElement unknownPatientCloseButton;

    @FindBy(css = "[data-test-id='patient-data-unknown-code-input']")
    private WebElement unknownPatientCodeInput;

    @FindBy(css = "[data-test-id='patient-data-unknown-gender-male-radio']")
    private WebElement unknownPatientMaleRadio;

    @FindBy(css = "[data-test-id='patient-data-unknown-gender-female-radio']")
    private WebElement unknownPatientFemaleRadio;

    @FindBy(css = "[data-test-id='patient-data-unknown-visit-date-input']")
    private WebElement unknownPatientVisitDateInput;

    @FindBy(css = "[data-test-id='patient-data-unknown-visit-time-input']")
    private WebElement unknownPatientVisitTimeInput;

    @FindBy(css = "[data-test-id='patient-data-unknown-notes-textarea']")
    private WebElement unknownPatientNotesTextarea;

    @FindBy(css = "[data-test-id='patient-data-save-unknown-btn']")
    private WebElement unknownPatientSaveButton;

    // ---------- Top action bar (visible once a patient is selected/created) ----------
    private static final By ADMISSION_BTN =
            By.cssSelector("[data-test-id='patient-data-admission-btn']");
    private static final By CATHETER_BTN =
            By.cssSelector("[data-test-id='patient-data-catheter-btn']");
    private static final By OPD_BTN =
            By.cssSelector("[data-test-id='patient-data-opd-btn']");
    private static final By RAYS_BTN =
            By.cssSelector("[data-test-id='patient-data-rays-btn']");
    private static final By TESTS_BTN =
            By.cssSelector("[data-test-id='patient-data-tests-btn']");
    private static final By ENDOSCOPY_BTN =
            By.cssSelector("[data-test-id='patient-data-endoscopy-btn']");
    private static final By EMERGENCY_BTN =
            By.cssSelector("[data-test-id='patient-data-emergency-btn']");
    private static final By DIALYSIS_BTN =
            By.cssSelector("[data-test-id='patient-data-dialysis-btn']");
    private static final By ARCHIVE_BTN =
            By.cssSelector("[data-test-id='patient-data-archive-btn']");
    private static final By PRINT_BARCODE_BTN =
            By.cssSelector("[data-test-id='patient-data-print-barcode-btn']");
    private static final By PATIENT_CODE_INPUT =
            By.cssSelector("[data-test-id='patient-data-patient-code-input']");

    @FindBy(css = "[data-test-id='patient-data-admission-btn']")
    private WebElement admissionButton;

    @FindBy(css = "[data-test-id='patient-data-catheter-btn']")
    private WebElement catheterButton;

    @FindBy(css = "[data-test-id='patient-data-opd-btn']")
    private WebElement opdButton;

    @FindBy(css = "[data-test-id='patient-data-rays-btn']")
    private WebElement raysButton;

    @FindBy(css = "[data-test-id='patient-data-tests-btn']")
    private WebElement testsButton;

    @FindBy(css = "[data-test-id='patient-data-endoscopy-btn']")
    private WebElement endoscopyButton;

    @FindBy(css = "[data-test-id='patient-data-emergency-btn']")
    private WebElement emergencyButton;

    @FindBy(css = "[data-test-id='patient-data-dialysis-btn']")
    private WebElement dialysisButton;

    @FindBy(css = "[data-test-id='patient-data-archive-btn']")
    private WebElement archiveButton;

    @FindBy(css = "[data-test-id='patient-data-print-barcode-btn']")
    private WebElement printBarcodeButton;

    public PatientAdmissionPage(WebDriver driver) {
        super(driver);
    }

    // =========================================================
    // Navigation
    // =========================================================

    /**
     * Opens the reception page via the navbar ("الملف الطبى"). Prefer
     * {@link #reloadReceptionFresh()} between tests — it is faster and does not
     * leave the nav dropdown open over the form toolbar.
     */
    public PatientAdmissionPage navigateToReception() {
        String receptionUrl = getReceptionUrl();
        try {
            WebElement group = wait.until(
                    ExpectedConditions.presenceOfElementLocated(RECEPTION_NAV_GROUP));
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", group);

            WebElement link = wait.until(
                    ExpectedConditions.presenceOfElementLocated(RECEPTION_NAV_LINK));
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", link);
            LOGGER.info("Opened مكتب الدخول and JS-clicked الملف الطبى immediately");
        } catch (Exception e) {
            LOGGER.warn("Nav link not found ({}); opening reception directly: {}",
                    e.getMessage(), receptionUrl);
            driver.get(receptionUrl);
        }

        wait.until(d -> isExactReceptionUrl(d.getCurrentUrl()));
        waitUntilLoaded();
        collapseOpenNavDropdowns();
        return this;
    }

    /**
     * Hard-reloads exact {@code /reception} (not /reception/patient/{code}).
     * Fastest reliable way to start each test as if the user just entered the page.
     */
    public PatientAdmissionPage reloadReceptionFresh() {
        String receptionUrl = getReceptionUrl();
        LOGGER.info("Hard-reloading reception page: {}", receptionUrl);
        dismissOverlaysAndToasts();
        String currentUrl = driver.getCurrentUrl();
        if (currentUrl != null && currentUrl.contains("/clinic/visits/")) {
            try {
                WebElement link = driver.findElement(By.xpath("//a[@href='/reception']"));
                ((JavascriptExecutor) driver).executeScript("arguments[0].click();", link);
            } catch (Exception e) {
                driver.get(receptionUrl);
            }
        } else {
            driver.get(receptionUrl);
        }
        wait.until(d -> isExactReceptionUrl(d.getCurrentUrl()));
        waitUntilLoaded();
        collapseOpenNavDropdowns();
        return this;
    }

    /** Waits until the admission form is rendered with retry and overlay dismissal. */
    public PatientAdmissionPage waitUntilLoaded() {
        By searchInput = By.cssSelector("[data-test-id='patient-data-search-input']");
        By nameInput = By.cssSelector("[data-test-id='patient-data-patient-name-input']");

        for (int attempt = 1; attempt <= 2; attempt++) {
            try {
                WebDriverWait shortWait = new WebDriverWait(driver, Duration.ofSeconds(6));
                shortWait.until(ExpectedConditions.visibilityOfElementLocated(searchInput));
                shortWait.until(ExpectedConditions.visibilityOfElementLocated(nameInput));
                return this;
            } catch (TimeoutException te) {
                LOGGER.warn("waitUntilLoaded attempt {} timed out waiting for search/name input; attempting recovery...", attempt);
                dismissOverlaysAndToasts();
                if (attempt == 1) {
                    try {
                        driver.navigate().refresh();
                    } catch (Exception e) {
                        driver.get(getReceptionUrl());
                    }
                }
            }
        }
        wait.until(ExpectedConditions.visibilityOfElementLocated(searchInput));
        wait.until(ExpectedConditions.visibilityOfElementLocated(nameInput));
        return this;
    }

    /**
     * Full isolation between tests while keeping the same authenticated browser:
     * <ol>
     *   <li>force-close modals / dropdowns / leftover toasts</li>
     *   <li>hard-reload exact {@code /reception}</li>
     *   <li>click جديد so every field is blank</li>
     * </ol>
     * Intentionally uses {@link #reloadReceptionFresh()} (not navbar clicks) so
     * prior patient URLs, open dropdowns, and modal backdrops cannot leak.
     */
    public PatientAdmissionPage prepareIsolatedTestState() {
        dismissOverlaysAndToasts();

        int attempts = 0;
        RuntimeException lastError = null;
        while (attempts < 2) {
            attempts++;
            try {
                reloadReceptionFresh();
                collapseOpenNavDropdowns();
                closeUnknownPatientModalIfOpen();
                closeReservationModalIfOpen();
                clickNew();
                wait.until(d -> getArabicNameValue().isEmpty() && getMobileValue().isEmpty());
                LOGGER.info("Isolated clean reception form ready (attempt {})", attempts);
                return this;
            } catch (RuntimeException e) {
                lastError = e;
                LOGGER.warn("Failed to prepare isolated state on attempt {}: {}",
                        attempts, e.getMessage());
                dismissOverlaysAndToasts();
            }
        }
        throw lastError != null
                ? lastError
                : new IllegalStateException("Could not prepare an isolated reception form");
    }

    /**
     * @deprecated use {@link #prepareIsolatedTestState()}
     */
    public PatientAdmissionPage refreshForNextTest() {
        return prepareIsolatedTestState();
    }

    /**
     * Closes open ng-select panels, unknown-patient modal, and nav dropdowns.
     * Does <strong>not</strong> wipe toast-stack innerHTML — that breaks Angular's
     * toaster until the next remount. Between tests, {@link #reloadReceptionFresh()}
     * remounts a clean toaster.
     */
    public PatientAdmissionPage dismissOverlaysAndToasts() {
        try {
            driver.switchTo().activeElement().sendKeys(Keys.ESCAPE);
        } catch (Exception ignored) {
            // No focused element — fine
        }

        closeUnknownPatientModalIfOpen();
        closeReservationModalIfOpen();
        collapseOpenNavDropdowns();
        dismissVisibleToastsViaCloseButtons();

        try {
            ((JavascriptExecutor) driver).executeScript(
                    "if (typeof Swal !== 'undefined' && Swal.close) { try { Swal.close(); } catch(e){} }"
                            + "document.querySelectorAll('ng-dropdown-panel, .swal2-container, .modal-backdrop, .overlay-backdrop, .modal-backdrop-show').forEach(p => p.remove());"
                            + "document.body.classList.remove('swal2-shown', 'swal2-height-auto', 'modal-open');");
            LOGGER.debug("Dismissed dropdown panels, Swal modals, and backdrops");
        } catch (Exception e) {
            LOGGER.debug("Could not JS-clear dropdown panels/swal: {}", e.getMessage());
        }
        return this;
    }

    /** Collapses any open navbar dropdown so it cannot intercept form clicks. */
    public PatientAdmissionPage collapseOpenNavDropdowns() {
        try {
            ((JavascriptExecutor) driver).executeScript(
                    "document.querySelectorAll('.nav-dropdown.has-active, .nav-dropdown.open')"
                            + ".forEach(function(d){ d.classList.remove('has-active','open'); });"
                            + "document.querySelectorAll('.dropdown-menu').forEach(function(m){"
                            + "  m.style.display='none';"
                            + "});"
                            + "document.body.click();");
        } catch (Exception e) {
            LOGGER.debug("Could not collapse nav dropdowns: {}", e.getMessage());
        }
        return this;
    }

    /**
     * Clicks each toast close button so Angular tears items down itself.
     * Prefer this over wiping innerHTML (which breaks later toasts).
     */
    public PatientAdmissionPage dismissVisibleToastsViaCloseButtons() {
        try {
            for (WebElement closeBtn : driver.findElements(By.cssSelector(
                    "[data-test-id='global-toast-stack'] [data-test-id$='-close-btn'],"
                            + "[data-test-id='global-toast-stack'] .close-btn"))) {
                try {
                    if (closeBtn.isDisplayed()) {
                        ((JavascriptExecutor) driver).executeScript("arguments[0].click();", closeBtn);
                    }
                } catch (StaleElementReferenceException ignored) {
                    // Toast already gone
                }
            }
        } catch (Exception e) {
            LOGGER.debug("Could not dismiss toasts via close buttons: {}", e.getMessage());
        }
        return this;
    }

    /**
     * @deprecated Wiping toast-stack innerHTML breaks Angular's toaster.
     * Use {@link #dismissVisibleToastsViaCloseButtons()} or {@link #reloadReceptionFresh()}.
     */
    @Deprecated
    public PatientAdmissionPage forceClearToastStack() {
        LOGGER.warn("forceClearToastStack() is deprecated — redirects to close-button dismiss");
        return dismissVisibleToastsViaCloseButtons();
    }

    /** Waits until the global toast stack has no toast-item nodes (or times out). */
    public PatientAdmissionPage waitUntilToastStackEmpty(int timeoutSeconds) {
        try {
            new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds))
                    .pollingEvery(Duration.ofMillis(200))
                    .until(d -> {
                        String html = getToastStackHtml();
                        return html == null
                                || html.isBlank()
                                || html.equals("<toast-stack not found>")
                                || !(html.contains("toast-item")
                                || html.contains("toast-warning")
                                || html.contains("toast-success")
                                || html.contains("toast-error"));
                    });
        } catch (TimeoutException e) {
            dismissVisibleToastsViaCloseButtons();
            LOGGER.warn("Toast stack was not empty within {}s; clicked close buttons", timeoutSeconds);
        }
        return this;
    }

    // =========================================================
    // Search
    // =========================================================

    public PatientAdmissionPage searchForPatient(String query) {
        WebElement search = wait.until(ExpectedConditions.elementToBeClickable(searchInput));
        search.clear();
        search.sendKeys(query);
        LOGGER.info("Searched for patient: {}", query);
        return this;
    }

    /**
     * Types the query into the global search bar, then selects the matching
     * result from the autocomplete dropdown.
     * <p>
     * TEMPORARY: pressing ENTER alone does not populate the form yet — the UI
     * only drops a one-item list and expects a click. Replace with the real
     * search-submit behaviour once product confirms how the field should work.
     *
     * @see TEMPORARY_WORKAROUNDS.md
     */
    public PatientAdmissionPage searchForPatientAndSubmit(String query) {
        searchForPatient(query);
        selectFirstSearchResult(query);
        LOGGER.info("TEMPORARY: selected the first search dropdown result for '{}'", query);
        return this;
    }

    /**
     * TEMPORARY: clicks the single patient row that appears under the search box.
     * Tries several common Angular/PrimeNG autocomplete structures until one matches.
     */
    private void selectFirstSearchResult(String query) {
        By[] candidates = new By[] {
                By.xpath("//div[contains(@class,'search-box-wrapper')]"
                        + "//*[self::li or self::a or self::div or self::button]"
                        + "[contains(normalize-space(.),'" + query + "')]"),
                By.cssSelector(".search-box-wrapper .p-autocomplete-item, "
                        + ".search-box-wrapper .ng-option, "
                        + ".search-box-wrapper [class*='result'], "
                        + ".search-box-wrapper [class*='suggestion'], "
                        + ".search-box-wrapper [class*='dropdown'] li, "
                        + ".search-box-wrapper li"),
                By.cssSelector(".p-autocomplete-panel .p-autocomplete-item, "
                        + "ng-dropdown-panel .ng-option, "
                        + "[class*='search-result'] li, "
                        + "[class*='autocomplete'] li"),
                By.xpath("//*[contains(@class,'p-autocomplete-panel') or "
                        + "contains(@class,'search-result') or "
                        + "contains(@class,'autocomplete')]"
                        + "//*[self::li or contains(@class,'item') or contains(@class,'option')]"
                        + "[contains(normalize-space(.),'" + query + "') "
                        + "or string-length(normalize-space(.))>0]")
        };

        RuntimeException lastError = null;
        for (By locator : candidates) {
            try {
                WebElement result = wait.until(ExpectedConditions.elementToBeClickable(locator));
                result.click();
                LOGGER.info("TEMPORARY: clicked search result using locator {}", locator);
                return;
            } catch (Exception e) {
                lastError = new RuntimeException("Search result not found with " + locator, e);
            }
        }
        throw lastError != null
                ? lastError
                : new IllegalStateException("No search dropdown result appeared for: " + query);
    }

    /** Waits until the Arabic name gets populated (e.g. after a successful search). */
    public boolean waitForFormPopulated() {
        try {
            wait.until(d -> {
                String value = arabicNameInput.getAttribute("value");
                return value != null && !value.isBlank();
            });
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * Reads the patient code after a successful save from the form field,
     * falling back to /reception/patient/{code} (or legacy /reception/{code}).
     */
    public String getPatientCodeValue() {
        try {
            WebElement codeInput = driver.findElement(
                    By.cssSelector("[data-test-id='patient-data-patient-code-input']"));
            String value = codeInput.getAttribute("value");
            if (value != null && !value.isBlank()) {
                return value.trim();
            }
        } catch (Exception ignored) {
            // fall through to URL parsing
        }

        String url = driver.getCurrentUrl();
        if (url == null) {
            return "";
        }
        String path = url.split("[?#]", 2)[0].replaceAll("/+$", "");
        if (path.matches(".*/reception/patient/[^/]+$")) {
            return path.substring(path.lastIndexOf('/') + 1);
        }
        if (path.matches(".*/reception/[^/]+$") && !path.endsWith("/reception")) {
            return path.substring(path.lastIndexOf('/') + 1);
        }
        return "";
    }

    /**
     * True when the browser is on a saved-patient details URL:
     * {@code .../reception/patient/{patientCode}}
     */
    public boolean isOnSavedPatientUrl() {
        String url = driver.getCurrentUrl();
        return url != null && url.matches(".*/reception/patient/[^/?#]+/?([?#].*)?$");
    }

    /**
     * Happy-path save succeeded if ANY of these happen within the timeout:
     * <ul>
     *   <li>a success toast</li>
     *   <li>a success alert</li>
     *   <li>URL becomes {@code /reception/patient/{code}}</li>
     * </ul>
     */
    public boolean waitForSuccessfulPatientSave() {
        return waitForSuccessfulPatientSave(10);
    }

    public boolean waitForSuccessfulPatientSave(int timeoutSeconds) {
        try {
            new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds))
                    .pollingEvery(Duration.ofMillis(200))
                    .until(d -> collectVisibleToastTypes().contains("success") || isOnSavedPatientUrl());
            LOGGER.info("Patient save succeeded. url={}, toastTypes={}",
                    driver.getCurrentUrl(), collectVisibleToastTypes());
            return true;
        } catch (TimeoutException e) {
            LOGGER.warn("Save success not detected within {}s. url={}, toastTypes={}, toastHtml={}",
                    timeoutSeconds, driver.getCurrentUrl(),
                    collectVisibleToastTypes(), getToastStackHtml());
            return false;
        }
    }

    /**
     * After Save, watches for both a WARNING toast/alert and a successful save
     * (success toast/alert OR /reception/patient/{code}) within the same window —
     * because short-name warnings can appear together with a successful registration.
     *
     * @return {@code true} only if both signals were observed
     */
    public boolean waitForWarningAndSuccessfulSave(int timeoutSeconds) {
        boolean[] signals = observeWarningAndSuccessfulSave(timeoutSeconds);
        boolean ok = signals[0] && signals[1];
        if (!ok) {
            LOGGER.warn(
                    "Did not observe both WARNING and save success within {}s. "
                            + "warningSeen={}, successSeen={}, url={}, toastHtml={}",
                    timeoutSeconds, signals[0], signals[1],
                    driver.getCurrentUrl(), getToastStackHtml());
        }
        return ok;
    }

    /**
     * Arms the toast latch, clicks Save, then observes warning+success in one
     * flow so a toast that appears during the click itself cannot be missed.
     *
     * @return {@code [warningSeen, successSeen]}
     */
    public boolean[] clickSaveAndObserveWarningAndSuccess(int timeoutSeconds) {
        armToastTypeLatch();
        // Native click — a pure JS click can skip Angular validators that emit the warning toast
        clickFresh(SAVE_BUTTON);
        LOGGER.info("Clicked Save (اضافة) with toast latch armed");
        return observeWarningAndSuccessfulSave(timeoutSeconds);
    }

    /**
     * Same as {@link #waitForWarningAndSuccessfulSave(int)} but returns
     * {@code [warningSeen, successSeen]}.
     * <p>
     * Prefer {@link #clickSaveAndObserveWarningAndSuccess(int)} so the latch is
     * armed before the click. Call {@link #armToastTypeLatch()} yourself if you
     * click Save through another path.
     */
    public boolean[] observeWarningAndSuccessfulSave(int timeoutSeconds) {
        boolean warningSeen = false;
        boolean successSeen = false;
        long deadline = System.currentTimeMillis() + timeoutSeconds * 1000L;

        while (System.currentTimeMillis() < deadline) {
            // Fast path: ask the browser directly (survives SPA route changes via sessionStorage)
            Object snap = ((JavascriptExecutor) driver).executeScript(
                    "var seen = window.__paymaxSeenToasts;"
                            + "if (!seen || !seen.length) {"
                            + "  try { seen = JSON.parse(sessionStorage.getItem('__paymaxSeenToasts')||'[]'); }"
                            + "  catch (e) { seen = []; }"
                            + "}"
                            + "var dom = [];"
                            + "document.querySelectorAll("
                            + "  \"[data-test-id^='toast-warning'],[data-test-id^='toast-success'],"
                            + "   [data-test-id^='toast-error'],.toast-item.warning,"
                            + "   .toast-item.success,.toast-item.error\").forEach(function(el) {"
                            + "  var id = (el.getAttribute('data-test-id')||'').toLowerCase();"
                            + "  var cls = (' '+(el.getAttribute('class')||'')+' ').toLowerCase();"
                            + "  var t = null;"
                            + "  if (id.indexOf('success')>=0 || cls.indexOf(' success ')>=0) t='success';"
                            + "  else if (id.indexOf('error')>=0 || cls.indexOf(' error ')>=0) t='error';"
                            + "  else if (id.indexOf('warning')>=0 || cls.indexOf(' warning ')>=0) t='warning';"
                            + "  if (t && dom.indexOf(t)<0) dom.push(t);"
                            + "});"
                            + "return {seen: seen||[], dom: dom,"
                            + " url: location.href};");

            if (snap instanceof java.util.Map<?, ?> map) {
                Object seenObj = map.get("seen");
                Object domObj = map.get("dom");
                if (seenObj instanceof java.util.List<?> seen) {
                    for (Object t : seen) {
                        if ("warning".equals(String.valueOf(t))) {
                            warningSeen = true;
                        }
                        if ("success".equals(String.valueOf(t))) {
                            successSeen = true;
                        }
                    }
                }
                if (domObj instanceof java.util.List<?> dom) {
                    for (Object t : dom) {
                        if ("warning".equals(String.valueOf(t))) {
                            warningSeen = true;
                        }
                        if ("success".equals(String.valueOf(t))) {
                            successSeen = true;
                        }
                    }
                }
            }

            for (String type : collectVisibleToastTypes()) {
                if ("warning".equals(type)) {
                    warningSeen = true;
                }
                if ("success".equals(type)) {
                    successSeen = true;
                }
            }
            if (isOnSavedPatientUrl()) {
                successSeen = true;
            }
            if (warningSeen && successSeen) {
                break;
            }
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }

        LOGGER.info("Save observation: warningSeen={}, successSeen={}, latched={}, url={}",
                warningSeen, successSeen, getLatchedToastTypes(), driver.getCurrentUrl());
        return new boolean[] {warningSeen, successSeen};
    }

    /**
     * Starts a page-level MutationObserver that records every toast/alert type
     * as it appears — even if it disappears before the next Selenium poll.
     * Safe to call more than once (re-arms a fresh latch).
     */
    public PatientAdmissionPage armToastTypeLatch() {
        ((JavascriptExecutor) driver).executeScript(
                "window.__paymaxSeenToasts = [];"
                        + "try { sessionStorage.setItem('__paymaxSeenToasts','[]'); } catch (e) {}"
                        + "if (window.__paymaxToastObserver) {"
                        + "  try { window.__paymaxToastObserver.disconnect(); } catch (e) {}"
                        + "}"
                        + "function remember(t) {"
                        + "  if (!t) return;"
                        + "  if (window.__paymaxSeenToasts.indexOf(t) < 0)"
                        + "    window.__paymaxSeenToasts.push(t);"
                        + "  try { sessionStorage.setItem('__paymaxSeenToasts',"
                        + "    JSON.stringify(window.__paymaxSeenToasts)); } catch (e) {}"
                        + "}"
                        + "function classify(el) {"
                        + "  if (!el || !el.getAttribute) return null;"
                        + "  var id = (el.getAttribute('data-test-id') || '').toLowerCase();"
                        + "  var cls = (typeof el.className === 'string' ? el.className"
                        + "    : (el.getAttribute('class') || '')).toLowerCase();"
                        + "  cls = ' ' + cls + ' ';"
                        + "  if (id === 'global-toast-stack' || id.indexOf('-stack') >= 0) return null;"
                        + "  if (id.indexOf('success') >= 0 || cls.indexOf(' success ') >= 0"
                        + "      || cls.indexOf('alert-success') >= 0) return 'success';"
                        + "  if (id.indexOf('error') >= 0 || id.indexOf('danger') >= 0"
                        + "      || cls.indexOf(' error ') >= 0 || cls.indexOf('alert-danger') >= 0"
                        + "      || cls.indexOf('alert-error') >= 0) return 'error';"
                        + "  if (id.indexOf('warning') >= 0 || id.indexOf('warn') >= 0"
                        + "      || cls.indexOf(' warning ') >= 0 || cls.indexOf('alert-warning') >= 0)"
                        + "    return 'warning';"
                        + "  return null;"
                        + "}"
                        + "function scan(root) {"
                        + "  if (!root) return;"
                        + "  remember(classify(root));"
                        + "  if (root.querySelectorAll) {"
                        + "    root.querySelectorAll("
                        + "      \"[data-test-id^='toast-'],.toast-item,.alert\").forEach(function(n) {"
                        + "      remember(classify(n));"
                        + "    });"
                        + "  }"
                        + "}"
                        + "var target = document.querySelector(\"[data-test-id='global-toast-stack']\")"
                        + "  || document.querySelector('app-global-toaster') || document.body;"
                        + "scan(target);"
                        + "window.__paymaxToastObserver = new MutationObserver(function(muts) {"
                        + "  muts.forEach(function(m) {"
                        + "    m.addedNodes.forEach(function(n) { scan(n); });"
                        + "    if (m.target) scan(m.target);"
                        + "  });"
                        + "});"
                        + "window.__paymaxToastObserver.observe(document.body,"
                        + "  { childList: true, subtree: true, attributes: true,"
                        + "    attributeFilter: ['class','data-test-id'] });");
        LOGGER.debug("Armed toast-type MutationObserver latch");
        return this;
    }

    @SuppressWarnings("unchecked")
    private java.util.List<String> getLatchedToastTypes() {
        try {
            Object raw = ((JavascriptExecutor) driver).executeScript(
                    "var mem = window.__paymaxSeenToasts;"
                            + "if (mem && mem.length) return mem;"
                            + "try {"
                            + "  return JSON.parse(sessionStorage.getItem('__paymaxSeenToasts') || '[]');"
                            + "} catch (e) { return []; }");
            if (raw instanceof java.util.List) {
                return (java.util.List<String>) raw;
            }
        } catch (Exception ignored) {
            // page may have navigated
        }
        return java.util.Collections.emptyList();
    }

    // =========================================================
    // Form filling
    // =========================================================

    /**
     * Fills all mandatory fields.
     *
     * @param birthDate ISO format yyyy-MM-dd (e.g. 1990-05-15)
     * @param gender    visible option text, e.g. "ذكر" or "أنثى"
     */
    public PatientAdmissionPage fillMandatoryFields(String arabicName, String mobile,
                                                    String birthDate, String gender) {
        enterArabicName(arabicName);
        enterMobile(mobile);
        setBirthDate(birthDate);
        selectGender(gender);
        return this;
    }

    public PatientAdmissionPage enterArabicName(String arabicName) {
        typeInto(arabicNameInput, arabicName);
        return this;
    }

    /**
     * Leaves the Arabic-name field so blur / focus-out validation fires
     * without clicking Save.
     * <p>
     * Uses click-away (not only TAB) plus explicit blur/focusout/change events —
     * Angular name validators often ignore a raw TAB from WebDriver.
     */
    public PatientAdmissionPage blurArabicNameField() {
        WebElement name = wait.until(ExpectedConditions.elementToBeClickable(arabicNameInput));
        name.click();

        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
                        + "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));"
                        + "arguments[0].blur();"
                        + "arguments[0].dispatchEvent(new Event('focusout', { bubbles: true }));"
                        + "arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));",
                name);

        // Click another field so the browser truly moves focus away
        wait.until(ExpectedConditions.elementToBeClickable(englishNameInput)).click();
        LOGGER.info("Blurred Arabic name field via JS events + click on English name");
        return this;
    }

    public PatientAdmissionPage enterEnglishName(String englishName) {
        typeInto(englishNameInput, englishName);
        return this;
    }

    public PatientAdmissionPage enterMobile(String mobile) {
        typeInto(mobileInput, mobile);
        return this;
    }

    public PatientAdmissionPage enterOtherPhone(String otherPhone) {
        typeInto(otherPhoneInput, otherPhone);
        return this;
    }

    public PatientAdmissionPage enterWhatsapp(String whatsapp) {
        typeInto(whatsappInput, whatsapp);
        return this;
    }

    public PatientAdmissionPage enterNationalId(String nationalId) {
        typeInto(nationalIdInput, nationalId);
        // TAB out so Angular runs the NID parsing / age auto-calculation
        nationalIdInput.sendKeys(Keys.TAB);
        return this;
    }

    public PatientAdmissionPage enterAddress(String address) {
        typeInto(addressInput, address);
        return this;
    }

    public PatientAdmissionPage enterEmail(String email) {
        typeInto(emailInput, email);
        return this;
    }

    public PatientAdmissionPage enterNotes(String notes) {
        typeInto(notesTextarea, notes);
        return this;
    }

    public PatientAdmissionPage enterInsuranceNumber(String insuranceNumber) {
        typeInto(insuranceNumberInput, insuranceNumber);
        return this;
    }

    /**
     * Sets the birth date on the native date input. Uses JavaScript with input/change
     * events because sendKeys on type=date is locale-dependent and flaky.
     *
     * @param isoDate yyyy-MM-dd
     */
    public PatientAdmissionPage setBirthDate(String isoDate) {
        setDateByJs(birthDateInput, isoDate);
        LOGGER.info("Set birth date to {}", isoDate);
        return this;
    }

    /** Sets the contract expiration date (تاريخ انتهاء الصلاحية), ISO yyyy-MM-dd. */
    public PatientAdmissionPage setExpirationDate(String isoDate) {
        setDateByJs(expirationDateInput, isoDate);
        LOGGER.info("Set expiration date to {}", isoDate);
        return this;
    }

    public PatientAdmissionPage selectGender(String genderText) {
        selectNgOption(genderSelect, genderText);
        LOGGER.info("Selected gender: {}", genderText);
        return this;
    }

    public PatientAdmissionPage selectIdType(String idTypeText) {
        selectNgOption(idTypeSelect, idTypeText);
        LOGGER.info("Selected identity type (إثبات الشخصية): {}", idTypeText);
        return this;
    }

    public PatientAdmissionPage selectReligion(String religionText) {
        selectNgOption(religionSelect, religionText);
        LOGGER.info("Selected religion: {}", religionText);
        return this;
    }

    public PatientAdmissionPage selectMaritalStatus(String statusText) {
        selectNgOption(maritalStatusSelect, statusText);
        LOGGER.info("Selected marital status: {}", statusText);
        return this;
    }

    public PatientAdmissionPage selectJob(String jobText) {
        selectNgOption(jobSelect, jobText);
        LOGGER.info("Selected job: {}", jobText);
        return this;
    }

    public PatientAdmissionPage selectClient(String clientText) {
        selectNgOption(clientSelect, clientText);
        LOGGER.info("Selected client (الجهة): {}", clientText);
        // Sub-company options reload asynchronously from the API after جهة changes
        waitForDependentNgSelectToSettle(insCompanySelect);
        return this;
    }

    public PatientAdmissionPage selectInsCompany(String companyText) {
        wait.until(ExpectedConditions.elementToBeClickable(insCompanySelect));
        wait.until(d -> isNgSelectEnabled(insCompanySelect));
        selectNgOption(insCompanySelect, companyText);
        LOGGER.info("Selected sub-company (الشركة الفرعية): {}", companyText);
        return this;
    }

    public PatientAdmissionPage selectContractType(String contractTypeText) {
        waitUntilContractTypeEnabled();
        selectNgOption(contractTypeSelect, contractTypeText);
        LOGGER.info("Selected contract type (نوع التعاقد): {}", contractTypeText);
        return this;
    }

    public PatientAdmissionPage selectRelativeDegree(String relativeText) {
        waitUntilRelativeDegreeEnabled();
        selectNgOption(relativeDegreeSelect, relativeText);
        LOGGER.info("Selected relative degree (درجة القرابة): {}", relativeText);
        return this;
    }

    /** Waits until نوع التعاقد is enabled (not ng-select-disabled) and clickable. */
    public PatientAdmissionPage waitUntilContractTypeEnabled() {
        wait.until(ExpectedConditions.visibilityOf(contractTypeSelect));
        wait.until(d -> isNgSelectEnabled(contractTypeSelect));
        wait.until(ExpectedConditions.elementToBeClickable(contractTypeSelect));
        LOGGER.info("Contract type (نوع التعاقد) is enabled");
        return this;
    }

    /** Waits until درجة القرابة is visible and enabled. */
    public PatientAdmissionPage waitUntilRelativeDegreeEnabled() {
        wait.until(ExpectedConditions.visibilityOf(relativeDegreeSelect));
        wait.until(d -> isNgSelectEnabled(relativeDegreeSelect));
        wait.until(ExpectedConditions.elementToBeClickable(relativeDegreeSelect));
        LOGGER.info("Relative degree (درجة القرابة) is enabled and visible");
        return this;
    }

    public boolean isContractTypeEnabled() {
        return isNgSelectEnabled(contractTypeSelect);
    }

    public boolean isRelativeDegreeEnabled() {
        return isNgSelectEnabled(relativeDegreeSelect);
    }

    public boolean isRelativeDegreeDisplayed() {
        try {
            return relativeDegreeSelect.isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * True when درجة القرابة does not allow free typing/search
     * (inner combobox is {@code readonly}).
     */
    public boolean isRelativeDegreeInputReadOnly() {
        wait.until(ExpectedConditions.visibilityOf(relativeDegreeSelect));
        WebElement inner = relativeDegreeSelect.findElement(
                By.cssSelector("input[role='combobox']"));
        String readonly = inner.getAttribute("readonly");
        boolean readOnly = readonly != null;
        LOGGER.info("Relative degree combobox readonly attr={}", readonly);
        return readOnly;
    }

    /** Visible selected text of نوع التعاقد. */
    public String getContractTypeSelectedText() {
        wait.until(ExpectedConditions.visibilityOf(contractTypeSelect));
        return getNgSelectText(contractTypeSelect);
    }

    /**
     * Opens نوع التعاقد and returns the visible option labels (then closes the panel).
     * Expected after جهة آجل + شركة فرعية: العضو نفسه / مريض تابع.
     */
    public List<String> getContractTypeOptionTexts() {
        waitUntilContractTypeEnabled();
        return getOpenNgSelectOptionTexts(contractTypeSelect);
    }

    /** Visible selected text of درجة القرابة. */
    public String getRelativeDegreeSelectedText() {
        wait.until(ExpectedConditions.visibilityOf(relativeDegreeSelect));
        return getNgSelectText(relativeDegreeSelect);
    }

    /**
     * Waits until درجة القرابة shows a non-blank selected value and returns it
     * (used after choosing "مريض تابع", which may auto-default the relative).
     */
    public String waitForRelativeDegreeSelectedText() {
        waitUntilRelativeDegreeEnabled();
        wait.until(d -> {
            String text = getNgSelectText(relativeDegreeSelect);
            return text != null && !text.isBlank();
        });
        return getRelativeDegreeSelectedText();
    }

    /**
     * Opens درجة القرابة and returns the first enabled option text (the list default),
     * then closes the panel without committing a change when possible.
     */
    public String getFirstRelativeDegreeOptionText() {
        waitUntilRelativeDegreeEnabled();
        WebElement select = wait.until(ExpectedConditions.elementToBeClickable(relativeDegreeSelect));
        select.click();
        By firstOption = By.cssSelector(
                "ng-dropdown-panel .ng-option:not(.ng-option-disabled)");
        WebElement option = wait.until(ExpectedConditions.visibilityOfElementLocated(firstOption));
        String text = option.getText().trim();
        try {
            driver.switchTo().activeElement().sendKeys(Keys.ESCAPE);
        } catch (Exception ignored) {
            // Panel may already be closed
        }
        LOGGER.info("First درجة القرابة option: {}", text);
        return text;
    }

    /**
     * After "مريض تابع": returns the auto-selected relative if Angular stamped one,
     * otherwise the first list option (observed default: الزوج/الزوجة).
     */
    public String getRelativeDegreeDefaultValue() {
        waitUntilRelativeDegreeEnabled();
        try {
            new WebDriverWait(driver, Duration.ofSeconds(3))
                    .pollingEvery(Duration.ofMillis(200))
                    .until(d -> {
                        String text = getNgSelectText(relativeDegreeSelect);
                        return text != null && !text.isBlank();
                    });
            return getRelativeDegreeSelectedText();
        } catch (TimeoutException e) {
            LOGGER.info("No auto-selected درجة القرابة value within 3s; reading first list option");
            return getFirstRelativeDegreeOptionText();
        }
    }

    /**
     * Label text of the identity-number field (updates with إثبات الشخصية,
     * e.g. "الرقم القومي" → "جواز سفر").
     */
    public String getIdNumberFieldLabelText() {
        By label = By.xpath(
                "//*[@data-test-id='patient-data-id-number-input']"
                        + "/ancestor::div[contains(@class,'fg')][1]//label");
        return wait.until(ExpectedConditions.visibilityOfElementLocated(label))
                .getText().trim();
    }

    /**
     * Selects إثبات الشخصية then waits until the adjacent field label equals
     * {@code expectedLabel}.
     */
    public PatientAdmissionPage selectIdTypeAndWaitForLabel(String idTypeText, String expectedLabel) {
        selectIdType(idTypeText);
        wait.until(d -> expectedLabel.equals(getIdNumberFieldLabelText()));
        LOGGER.info("Identity field label updated to '{}'", expectedLabel);
        return this;
    }

    /**
     * Hard-reloads /reception (without clicking جديد) and waits until الجهة
     * shows the page default value.
     */
    public PatientAdmissionPage reloadAndWaitForDefaultClient(String expectedClient) {
        reloadReceptionFresh();
        wait.until(ExpectedConditions.visibilityOf(clientSelect));
        wait.until(d -> expectedClient.equals(getNgSelectText(clientSelect)));
        LOGGER.info("Default client (الجهة) is '{}'", expectedClient);
        return this;
    }

    /** Opens the dropdown and picks the first enabled option (for optional lookups). */
    public PatientAdmissionPage selectFirstReligionOption() {
        selectFirstNgOption(religionSelect);
        return this;
    }

    public PatientAdmissionPage selectFirstMaritalStatusOption() {
        selectFirstNgOption(maritalStatusSelect);
        return this;
    }

    public PatientAdmissionPage selectFirstJobOption() {
        selectFirstNgOption(jobSelect);
        return this;
    }

    public PatientAdmissionPage selectFirstClientOption() {
        selectFirstNgOption(clientSelect);
        waitForDependentNgSelectToSettle(insCompanySelect);
        return this;
    }

    public PatientAdmissionPage selectFirstInsCompanyOption() {
        wait.until(ExpectedConditions.visibilityOf(insCompanySelect));
        wait.until(d -> isNgSelectEnabled(insCompanySelect));
        selectFirstNgOption(insCompanySelect);
        return this;
    }

    public PatientAdmissionPage selectFirstContractTypeOption() {
        if (hasClass(contractTypeSelect, "ng-select-disabled")) {
            LOGGER.info("Contract type dropdown is disabled; skipping");
            return this;
        }
        selectFirstNgOption(contractTypeSelect);
        return this;
    }

    /**
     * Fills a broad set of mandatory + optional fields used by full-coverage tests.
     * Optional dropdowns pick the first available option when exact labels vary by env.
     */
    public PatientAdmissionPage fillAllAvailableFields(String arabicName, String englishName,
                                                       String mobile, String nationalId,
                                                       String birthDate, String gender,
                                                       String address, String email, String notes,
                                                       String insuranceNumber, String expiryDate) {
        fillMandatoryFields(arabicName, mobile, birthDate, gender);
        enterEnglishName(englishName);
        enterOtherPhone(mobile);
        enterWhatsapp(mobile);
        selectIdType("رقم قومي");
        enterNationalId(nationalId);
        selectFirstReligionOption();
        selectFirstMaritalStatusOption();
        enterAddress(address);
        enterEmail(email);
        selectFirstJobOption();
        enterNotes(notes);
        // Prefer the known cash جهة — "first option" varies by API order and may have
        // no/slow شركة فرعية options, which made this path flake.
        selectClient("$$نقدي 2019");
        selectFirstInsCompanyOption();
        selectFirstContractTypeOption();
        // Insurance fields may be disabled for cash contracts — only fill when enabled
        if (insuranceNumberInput.isEnabled()) {
            enterInsuranceNumber(insuranceNumber);
        }
        if (expirationDateInput.isEnabled()) {
            setExpirationDate(expiryDate);
        }
        return this;
    }

    public void clickSave() {
        clickFresh(SAVE_BUTTON);
        LOGGER.info("Clicked Save (اضافة)");
    }

    public void clickNew() {
        clickFresh(NEW_BUTTON);
        LOGGER.info("Clicked New (جديد)");
    }

    /**
     * Clicks جديد and waits until the browser is on exact {@code /reception}
     * (not {@code /reception/patient/{code}}).
     */
    public PatientAdmissionPage clickNewAndWaitForReceptionUrl() {
        clickNew();
        waitForExactReceptionUrl();
        waitUntilLoaded();
        LOGGER.info("After جديد, URL is exact /reception: {}", driver.getCurrentUrl());
        return this;
    }

    /** Browser refresh of the current page (F5). */
    public PatientAdmissionPage refreshCurrentPage() {
        LOGGER.info("Refreshing current page: {}", driver.getCurrentUrl());
        driver.navigate().refresh();
        return this;
    }

    /**
     * Refresh while on a patient profile and wait until the app redirects to
     * exact {@code /reception}.
     */
    public PatientAdmissionPage refreshPatientProfileAndWaitForReceptionUrl() {
        if (!isOnSavedPatientUrl()) {
            throw new IllegalStateException(
                    "Expected to be on /reception/patient/{code} before refresh. URL="
                            + driver.getCurrentUrl());
        }
        refreshCurrentPage();
        waitForExactReceptionUrl();
        waitUntilLoaded();
        LOGGER.info("After refresh on patient profile, URL is exact /reception: {}",
                driver.getCurrentUrl());
        return this;
    }

    /** True when URL is exactly {@code .../reception} (not a patient-detail URL). */
    public boolean isOnExactReceptionUrl() {
        return isExactReceptionUrl(driver.getCurrentUrl());
    }

    public PatientAdmissionPage waitForExactReceptionUrl() {
        wait.until(d -> isExactReceptionUrl(d.getCurrentUrl()));
        return this;
    }

    // =========================================================
    // Unknown patient (مريض غير معروف) modal
    // =========================================================

    /** Opens the "المرضى الغير معروفين" modal and waits until it is rendered. */
    public PatientAdmissionPage openUnknownPatientModal() {
        collapseOpenNavDropdowns();
        clickThroughOverlays(UNKNOWN_PATIENT_OPEN_BUTTON);
        wait.until(ExpectedConditions.visibilityOfElementLocated(UNKNOWN_PATIENT_MODAL));
        wait.until(ExpectedConditions.visibilityOf(unknownPatientCodeInput));
        LOGGER.info("Opened the unknown-patient modal");
        return this;
    }

    /**
     * Fills the modal form. Any {@code null} argument leaves that field untouched.
     *
     * @param gender    "ذكر" / "male" or "أنثى" / "female"
     * @param visitDate ISO date (yyyy-MM-dd)
     * @param visitTime 24h time (HH:mm)
     * @param notes     free text, may be null
     */
    public PatientAdmissionPage fillUnknownPatientForm(String gender, String visitDate,
                                                       String visitTime, String notes) {
        if (gender != null && !gender.isBlank()) {
            selectUnknownPatientGender(gender);
        }
        if (visitDate != null && !visitDate.isBlank()) {
            setDateByJs(unknownPatientVisitDateInput, visitDate);
            LOGGER.info("Set unknown-patient visit date: {}", visitDate);
        }
        if (visitTime != null && !visitTime.isBlank()) {
            setDateByJs(unknownPatientVisitTimeInput, visitTime);
            LOGGER.info("Set unknown-patient visit time: {}", visitTime);
        }
        if (notes != null) {
            typeInto(unknownPatientNotesTextarea, notes);
        }
        return this;
    }

    /** Selects the الجنس radio inside the modal. */
    public PatientAdmissionPage selectUnknownPatientGender(String gender) {
        String normalized = gender.trim();
        boolean female = normalized.equalsIgnoreCase("female")
                || normalized.contains("أنثى")
                || normalized.contains("انثى");

        WebElement radio = female ? unknownPatientFemaleRadio : unknownPatientMaleRadio;
        WebElement target = wait.until(ExpectedConditions.elementToBeClickable(radio));
        // Radios sit behind a styled label in this modal; JS-click is the reliable path
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].click();"
                        + "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                target);
        LOGGER.info("Selected unknown-patient gender: {}", female ? "أنثى" : "ذكر");
        return this;
    }

    /** Clicks "حفظ مريض غير معروف". */
    public void clickSaveUnknownPatient() {
        clickThroughOverlays(UNKNOWN_PATIENT_SAVE_BUTTON);
        LOGGER.info("Clicked Save unknown patient (حفظ مريض غير معروف)");
    }

    /** Closes the modal via the X button and waits until it disappears. */
    public PatientAdmissionPage closeUnknownPatientModal() {
        clickThroughOverlays(UNKNOWN_PATIENT_CLOSE_BUTTON);
        wait.until(ExpectedConditions.invisibilityOfElementLocated(UNKNOWN_PATIENT_MODAL));
        LOGGER.info("Closed the unknown-patient modal");
        return this;
    }

    /**
     * Cleanup hook: closes the modal when a previous test left it open so the
     * next test does not click through a blocking backdrop.
     */
    public PatientAdmissionPage closeUnknownPatientModalIfOpen() {
        try {
            if (isUnknownPatientModalDisplayed()) {
                closeUnknownPatientModal();
            }
        } catch (Exception e) {
            LOGGER.debug("Could not close unknown-patient modal: {}", e.getMessage());
        }
        return this;
    }

    /** True while the modal container is present and visible. */
    public boolean isUnknownPatientModalDisplayed() {
        List<WebElement> modals = driver.findElements(UNKNOWN_PATIENT_MODAL);
        return !modals.isEmpty() && modals.get(0).isDisplayed();
    }

    public boolean isUnknownPatientCodeInputDisplayed() {
        List<WebElement> inputs = driver.findElements(UNKNOWN_PATIENT_CODE_INPUT);
        return !inputs.isEmpty() && inputs.get(0).isDisplayed();
    }

    /** True when the auto-generated code cannot be edited (readonly or disabled). */
    public boolean isUnknownPatientCodeInputNotEditable() {
        WebElement code = wait.until(
                ExpectedConditions.visibilityOfElementLocated(UNKNOWN_PATIENT_CODE_INPUT));
        boolean readonly = code.getAttribute("readonly") != null;
        boolean disabled = code.getAttribute("disabled") != null || !code.isEnabled();
        LOGGER.info("Unknown-patient code input: readonly={}, disabled={}", readonly, disabled);
        return readonly || disabled;
    }

    public String getUnknownPatientCodeValue() {
        WebElement code = wait.until(
                ExpectedConditions.visibilityOfElementLocated(UNKNOWN_PATIENT_CODE_INPUT));
        String value = code.getAttribute("value");
        return value == null ? "" : value.trim();
    }

    // =========================================================
    // Reservation Agenda Modal
    // =========================================================

    public PatientAdmissionPage openReservationAgenda() {
        wait.until(ExpectedConditions.presenceOfElementLocated(RESERVATION_AGENDA_BTN));
        clickThroughOverlays(RESERVATION_AGENDA_BTN);
        wait.until(ExpectedConditions.visibilityOfElementLocated(RESERVATION_MODAL_BACKDROP));
        LOGGER.info("Opened Reservation Agenda modal");
        return this;
    }

    public boolean isReservationModalDisplayed() {
        List<WebElement> backdrops = driver.findElements(RESERVATION_MODAL_BACKDROP);
        return !backdrops.isEmpty() && backdrops.get(0).isDisplayed();
    }

    public String getReservationFromDateValue() {
        WebElement input = wait.until(ExpectedConditions.visibilityOfElementLocated(RESERVATION_FROM_DATE_INPUT));
        return input.getAttribute("value");
    }

    public String getReservationToDateValue() {
        WebElement input = wait.until(ExpectedConditions.visibilityOfElementLocated(RESERVATION_TO_DATE_INPUT));
        return input.getAttribute("value");
    }

    public PatientAdmissionPage setReservationFromDate(String date) {
        WebElement input = wait.until(ExpectedConditions.visibilityOfElementLocated(RESERVATION_FROM_DATE_INPUT));
        input.clear();
        input.sendKeys(date);
        // Fallback for different locales if clearing and typing doesn't set the value in yyyy-MM-dd
        if (!date.equals(input.getAttribute("value")) && date.matches("\\d{4}-\\d{2}-\\d{2}")) {
            String[] parts = date.split("-");
            String formattedDate = parts[2] + "-" + parts[1] + "-" + parts[0];
            input.clear();
            input.sendKeys(formattedDate);
        }
        LOGGER.info("Set reservation from date: {}", date);
        return this;
    }

    public PatientAdmissionPage setReservationToDate(String date) {
        WebElement input = wait.until(ExpectedConditions.visibilityOfElementLocated(RESERVATION_TO_DATE_INPUT));
        input.clear();
        input.sendKeys(date);
        if (!date.equals(input.getAttribute("value")) && date.matches("\\d{4}-\\d{2}-\\d{2}")) {
            String[] parts = date.split("-");
            String formattedDate = parts[2] + "-" + parts[1] + "-" + parts[0];
            input.clear();
            input.sendKeys(formattedDate);
        }
        LOGGER.info("Set reservation to date: {}", date);
        return this;
    }

    public PatientAdmissionPage clickReservationShowButton() {
        WebElement btn = wait.until(ExpectedConditions.elementToBeClickable(RESERVATION_SHOW_BTN));
        btn.click();
        LOGGER.info("Clicked Reservation Show button (عرض)");
        return this;
    }

    public int getReservationGridRowCount() {
        wait.until(ExpectedConditions.presenceOfElementLocated(RESERVATION_TABLE_ROWS));
        List<WebElement> rows = driver.findElements(RESERVATION_TABLE_ROWS);
        if (rows.size() == 1) {
            String text = rows.get(0).getText();
            String html = rows.get(0).getAttribute("innerHTML");
            if (text.contains("لا يوجد") || text.contains("empty-tab") || html.contains("empty-tab")) {
                return 0;
            }
        }
        return rows.size();
    }

    public boolean isReservationGridEmpty() {
        return getReservationGridRowCount() == 0;
    }

    public PatientAdmissionPage waitForReservationGridRows(int expectedRows) {
        new WebDriverWait(driver, Duration.ofSeconds(5))
                .until(d -> getReservationGridRowCount() == expectedRows);
        return this;
    }

    public PatientAdmissionPage closeReservationModal() {
        WebElement btn = wait.until(ExpectedConditions.elementToBeClickable(RESERVATION_CLOSE_BTN));
        btn.click();
        wait.until(ExpectedConditions.invisibilityOfElementLocated(RESERVATION_MODAL_BACKDROP));
        LOGGER.info("Closed Reservation Agenda modal");
        return this;
    }

    public PatientAdmissionPage closeReservationModalIfOpen() {
        try {
            if (isReservationModalDisplayed()) {
                closeReservationModal();
            }
        } catch (Exception e) {
            LOGGER.debug("Could not close reservation agenda modal: {}", e.getMessage());
        }
        return this;
    }


    // =========================================================
    // Top action bar (patient selected / created)
    // =========================================================

    /**
     * Searches for an existing automation patient and opens their profile so the
     * top action bar is available. Prefer a distinctive prefix such as
     * {@code يحيى تيست اوتوميشن}.
     */
    public PatientAdmissionPage openPatientProfileBySearch(String searchQuery) {
        collapseOpenNavDropdowns();
        searchForPatientAndSubmit(searchQuery);
        wait.until(d -> {
            String code = getSelectedPatientCode();
            return code != null && !code.isBlank();
        });
        wait.until(ExpectedConditions.visibilityOfElementLocated(ADMISSION_BTN));
        LOGGER.info("Opened patient profile via search '{}'; code={}",
                searchQuery, getSelectedPatientCode());
        return this;
    }

    /**
     * Opens a patient profile by patient code so the top action bar is available.
     * Uses search by code to avoid hard page reloads (which redirect to /reception in SPA).
     */
    public PatientAdmissionPage openPatientProfileByCode(String patientCode) {
        if (patientCode == null || patientCode.isBlank()) {
            throw new IllegalArgumentException("patientCode is required");
        }
        String trimmedCode = patientCode.trim();
        String expectedUrlPart = "/reception/patient/" + trimmedCode;

        if (driver.getCurrentUrl() != null && driver.getCurrentUrl().contains(expectedUrlPart)) {
            wait.until(ExpectedConditions.visibilityOfElementLocated(ADMISSION_BTN));
            return this;
        }

        if (!isExactReceptionUrl(driver.getCurrentUrl()) && !driver.getCurrentUrl().contains("/reception")) {
            navigateToReception();
        }

        return openPatientProfileBySearch(trimmedCode);
    }

    /**
     * Dynamic patient code from the form field, falling back to
     * {@code /reception/patient/{code}} in the URL.
     */
    public String getSelectedPatientCode() {
        try {
            WebElement codeInput = wait.until(
                    ExpectedConditions.visibilityOfElementLocated(PATIENT_CODE_INPUT));
            String value = codeInput.getAttribute("value");
            if (value != null && !value.isBlank()) {
                return value.trim();
            }
        } catch (Exception ignored) {
            // fall through to URL
        }
        return getPatientCodeValue();
    }

    public boolean isTopActionBarVisible() {
        List<WebElement> buttons = driver.findElements(ADMISSION_BTN);
        return !buttons.isEmpty() && buttons.get(0).isDisplayed();
    }

    public void clickAdmissionButton() {
        clickActionBarButton(ADMISSION_BTN, "دخول");
    }

    public void clickOpdButton() {
        clickActionBarButton(OPD_BTN, "عيادات خارجية");
    }

    public void clickRaysButton() {
        clickActionBarButton(RAYS_BTN, "الأشعة");
    }

    public void clickTestsButton() {
        clickActionBarButton(TESTS_BTN, "تحاليل");
    }

    public void clickEmergencyButton() {
        clickActionBarButton(EMERGENCY_BTN, "إسعاف وطوارئ");
    }

    public void clickPrintBarcodeButton() {
        clickActionBarButton(PRINT_BARCODE_BTN, "باركود المريض");
    }

    public void clickCatheterButton() {
        clickActionBarButton(CATHETER_BTN, "قسطرة");
    }

    public void clickDialysisButton() {
        clickActionBarButton(DIALYSIS_BTN, "غسيل كلى");
    }

    public void clickEndoscopyButton() {
        clickActionBarButton(ENDOSCOPY_BTN, "المناظير");
    }

    public void clickArchiveButton() {
        clickActionBarButton(ARCHIVE_BTN, "الأرشيف");
    }

    /**
     * Clicks an action-bar button and waits until the current URL contains
     * {@code expectedUrlFragment} (use for same-tab redirects).
     */
    public PatientAdmissionPage clickActionAndWaitForUrl(By button, String expectedUrlFragment) {
        clickThroughOverlays(button);
        wait.until(ExpectedConditions.urlContains(expectedUrlFragment));
        LOGGER.info("Navigated to URL containing '{}': {}", expectedUrlFragment, driver.getCurrentUrl());
        return this;
    }

    public PatientAdmissionPage waitForUrlContains(String fragment) {
        wait.until(ExpectedConditions.urlContains(fragment));
        return this;
    }

    /**
     * Clicks باركود المريض, switches to the print popup window, asserts the
     * barcode URL, closes the popup (avoids getting stuck on the native print
     * dialog), and returns to the main window.
     *
     * @return the popup URL that was asserted
     */
    public String verifyBarcodeWindow(String expectedPatientCode) {
        String mainWindow = driver.getWindowHandle();
        int handlesBefore = driver.getWindowHandles().size();

        clickPrintBarcodeButton();

        wait.until(d -> d.getWindowHandles().size() > handlesBefore);

        String popupHandle = null;
        for (String handle : driver.getWindowHandles()) {
            if (!handle.equals(mainWindow)) {
                popupHandle = handle;
                break;
            }
        }
        if (popupHandle == null) {
            throw new IllegalStateException("Barcode popup window did not open");
        }

        driver.switchTo().window(popupHandle);
        wait.until(ExpectedConditions.urlContains("/print/barcode?id="));
        String popupUrl = driver.getCurrentUrl();
        LOGGER.info("Barcode popup URL: {}", popupUrl);

        if (expectedPatientCode != null && !expectedPatientCode.isBlank()) {
            wait.until(ExpectedConditions.urlContains("id=" + expectedPatientCode));
        }

        // Close quickly so the native print dialog does not block the session
        driver.close();
        driver.switchTo().window(mainWindow);
        LOGGER.info("Closed barcode popup and switched back to main window");
        return popupUrl;
    }

    /** Alias kept for callers that still use the earlier method name. */
    public String verifyBarcodeInNewTab(String expectedPatientCode) {
        return verifyBarcodeWindow(expectedPatientCode);
    }

    /**
     * True when the button is disabled via HTML disabled / aria-disabled /
     * CSS class — used for under-development actions.
     */
    public boolean isActionButtonInactive(By buttonLocator) {
        WebElement button = wait.until(ExpectedConditions.presenceOfElementLocated(buttonLocator));
        String disabled = button.getAttribute("disabled");
        String ariaDisabled = button.getAttribute("aria-disabled");
        String classes = button.getAttribute("class");
        boolean inactive = disabled != null
                || "true".equalsIgnoreCase(ariaDisabled)
                || (classes != null && (classes.contains("disabled") || classes.contains("tb-disabled")));
        LOGGER.info("Action button {} inactive={}", buttonLocator, inactive);
        return inactive;
    }

    public boolean isCatheterButtonInactive() {
        return isActionButtonInactive(CATHETER_BTN);
    }

    public boolean isDialysisButtonInactive() {
        return isActionButtonInactive(DIALYSIS_BTN);
    }

    public boolean isEndoscopyButtonInactive() {
        return isActionButtonInactive(ENDOSCOPY_BTN);
    }

    public boolean isArchiveButtonInactive() {
        return isActionButtonInactive(ARCHIVE_BTN);
    }

    /**
     * Clicks an under-development action and asserts the app does not navigate
     * away from the patient profile (URL still contains /reception/patient/).
     */
    public boolean clickUnderDevelopmentActionStaysOnPatientProfile(By buttonLocator) {
        String urlBefore = driver.getCurrentUrl();
        try {
            clickThroughOverlays(buttonLocator);
        } catch (Exception e) {
            LOGGER.info("Under-dev button not clickable (treated as inactive): {}", e.getMessage());
            return urlBefore != null && urlBefore.contains("/reception/patient/");
        }
        try {
            Thread.sleep(800);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        String urlAfter = driver.getCurrentUrl();
        boolean stayed = urlAfter != null
                && urlAfter.contains("/reception/patient/")
                && !urlAfter.contains("/clinic/visits/")
                && !urlAfter.contains("/emergency/");
        LOGGER.info("After under-dev click: stayedOnProfile={}, url={}", stayed, urlAfter);
        return stayed;
    }

    public By catheterButtonLocator() {
        return CATHETER_BTN;
    }

    public By dialysisButtonLocator() {
        return DIALYSIS_BTN;
    }

    public By endoscopyButtonLocator() {
        return ENDOSCOPY_BTN;
    }

    public By archiveButtonLocator() {
        return ARCHIVE_BTN;
    }

    public By admissionButtonLocator() {
        return ADMISSION_BTN;
    }

    public By opdButtonLocator() {
        return OPD_BTN;
    }

    public By raysButtonLocator() {
        return RAYS_BTN;
    }

    public By testsButtonLocator() {
        return TESTS_BTN;
    }

    public By emergencyButtonLocator() {
        return EMERGENCY_BTN;
    }

    private void clickActionBarButton(By locator, String label) {
        collapseOpenNavDropdowns();
        wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        clickThroughOverlays(locator);
        LOGGER.info("Clicked top-bar action: {}", label);
    }

    /**
     * Reads {@code كود الزيارة} from the clinic/emergency visit page.
     * TEMPORARY locator: matches the label inside {@code .info-field} until a
     * stable {@code data-test-id} is added by frontend.
     */
    public String getVisitCodeFromVisitPage() {
        wait.until(d -> {
            String code = readVisitCodeValue();
            return code != null && !code.isBlank();
        });
        String code = readVisitCodeValue();
        LOGGER.info("Read visit code from visit page: {}", code);
        return code;
    }

    private String readVisitCodeValue() {
        By[] candidates = new By[] {
                By.xpath("//*[contains(@class,'info-field')]"
                        + "[.//*[contains(normalize-space(.),'كود الزيارة')]]"
                        + "//input"),
                By.xpath("//*[contains(@class,'info-field')]"
                        + "[.//*[contains(normalize-space(.),'كود الزيارة')]]"
                        + "//*[self::span or self::div or self::strong or self::b]"
                        + "[normalize-space(.)!='' and not(contains(normalize-space(.),'كود الزيارة'))]"),
                By.xpath("//*[contains(@class,'info-field') and contains(normalize-space(.),'كود الزيارة')]"
                        + "//input"),
                By.xpath("//label[contains(normalize-space(.),'كود الزيارة')]"
                        + "/following::input[1]"),
                By.xpath("//*[contains(normalize-space(.),'كود الزيارة')]"
                        + "/following::*[self::input or self::span][1]")
        };

        for (By locator : candidates) {
            List<WebElement> elements = driver.findElements(locator);
            for (WebElement element : elements) {
                try {
                    if (!element.isDisplayed()) {
                        continue;
                    }
                    String value = element.getAttribute("value");
                    if (value == null || value.isBlank()) {
                        value = element.getText();
                    }
                    if (value != null && !value.isBlank()
                            && !value.contains("كود الزيارة")) {
                        return value.trim();
                    }
                } catch (StaleElementReferenceException ignored) {
                    // retry next candidate
                }
            }
        }
        return "";
    }

    // =========================================================
    // Toast / validation popup helpers
    // =========================================================

    /**
     * Checks whether a system message (toast or top alert) of the given type is
     * visible, without inspecting its text. Waits up to 5 seconds so the toast
     * is caught before it auto-dismisses.
     *
     * @param messageType one of "success", "error", "warning"
     */
    public boolean isSystemMessageDisplayed(String messageType) {
        return isSystemMessageDisplayed(messageType, 5);
    }

    /**
     * Same as {@link #isSystemMessageDisplayed(String)} with a custom timeout
     * (useful for quick negative checks after a success toast already appeared).
     */
    public boolean isSystemMessageDisplayed(String messageType, int timeoutSeconds) {
        String expected = messageType.toLowerCase().trim();
        if (!expected.equals("success") && !expected.equals("error") && !expected.equals("warning")) {
            throw new IllegalArgumentException(
                    "Unsupported message type: '" + messageType
                            + "'. Supported: success, error, warning");
        }

        try {
            new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds))
                    .pollingEvery(Duration.ofMillis(200))
                    .until(d -> expected.equals(detectVisibleToastType()));
            LOGGER.info("System message of type '{}' is displayed", expected);
            return true;
        } catch (TimeoutException e) {
            LOGGER.warn("Expected system message '{}', but detected='{}'. toast-stack HTML: {}",
                    expected, detectVisibleToastType(), getToastStackHtml());
            return false;
        }
    }

    /**
     * Waits until any toast/alert is visible and returns its type
     * ({@code success}, {@code error}, or {@code warning}), or {@code null} on timeout.
     */
    public String waitForVisibleSystemMessageType(int timeoutSeconds) {
        try {
            return new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds))
                    .pollingEvery(Duration.ofMillis(200))
                    .until(d -> {
                        String type = detectVisibleToastType();
                        return type == null ? null : type;
                    });
        } catch (TimeoutException e) {
            LOGGER.warn("No system message appeared within {}s. toast-stack HTML: {}",
                    timeoutSeconds, getToastStackHtml());
            return null;
        }
    }

    /**
     * Inspects currently visible toast/alert nodes and classifies them by
     * {@code data-test-id} first, then CSS class tokens — never by Arabic text.
     */
    private String detectVisibleToastType() {
        List<String> types = collectVisibleToastTypes();
        return types.isEmpty() ? null : types.get(0);
    }

    /** All distinct toast/alert types currently visible (order preserved). */
    private List<String> collectVisibleToastTypes() {
        List<String> types = new java.util.ArrayList<>();
        // Prefer stable data-test-id locators from frontend; keep class fallbacks.
        List<WebElement> candidates = driver.findElements(By.cssSelector(
                "[data-test-id^='toast-warning'],"
                        + "[data-test-id^='toast-success'],"
                        + "[data-test-id^='toast-error'],"
                        + "[data-test-id='global-toast-stack'] [data-test-id],"
                        + "[data-test-id='global-toast-stack'] > *,"
                        + "[data-test-id='global-toast-stack'] .toast-item,"
                        + "[data-test-id*='toast'][data-test-id*='success'],"
                        + "[data-test-id*='toast'][data-test-id*='error'],"
                        + "[data-test-id*='toast'][data-test-id*='warning'],"
                        + "[data-test-id*='alert'][data-test-id*='success'],"
                        + "[data-test-id*='alert'][data-test-id*='error'],"
                        + "[data-test-id*='alert'][data-test-id*='warning'],"
                        + "[data-test-id*='alert'][data-test-id*='danger'],"
                        + "app-global-toaster .toast-stack .toast-item,"
                        + "app-global-toaster .toast-stack > *,"
                        + "div.toast-item,"
                        + "div.alert.alert-success,"
                        + "div.alert.alert-danger,"
                        + "div.alert.alert-warning,"
                        + "div.alert.alert-error"));

        for (WebElement item : candidates) {
            try {
                if (!item.isDisplayed()) {
                    continue;
                }
                String type = classifyMessageType(
                        item.getAttribute("data-test-id"),
                        item.getAttribute("class"));
                if (type != null && !types.contains(type)) {
                    types.add(type);
                }
            } catch (StaleElementReferenceException ignored) {
                // Toast was redrawn mid-poll; try again on next iteration
            }
        }
        return types;
    }

    private String classifyMessageType(String dataTestId, String classAttr) {
        String fromTestId = classifyFromDataTestId(dataTestId);
        if (fromTestId != null) {
            return fromTestId;
        }
        return classifyFromCssClass(classAttr);
    }

    /** Prefer explicit type tokens in data-test-id (e.g. global-toast-success). */
    private String classifyFromDataTestId(String dataTestId) {
        if (dataTestId == null || dataTestId.isBlank()) {
            return null;
        }
        String id = dataTestId.toLowerCase().replace('_', '-').trim();
        // The stack container itself is not a message
        if (id.equals("global-toast-stack") || id.endsWith("-stack")) {
            return null;
        }
        if (id.contains("success")) {
            return "success";
        }
        if (id.contains("error") || id.contains("danger")) {
            return "error";
        }
        if (id.contains("warning") || id.contains("warn")) {
            return "warning";
        }
        return null;
    }

    private String classifyFromCssClass(String classAttr) {
        if (classAttr == null || classAttr.isBlank()) {
            return null;
        }
        String normalized = " " + classAttr.toLowerCase().replace('_', '-').trim() + " ";

        if (normalized.contains(" success ")
                || normalized.contains(" alert-success ")
                || normalized.contains(" toast-success ")
                || normalized.contains(" success-")
                || normalized.contains("-success ")) {
            return "success";
        }
        if (normalized.contains(" error ")
                || normalized.contains(" danger ")
                || normalized.contains(" alert-danger ")
                || normalized.contains(" alert-error ")
                || normalized.contains(" toast-error ")
                || normalized.contains(" error-")
                || normalized.contains("-error ")) {
            return "error";
        }
        if (normalized.contains(" warning ")
                || normalized.contains(" warn ")
                || normalized.contains(" alert-warning ")
                || normalized.contains(" toast-warning ")
                || normalized.contains(" warning-")
                || normalized.contains("-warning ")
                || normalized.contains(" warn-")
                || normalized.contains("-warn ")) {
            return "warning";
        }
        return null;
    }

    private WebElement findToastStackElement() {
        List<WebElement> primary = driver.findElements(TOAST_STACK);
        if (!primary.isEmpty()) {
            return primary.get(0);
        }
        List<WebElement> fallback = driver.findElements(TOAST_STACK_FALLBACK);
        return fallback.isEmpty() ? null : fallback.get(0);
    }

    private String getToastStackHtml() {
        try {
            WebElement stack = findToastStackElement();
            if (stack == null) {
                return "<toast-stack not found>";
            }
            return stack.getAttribute("innerHTML");
        } catch (Exception e) {
            return "<toast-stack not found>";
        }
    }

    /**
     * Ensures leftover toasts from a previous action are gone before asserting
     * a new message. Closes via the toast X buttons (never wipes innerHTML).
     */
    public PatientAdmissionPage waitForPreviousToastsToClear() {
        dismissVisibleToastsViaCloseButtons();
        waitUntilToastStackEmpty(2);
        LOGGER.info("Previous toasts cleared; ready for the next assertion");
        return this;
    }

    /**
     * Waits for the global toaster (app-global-toaster) to show a message
     * containing the given text and returns the full toast text.
     */
    public String waitForToastContaining(String expectedText) {
        By toastWithText = By.xpath(
                "//app-global-toaster//*[contains(normalize-space(.),'" + expectedText + "')]");
        WebElement toast = wait.until(ExpectedConditions.visibilityOfElementLocated(toastWithText));
        String message = toast.getText().trim();
        LOGGER.info("Validation toast visible: {}", message);
        return message;
    }

    /** Waits for any toast message to appear and returns its text. */
    public String waitForAnyToast() {
        wait.until(d -> {
            WebElement stack = d.findElement(TOAST_STACK);
            return !stack.getText().trim().isEmpty();
        });
        String message = driver.findElement(TOAST_STACK).getText().trim();
        LOGGER.info("Toast visible: {}", message);
        return message;
    }

    /** True if a toast containing the given text shows up within the wait window. */
    public boolean isToastVisibleContaining(String expectedText) {
        try {
            waitForToastContaining(expectedText);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    // =========================================================
    // State readers (for assertions)
    // =========================================================

    public String getArabicNameValue() {
        return arabicNameInput.getAttribute("value");
    }

    public String getEnglishNameValue() {
        return englishNameInput.getAttribute("value");
    }

    public String getMobileValue() {
        return mobileInput.getAttribute("value");
    }

    public String getNationalIdValue() {
        return nationalIdInput.getAttribute("value");
    }

    public String getBirthDateValue() {
        return birthDateInput.getAttribute("value");
    }

    /** The max attribute of the birth-date input (future dates are blocked above it). */
    public String getBirthDateMaxAttribute() {
        return birthDateInput.getAttribute("max");
    }

    public String getAgeYearsValue() {
        return ageYearsInput.getAttribute("value");
    }

    public String getAgeMonthsValue() {
        return ageMonthsInput.getAttribute("value");
    }

    /** Waits until the age-years field is auto-populated and returns its value. */
    public String waitForAgeYearsPopulated() {
        wait.until(d -> {
            String value = ageYearsInput.getAttribute("value");
            return value != null && !value.isBlank();
        });
        return getAgeYearsValue();
    }

    /** Waits until the age-months field equals {@code expectedMonths}. */
    public PatientAdmissionPage waitForAgeMonthsValue(String expectedMonths) {
        wait.until(d -> expectedMonths.equals(getAgeMonthsValue()));
        return this;
    }

    public String getInsuranceNumberValue() {
        return insuranceNumberInput.getAttribute("value");
    }

    public String getExpirationDateValue() {
        return expirationDateInput.getAttribute("value");
    }

    public String getOtherPhoneValue() {
        return otherPhoneInput.getAttribute("value");
    }

    public String getWhatsappValue() {
        return whatsappInput.getAttribute("value");
    }

    public String getAddressValue() {
        return addressInput.getAttribute("value");
    }

    public String getEmailValue() {
        return emailInput.getAttribute("value");
    }

    public String getNotesValue() {
        return notesTextarea.getAttribute("value");
    }

    public String getAddedByValue() {
        return addedByInput.getAttribute("value");
    }

    public String getAddedDateValue() {
        return addedDateInput.getAttribute("value");
    }

    public boolean isAddedByReadonly() {
        return addedByInput.getAttribute("readonly") != null
                || addedByInput.getAttribute("disabled") != null;
    }

    public boolean isAddedDateReadonly() {
        return addedDateInput.getAttribute("readonly") != null
                || addedDateInput.getAttribute("disabled") != null;
    }

    /**
     * Attempts to type into a read-only field. Returns {@code true} if the field
     * blocked the edit (value unchanged or element not editable).
     */
    public boolean tryTypeIntoAddedBy(String text) {
        String before = getAddedByValue();
        try {
            addedByInput.clear();
            addedByInput.sendKeys(text);
        } catch (Exception ignored) {
            // Not interactable / not editable — expected for readonly fields
        }
        String after = getAddedByValue();
        return before.equals(after);
    }

    public boolean tryTypeIntoAddedDate(String text) {
        String before = getAddedDateValue();
        try {
            addedDateInput.clear();
            addedDateInput.sendKeys(text);
        } catch (Exception ignored) {
            // Not interactable / not editable — expected for readonly fields
        }
        String after = getAddedDateValue();
        return before.equals(after);
    }

    /** The visible selected text of the gender ng-select ("" when nothing selected). */
    public String getGenderSelectedText() {
        return getNgSelectText(genderSelect);
    }

    /** The visible selected text of the client (الجهة) ng-select. */
    public String getClientSelectedText() {
        return getNgSelectText(clientSelect);
    }

    public String getReligionSelectedText() {
        return getNgSelectText(religionSelect);
    }

    public String getMaritalStatusSelectedText() {
        return getNgSelectText(maritalStatusSelect);
    }

    public String getJobSelectedText() {
        return getNgSelectText(jobSelect);
    }

    private boolean isNgSelectAtPlaceholder(WebElement ngSelect) {
        return getNgSelectText(ngSelect).isEmpty();
    }

    public boolean isGenderAtPlaceholder() {
        return getGenderSelectedText().isEmpty();
    }

    public boolean isReligionAtPlaceholder() {
        return getReligionSelectedText().isEmpty();
    }

    public boolean isMaritalStatusAtPlaceholder() {
        return getMaritalStatusSelectedText().isEmpty();
    }

    public boolean isJobAtPlaceholder() {
        return getJobSelectedText().isEmpty();
    }

    /** The date text shown in the top navbar (Arabic formatted). */
    public String getHeaderDateText() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(HEADER_DATE))
                .getText().trim();
    }

    public boolean isArabicNameMarkedInvalid() {
        return hasClass(arabicNameInput, "ng-invalid");
    }

    public boolean isMobileMarkedInvalid() {
        return hasClass(mobileInput, "ng-invalid");
    }

    /** True if any mandatory control is flagged invalid by Angular. */
    public boolean hasInvalidMandatoryFields() {
        return isArabicNameMarkedInvalid()
                || isMobileMarkedInvalid()
                || hasClass(birthDateInput, "ng-invalid")
                || hasClass(genderSelect, "ng-invalid");
    }

    public boolean isOnReceptionPage() {
        return driver.getCurrentUrl().contains("/reception");
    }

    // =========================================================
    // Internals
    // =========================================================

    private String getReceptionUrl() {
        return ConfigReader.getNewSystemUrl().replaceAll("/+$", "") + "/reception";
    }

    /**
     * Unlike contains("/reception"), this rejects patient-detail URLs such as
     * /reception/patient/12345, which retain the previously saved patient's data.
     */
    private boolean isExactReceptionUrl(String currentUrl) {
        if (currentUrl == null) {
            return false;
        }

        String withoutQueryOrFragment = currentUrl.split("[?#]", 2)[0]
                .replaceAll("/+$", "");
        return withoutQueryOrFragment.equalsIgnoreCase(getReceptionUrl());
    }

    private void typeInto(WebElement element, String text) {
        WebElement target = wait.until(ExpectedConditions.elementToBeClickable(element));
        target.clear();
        target.sendKeys(text);
    }

    private void setDateByJs(WebElement dateInput, String isoDate) {
        WebElement target = wait.until(ExpectedConditions.visibilityOf(dateInput));
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].value = arguments[1];"
                        + "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));"
                        + "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                target, isoDate);
    }

    /**
     * Locates an action button again on every retry. Angular replaces parts of
     * the form after Save, so a previously resolved PageFactory element can
     * become stale before the following click.
     */
    private void clickFresh(By locator) {
        wait.ignoring(StaleElementReferenceException.class).until(currentDriver -> {
            WebElement element = currentDriver.findElement(locator);
            if (!element.isDisplayed() || !element.isEnabled()) {
                return false;
            }

            try {
                element.click();
                return true;
            } catch (StaleElementReferenceException e) {
                LOGGER.debug("Element was redrawn before click; locating it again: {}", locator);
                return false;
            }
        });
    }

    /**
     * Same as {@link #clickFresh(By)} but falls back to a JS click when another
     * layer (open nav dropdown, modal backdrop) covers the target.
     */
    private void clickThroughOverlays(By locator) {
        WebElement element = wait.until(ExpectedConditions.presenceOfElementLocated(locator));
        ((JavascriptExecutor) driver).executeScript(
                "arguments[0].scrollIntoView({block:'center'});", element);
        try {
            clickFresh(locator);
        } catch (Exception e) {
            LOGGER.debug("Native click blocked for {} ({}); using JS click", locator, e.getClass().getSimpleName());
            WebElement fresh = driver.findElement(locator);
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", fresh);
        }
    }

    /**
     * Opens an ng-select, collects visible non-disabled option labels, closes the
     * panel without changing the selection when possible.
     */
    private List<String> getOpenNgSelectOptionTexts(WebElement ngSelect) {
        closeOpenNgDropdownPanels();
        WebElement select = wait.until(ExpectedConditions.elementToBeClickable(ngSelect));
        select.click();

        By options = By.cssSelector("ng-dropdown-panel .ng-option:not(.ng-option-disabled)");
        wait.until(ExpectedConditions.visibilityOfElementLocated(options));

        List<String> texts = new java.util.ArrayList<>();
        for (WebElement option : driver.findElements(options)) {
            try {
                if (!option.isDisplayed()) {
                    continue;
                }
                String text = option.getText().trim();
                if (!text.isBlank() && !texts.contains(text)) {
                    texts.add(text);
                }
            } catch (StaleElementReferenceException ignored) {
                // Option redraw mid-read
            }
        }
        closeOpenNgDropdownPanels();
        LOGGER.info("ng-select options: {}", texts);
        return texts;
    }

    /**
     * Selects an option from an ng-select component: opens the dropdown, types the
     * text when the inner input is searchable, then clicks the matching option.
     */
    private void selectNgOption(WebElement ngSelect, String optionText) {
        closeOpenNgDropdownPanels();
        WebElement select = wait.until(ExpectedConditions.elementToBeClickable(ngSelect));
        select.click();

        WebElement innerInput = select.findElement(By.cssSelector("input[role='combobox']"));
        if (innerInput.getAttribute("readonly") == null) {
            innerInput.sendKeys(optionText);
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

    /**
     * Opens an ng-select and clicks the first non-disabled option.
     * Retries because dependent dropdowns (e.g. شركة فرعية after جهة) load options
     * asynchronously — the panel can open empty for a moment.
     */
    private void selectFirstNgOption(WebElement ngSelect) {
        By panel = By.cssSelector("ng-dropdown-panel");
        By firstOption = By.cssSelector(
                "ng-dropdown-panel .ng-option:not(.ng-option-disabled)");

        RuntimeException lastError = null;
        for (int attempt = 1; attempt <= 4; attempt++) {
            try {
                closeOpenNgDropdownPanels();
                WebElement select = wait.until(ExpectedConditions.elementToBeClickable(ngSelect));
                if (!isNgSelectEnabled(select)) {
                    throw new IllegalStateException("ng-select is disabled; cannot pick an option");
                }
                select.click();

                wait.until(ExpectedConditions.presenceOfElementLocated(panel));
                WebElement option = new WebDriverWait(driver, Duration.ofSeconds(8))
                        .pollingEvery(Duration.ofMillis(200))
                        .until(ExpectedConditions.elementToBeClickable(firstOption));
                option.click();
                closeOpenNgDropdownPanels();
                LOGGER.info("Selected first available option from ng-select (attempt {})", attempt);
                return;
            } catch (RuntimeException e) {
                lastError = e;
                LOGGER.warn("selectFirstNgOption attempt {} failed: {}", attempt, e.getMessage());
                closeOpenNgDropdownPanels();
                try {
                    Thread.sleep(400L * attempt);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
        throw lastError != null
                ? lastError
                : new TimeoutException("Could not select the first ng-select option");
    }

    /**
     * After جهة (or similar parent) changes, wait until the dependent ng-select is
     * enabled and briefly settles so its options request can finish.
     */
    private void waitForDependentNgSelectToSettle(WebElement dependentSelect) {
        try {
            wait.until(ExpectedConditions.visibilityOf(dependentSelect));
            // May stay disabled for some جهة values — don't fail the parent selection
            new WebDriverWait(driver, Duration.ofSeconds(5))
                    .pollingEvery(Duration.ofMillis(200))
                    .until(d -> isNgSelectEnabled(dependentSelect));
        } catch (TimeoutException e) {
            LOGGER.info("Dependent ng-select still disabled after parent change (may be expected)");
            return;
        }
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    /** Dismisses any open ng-select panel so the next open is clean. */
    private void closeOpenNgDropdownPanels() {
        try {
            driver.switchTo().activeElement().sendKeys(Keys.ESCAPE);
        } catch (Exception ignored) {
            // No focused element
        }
        try {
            ((JavascriptExecutor) driver).executeScript(
                    "document.querySelectorAll('ng-dropdown-panel').forEach(p => p.remove());");
        } catch (Exception ignored) {
            // Best-effort cleanup
        }
    }

    /** Reads the visible value label of an ng-select; "" when nothing is selected. */
    private String getNgSelectText(WebElement ngSelect) {
        try {
            return ngSelect.findElement(By.cssSelector(".ng-value-label")).getText().trim();
        } catch (Exception e) {
            return "";
        }
    }

    private boolean hasClass(WebElement element, String cssClass) {
        String classes = element.getAttribute("class");
        return classes != null && classes.contains(cssClass);
    }

    private boolean isNgSelectEnabled(WebElement ngSelect) {
        return !hasClass(ngSelect, "ng-select-disabled");
    }
}
