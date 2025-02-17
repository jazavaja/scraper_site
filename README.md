# Web Scrapers for Divar, TalarKadeh, Instagram, and WhatsApp

This repository contains web scrapers for **Divar**, **TalarKadeh**, **Instagram**, and **WhatsApp**, built using **Selenium**, **Scrapy**, **Headless Chrome**, and **CSV** for data storage. These scrapers automate data extraction efficiently while handling challenges such as dynamic content, login authentication, and bot detection.

## 📌 Features
- ✅ **Divar Scraper**: Extracts listings, prices, and contact details.
- ✅ **TalarKadeh Scraper**: Scrapes event halls, pricing, and locations.
- ✅ **Instagram Scraper**: Fetches public profile details, posts, and hashtags.
- ✅ **WhatsApp Scraper**: Automates WhatsApp Web to extract chats, contacts, and media.
- ✅ **Uses Headless Chrome**: For efficient and automated browsing.
- ✅ **CSV Data Export**: Saves extracted data in a structured format.
- ✅ **Scrapy for Structured Crawling**: Efficient for handling paginated and structured websites.
- ✅ **Selenium for JavaScript-based Sites**: Handles interactive pages requiring automation.

## 🛠️ Technologies Used
- **Python** 🐍
- **Selenium** (for automating browser interactions)
- **Scrapy** (for structured web crawling)
- **Headless Chrome** (for efficient data scraping)
- **CSV** (for saving extracted data)

## 🚀 Installation

### 1. Clone the Repository
```sh
git clone https://github.com/your-username/web-scrapers.git
cd web-scrapers
```

### 2. Create a Virtual Environment (Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Install ChromeDriver (For Selenium)
Ensure you have the correct **ChromeDriver** version installed. Download it from:
[ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)

Place the `chromedriver` file in the project directory or set up the system path.

## 📖 Usage

Each scraper is in a separate directory. Navigate to the respective folder and run the script.

### 🏡 Divar Scraper
```sh
cd divar_scraper
python divar_scraper.py
```

### 🎉 TalarKadeh Scraper
```sh
cd talarkadeh_scraper
python talarkadeh_scraper.py
```

### 📷 Instagram Scraper
**Note**: Instagram has strict bot detection. Consider logging in with Selenium.
```sh
cd instagram_scraper
python instagram_scraper.py --username your_username
```

### 💬 WhatsApp Scraper
**Requires WhatsApp Web login**
```sh
cd whatsapp_scraper
python whatsapp_scraper.py
```

## ⚠️ Legal Disclaimer
This project is for **educational purposes only**. Scraping certain platforms may violate their terms of service. Use responsibly.

## 📩 Contact
For inquiries, feel free to reach out via:  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/javadsarlak)  
📧 Email: javadesmesh@gmail.com

---
