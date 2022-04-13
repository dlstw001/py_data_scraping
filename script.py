from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import time # Set time interval
import tldextract # Get domain
import string # Reduce whitespaces
import redis # Caching

# Setting
redisClient = redis.Redis(host='localhost', port=6379, db=0)
opts = webdriver.ChromeOptions()
opts.add_argument("--disable-notifications, --headless")
s = Service(r'C:\Users\davidl\Desktop\py_data_scraping\driver\chromedriver.exe')
global_link_lst = ["https://www.ctonet.mx/"]
driver = webdriver.Chrome(service=s, options=opts)


# Function
def getsoup():
    time.sleep(2)
    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    return soup


def getlink(soup):
    for element in soup.findAll('a', href=True):
        link = str(element.get('href'))
        check = tldextract.extract(link).domain
        if (link.startswith('http://') or link.startswith('https://')) and \
                (domain == check) and (link not in local_link_lst):
            local_link_lst.append(link)


# Main Function
for g_link in global_link_lst:
    # Setting
    local_link_lst = []
    domain = tldextract.extract(g_link).domain
    driver.get(g_link)
    # Scroll down & Make soup
    g_soup = getsoup()
    # Get links from global
    getlink(g_soup)

    # Loop through local name list
    for l_link in local_link_lst:
        try:
            driver.get(l_link)
            # Scroll down & Make soup
            l_soup = getsoup()
            # Get links from local
            getlink(l_soup)
            # Get all the content and push to redis
            l_text = l_soup.text.translate({ord(c): None for c in string.whitespace})
            key = f'link-{global_link_lst.index(g_link)}-{local_link_lst.index(l_link)}'
            redisClient.hset(key, "link", l_link)
            redisClient.hset(key, "content", l_text)
            print(f'{key}: successful')
        except WebDriverException:
            print(f'{key}, {l_link}: failed')
            continue

print('Finished')




















