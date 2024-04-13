import os
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
from time import time
import datetime
import logging

date = datetime.datetime.now().strftime('%d-%m-%Y')

start_time = time()

logging.basicConfig(level=logging.DEBUG)

opts = ChromeOptions()

# AnimeCorner - Friday
# Anitrendz - Sunday


options = [
    "--headless", #Background usage
    "--disable-gpu", #Disable GPU Usage
    "--ignore-certificate-errors",
    "--disable-dev-shm-usage", 
    "--incognito", 
]

for option in options:
    opts.add_argument(option)

logging.info("Opening the browser")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
# driver.maximize_window()



logging.info("Opening Anitrendz")

driver.get("https://www.anitrendz.com/")
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "Navbar_logoContainer__fnjlx")))

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "simple-tabpanel-0")))
elements = driver.find_elements(By.ID, "simple-tabpanel-0")

logging.debug("Getting the image")
# elements[0].find_element(By.TAG_NAME, "img").get_attribute("src")
at_image = elements[0].find_element(By.TAG_NAME, "img").get_attribute("src")
at_time = time()
at_image


logging.info("Opening AnimeCorner")
driver.get("https://animecorner.me/category/anime-corner/rankings/anime-of-the-week/")
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "penci-mainlogo")))

logging.debug("Closing popups, if any")
try:
    driver.find_element(By.ID, "dismiss-button").click()
    logging.debug("Popup found, closed it")
except:
    pass

logging.info("Finding the latest article")
elems = driver.find_elements(By.CLASS_NAME, "penci-entry-title")
new_link = elems[0].find_element(By.TAG_NAME, "a").get_attribute("href")

logging.info("Opening the latest rankings page")
driver.get(new_link)
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "penci-mainlogo")))

logging.debug("Closing popups, if any")
try:
    driver.find_element(By.ID, "dismiss-button").click()
    logging.debug("Popup found, closed it")
except:
    pass

logging.debug("Finding the image (this takes long for AC)")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "wp-block-image")))
ac_image = driver.find_element(By.CLASS_NAME, "wp-block-image").find_element(By.TAG_NAME, "img").get_attribute("src")
ac_time = time()
ac_image

logging.info("Closing the browser")
driver.quit()

logging.info("Saving the data")

if "anime_images.json" in os.listdir():
    with open("anime_images.json", "r") as f:
        data = json.load(f)
else:
    data = {}


date_key = datetime.datetime.utcfromtimestamp(at_time).strftime('%d-%m-%Y')
data[date_key] = {
    "anitrendz": 
    {
        "last_updated_utc": int(at_time), 
        "image_url": at_image
    }, 
    "animecorner": 
    {
        "last_updated_utc": int(ac_time), 
        "image_url": ac_image
    }
}

with open("anime_images.json", "w") as f:
    json.dump(data, f, indent=4)

logging.info("Data saved")

logging.info(f"Total time taken: {int(time()-start_time)} seconds")