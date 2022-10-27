import scrapy


class PixivSpider(scrapy.Spider):
    name = 'pixiv'
    allowed_domains = ['www.pixiv.net']
    start_urls = ['http://www.pixiv.net/']

    def parse(self, response):
        pass
