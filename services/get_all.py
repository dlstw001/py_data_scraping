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


redisClient = redis.Redis(host='localhost', port=6379, db=0)
opts = webdriver.ChromeOptions()
opts.add_argument("--disable-notifications, --headless")
s = Service(r'C:\Users\davidl\Desktop\py_data_scraping\driver\chromedriver.exe') # Browser driver location

global_link_lst = ["https://www.smartone.com/"]
""" keywords = ['peplink','Peplink','SD-WAN','WIFI'] """

driver = webdriver.Chrome(service=s, options=opts)
cluster = "mongodb+srv://admin:admin@cluster0.zuec9.mongodb.net/test"
client = MongoClient(cluster)


def get_all():
    # Main Script
    for g_link in global_link_lst:
        # Create local list for iteration
        local_link_lst = []
        local_link_lst.append(g_link)
        domain = tldextract.extract(g_link).domain

        # Loop through local list
        for l_link in local_link_lst:
            try:              
                driver.get(l_link)

                # Scroll down & Make soup
                time.sleep(3)
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

                # Get links from soup
                for element in soup.findAll('a', href=True):
                    link = str(element.get('href'))
                    doamin_check = tldextract.extract(link).domain
                    if (link.startswith('http://') or link.startswith('https://')) and \
                            (domain == doamin_check) and (link not in local_link_lst):
                        local_link_lst.append(link)

                r""" # Check repeated data
                key = f'link-{global_link_lst.index(g_link)}-{local_link_lst.index(l_link)}'
                link_check = redisClient.hget(key, "link")
                if link_check == None:
                    # Get data and submit to redis
                    content = soup.text.translate({ord(c): None for c in string.whitespace})
                    redisClient.hset(key, "link", l_link)
                    redisClient.hset(key, "content", content)
                    redisClient.expire(key, 28800)
                    # Get matches and submit to mongodb (Need to add peplink.com/estore link check)
                    path = urlparse(l_link).path
                    db = client.data
                    data = db.match
                    result = {}
                    for word in keywords:
                        count = content.count(word)
                        if count > 0:
                            result[word] = count
                    match = {'link': l_link, 'domain': domain, 'path': path, 'result': result}
                    data.insert_one(match)
                    print('All data submitted')
                else:
                    print('Data already existed') """

            except WebDriverException:
                key = f'link-{global_link_lst.index(g_link)}-{local_link_lst.index(l_link)}'
                print(f'{key}, {l_link}: failed')
                continue


