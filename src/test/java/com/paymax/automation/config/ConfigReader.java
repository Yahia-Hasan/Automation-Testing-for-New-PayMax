package com.paymax.automation.config;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/**
 * Loads and exposes test configuration from config.properties on the classpath.
 */
public final class ConfigReader {

    private static final Properties PROPERTIES = new Properties();

    static {
        try (InputStream inputStream = ConfigReader.class
                .getClassLoader()
                .getResourceAsStream("config.properties")) {
            if (inputStream == null) {
                throw new IllegalStateException("config.properties not found on the classpath");
            }
            PROPERTIES.load(inputStream);
        } catch (IOException e) {
            throw new ExceptionInInitializerError("Failed to load config.properties: " + e.getMessage());
        }
    }

    private ConfigReader() {
        // Utility class
    }

    public static String getProperty(String key) {
        String value = PROPERTIES.getProperty(key);
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Missing or empty configuration key: " + key);
        }
        return value.trim();
    }

    public static String getBrowser() {
        return getProperty("browser");
    }

    public static String getBaseUrl() {
        return getProperty("base.url");
    }

    public static int getImplicitWait() {
        return Integer.parseInt(getProperty("implicit.wait"));
    }

    public static int getExplicitWait() {
        return Integer.parseInt(getProperty("explicit.wait"));
    }

    /** TEMPORARY: remove when the new login page replaces the legacy bridge. */
    public static String getLegacyLoginUrl() {
        return getProperty("legacy.login.url");
    }

    /** TEMPORARY: remove when the new login page replaces the legacy bridge. */
    public static String getLegacyUsername() {
        return getProperty("legacy.username");
    }

    /** TEMPORARY: remove when the new login page replaces the legacy bridge. */
    public static String getLegacyPassword() {
        return getProperty("legacy.password");
    }

    /** TEMPORARY: remove when the new login page replaces the legacy bridge. */
    public static String getLegacyBranch() {
        return getProperty("legacy.branch");
    }

    /** TEMPORARY: remove when the new login page replaces the legacy bridge. */
    public static String getLegacyLandingUrl() {
        return getProperty("legacy.landing.url");
    }

    /** TEMPORARY: remove when the new login page replaces the legacy bridge. */
    public static String getNewSystemUrl() {
        return getProperty("new.system.url");
    }
}
