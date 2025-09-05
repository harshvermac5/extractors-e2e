# 🧪 selenium-e2e

This repository contains multiple Python automation script that streamlines inventory management in **E2E Networks' internal asset portal** using Selenium WebDriver.

---

## 📦 Dependencies

Install required packages using pip:

```bash
pip install selenium python-dotenv
```

---

## 🚀 Features for "fetch-rack-no.py"

- 🔍 Automates search for multiple assets using `search_terms.txt`
- 🧾 Extracts and stores rack numbers in `rack_numbers.txt`
- 🔄 Modular design with clearly separated functions for each task
- 🛡️ Secure credential handling via `.env` file
- 💾 Writes results incrementally to `output.txt` every 5 records for reliability
- 🔗 Requires VPN access to connect to E2E internal services

