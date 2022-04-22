from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto("https://www.smartone.com/tc/home/")
        page.wait_for_timeout(2000)
        prev_height = None
        while True:
            curr_height = page.evaluate('(window.innerHeight + window.scrollY)')
            if not prev_height:
                prev_height = curr_height
                page.wait_for_timeout(1000)
            elif prev_height == curr_height:
                page.evaluate('clearInterval(intervalID)')
                break
            else:
                prev_height = curr_height
                page.wait_for_timeout(1000)
        content = page.content()
        print(content)

main()

