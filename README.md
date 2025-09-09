# 🧪 selenium-e2e

This repository contains Python automation scripts designed to streamline **inventory management** in **E2E Networks' internal asset portal** using **Selenium WebDriver**.

---

## 🚀 Features

Both `fetch-rack-no.py` and `fetch-port-details.py` share the same robust automation architecture with the following features:

* 🔍 **Automated asset lookup** using `search_terms.txt` as input (supports IP addresses or hostnames)
* 🧾 **Data extraction**:

  * `fetch-rack-no.py`: Extracts and saves rack numbers to `rack_numbers.txt`
  * `fetch-port-details.py`: Extracts and saves port details to `port_numbers.txt`
* 🔄 **Modular design** with well-structured functions for maintainability
* 🛡️ **Secure credential handling** via `.env` file (no hardcoded credentials)
* 💾 **Incremental data writing**: Saves output to `output.txt` every 5 records for better fault tolerance
* ⚙️ **Advanced element interaction** using JavaScript clicks and Selenium Action Chains
* 🧠 **Optimized memory usage**: Opens a maximum of 5 Chrome tabs concurrently
* 👻 **Runs in headless mode**: Enables silent, UI-free execution
* 🖼️ **Error diagnostics**:

  * Saves screenshots and HTML dumps for failed records
  * Helps with debugging portal behavior changes or login issues

---

## 📦 Dependencies

Install the required packages using pip:

```bash
pip install selenium python-dotenv
```

Make sure **ChromeDriver** is installed and available in your system's `PATH`.

---

## ⚙️ Setup & Usage

1. **Clone the repository**:

   ```bash
   git clone https://github.com/harshvermac5/selenium-e2e.git
   cd selenium-e2e
   ```

2. **Create a `.env` file** with your E2E portal credentials:

   ```env
   E2E_USERNAME="your_username"
   E2E_PASSWORD="your_password"
   ```

3. **Connect to the E2E VPN** to access the internal portal.

4. **Prepare input**:

   * Add a list of IP addresses or hostnames (one per line) to `search_terms.txt`

5. **Run the desired script**:

   * To fetch rack numbers:

     ```bash
     python3 fetch-rack-no.py
     ```
   * To fetch port details:

     ```bash
     python3 fetch-port-details.py
     ```

6. **View the output**:

   ```bash
   cat rack_numbers.txt
   cat port_numbers.txt
   ```

---

## 📁 Output Files

| File                  | Description                                       |
| --------------------- | ------------------------------------------------- |
| `rack_numbers.txt`    | Rack numbers extracted by `fetch-rack-no.py`      |
| `port_numbers.txt`    | Port details extracted by `fetch-port-details.py` |
| `output.txt`          | Incremental results (every 5 records)             |
| `failed_screenshots/` | Screenshots of failed cases                       |
| `failed_html_dumps/`  | HTML dumps for debugging failed records           |
| `automation.log`      | Logs the progress of script                       |

---

## 🧩 Notes

* Scripts are intended for **internal use** within E2E Networks.
* Ensure you're using a **compatible version of Chrome** and **ChromeDriver**.
* Extend or modify the scripts as needed for other automation within the portal.


⚠️ **Warning:** : This code is provided "as is", **without any warranty of any kind**, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement.

The author(s) shall **not be held liable for any damages** arising from the use of this tool.