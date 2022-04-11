from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def getlink(link_lst):
    for link in link_lst:
        website = link
        opts = webdriver.ChromeOptions()
        opts.add_argument("--disable-notifications, --headless")
        s = Service(r'C:\Users\davidl\Desktop\py_data_scraping\driver\chromedriver.exe')

        driver = webdriver.Chrome(service=s, options=opts)
        driver.get(website)
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        driver.quit()

    for element in soup.findAll('a', href=True):
        link = str(element.get('href'))
        check = ['http://', 'https://']
        if any(x in link for x in check) and link not in link_lst:
            link_lst.append(link)