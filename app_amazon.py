import json
import time
import pandas as pd
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

LOGIN_EMAIL = "armoore4@gmail.com"
LOGIN_PASS = "HunterKaylee100@"

def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent="
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.5735.90 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
    return driver

def login(driver):
    wait = WebDriverWait(driver, 20)
    driver.get(
        "https://auth.bstock.com/oauth2/authorize?client_id=1b094c5f-c8a6-416c-8c62-4dc77ca88ce9&email=armoore4%40gmail.com&redirect_uri=https%3A%2F%2Fbstock.com%2Facct%2Flogin&response_type=code&scope=offline_access&state=%7B%22isEnterpriseUser%22%3Atrue%2C%22identityProviderType%22%3A%22FUSIONAUTH%22%2C%22redirectAfterLogin%22%3A%22%2Fall-auctions%22%7D"
    )
    password_box = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_box.send_keys(LOGIN_PASS)
    submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    submit_btn.click()
    time.sleep(8)
    print("✅ Logged in!")

def scrape_url(driver, url):
    wait = WebDriverWait(driver, 8)
    driver.get(url)
    time.sleep(2)

    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="product-name"]//h1')))
    except TimeoutException:
        print("❌ Main element not found after navigation. Skipping.")
        return None

    def safe_get(xpath):
        try:
            return driver.find_element(By.XPATH, xpath).text
        except:
            return ""

    def get_manifest():
        try:
            raw = driver.find_element(By.XPATH,"//button[@class='button' and contains(@onclick, 'window.open')]").get_attribute("onclick")
            if raw:
                return raw.replace("window.open('","").replace("');",""), "yes"
        except:
            pass
        return "", "No"

    title = safe_get('//div[@class="product-name"]//h1')
    current_bit = safe_get('//span[@id="current_bid_amount"]')
    avg_unit = safe_get('//span[@id="unit_per_price_span"]')
    address = safe_get('//address[@id="softcheckout-display-address"]')
    close_in = safe_get('//span[@id="auction_time_remaining"]')
    close_date = safe_get('//span[@id="auction_end_time"]')
    manifest_url, manifest_status = get_manifest()

    return {
        "id": driver.current_url.rstrip('/').split('/')[-1],
        "title": title,
        "current_bit": current_bit,
        "avergae_per_unit": avg_unit,
        "address": address,
        "close_in": close_in,
        "close_date": close_date,
        "minifest_url": manifest_url,
        "minifest_status": manifest_status,
        "url": driver.current_url
    }

def connect_db():
    return mysql.connector.connect(
        host="dbaas-db-4996826-do-user-21691157-0.f.db.ondigitalocean.com",
        user="doadmin",
        password="AVNS_Xf8UURLVY69Q2X4UO2q",  # ← Change if your DB has password
        database="Bstock",  # ← Replace with your DB
        port = 25060
    )

def insert_to_db(cursor, item):
    try:
        cursor.execute("""
            INSERT INTO bstock_auctions (
                id, title, current_bit, avergae_per_unit,
                address, close_in, close_date,
                minifest_url, minifest_status, url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                title=VALUES(title),
                current_bit=VALUES(current_bit),
                avergae_per_unit=VALUES(avergae_per_unit),
                address=VALUES(address),
                close_in=VALUES(close_in),
                close_date=VALUES(close_date),
                minifest_url=VALUES(minifest_url),
                minifest_status=VALUES(minifest_status),
                url=VALUES(url)
        """, (
            item["id"],
            item["title"],
            item["current_bit"],
            item["avergae_per_unit"],
            item["address"],
            item["close_in"],
            item["close_date"],
            item["minifest_url"],
            item["minifest_status"],
            item["url"]
        ))
        conn.commit()
    except Exception as e:
        print(f"❌ DB Insert Error for {item['id']}: {e}")

### Start scraping

with open("output.json", "r") as file:
    urls = json.load(file)
print(f"json urls : {len(urls)}")
conn = connect_db()
cursor = conn.cursor()

batch_size = len(urls)//3
urls = urls[:batch_size]
print(len(urls))

names = [item['name'] for item in urls]
names = list(set(names))
count = 0
for i in range(0, len(names)):

    filtered_urls = [item for item in urls if item['name'] == names[i]]
    
    driver = create_driver()
    login(driver)
    login_counter = 0

    for url in filtered_urls:
        print(count)
        print(count+1)

        print("🔗 Scraping:", url['url'])
        result = scrape_url(driver, url['url'])

        if not result or result["title"] == "":
            print("⚠️ Title not found. Trying re-login...")
            driver.quit()
            driver = create_driver()
            login(driver)
            result = scrape_url(driver, url['url'])

        if result:
            insert_to_db(cursor, result)

    driver.quit()


cursor.close()
conn.close()
print("✅ All data inserted into the database.")
