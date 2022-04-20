import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import tldextract # Get domain
from urllib.parse import urlparse # Get path
from pymongo import MongoClient # Main DB
import time

url_lst = ["https://www.smartone.com/"]

async def mainFunc(url,count):
    opts = webdriver.ChromeOptions()
    opts.add_argument("--disable-notifications")
    s = Service(r'C:\Users\davidl\Desktop\py_data_scraping\driver\chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=opts)
    domain = tldextract.extract(url).domain
    driver.get(url)
    # Scroll down & Make soup
    await asyncio.sleep(2)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        time.sleep(2)
        # Get new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    def get_link():
        for element in soup.findAll('a', href=True):
            i_link = str(element.get('href'))
            doamin_check = tldextract.extract(i_link).domain
            if (i_link.startswith('http://') or i_link.startswith('https://')) and (i_link.endswith('.js') != True) and (domain == doamin_check) and (i_link not in url_lst):
                url_lst.append(i_link)
    get_link()
    url_lst.pop(0)
    driver.close()

    
async def main():
    t0 = time.time()
    count = 0
    while len(url_lst) > 0 :
        for url in url_lst:
            get_link = asyncio.create_task(mainFunc(url,count))
        await get_link
    print(count)
    t1 = time.time()
    print(f'Time needed : {t1-t0}')


asyncio.run(main())

