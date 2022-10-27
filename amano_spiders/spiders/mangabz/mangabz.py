import re

import scrapy

from amano_spiders.spiders.model.comic import ComicItem


class MangabzSpider(scrapy.Spider):
    name = 'mangabz'
    allowed_domains = ['www.mangabz.com']
    start_urls = ['http://www.mangabz.com/manga-list/']
    base_url = 'http://www.mangabz.com'

    def parse(self, response):
        manga_detail_suffix = response.xpath('//div[@class="mh-item"]/a')
        for suffix in manga_detail_suffix:
            detail_url = self.base_url + suffix.attrib['href']
            print(detail_url)
            yield scrapy.Request(url=detail_url, callback=self.parse_detail_page)
        # next_page
        next_page_url = self.base_url + response.xpath('//div[@class="page-pagination"]//li[last()]/a').attrib['href']
        yield scrapy.Request(url=next_page_url)

    def parse_detail_page(self, response):
        item = ComicItem()
        item['detail_url'] = response.url
        # cover_url
        cover_url = response.xpath('//img[@class="detail-info-cover"]').attrib['src']
        item['cover_url'] = cover_url
        # title
        title = response.xpath('//p[@class="detail-info-title"]/text()').extract()[0][3:]
        item['comic_name'] = title
        # score
        score = response.xpath('//p[@class="detail-info-stars"]/span/text()').extract()[0][:-1]
        item['score'] = score
        # author
        author = response.xpath('//p[@class="detail-info-tip"]/span[1]/a/text()').extract()[0]
        item['author'] = author
        # state
        state = response.xpath('//p[@class="detail-info-tip"]/span[2]/span/text()').extract()[0]
        item['state'] = 1 if state == '已完结' else 0
        # tags
        tags = response.xpath('//p[@class="detail-info-tip"]/span[3]/span/text()').extract()
        item['tags'] = tags
        # describe
        desc_ele = response.xpath('//p[@class="detail-info-content"]/text()').extract()
        if desc_ele:
            describe = desc_ele[0]
            describe_sec = response.xpath('//p[@class="detail-info-content"]/span/text()').extract()
            if describe_sec:
                describe += describe_sec[0]
            item['describe'] = describe
        # update_time
        print(response.xpath('//div[@class="detail-list-form-title"]/text()').extract()[1])
        data = re.compile('\d{4}-\d{2}-\d{2}|今天|昨天|前天|(\d{4}年)?\d{2}月\d{2}號')\
            .search(response.xpath('//div[@class="detail-list-form-title"]/text()').extract()[1]).group(0)