package com.paymax.automation.helpers;

import com.paymax.automation.config.ConfigReader;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverException;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.WindowType;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

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

    private static final By USERNAME_INPUT = By.id("txtInvUserName");
    private static final By PASSWORD_INPUT = By.id("txtInvPassword");
    private static final By LOGIN_BUTTON = By.id("btnLogin");
    private static final By BRANCHES_DDL_INPUT = By.id("ddlBranches_Input");
    private static final By CONTINUE_BUTTON = By.id("btnContinue");

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
        wait.until(ExpectedConditions.visibilityOfElementLocated(USERNAME_INPUT));
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
        branchInput.click();
        branchInput.sendKeys(Keys.CONTROL + "a");
        branchInput.sendKeys(branchName);

        // Telerik / RadComboBox style list item
        By branchOption = By.xpath(
                "//*[self::li or self::div][normalize-space()='" + branchName + "']");
        wait.until(ExpectedConditions.elementToBeClickable(branchOption)).click();
        LOGGER.info("Selected branch: {}", branchName);

        wait.until(ExpectedConditions.elementToBeClickable(CONTINUE_BUTTON)).click();
        LOGGER.info("Clicked Continue on branch selection page");
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
