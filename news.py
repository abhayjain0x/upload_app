from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json 
import telebot 
import random 
import logging 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_urls_and_titles():
    logger.info("Scraping URLs and titles...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("start-maximized")
    options.binary_location = '/app/.apt/usr/bin/google-chrome'

    driver = webdriver.Chrome(executable_path='/app/.chromedriver/bin/chromedriver', options=options)
    driver.get('https://hype.replicate.dev/')

    time.sleep(10)

    links = driver.find_elements(By.TAG_NAME, 'a')
    urls_and_titles = [{"url": link.get_attribute('href'), "title": link.text} for link in links[6:-2]]

    driver.quit()

    with open('maal.json', 'w') as json_file:
        json.dump(urls_and_titles, json_file, indent=4)
        logger.info("URLs and titles scraped and saved to maal.json")
    

API_TOKEN = '7384734320:AAFv5pWnSMiAsjw0OYs8Y7lEjKPnMlBAEBA'

channel_id = '-1002151986147'
bot = telebot.TeleBot(API_TOKEN)

def send_mes():

    try:
        with open('maal.json', 'r') as json_file:
            data = json.load(json_file)
            logger.info("URLs and titles loaded from maal.json")
    except FileNotFoundError:
        logger.info("maal.json not found, scraping URLs and titles...")
        scrape_urls_and_titles()
        with open('maal.json', 'r') as json_file:
            data = json.load(json_file)
        logger.info("URLs and titles scraped and saved to maal.json")
    except json.JSONDecodeError:
        logger.info("maal.json not found, scraping URLs and titles...")
        scrape_urls_and_titles()
        with open('maal.json', 'r') as json_file:
            data = json.load(json_file)
        logger.info("URLs and titles scraped and saved to maal.json")
    
    while data:
        item = data.pop(0)
        message = f"`[✠]` Title: `{item['title']}`\n`[✠]` URL: {item['url']}\n`━━━━━━━━━━━━━━━━━━━━━━━━`"

        images = ['aiwaifu2.jpg', 'aiwaifu.jpg']
        try:
            with open(random.choice(images), 'rb') as image_file:
                bot.send_photo(channel_id, image_file, caption=message, parse_mode="Markdown")
                logger.info(f"{item['title']} sent to channel")
        except FileNotFoundError:
            with open('aiwaifu.jpg', 'rb') as image_file:
                bot.send_photo(channel_id, image_file, caption=message, parse_mode="Markdown")
        
        with open('maal.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
            logger.info("URLs and titles updated")

        
        time.sleep(120)

send_mes()
