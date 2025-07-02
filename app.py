import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
LOGIN_EMAIL = "armoore4@gmail.com"
LOGIN_PASS  = "HunterKaylee100@"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-agent="
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.5735.90 Safari/537.36")

driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

# ایک مرکزی ویٹ آبجیکٹ بنا لیں
wait = WebDriverWait(driver, 20)          # 20 ثانیے تک کوشش کرے گا

# STEP 1: Login page کھولیں
driver.get(
    "https://auth.bstock.com/oauth2/authorize?"
    "client_id=1b094c5f-c8a6-416c-8c62-4dc77ca88ce9&"
    "email=armoore4%40gmail.com&"
    "redirect_uri=https%3A%2F%2Fbstock.com%2Facct%2Flogin&"
    "response_type=code&scope=offline_access&"
    "state=%7B%22role%22%3A%22buyer%22%2C%22isEnterpriseUser%22%3Afalse%2C"
    "%22identityProviderType%22%3A%22FUSIONAUTH%22%7D"
)

# ❶ پاس ورڈ فیلڈ نظر آنے تک رُکیں
password_box = wait.until(
    EC.presence_of_element_located((By.NAME, "password"))
)
password_box.send_keys(LOGIN_PASS)

# ❷ سب مٹ بٹن کلک کرنے سے پہلے یہ یقینی بنائیں کہ بٹن enable ہے
submit_btn = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
)
submit_btn.click()

# ❸ جب تک ری ڈائریکٹ مکمل نہ ہو جائے URL میں اس پیٹرن کا انتظار کریں
time.sleep(20)

print("✅ Page Title:", driver.title)
print("✅ URL:", driver.current_url)

with open("output.json", "r") as file:
    urls = json.load(file)
data = []
for url in urls:
    # ٹارگٹ آکشن پیج کھولیں اور اس کا بھی ویٹ رکھیں
    try:
        title = driver.find_element(By.XPATH,'//div[@class="product-name"]//h1').text
    except:
        title = ""
    driver.get(url)
    time.sleep(4)
    items = driver.find_elements(By.XPATH, '//tr[@class="StyledTableCells__StyledTR-sc-834be6c8-5 dABxwA"]')
    if items :
        print(f'positive:{url}')
        print(len(items))
        count = 0
        for item in items:
            count += 1
            print(count)
            data.append(
                {
                    "Pallet ID" : item.find_element(By.XPATH, './/td[1]' ).text,
                    "#Item" : item.find_element(By.XPATH, './/td[2]' ).text,
                    "Product Class" : item.find_element(By.XPATH, './/td[3]' ).text,
                    "Category Code" : item.find_element(By.XPATH, './/td[4]' ).text,
                    "Seller Category" : item.find_element(By.XPATH, './/td[5]' ).text,
                    "Item Description" : item.find_element(By.XPATH, './/td[6]' ).text,
                    "Qty" : item.find_element(By.XPATH, './/td[7]' ).text,
                    "Unit Retail" : item.find_element(By.XPATH, './/td[8]' ).text,
                    "Ext. Retail" : item.find_element(By.XPATH, './/td[9]' ).text,
                    "Origin" : item.find_element(By.XPATH, './/td[10]' ).text,
                    "UPC" : item.find_element(By.XPATH, './/td[11]' ).text,
                    "TCIN" : item.find_element(By.XPATH, './/td[12]' ).text,
                    "Brand" : item.find_element(By.XPATH, './/td[13]' ).text,
                    "Division" : item.find_element(By.XPATH, './/td[14]' ).text,
                    "Subcategory" : item.find_element(By.XPATH, './/td[15]' ).text,
                    "Department" : item.find_element(By.XPATH, './/td[16]' ).text,
                    "Category" : item.find_element(By.XPATH, './/td[17]' ).text,
                    "Subcategory" : item.find_element(By.XPATH, './/td[18]' ).text,
                    "Condition" : item.find_element(By.XPATH, './/td[19]' ).text,
                    "Optoro Condition" : item.find_element(By.XPATH, './/td[20]' ).text,

                }
            )
    else:
        print(f'nagitive:{url}')
import pdb;pdb.set_trace()
df = pd.DataFrame(data)

# CSV file save karo
# df.to_csv('output.csv', index=False)
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))

# print("✅ Auction page loaded")
# import pdb;pdb.set_trace()