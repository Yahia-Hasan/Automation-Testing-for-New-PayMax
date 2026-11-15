package com.paymax.automation.config;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Properties;

/**
 * Loads and exposes test configuration from shared/config/config.properties
 * or config.properties on the classpath.
 */
public final class ConfigReader {

    private static final Properties PROPERTIES = new Properties();

    static {
        boolean loaded = false;
        
        // Priority 1: System property 'config.path'
        String customPath = System.getProperty("config.path");
        if (customPath != null && !customPath.isBlank()) {
            loaded = tryLoadFromFile(Paths.get(customPath));
        }

        // Priority 2: shared/config/config.properties relative to working dir or project dir
        if (!loaded) {
            String[] candidatePaths = {
                "shared/config/config.properties",
                "../shared/config/config.properties",
                "../../shared/config/config.properties"
            };
            for (String candidate : candidatePaths) {
                if (tryLoadFromFile(Paths.get(candidate))) {
                    loaded = true;
                    break;
                }
            }
        }

        // Priority 3: Classpath resource
        if (!loaded) {
            try (InputStream inputStream = ConfigReader.class
                    .getClassLoader()
                    .getResourceAsStream("config.properties")) {
                if (inputStream != null) {
                    PROPERTIES.load(inputStream);
                    loaded = true;
                }
            } catch (IOException ignored) {
            }
        }

        if (!loaded) {
            throw new IllegalStateException("config.properties not found in shared/config/ or on classpath");
        }
    }

    private static boolean tryLoadFromFile(Path path) {
        File file = path.toFile();
        if (file.exists() && file.isFile()) {
            try (FileInputStream fis = new FileInputStream(file)) {
                PROPERTIES.load(fis);
                return true;
            } catch (IOException ignored) {
            }
        }
        return false;
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
