from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import tldextract
import html2text


# Setting
text_maker = html2text.HTML2Text()
text_maker.ignore_links = True
text_maker.ignore_images = True
opts = webdriver.ChromeOptions()
opts.add_argument("--disable-notifications, --headless")
s = Service(r'C:\Users\davidl\Desktop\py_data_scraping\driver\chromedriver.exe')
global_link_lst = ["https://www.smartone.com/tc/home/"]
link = "https://www.smartone.com/tc/home/"
driver = webdriver.Chrome(service=s, options=opts)


domain = tldextract.extract(link).domain
for link in global_link_lst:
    driver.get(link)

    # Scroll down until the end
    time.sleep(3)
    previous_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            break

    # Make BeautifulSoup
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    text = html2text.html2text(soup.prettify())
    print(text)
