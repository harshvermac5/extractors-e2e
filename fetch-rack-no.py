from selenium import webdriver
from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import filehandler
import time
import os

# ---------- Configuration ----------
SEARCH_FILE = 'search_terms.txt'
OUTPUT_FILE = 'rack_numbers.txt'
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
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless")  # Uncomment to run headless
    return webdriver.Chrome(options=options)

# ---------- Core Functions ----------
def open_new_tab(driver, url):
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)

def search_term(driver, term, wait):
    try:
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys(term)
        search_box.send_keys(Keys.RETURN)
        return True
    except Exception as e:
        print(f"[ERROR] Could not search for term '{term}': {e}")
        return False

def click_first_result_if_needed(driver, wait):
    foldertab_elements = driver.find_elements(By.ID, "foldertab")
    if foldertab_elements:
        print("[INFO] 'foldertab' found — already in correct view.")
        return True

    try:
        first_result = wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@class='slbcell vscell']//a[1]")))
        first_result.click()
        print("[INFO] Clicked first search result.")
        return True
    except Exception:
        try:
            no_results = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[1]")))
            if no_results.text.startswith("Nothing found"):
                print("[INFO] No results found.")
                return False
        except:
            print("[WARNING] Could not determine if results were found.")
        return False

def extract_rack_number(driver, wait):
    try:
        rackspace = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@id='foldertab']/li[4]/a")))
        
        if "Rackspace" in rackspace.text:
            rackspace.click()
        else:
            return "not assigned"

        rackno = wait.until(EC.presence_of_element_located((By.XPATH, "//center/h2[1]")))
        value = rackno.text.strip()
        if value:
            print(f"[SUCCESS] Extracted rack number: {value}")
            return value
    except Exception as e:
        print(f"[ERROR] Failed to extract rack number: {e}")
    
    return "not assigned"

def close_extra_tabs(driver):
    while len(driver.window_handles) > TAB_LIMIT:
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])

def process_term(driver, term, wait):
    open_new_tab(driver, BASE_URL)
    if not search_term(driver, term, wait):
        return "not assigned or found"
    
    if not click_first_result_if_needed(driver, wait):
        return "not assigned or found"

    return extract_rack_number(driver, wait)

# ---------- Main Program ----------
def main():
    driver = init_driver()
    wait = WebDriverWait(driver, WAIT_TIME)
    driver.get(BASE_URL)

    search_terms = filehandler.load_keywords_from_file(SEARCH_FILE)
    extracted_results = []

    filehandler.save_array_to_file([], OUTPUT_FILE)  # clear file once

    for index, term in enumerate(search_terms):
        print(f"\n[PROCESSING] Term {index + 1}/{len(search_terms)}: '{term}'")
        result = process_term(driver, term, wait)
        extracted_results.append(result)
        close_extra_tabs(driver)

        # ✅ Save every 5 searches
        if (index + 1) % 5 == 0:
            print(f"[INFO] Saving intermediate results after {index + 1} terms.")
            filehandler.save_array_to_file(extracted_results, OUTPUT_FILE)

    # Final save after all terms
    print("\n[INFO] Final save of all extracted values.")
    filehandler.save_array_to_file(extracted_results, OUTPUT_FILE)

    print("\n[COMPLETED] All values processed.")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
