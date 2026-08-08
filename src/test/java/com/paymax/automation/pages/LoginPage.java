package com.paymax.automation.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

/**
 * Sample Login Page Object.
 * Replace the placeholder locators with real selectors for your application.
 */
public class LoginPage extends BasePage {

    // TODO: Replace these example locators with real ones for Paymax
    @FindBy(id = "username")
    private WebElement usernameField;

    @FindBy(id = "password")
    private WebElement passwordField;

    @FindBy(css = "button[type='submit']")
    private WebElement loginButton;

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    public LoginPage enterUsername(String username) {
        usernameField.clear();
        usernameField.sendKeys(username);
        return this;
    }

    public LoginPage enterPassword(String password) {
        passwordField.clear();
        passwordField.sendKeys(password);
        return this;
    }

    public void clickLogin() {
        loginButton.click();
    }

    public void login(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        clickLogin();
    }

    public String getPageTitle() {
        return driver.getTitle();
    }
}
