from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Setting
opts = webdriver.ChromeOptions()
opts.add_argument("--disable-notifications, --headless")
s = Service(r'C:\Users\user\Desktop\py_data_scraping\driver\chromedriver.exe')
website = "https://www.smartone.com/tc/home/"
link_lst = []

# Get HTML
driver = webdriver.Chrome(service=s, options=opts)
driver.get(website)
content = driver.page_source
soup = BeautifulSoup(content, 'lxml')
driver.quit()

# Check keywords exists
""" for keyword in keywordslist: """

# Get all the link from the webpage
for element in soup.findAll('a', href=True):
    link = str(element.get('href'))
    check = ['http://', 'https://']
    if any(x in link for x in check) and link not in link_lst:
        link_lst.append(link)
