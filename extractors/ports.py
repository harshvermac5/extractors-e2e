import time, logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webhandler import safe_click


OUTPUT_FILE = "results_ports.txt"

logger = logging.getLogger(__name__)

def extract(driver, wait, term, web):
    for attempt in range(1, 4):
        try:
            view_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@id='foldertab']/li[1]/a")))
            if "View" in view_tab.text:
                if not safe_click(driver, view_tab, term):
                    return "Failed to click View tab"
            else:
                return "Not an assigned IP or Asset tag"

            port_details = wait.until(
                EC.presence_of_element_located((By.XPATH, "//tbody//tr//div[h2[translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='ports and links']]"))
            )
            return port_details.text.strip()
        
        except Exception as e:
            logger.warning(f"[{term}] Attempt {attempt} failed: {e}")
            if attempt < 3:
                driver.refresh()
                web.search_term(driver, wait, term)
                if not web.validate_properties_page(driver, wait, term):
                    return "Not on properties page"
                
    return "Failed to extract port details"
