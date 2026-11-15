import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.set_capability("acceptInsecureCerts", True)

driver = webdriver.Chrome(options=options)
try:
    # First set token in localStorage on 4040
    driver.get("https://196.218.246.250:4040/home")
    time.sleep(3)

    # Load session
    with open("session.json", "r", encoding="utf-8") as f:
        s = json.load(f)
    token = s.get("token")

    # Set cookies
    for name, val in s.get("cookies", {}).items():
        try:
            driver.add_cookie({"name": name, "value": val, "domain": "196.218.246.250", "path": "/"})
        except Exception:
            pass

    # Set localStorage
    driver.execute_script(f"window.localStorage.setItem('baymax_token', '{token}');")
    driver.get("https://196.218.246.250:4040/home")
    time.sleep(5)

    # 1. Get all loaded network resources
    resources = driver.execute_script("return window.performance.getEntriesByType('resource').map(r => r.name);")
    print("Loaded Resources:")
    for r in resources:
        if "api" in r or "json" in r or "config" in r or "env" in r or ".js" in r:
            print(" ", r)

    # 2. Check window objects
    win_env = driver.execute_script("""
        let info = {};
        for (let key of Object.keys(window)) {
            if (key.toLowerCase().includes('api') || key.toLowerCase().includes('url') || key.toLowerCase().includes('config') || key.toLowerCase().includes('env') || key.toLowerCase().includes('baymax')) {
                try {
                    info[key] = window[key];
                } catch(e) {}
            }
        }
        return info;
    """)
    print("\nWindow config/env:", json.dumps(win_env, indent=2, default=str))

    # 3. Search HTML for API URLs or ports (like 5250, 5000, 8080, api)
    html = driver.page_source
    print(f"\nHTML length: {len(html)}")
    with open("frontend_home.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved frontend_home.html")

finally:
    driver.quit()
