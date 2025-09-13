import os, time, logging
from urllib.parse import quote
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

TAB_LIMIT = 5
WAIT_TIME = 10

logger = logging.getLogger(__name__)

load_dotenv()
USERNAME = quote(os.getenv('E2E_USERNAME', '').strip())
PASSWORD = quote(os.getenv('E2E_PASSWORD', '').strip())
BASE_URL = f"https://{USERNAME}:{PASSWORD}@assets.e2enetworks.net/"

def init_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/117.0.0.0 Safari/537.36")
    options.add_argument("--disable-accelerated-2d-canvas")
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-cloud-import")
    options.add_argument("--disable-component-update")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-features=TranslateUI")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--disable-software-rasterizer")
    return webdriver.Chrome(options=options)

def open_new_tab(driver, url):
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)

def close_extra_tabs(driver):
    main_tab = driver.window_handles[0]
    while len(driver.window_handles) > TAB_LIMIT:
        for handle in driver.window_handles:
            if handle != main_tab:
                driver.switch_to.window(handle)
                driver.close()
                break
        driver.switch_to.window(main_tab)

def search_term(driver, wait, term):
    try:
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(term)
        search_box.send_keys(Keys.RETURN)
        return True
    except Exception as e:
        logger.error(f"Search failed for '{term}': {e}")
        return False

def validate_properties_page(driver, wait, term):
    time.sleep(1)
    try:
        driver.find_element(By.CSS_SELECTOR, "div.greynavbar > ul#foldertab")
        return True
    except Exception:
        return False

def click_first_search_result(driver, term, debug_dir="debug"):
    try:
        first_result = driver.find_element(By.XPATH, "/html/body/div/div[5]/div/table/tbody/tr[2]/td[1]/table/tbody/tr[1]/td[2]/a")
        if safe_click(driver, first_result, term, debug_dir):
            return True
        else:
            screenshot_path = os.path.join(debug_dir, f"screenshot_click_failure_{term.replace('.', '_')}.png")
            driver.save_screenshot(screenshot_path)
            return False
    except Exception as e:
        logger.error(f"Click first result failed for '{term}': {e}")
        screenshot_path = os.path.join(debug_dir, f"screenshot_no_search_result_{term.replace('.', '_')}.png")
        driver.save_screenshot(screenshot_path)
        return False

def safe_click(driver, element, term, debug_dir="debug"):
    """Try JS click first, fallback to ActionChains."""
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)

        try:
            driver.execute_script("arguments[0].click();", element)
            logger.info("Clicked element via JS.")
            return True
        except Exception as js_error:
            logger.warning(f"JS click failed: {js_error}")

        try:
            ActionChains(driver).move_to_element(element).click().perform()
            logger.info("Clicked element via ActionChains.")
            return True
        except Exception as ac_error:
            screenshot_path = os.path.join(debug_dir, f"screenshot_safe_click_failure_{term.replace('.', '_')}.png")
            driver.save_screenshot(screenshot_path)
            logger.error(f"ActionChains click failed: {ac_error}")
            return False

    except Exception as e:
        logger.error(f"Could not scroll/click element for term '{term}': {e}")
        return False