package com.paymax.automation.helpers;

import com.paymax.automation.config.ConfigReader;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverException;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.WindowType;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;

/**
 * TEMPORARY bridge for authenticating via the legacy .NET login,
 * selecting a branch, then manually opening the new system URL.
 * <p>
 * Delete or replace this class once the new login page is available.
 */
public final class LoginHelper {

    private static final Logger LOGGER = LogManager.getLogger(LoginHelper.class);
    private static final int NEW_SYSTEM_NAV_RETRIES = 3;
    private static final long RETRY_DELAY_MS = 2000L;

    private static final By WORKSPACE_HOSPITAL_BUTTON = By.id("btnWorkspaceHospital");
    private static final By WORKSPACE_HOSPITAL_FALLBACK = By.xpath(
            "//*[@id='btnWorkspaceHospital']"
                    + " | //*[contains(@id,'btnWorkspaceHospital')]"
                    + " | //*[contains(normalize-space(),'Open Hospital') or contains(normalize-space(),'Hospital')]"
                    + "[self::button or self::a or contains(@class,'btn') or contains(@class,'card') or contains(@class,'workspace')]");

    private static final By USERNAME_INPUT = By.id("txtInvUserName");
    private static final By PASSWORD_INPUT = By.id("txtInvPassword");
    private static final By LOGIN_BUTTON = By.id("btnLogin");
    private static final By BRANCHES_DDL_INPUT = By.id("ddlBranches_Input");
    private static final By BRANCHES_DDL_ARROW = By.cssSelector("#ddlBranches_Arrow, .rcbArrowCell a, #ddlBranches .rcbArrow");
    private static final By CONTINUE_BUTTON = By.cssSelector("#btnContinue, [id$='btnContinue'], input[name*='btnContinue']");

    private final WebDriver driver;
    private final WebDriverWait wait;

