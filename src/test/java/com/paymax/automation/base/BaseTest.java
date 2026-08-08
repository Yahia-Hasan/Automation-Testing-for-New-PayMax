package com.paymax.automation.base;

import com.paymax.automation.config.ConfigReader;
import com.paymax.automation.helpers.LoginHelper;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Optional;
import org.testng.annotations.Parameters;

import java.time.Duration;

/**
 * Base test class that initializes one WebDriver per test class and tears it
 * down after all methods in that class finish.
 */
public abstract class BaseTest {

    private static final Logger LOGGER = LogManager.getLogger(BaseTest.class);
    private static final ThreadLocal<WebDriver> DRIVER = new ThreadLocal<>();

    protected WebDriver getDriver() {
        return DRIVER.get();
    }

    @Parameters("browser")
    @BeforeClass(alwaysRun = true)
    public void setUp(@Optional String browser) {
        String selectedBrowser = (browser == null || browser.isBlank())
                ? ConfigReader.getBrowser()
                : browser;

        LOGGER.info("Initializing WebDriver for browser: {}", selectedBrowser);
        WebDriver driver = createDriver(selectedBrowser.toLowerCase().trim());
        DRIVER.set(driver);

        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(ConfigReader.getImplicitWait()));
        driver.manage().window().maximize();
        // Intentionally does not navigate yet — use loginAndNavigateToNewSystem() for the auth bridge.
    }

    /**
     * TEMPORARY: authenticates via the legacy login page, selects a branch,
     * then opens the new system URL. Replace when native new-system login is ready.
     *
     * @see LoginHelper#loginAndNavigateToNewSystem()
     */
    protected void loginAndNavigateToNewSystem() {
        new LoginHelper(getDriver()).loginAndNavigateToNewSystem();
    }

    private WebDriver createDriver(String browser) {
        switch (browser) {
            case "chrome" -> {
                WebDriverManager.chromedriver().setup();
                ChromeOptions chromeOptions = new ChromeOptions();
                chromeOptions.addArguments("--remote-allow-origins=*");
                chromeOptions.addArguments("--disable-popup-blocking");
                // Avoid hanging the session on the native print dialog opened by barcode popup
                chromeOptions.addArguments("--kiosk-printing");
                chromeOptions.addArguments("--disable-blink-features=AutomationControlled");
                // Tolerate self-signed/internal certificates if the new system moves to HTTPS
                chromeOptions.setAcceptInsecureCerts(true);
                chromeOptions.addArguments("--ignore-certificate-errors");
                // The new system is plain HTTP on port 4040. Chrome silently upgrades
                // http:// to https:// (HTTPS-First mode); the server has no TLS, so the
                // request dies with ERR_CONNECTION_RESET. Disable all upgrade variants.
                chromeOptions.addArguments("--disable-features=HttpsUpgrades,HttpsFirstModeV2ForEngagedSites,HttpsFirstModeV2ForTypicallySecureUsers,HttpsFirstBalancedMode,HttpsFirstBalancedModeAutoEnable");
                java.util.Map<String, Object> prefs = new java.util.HashMap<>();
                prefs.put("https_only_mode_enabled", false);
                prefs.put("https_first_balanced_mode_enabled", false);
                chromeOptions.setExperimentalOption("prefs", prefs);
                chromeOptions.setExperimentalOption("excludeSwitches", java.util.Collections.singletonList("enable-automation"));
                chromeOptions.setExperimentalOption("useAutomationExtension", false);
                // EAGER: return after DOMContentLoaded — avoids hanging on SPAs that never reach "complete"
                chromeOptions.setPageLoadStrategy(org.openqa.selenium.PageLoadStrategy.EAGER);
                return new ChromeDriver(chromeOptions);
            }
            case "firefox" -> {
                WebDriverManager.firefoxdriver().setup();
                FirefoxOptions firefoxOptions = new FirefoxOptions();
                firefoxOptions.addPreference("dom.webdriver.enabled", false);
                firefoxOptions.addPreference("useAutomationExtension", false);
                return new FirefoxDriver(firefoxOptions);
            }
            default -> throw new IllegalArgumentException(
                    "Unsupported browser: '" + browser + "'. Supported values: chrome, firefox");
        }
    }

    @AfterClass(alwaysRun = true)
    public void tearDown() {
        WebDriver driver = DRIVER.get();
        if (driver != null) {
            LOGGER.info("Quitting WebDriver");
            driver.quit();
            DRIVER.remove();
        }
    }
}
