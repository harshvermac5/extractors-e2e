import os
import time
import logging
import filehandler
from urllib.parse import quote
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# ---------- Logging Setup ----------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("automation.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# ---------- Configuration ----------
SEARCH_FILE = 'search_terms.txt'
OUTPUT_FILE = 'port_details.txt'
TAB_LIMIT = 5
WAIT_TIME = 10

# ---------- Environment Setup ----------
load_dotenv()
USERNAME = quote(os.getenv('E2E_USERNAME', '').strip())
PASSWORD = quote(os.getenv('E2E_PASSWORD', '').strip())
BASE_URL = f"https://{USERNAME}:{PASSWORD}@assets.e2enetworks.net/"

# ---------- WebDriver Setup ----------
def init_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--mute-audio")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-accelerated-2d-canvas")
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-cloud-import")
    options.add_argument("--disable-component-update")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-features=TranslateUI")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    return driver

# ---------- Page Validation ----------
def is_properties_page(driver, term):
    try:
        xpath_check = driver.find_element(By.XPATH, "//div[contains(@class, 'greynavbar')]//ul[@id='foldertab']")
        css_check = driver.find_element(By.CSS_SELECTOR, "div.greynavbar > ul#foldertab")
        logging.info("Confirmed: Properties page detected via both XPath and CSS.")
        return True
    except Exception as e:
        logging.warning(f"Properties page check failed for term '{term}': {e}")
        driver.save_screenshot(f"screenshot_properties_check_failed_{term.replace('.', '_')}.png")
        with open(f"debug_{term.replace('.', '_')}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        return False

def validate_properties_page(driver, wait, term):
    time.sleep(1)
    return is_properties_page(driver, term)

# ---------- Core Functions ----------
def open_new_tab(driver, url):
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)

def search_term(driver, term, wait):
    try:
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(term)
        search_box.send_keys(Keys.RETURN)
        return True
    except Exception as e:
        logging.error(f"Could not search for term '{term}': {e}")
        return False

def extract_port_details(driver, wait, term):
    for attempt in range(1, 4):
        try:
            view_tab = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//ul[@id='foldertab']/li[1]/a"))
            )

            if "View" in view_tab.text:
                view_tab.click()
            else:
                return "Not an assigned IP or Asset tag"
            
            time.sleep(1)

            port_details = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//tbody//tr//div[h2[translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='ports and links']]")
                )
            )
            value = port_details.text.strip()
            if value:
                logging.info(f"Extracted port_details  (attempt {attempt}): {value}")
                return value
        except Exception as e:
            logging.warning(f"Attempt {attempt} failed to extract port_details : {e}")
            if attempt < 3:
                logging.info(f"Retrying search for term '{term}'...")
                driver.refresh()
                time.sleep(2)
                if not search_term(driver, term, wait):
                    logging.error(f"Retry search failed for term '{term}'")
                    return f"Not found even after {attempt} attemps"
                if not validate_properties_page(driver, wait, term):
                    return "Not on properties page"
                time.sleep(2)

    logging.error(f"All attempts failed for term '{term}'")
    return "Not found after exhausting all attempts"

def click_first_search_result(driver, term):
    try:
        # Try locating the first result using XPath
        first_result = driver.find_element(By.XPATH, "/html/body/div/div[5]/div/table/tbody/tr[2]/td[1]/table/tbody/tr[1]/td[2]/a")
        driver.execute_script("arguments[0].scrollIntoView(true);", first_result)
        time.sleep(1)
        try:
            driver.execute_script("arguments[0].click();", first_result)
            logging.info("Clicked first search result via JS.")
        except Exception as js_error:
            logging.warning(f"JS click failed: {js_error}")
            logging.info("Trying ActionChains fallback...")
            try:
                actions = ActionChains(driver)
                actions.move_to_element(first_result).click().perform()
                logging.info("Clicked first search result via ActionChains.")
            except Exception as ac_error:
                logging.error(f"ActionChains click failed: {ac_error}")
                driver.save_screenshot(f"screenshot_click_failure_{term.replace('.', '_')}.png")
                return False
        return True
    except Exception as e:
        logging.error(f"Could not locate or click first search result for term '{term}': {e}")
        driver.save_screenshot(f"screenshot_no_search_result_{term.replace('.', '_')}.png")
        return False


def close_extra_tabs(driver):
    main_tab = driver.window_handles[0]
    while len(driver.window_handles) > TAB_LIMIT:
        for handle in driver.window_handles:
            if handle != main_tab:
                driver.switch_to.window(handle)
                driver.close()
                break
        driver.switch_to.window(main_tab)

def process_term(driver, term, wait):
    open_new_tab(driver, BASE_URL)
    if not search_term(driver, term, wait):
        return "Could not locate the search box"
    if not validate_properties_page(driver, wait, term):
        logging.info("Properties page not detected — attempting to click first search result.")
        if not click_first_search_result(driver, term):
            return "Failed to click first result"
        time.sleep(2)
        if not validate_properties_page(driver, wait, term):
            logging.error("Still not on properties page after clicking first result.")
            return "Properties page not found"

    return extract_port_details(driver, wait, term)

# ---------- Main Program ----------
def main():
    driver = init_driver()
    wait = WebDriverWait(driver, WAIT_TIME)
    driver.get(BASE_URL)

    search_terms = filehandler.load_keywords_from_file(SEARCH_FILE)
    extracted_results = []

    filehandler.save_array_to_file([], OUTPUT_FILE)

    for index, term in enumerate(search_terms):
        logging.info(f"Processing term {index + 1}/{len(search_terms)}: '{term}'")
        result = process_term(driver, term, wait)
        extracted_results.extend([term, result, "\n"])
        close_extra_tabs(driver)

        if (index + 1) % 5 == 0:
            logging.info(f"Saving intermediate results after {index + 1} terms.")
            filehandler.save_array_to_file(extracted_results, OUTPUT_FILE)

    logging.info("Final save of all extracted values.")
    filehandler.save_array_to_file(extracted_results, OUTPUT_FILE)

    logging.info("All values processed.")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
