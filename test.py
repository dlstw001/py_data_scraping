from curses import meta
import scrapy
from scrapy.linkextractors import LinkExtractor
import tldextract

class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = []
    start_urls = ['https://www.smartone.com/tc/home/']
    keywords = []
    backlink = []
    links=[]
    for url in start_urls:
        allowed_domains.append(tldextract.extract(url).registered_domain)

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, meta={"playwright": True})

    def parse(self, response):
        all_links = response.xpath('*//a/@href').extract()
        for link in all_links:
            try:
                domain = tldextract.extract(link).registered_domain
            except:
                domain = ''
            if (link.startswith('http://') or link.startswith('https://')) and (domain in self.allowed_domains) and (link not in self.links):
                    try:
                        self.links.append(link)
                        print(len(self.links))
                        yield response.follow(link, callback=self.parse, meta={"playwright": True})
                    except:
                        print('error')
