import asyncio
from pyppeteer import launch
import traceback
import tldextract # Get domain


URLS = [
    "https://www.smartone.com/",
    "https://eshop.hk.chinamobile.com/tc/index.html",
    "https://www.cmi.chinamobile.com/",
    "https://www.three.com.hk/",
]


async def fetch(browser, url):
    page = await browser.newPage()

    try:
        await page.goto(url)
    except Exception:
        traceback.print_exc()
    else:
        html = await page.content()
        return (url, html)
    finally:
        await page.close()


async def main():
    tasks = []
    browser = await launch(headless=True, args=["--no-sandbox"])

    for url in URLS:
        tasks.append(asyncio.create_task(fetch(browser, url)))

    for coro in asyncio.as_completed(tasks):
        url, html = await coro
        print(f"{url}: ({len(html)})")

    await browser.close()


if __name__ == "__main__":
    main = asyncio.run(main())


