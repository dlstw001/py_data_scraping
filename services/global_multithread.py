from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import tldextract # Get domain
import time

url_lst = ["https://www.smartone.com/","https://eshop.hk.chinamobile.com/tc/index.html","https://www.cmi.chinamobile.com/","https://www.three.com.hk/"]
count = 0

def mainFunc(url):
    count = count + 1
    opts = webdriver.ChromeOptions()
    opts.add_argument("--disable-notifications")
    s = Service(r'C:\Users\davidl\Desktop\py_data_scraping\driver\chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=opts)
    domain = tldextract.extract(url).domain
    driver.get(url)
    # Scroll down & Make soup
    time.sleep(2)
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

    for element in soup.findAll('a', href=True):
        i_link = str(element.get('href'))
        doamin_check = tldextract.extract(i_link).domain
        if (i_link.startswith('http://') or i_link.startswith('https://')) and (i_link.endswith('.js') != True) and (domain == doamin_check) and (i_link not in url_lst):
            url_lst.append(i_link)
    
    

if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=5)
    while len(url_lst) > 0:
        executor.map(mainFunc, url_lst)
        time.sleep(5)
    print(count)





    
    







