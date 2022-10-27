import scrapy


class MangabzSpider(scrapy.Spider):
    name = 'mangabz'
    allowed_domains = ['www.mangabz.com']
    start_urls = ['http://www.mangabz.com/manga-list/']

    def parse(self, response):
        print(response.text)
        pass
