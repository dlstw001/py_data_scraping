from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Setting
opts = webdriver.ChromeOptions()
opts.add_argument("--disable-notifications, --headless")
s = Service(r'C:\Users\user\Desktop\py_data_scraping\driver\chromedriver.exe')
website = "https://frontierbv.nl/?lang=en"
wordlst = ['maritime', 'transportation','public safety', 'M2M and IoT', 'financial','Poynting', 'Mondicon']

# Get HTML
driver = webdriver.Chrome(service=s, options=opts)
driver.get(website) # need check the drive element
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
test = soup.find('a', class_='xQ_iF')
print(test)

