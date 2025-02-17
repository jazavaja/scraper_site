from selenium.webdriver.chrome import webdriver
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



class InstagramScraper:
    def __init__(self, profile_path):
        self.profile_path = profile_path
        self.ads_list = []
        self.driver = None

    def _initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={self.profile_path}")
        # chrome_options.add_argument("--proxy-server=http://185.18.250.177:80")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36"
        )
        print("Initializing browser...")
        time.sleep(1)
        return webdriver.Chrome(options=chrome_options)

    def cleanup(self):
        if self.driver:
            print("Closing the browser...")
            self.driver.quit()

    def load_site_instagram(self):
        try:
            self.driver = self._initialize_driver()
            print("Navigating to Instagram...")
            self.driver.get("https://www.instagram.com")
            print("Instagram loaded successfully!")
            time.sleep(20)
        except Exception as e:
            print(f"Error while loading Instagram: {e}")
            self.cleanup()
            raise

    def run(self):
        try:
            self.load_site_instagram()
            input("Press Enter to close the browser...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.cleanup()


if __name__ == "__main__":
    PROFILE_PATH = r"C:\path\to\custom\instagram_profile"
    instagram = InstagramScraper(PROFILE_PATH)
    instagram.run()
