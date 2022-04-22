from os import link
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_playwright.page import PageMethod
from bs4 import BeautifulSoup
import tldextract


class TestSpider(scrapy.Spider):
    name = 'test'
    list = []
    start_urls = ["https://www.smartone.com/"]

    for url in start_urls:
        def start_requests(self):
            yield scrapy.Request(
                url= self.url,
                meta={
                    'playwright': True,
                    'playwright_include_page': True,
                },
                errback=self.errback,            
            )

        
        async def parse(self, response):
            page = response.meta["playwright_page"]
            domain = tldextract.extract(page.url).domain
            content = await page.content()
            soup = BeautifulSoup(content, 'lxml')
            await page.close()
            for element in soup.find_all('a'):
                link = str(element.get('href'))
                domain_check = tldextract.extract(link).domain
                if (link.startswith('http://') or link.startswith('https://')) and (domain == domain_check) and (link not in self.list):
                    self.list.append(link)
                    yield response.follow(link, callback=self.parse)
            print(list)




        async def errback(self, failure):
            page = failure.request.meta["playwright_page"]
            await page.close()