# 📘 Asset Automation Extractor

Automates search and extraction of asset information (ports, racks, etc.) from the **E2E Asset Management Portal** using Selenium.

---

## ✨ Features

* 🔍 **Automated search** for Asset Tags / IPs from an input file.
* 📑 **Extractor modules** for different data types:

  * `ports` → extracts *Ports & Links* information.
  * `racks` → extracts *Rack number* information.
* 🧭 **Robust navigation**:

  * Handles multiple search attempts.
  * Confirms *Properties Page* before extraction.
  * Clicks elements using **JS click** with **ActionChains fallback**.
* 🛠 **Tab management** — prevents too many open tabs (`TAB_LIMIT`).
* 📂 **Debug mode**:

  * Saves page source and screenshots on failure in `debug/`.
  * Logs all actions to `debug/automation.log`.
* ⏳ **Resilient retries** — up to 3 attempts per term if failures occur.
* 🖥 **Headless mode** — runs without a visible browser window.

---

## 📦 Dependencies

Install required dependencies:

```bash
pip install selenium python-dotenv
```

This will automatically install:

* **Google Chrome** (latest stable).
* **ChromeDriver** matching your Chrome version (ensure it’s in your PATH).

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```ini
E2E_USERNAME=your-username
E2E_PASSWORD=your-password
```

Credentials are automatically URL-encoded.

---

## 📂 Project Structure

```
.
├── main.py               # Entry point
├── webhandler.py         # Browser and navigation helpers
├── filehandler.py        # File I/O utilities
├── extractors/
│   ├── ports.py          # Ports & Links extractor
│   └── racks.py          # Rack number extractor
├── search_terms.txt      # Input search keywords
├── debug/                # Logs, screenshots, HTML dumps
│   └── automation.log
└── results_ports.txt     # Example output
```

---

## 🚀 Usage

### Run an extractor

```bash

# Clone the repository
git clone https://github.com/harshvermac5/extractors-e2e.git

# Change into the folder
cd extractors-e2e

# Run the main file with parameter
python main.py <extractor>
```

Where `<extractor>` can be:

* `ports` → extract *Ports & Links*.
* `racks` → extract *Rack number*.

Example:

```bash
python main.py ports
```

---

## 📤 Input & Output

### Input file: `search_terms.txt`

* Each line contains one Asset Tag or IP to search.

Example:

```
NMNE-000
SPK-X-0000
SPK-D-0000
```

### Output files

Each extractor writes results to its own file:

* `results_ports.txt`
* `results_racks.txt`

---

## 🪲 Debugging

If something fails:

* Check **`debug/automation.log`** for detailed logs.
* Screenshots and page dumps are saved in `debug/`.

  * Example:

    * `screenshot_click_failure_NMNE-479.png`
    * `debug_NMNE-479.html`

---

## ⚠️ Notes & Warnings

* ❗ **Fragile DOM locators**: Some XPaths rely on the current structure of the E2E portal. If the UI changes, locators must be updated.
* ❗ **Headless issues**: Some interactions may fail in headless mode. Run without `--headless=new` for debugging.
* 📄 **Rate limits**: Excessive requests may slow down or trigger portal protections.
* 💾 **Output overwrite**: Results file is cleared at the start of each run.
