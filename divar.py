import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random
import os


class DivarScraper:
    def __init__(self, profile_path):
        self.profile_path = profile_path
        self.ads_list = []
        self.driver = None

    def _initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={self.profile_path}")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36"
        )
        print("Initializing browser...")
        time.sleep(1)
        return webdriver.Chrome(options=chrome_options)

    def search_ads(self, search_query):
        print(f"Opening Divar website...")
        baseUrl = input("Enter the base URL: ")
        if baseUrl == '':
            baseUrl = "https://divar.ir/s/tehran"
        self.driver.get(baseUrl)
        time.sleep(2)

        print(f"Searching for '{search_query}'...")
        search_box = self.driver.find_element(By.CLASS_NAME, "kt-nav-text-field__input")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

    def extract_ads(self, output_file, how_many_page=30):
        print("Extracting ads from search results...")
        seen_ads = set()
        scroll_attempts = 0

        while scroll_attempts < how_many_page:  # محدود کردن تعداد اسکرول برای جلوگیری از مسدود شدن
            scroll_distance = random.randint(600, 1200)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
            time.sleep(random.uniform(1, 3))  # تاخیر تصادفی بین اسکرول‌ها

            ad_elements = self.driver.find_elements(By.CLASS_NAME, "kt-post-card__action")
            new_ads = []  # ذخیره آگهی‌های جدید در این لیست
            for ad in ad_elements:
                link = ad.get_attribute("href")
                if link and link not in seen_ads:  # بررسی لینک‌های معتبر و غیرتکراری
                    seen_ads.add(link)
                    try:
                        title = ad.find_element(By.CLASS_NAME, "kt-post-card__title").text
                    except Exception as e:
                        title = "عنوان نامشخص"
                        print(f"Error retrieving title: {e}")
                    new_ad = {"title": title, "link": link, "contact": None}
                    new_ads.append(new_ad)  # فقط آگهی جدید اضافه می‌شود

            self.ads_list.extend(new_ads)  # افزودن آگهی‌های جدید به لیست اصلی
            self.save_to_csv(output_file, new_ads, mode="a")  # ذخیره فقط آگهی‌های جدید در فایل

            if len(new_ads) == 0:  # اگر آگهی جدیدی اضافه نشد، شمارنده افزایش پیدا می‌کند
                scroll_attempts += 1
            else:
                scroll_attempts = 0

        print(f"Found {len(self.ads_list)} ads.")

    def process_ad(self, ad, output_file):
        if ad['contact'].strip() == '':
            try:
                print(f"Processing ad: {ad['title']}...")
                self.driver.get(ad['link'])
                time.sleep(random.uniform(2, 5))  # تاخیر تصادفی برای جلوگیری از رفتار ربات‌گونه
                contact_button = self.driver.find_element(By.CLASS_NAME, "post-actions__get-contact")
                contact_button.click()
                time.sleep(random.uniform(5, 15))  # تأخیر 15 تا 30 ثانیه بین هر درخواست

                contact_element = self.driver.find_element(By.XPATH, "//a[starts-with(@href, 'tel:')]")
                ad['contact'] = contact_element.get_attribute("href").replace("tel:", "")
                print(f"Contact number retrieved: {ad['contact']}")

                # Load existing ads and update the ad if it exists
                self.update_ad_in_csv(output_file, ad)
            except Exception as e:
                ad['contact'] = -1
                self.update_ad_in_csv(output_file, ad)
                print(f"Failed to retrieve contact for {ad['title']}: We save contact number -1")
        else:
            print("Contact number is Exist : ", ad['contact'])

    @staticmethod
    def save_to_csv(output, ads, mode='w'):
        file_exists = os.path.isfile(output)
        print(f"Saving ads to {output}...")
        with open(output, mode=mode, encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "link", "contact"])
            if mode == 'w' or (not file_exists):
                writer.writeheader()  # فقط یکبار هدر نوشته می‌شود، در حالت 'w'
            writer.writerows(ads)
        print("File saved successfully.")

    def load_csv_to_list(self, csv_file_path):
        try:
            with open(csv_file_path, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                self.ads_list = [row for row in reader]
            print(f"Data loaded successfully from {csv_file_path}.")
        except FileNotFoundError:
            raise Exception(f"File not found: {csv_file_path}")
        except Exception as e:
            raise Exception(f"An error occurred while reading the file: {e}")

    def remove_duplicate_ads(self, output_file):
        print(f"Removing duplicates from {output_file}...")

        # Read the existing ads from CSV
        ads = []
        if os.path.isfile(output_file):
            with open(output_file, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                ads = [row for row in reader]

        # Create a dictionary to store unique ads based on their link
        unique_ads = {}
        for ad in ads:
            link = ad['link']
            if link not in unique_ads:
                unique_ads[link] = ad
            else:
                # If the ad already exists, check if it has a contact number
                if ad['contact'] and ad['contact'] != '-1':
                    unique_ads[link] = ad  # Keep the ad with the contact number

        # Convert the unique_ads dictionary back to a list
        unique_ads_list = list(unique_ads.values())

        # Save the unique ads back to the CSV file
        self.save_to_csv(output_file, unique_ads_list, mode="w")
        print("Duplicates removed and file updated successfully.")

    def clean_invalid_ads(self, input_file, output_file, removed_file):
        print(f"Cleaning invalid ads from {input_file}...")

        # Read the existing ads from CSV
        valid_ads = []
        invalid_ads = []
        if os.path.isfile(input_file):
            with open(input_file, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for ad in reader:
                    if ad['contact'] and ad['contact'] != '-1':
                        valid_ads.append(ad)  # Keep ads with valid contact
                    else:
                        invalid_ads.append(ad)  # Add invalid ads to separate list

        # Save the valid ads back to the original CSV
        self.save_to_csv(output_file, valid_ads, mode="w")

        # Save the invalid ads to a new file
        if invalid_ads:
            self.save_to_csv(removed_file, invalid_ads, mode="w")
            print(f"Removed ads saved to {removed_file}.")
        else:
            print("No invalid ads found.")

        print(f"File cleaned and saved to {output_file}.")

    def update_ad_in_csv(self, output_file, updated_ad):
        # Read the existing ads from CSV
        ads = []
        if os.path.isfile(output_file):
            with open(output_file, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                ads = [row for row in reader]

        # Create a dictionary to store unique ads based on their link
        ad_found = False
        for ad in ads:
            if ad['link'] == updated_ad['link']:
                ad['contact'] = updated_ad['contact']
                ad_found = True
                break

        # If the ad wasn't found, add it as new (no duplicates)
        if not ad_found:
            ads.append(updated_ad)

        # Save the updated list of ads to the CSV file
        self.save_to_csv(output_file, ads, mode="w")

    def run(self, get_choice):
        try:
            if get_choice == 2:
                search_query = input("چیزی که میخوای جستجو کنی رو اینجا بزن:\n")
                output_file = input("نام فایل رو بنویس: ") + '.csv'
                page = int(input(" چند صفحه بررسی شود  \n"))
                self.driver = self._initialize_driver()
                self.search_ads(search_query)
                self.extract_ads(output_file, page)
            elif get_choice == 1:
                which_file_read = input("\n: نام فایلی که میخواهی از داخلش بخونه رو بگو با نام کامل")
                self.load_csv_to_list(which_file_read)
                try:
                    self.driver = self._initialize_driver()
                    for ad in self.ads_list:
                        self.process_ad(ad, which_file_read)
                except Exception as e:
                    print(f"Error while initializing driver: {e}")
                    raise
            elif get_choice == 3:
                input_file = input("نام فایل رو بنویس :   ")
                self.remove_duplicate_ads(input_file)
            elif get_choice == 4:
                input_file = input("فایلی که قصد دارید دیتاهارا پاکسازی کنید وارد نمایید")
                output_file = input("فایلی که قصد دارید خروجی خالص باشه وارد کن")
                harz_file = input("فایلی که قصد دارید اگهی های هرز باشد وارد کن")
                self.clean_invalid_ads(input_file,output_file,harz_file)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if self.driver:
                self.driver.quit()


def get_choice():
    print("1 - دریافت شماره آگهی‌ها از فایل")
    print("2 - ساخت فایل بر اساس یک جستجو")
    print("3 -حذف تکراری ها")
    print("4 - پاکسازی داده ها و ذخیره فایل خالص")

    while True:
        try:
            choice = int(input("\nشماره گزینه مورد نظر خود را وارد کنید : ").strip())
            if choice in [1, 2, 3,4]:
                return choice
            else:
                print("ورودی نامعتبر است. لطفاً یکی از گزینه‌های را انتخاب کنید.")
        except ValueError:
            print("لطفاً یک عدد وارد کنید.")


# تنظیمات و اجرای کد
if __name__ == "__main__":
    PROFILE_PATH = r"C:\path\to\custom\profile"

    GET_CHOICE = get_choice()
    scraper = DivarScraper(PROFILE_PATH)
    scraper.run(GET_CHOICE)
