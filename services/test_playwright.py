import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import tldextract

global_link_lst = ["https://www.smartone.com/"]

async def run(playwright):
    for g_link in global_link_lst:
        # Create local list for iteration
        local_link_lst = []
        local_link_lst.append(g_link)
        domain = tldextract.extract(g_link).domain
        for l_link in local_link_lst:
            async with async_playwright() as p:
                chromium = playwright.chromium # or "firefox" or "webkit".
                browser = await chromium.launch(headless=False)
                page = await browser.new_page()
                await page.goto(l_link)
                await page.wait_for_timeout(2000)
                await page.evaluate('() => window.scrollTo(0, document.body.scrollHeight)')
                await page.wait_for_timeout(2000)
                content = page.content()
                soup = BeautifulSoup(content, 'lxml')

                # Get links from soup
                for element in soup.findAll('a', href=True):
                    link = str(element.get('href'))
                    doamin_check = tldextract.extract(link).domain
                    if (link.startswith('http://') or link.startswith('https://')) and \
                            (domain == doamin_check) and (link not in local_link_lst):
                        local_link_lst.append(link)
                print(local_link_lst)
                await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())




""" 
            # Check repeated data
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
                print('Data already existed') 
"""



