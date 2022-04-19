from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import time # Set time interval
import tldextract # Get domain
import string # Reduce whitespaces
from urllib.parse import urlparse # Get path
import redis # Caching
from pymongo import MongoClient # Main DB
import asyncio


g_link_list = ["https://www.smartone.com/", "https://www.cmi.chinamobile.com/","https://www.three.com.hk/","https://www.citictel.com/","https://eshop.hk.chinamobile.com/tc/index.html"]
local_link_lst = []

def get_link(g_link):
    opts = webdriver.ChromeOptions()
    opts.add_argument("--disable-notifications, --headless")
    s = Service(r'C:\Users\davidl\Desktop\py_data_scraping\driver\chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=opts)
    domain = tldextract.extract(g_link).domain
    driver.get(g_link)
    # Scroll down & Make soup
    time.sleep(2)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        time.sleep(3)
        # Get new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')

    for element in soup.findAll('a', href=True):
        i_link = str(element.get('href'))
        doamin_check = tldextract.extract(i_link).domain
        if (i_link.startswith('http://') or i_link.startswith('https://')) and \
                (domain == doamin_check) and (i_link not in local_link_lst):
            local_link_lst.append(i_link)
    driver.close()
    driver.quit()
    

if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=2)
    executor.map(get_link, g_link_list)
    time.sleep(30)
    print(local_link_lst)

    
    







