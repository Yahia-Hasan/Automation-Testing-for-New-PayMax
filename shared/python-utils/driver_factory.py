import os
import tempfile
import logging
from typing import Optional, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from unified_config import UnifiedConfig

logger = logging.getLogger("SharedDriverFactory")

def create_driver(
    headless: Optional[bool] = None,
    window_size: Optional[Tuple[int, int]] = None,
    lang: str = "ar"
) -> webdriver.Chrome:
    """
    Creates and returns an optimized, robust Chrome WebDriver instance:
    1. Isolated temporary user-data-dir to prevent HSTS auto-redirects on legacy port 80.
    2. SSL error suppression for self-signed certificates on port 4040.
    3. Disabled modern Chrome automatic HTTPS-first upgrades.
    4. Configurable resolution and Arabic locale.
    """
    if headless is None:
        headless = UnifiedConfig.HEADLESS
    if window_size is None:
        window_size = (UnifiedConfig.WINDOW_WIDTH, UnifiedConfig.WINDOW_HEIGHT)

    options = Options()
    
    # 1. Isolated profile
    temp_profile = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_profile}")
    
    # 2. SSL & Security bypass
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-web-security")
    options.add_argument("--ignore-ssl-errors=yes")
    options.set_capability("acceptInsecureCerts", True)
    
    # 3. Disable Chrome HTTPS upgrades for legacy bridge
    options.add_argument("--disable-features=HttpsUpgrades,HttpsFirstModeV2,HttpsFirstBalancedMode,HttpsFirstModeV2ForEngagedSites,AutoupgradeMixedContent")
    
    # 4. Window, Locale & Rendering
    options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
    options.add_argument(f"--lang={lang}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    if headless:
        options.add_argument("--headless=new")
        
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        logger.warning(f"ChromeDriverManager install skipped or failed ({e}), falling back to default driver...")
        driver = webdriver.Chrome(options=options)
        
    driver.set_page_load_timeout(UnifiedConfig.DEFAULT_TIMEOUT + 15)
    if UnifiedConfig.IMPLICIT_WAIT > 0:
        driver.implicitly_wait(UnifiedConfig.IMPLICIT_WAIT)
        
    return driver
