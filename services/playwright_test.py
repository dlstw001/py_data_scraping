import asyncio
import tldextract
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


urls = ['https://www.smartone.com/tc/home/','https://www.three.com.hk/']
domains = []



async def main(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(1000)
        await page.wait_for_selector('footer')
        await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
        await page.wait_for_timeout(1000)    
        content = page.content()
        print(content) 
    
for url in urls:
    domains.append(tldextract.extract(url).registered_domain)
    asyncio.run(main(url))