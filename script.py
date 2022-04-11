from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import tldextract


# Setting
opts = webdriver.ChromeOptions()
opts.add_argument("--disable-notifications, --headless")
s = Service(r'C:\Users\davidl\Desktop\py_data_scraping\driver\chromedriver.exe')
global_link_lst = ["https://www.smartone.com/tc/home/"]
driver = webdriver.Chrome(service=s, options=opts)


# Main Function
for item in global_link_lst:
    # Create Local workspace
    local_link_lst = [item]
    domain = tldextract.extract(item).domain
    for link in local_link_lst:
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

        # Get all the link from the soup
        for element in soup.findAll('a', href=True):
            link = str(element.get('href'))
            check = tldextract.extract(link).domain
            if (link.startswith('http://') or link.startswith('https://')) and\
                    (domain == check) and (link not in local_link_lst):
                print(link)
                local_link_lst.append(link)

    # Get all the text from the page


