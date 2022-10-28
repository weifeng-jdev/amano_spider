import datetime
import re
import datedays
from amano_spiders.spiders.mangabz import mangabz_site_info
import scrapy

from amano_spiders.spiders.model.chapter import ChapterItem
from amano_spiders.spiders.model.comic import ComicItem

site = mangabz_site_info()

class MangabzSpider(scrapy.Spider):
    name = 'mangabz'

    def __init__(self):
        self.site_code = site.id
        self.allowed_domains = ['www.mangabz.com']
        self.start_urls = ['http://www.mangabz.com/manga-list/']
        self.base_url = site.domain
        self.update_time_rex = re.compile('\d{4}-\d{2}-\d{2}|今天|昨天|前天|(\d{4}年)?\d{2}月\d{2}號')
        self.ymd_rex = re.compile('\d{4}-\d{2}-\d{2}')
        self.ft_rex = re.compile('(\d{4}年)?\d{2}月\d{2}號')
        self.yesterday =datedays.getyesterday()
        self.today = datetime.datetime.strptime(datedays.getnow()[0:10], "%Y-%m-%d")
        self.yesterday2 = datedays.getyesterday(days=2)

    def parse(self, response):
        manga_detail_suffix = response.xpath('//div[@class="mh-item"]/a')
        for suffix in manga_detail_suffix:
            detail_url = self.base_url + suffix.attrib['href']
            yield scrapy.Request(url=detail_url, callback=self.parse_detail_page)
        # next_page
        next_page_url = self.base_url + response.xpath('//div[@class="page-pagination"]//li[last()]/a').attrib['href']
        yield scrapy.Request(url=next_page_url)

    def parse_detail_page(self, response):
        # 格式化漫画详情
        item = self.parse_detail_item(response)
        # yield item
        # 获取章节数据
        chapter_list = response.xpath('//div[@id="chapterlistload"]/a')
        for page_number_ele in chapter_list:
            yield self.parse_chapter(page_number_ele, item)

    def parse_chapter(self, page_number_ele, item):
        chapter = ChapterItem()
        chapter['comic_id'] = item['comic_id']
        chapter['title'] = page_number_ele.xpath('text()').extract()[0]
        chapter['reading_url'] = self.base_url + page_number_ele.attrib['href']
        chapter['page_number'] = page_number_ele.xpath('span/text()').extract()[0][1:-2]
        return chapter



    def parse_detail_item(self, response):
        item = ComicItem()
        item['comic_id'] = response.url[23:-1]
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
        date = self.update_time_rex.search(
            response.xpath('//div[@class="detail-list-form-title"]/text()').extract()[1]).group(0)
        item['update_time'] = self.format_date(date)
        item['source_site'] = self.site_code
        return item

    def format_date(self, date):
        if date == '今天':
            return self.today
        elif date == '昨天':
            return self.yesterday
        elif date == '前天':
            return self.yesterday2
        elif self.ymd_rex.match(date):
            return datetime.datetime.strptime(date, "%Y-%m-%d")
        elif self.ft_rex.match(date):
            if '年' not in date:
                date = datedays.getnow()[0:4] + '年' + date
            return datetime.datetime.strptime(date, "%Y年%m月%d號")