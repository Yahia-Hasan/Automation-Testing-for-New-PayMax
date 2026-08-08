package com.paymax.automation.tests;

import com.paymax.automation.base.BaseTest;
import com.paymax.automation.config.ConfigReader;
import org.testng.Assert;
import org.testng.annotations.Test;

/**
 * Verifies the temporary legacy-login bridge lands on the new system home.
 */
public class LoginTest extends BaseTest {

    @Test(description = "Login via legacy system and open the new Paymax home URL")
    public void verifyLoginAndNavigateToNewSystem() {
        loginAndNavigateToNewSystem();

        String currentUrl = getDriver().getCurrentUrl();
        Assert.assertTrue(
                currentUrl.contains(":4040"),
                "Expected new system URL on port 4040, but was: " + currentUrl);

        String title = getDriver().getTitle();
        Assert.assertNotNull(title, "Page title should not be null");
        Assert.assertFalse(title.isBlank(), "Page title should not be blank");
    }
}
