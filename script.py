from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time


# Setting
opts = webdriver.ChromeOptions()
opts.add_argument("--disable-notifications")
s = Service(r'C:\Users\davidl\Desktop\py_data_scraping\driver\chromedriver.exe')
link_lst = ["https://www.smartone.com/tc/home/"]
driver = webdriver.Chrome(service=s, options=opts)

# Get HTML
for link in link_lst:
    driver.get(link)
    time.sleep(3)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(2)
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')

    # Get all the link from the webpage
    for element in soup.findAll('a', href=True):
        link = str(element.get('href'))
        check = ['http://', 'https://']
        if any(x in link for x in check) and link not in link_lst:
            print(link)
            link_lst.append(link)



