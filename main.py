import time, logging, sys, os
import filehandler, webhandler as web
from selenium.webdriver.support.ui import WebDriverWait
from extractors import ports, racks  # add more extractors here

DEBUG_DIR = "debug"
os.makedirs(DEBUG_DIR, exist_ok=True)


# ---------- Logging Setup ----------
log_path = os.path.join(DEBUG_DIR, "automation.log")

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(
            sys.stdout
        )
    ]
)



SEARCH_FILE = "search_terms.txt"

EXTRACTORS = {
    "ports": ports,
    "racks": racks,
    # "servers": servers (future)
}

def process_terms(extractor_key):
    extractor = EXTRACTORS[extractor_key]
    output_file = extractor.OUTPUT_FILE  # 🔹 each extractor controls its own output

    driver = web.init_driver()
    wait = WebDriverWait(driver, web.WAIT_TIME)
    driver.get(web.BASE_URL)

    search_terms = filehandler.load_keywords_from_file(SEARCH_FILE)
    extracted_results = []
    filehandler.save_array_to_file([], output_file)

    for index, term in enumerate(search_terms):
        logging.info(f"Processing {term} with {extractor_key}")
        web.open_new_tab(driver, web.BASE_URL)

        if not web.search_term(driver, wait, term):
            result = "Search failed"
        elif not web.validate_properties_page(driver, wait, term):
            if not web.click_first_search_result(driver, term):
                result = "No result found"
            else:
                result = extractor.extract(driver, wait, term, web)
        else:
            result = extractor.extract(driver, wait, term, web)

        extracted_results.extend([term, str(result), "\n"])
        web.close_extra_tabs(driver)

        if (index + 1) % 5 == 0:
            filehandler.save_array_to_file(extracted_results, output_file)

    filehandler.save_array_to_file(extracted_results, output_file)
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <extractor>")
        print(f"Available extractors: {', '.join(EXTRACTORS.keys())}")
        sys.exit(1)

    extractor_key = sys.argv[1].lower()
    if extractor_key not in EXTRACTORS:
        print(f"Invalid extractor '{extractor_key}'. Available: {', '.join(EXTRACTORS.keys())}")
        sys.exit(1)

    process_terms(extractor_key)
