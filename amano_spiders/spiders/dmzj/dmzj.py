import datetime
import os


import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy import Date

from amano_spiders.spiders.dmzj.model.comic import ComicItem


class DmzjSpider(scrapy.Spider):
    name = 'dmzj'

    def __init__(self):
        self.base_url = 'https://www.dmzj.com'
        self.allowed_domains = ['dmzj.com']
        self.start_urls = ['https://www.dmzj.com/category/1-0-0-0-0-0-1.html']
        # self.chrome_options = Options()
        # self.chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        # self.chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        # self.abspath = os.path.abspath(r"/Users/weifeng/python/drivers/chromedriver")
        # self.dr = webdriver.Chrome(executable_path=self.abspath, chrome_options=self.chrome_options)
        # self.abspath = os.path.abspath(r"D:/Develop/Python/drivers/chromedriver.exe")
        # self.dr = webdriver.Chrome(executable_path=self.abspath, chrome_options=self.chrome_options)

    def parse(self, response):
        manga_page_url_list = response.xpath('//a[@class="comic_img"]')
        title = response.xpath('//span[@class="comic_list_det"]/h3/a/text()')
        manga_cover_url_list = response.xpath('//a[@class="comic_img"]/img')
        # 爬当前页漫画
        for i in range(len(manga_page_url_list)):
            item = ComicItem()
            item['comic_name'] = title[i].extract()
            item['detail_url'] = manga_page_url_list[i].attrib['href']
            item['cover_url'] = manga_cover_url_list[i].attrib['src']
            # 进详情页
            yield scrapy.Request(url=item['detail_url'], callback=self.detail_page, meta={'item': item})

        # 翻页爬下一页
        next_page_ele = response.xpath('//div[@class="bottom_page page"]/a[@class="pg_next"]')
        if len(next_page_ele) == 0:
            print("运行结束...")
            return
        next_page_url = self.base_url + next_page_ele[0].attrib['href']
        yield scrapy.Request(url=next_page_url)

    def detail_page(self, response):
        item = response.meta['item']
        info_eles = response.xpath('//ul[@class="comic_deCon_liO"]/li/text()')
        item["describe"] = response.xpath('//p[@class="comic_deCon_d"]/text()').extract()[0]
        if info_eles[0].extract():
            item["author"] = info_eles[0].extract()[3:-1]
        if info_eles[1].extract():
            state = info_eles[1].extract()
            item['state'] = (state == '连载中') if 0 else 1
        if info_eles[2].extract():
            item["category"] = info_eles[2].extract()[3:]
        if info_eles[3].extract():
            item["tags"] = info_eles[3].extract()[0]
        update_time_ele = response.xpath('//span[@class="zj_list_head_dat"]/text()').extract()[0][7:-2]
        item['update_time'] = datetime.datetime.strptime(update_time_ele, "%Y-%m-%d")
        item['popularity'] = response.xpath('//span[@id="hot_hits"]/text()').extract()[0]
        yield item