    public LoginHelper(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(ConfigReader.getExplicitWait()));
    }

    /**
     * Logs in through the legacy system, selects branch "Ad Doqi",
     * waits for the landing page, then navigates to the new system.
     */
    public void loginAndNavigateToNewSystem() {
        LOGGER.info("TEMPORARY: starting legacy login bridge to new system");

        openLegacyLoginPage();
        submitLegacyCredentials();
        selectBranchAndContinue();
        waitForLegacyLandingPage();

        LOGGER.info("Opening new tab to navigate to the new system");
        driver.switchTo().newWindow(WindowType.TAB);
        openNewSystem();

        LOGGER.info("TEMPORARY: navigated to new system at {}", driver.getCurrentUrl());
    }

    private void openLegacyLoginPage() {
        String loginUrl = ConfigReader.getLegacyLoginUrl();
        LOGGER.info("Opening legacy login page: {}", loginUrl);
        driver.get(loginUrl);
        chooseWorkspaceIfPresent();
        wait.until(ExpectedConditions.visibilityOfElementLocated(USERNAME_INPUT));
    }

    /**
     * Handles the "Choose your workspace" screen if present by clicking the Hospital tab (btnWorkspaceHospital).
     */
    private void chooseWorkspaceIfPresent() {
        try {
            WebDriverWait waitWorkspace = new WebDriverWait(driver, Duration.ofSeconds(8));
            waitWorkspace.until(d -> !d.findElements(WORKSPACE_HOSPITAL_BUTTON).isEmpty()
                    || !d.findElements(WORKSPACE_HOSPITAL_FALLBACK).isEmpty()
                    || !d.findElements(USERNAME_INPUT).isEmpty());

            WebElement workspaceBtn = null;
            List<WebElement> exactMatches = driver.findElements(WORKSPACE_HOSPITAL_BUTTON);
            for (WebElement el : exactMatches) {
                if (el.isDisplayed()) {
                    workspaceBtn = el;
                    break;
                }
            }
            if (workspaceBtn == null) {
                List<WebElement> fallbacks = driver.findElements(WORKSPACE_HOSPITAL_FALLBACK);
                for (WebElement el : fallbacks) {
                    if (el.isDisplayed()) {
                        workspaceBtn = el;
                        break;
                    }
                }
            }

            if (workspaceBtn != null) {
                LOGGER.info("Workspace selection screen detected. Clicking Hospital workspace (btnWorkspaceHospital)");
                ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", workspaceBtn);
                try {
                    wait.until(ExpectedConditions.elementToBeClickable(workspaceBtn)).click();
                } catch (Exception e) {
                    LOGGER.info("Standard click intercepted; clicking Hospital workspace via JS");
                    ((JavascriptExecutor) driver).executeScript("arguments[0].click();", workspaceBtn);
                }

                // If clicking opens a new tab or window, switch to the active one
                if (driver.getWindowHandles().size() > 1) {
                    for (String handle : driver.getWindowHandles()) {
                        driver.switchTo().window(handle);
                    }
                }
                LOGGER.info("Hospital workspace (btnWorkspaceHospital) clicked successfully");
            } else {
                LOGGER.info("Workspace screen not displayed or already bypassed; continuing to login form");
            }
        } catch (Exception e) {
            LOGGER.info("Workspace selection screen was not displayed or already bypassed: {}", e.getMessage());
        }
    }

    private void submitLegacyCredentials() {
        WebElement username = wait.until(ExpectedConditions.elementToBeClickable(USERNAME_INPUT));
        username.clear();
        username.sendKeys(ConfigReader.getLegacyUsername());

        WebElement password = wait.until(ExpectedConditions.elementToBeClickable(PASSWORD_INPUT));
        password.clear();
        password.sendKeys(ConfigReader.getLegacyPassword());

        wait.until(ExpectedConditions.elementToBeClickable(LOGIN_BUTTON)).click();
        LOGGER.info("Submitted legacy login credentials");
    }

    private void selectBranchAndContinue() {
        wait.until(ExpectedConditions.urlContains("frmSelectBranch.aspx"));
        LOGGER.info("Branch selection page opened: {}", driver.getCurrentUrl());

        String branchName = ConfigReader.getLegacyBranch();
        WebElement branchInput = wait.until(ExpectedConditions.elementToBeClickable(BRANCHES_DDL_INPUT));

        // 1. Try selecting via Telerik RadComboBox JS API directly
        boolean jsSelected = false;
        try {
            Object result = ((JavascriptExecutor) driver).executeScript(
                    "try {"
                            + "  var combo = (window.$find && (window.$find('ddlBranches') || window.$find(document.querySelector(\"[id$='ddlBranches']\")?.id)));"
                            + "  if (combo) {"
                            + "    var item = combo.findItemByText(arguments[0]);"
                            + "    if (!item) {"
                            + "      for (var i = 0; i < combo.get_items().get_count(); i++) {"
                            + "        var it = combo.get_items().getItem(i);"
                            + "        if (it.get_text().indexOf(arguments[0]) !== -1) { item = it; break; }"
                            + "      }"
                            + "    }"
                            + "    if (item) { item.select(); return true; }"
                            + "  }"
                            + "} catch(e) {}"
                            + "return false;",
                    branchName);
            jsSelected = Boolean.TRUE.equals(result);
            if (jsSelected) {
                LOGGER.info("Selected branch '{}' via Telerik RadComboBox JS API", branchName);
            }
        } catch (Exception e) {
            LOGGER.debug("Telerik JS API select branch skipped: {}", e.getMessage());
        }

        // 2. UI interaction fallback or confirmation if not selected via JS
        String currentVal = branchInput.getAttribute("value");
        if (!jsSelected || currentVal == null || currentVal.isBlank()) {
            LOGGER.info("Selecting branch via UI interaction for: {}", branchName);

            // Open dropdown via arrow or input click
            try {
                List<WebElement> arrows = driver.findElements(BRANCHES_DDL_ARROW);
                if (!arrows.isEmpty() && arrows.get(0).isDisplayed()) {
                    arrows.get(0).click();
                } else {
                    branchInput.click();
                }
            } catch (Exception e) {
                branchInput.click();
            }

            sleepQuietly(300);

            // Type branch name to filter
            branchInput.sendKeys(Keys.CONTROL + "a");
            branchInput.sendKeys(branchName);

            sleepQuietly(400);

            // Look for matching dropdown option in Telerik list
            By branchOption = By.xpath(
                    "//div[contains(@class,'rcbSlide') or contains(@class,'rcbDropDown')]//li[contains(normalize-space(),'" + branchName + "')]"
                            + " | //li[contains(@class,'rcbItem') and contains(normalize-space(),'" + branchName + "')]"
                            + " | //*[self::li or self::div][contains(@class,'rcb') and contains(normalize-space(),'" + branchName + "')]");

            try {
                WebElement optionEl = new WebDriverWait(driver, Duration.ofSeconds(4))
                        .until(ExpectedConditions.visibilityOfElementLocated(branchOption));
                try {
                    optionEl.click();
                } catch (Exception e) {
                    ((JavascriptExecutor) driver).executeScript("arguments[0].click();", optionEl);
                }
            } catch (Exception e) {
                LOGGER.warn("Could not click branch option in dropdown list, sending ENTER: {}", e.getMessage());
                branchInput.sendKeys(Keys.ENTER);
            }

            // Also send TAB to commit selection
            branchInput.sendKeys(Keys.TAB);
        }

        // 3. Ensure branch input has a value before continuing (prevents clicking Continue prematurely)
        try {
            new WebDriverWait(driver, Duration.ofSeconds(5)).until(d -> {
                String val = branchInput.getAttribute("value");
                return val != null && !val.isBlank();
            });
            LOGGER.info("Branch input populated with value: '{}'", branchInput.getAttribute("value"));
        } catch (Exception e) {
            LOGGER.warn("Branch input still appears blank after selection attempts");
        }

        sleepQuietly(500);

        // 4. Click Continue button
        WebElement continueBtn = wait.until(ExpectedConditions.elementToBeClickable(CONTINUE_BUTTON));
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView({block:'center'});", continueBtn);
        try {
            continueBtn.click();
        } catch (Exception e) {
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", continueBtn);
        }
        LOGGER.info("Clicked Continue on branch selection page");

        // 5. If still on frmSelectBranch after 3 seconds, retry clicking Continue
        try {
            new WebDriverWait(driver, Duration.ofSeconds(3))
                    .until(ExpectedConditions.not(ExpectedConditions.urlContains("frmSelectBranch.aspx")));
        } catch (TimeoutException e) {
            if (driver.getCurrentUrl() != null && driver.getCurrentUrl().contains("frmSelectBranch.aspx")) {
                LOGGER.warn("Still on frmSelectBranch.aspx after 3s. Re-clicking continue button via JS...");
                ((JavascriptExecutor) driver).executeScript("arguments[0].click();", continueBtn);
            }
        }
    }

    private void waitForLegacyLandingPage() {
        String expectedLanding = ConfigReader.getLegacyLandingUrl();
        wait.until(ExpectedConditions.urlContains("frmLandingPage.aspx"));
        LOGGER.info("Legacy landing page reached: {} (expected {})", driver.getCurrentUrl(), expectedLanding);

        // Brief settle so session cookies can be established after login
        try {
            new WebDriverWait(driver, Duration.ofSeconds(5))
                    .until(d -> !d.manage().getCookies().isEmpty());
        } catch (Exception ignored) {
            LOGGER.warn("No cookies detected after legacy login; continuing to new system");
        }

        sleepQuietly(1500);
    }

    /**
     * Opens the new system URL with retries.
     * ERR_CONNECTION_RESET means the host/port reset the TCP connection —
     * navigation was attempted, but the network/server rejected it.
     */
    private void openNewSystem() {
        String newSystemUrl = ConfigReader.getNewSystemUrl();
        WebDriverException lastError = null;

        // Fail faster on flaky network resets instead of waiting the default page load timeout
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));

        for (int attempt = 1; attempt <= NEW_SYSTEM_NAV_RETRIES; attempt++) {
            try {
                LOGGER.info("Navigating to new system URL (attempt {}/{}): {}",
                        attempt, NEW_SYSTEM_NAV_RETRIES, newSystemUrl);

                if (attempt == 1) {
                    driver.get(newSystemUrl);
                } else {
                    // JS fallback — Chromedriver still waits for load; EAGER strategy short-circuits
                    ((JavascriptExecutor) driver)
                            .executeScript("window.location.assign(arguments[0]);", newSystemUrl);
                }

                if (isOnNewSystem()) {
                    LOGGER.info("New system URL loaded successfully: {}", driver.getCurrentUrl());
                    return;
                }
            } catch (WebDriverException e) {
                lastError = e;
                // Page may still have navigated before the load-timeout fired
                if (isOnNewSystem()) {
                    LOGGER.warn("Page load timed out, but already on new system URL: {}",
                            driver.getCurrentUrl());
                    return;
                }
                LOGGER.warn("Failed to open new system on attempt {}/{}: {}",
                        attempt, NEW_SYSTEM_NAV_RETRIES, e.getMessage());
                sleepQuietly(RETRY_DELAY_MS);
            }
        }

        throw new WebDriverException(
                "Could not open new system URL after " + NEW_SYSTEM_NAV_RETRIES
                        + " attempts: " + newSystemUrl
                        + ". Check that http://196.218.246.250:4040 is reachable from this machine "
                        + "(open it manually in Chrome). Root cause is usually ERR_CONNECTION_RESET "
                        + "(server/firewall/port), not skipped navigation.",
                lastError);
    }

    private boolean isOnNewSystem() {
        try {
            String currentUrl = driver.getCurrentUrl();
            return currentUrl != null && currentUrl.contains(":4040");
        } catch (WebDriverException e) {
            return false;
        }
    }

    private static void sleepQuietly(long millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
