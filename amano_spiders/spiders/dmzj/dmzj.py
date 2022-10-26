import os
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from amano_spiders.spiders.dmzj.model.comic import ComicItem

class DmzjSpider(scrapy.Spider):
    name = 'dmzj'

    def __init__(self):
        self.allowed_domains = ['dmzj.com']
        self.start_urls = ['https://www.dmzj.com/rank/all/1-1.html']
        self.base_url = 'https://www.dmzj.com'
        self.chrome_options = Options()
        self.chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        self.chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        self.abspath = os.path.abspath(r"/Users/weifeng/python/drivers/chromedriver")
        self.dr = webdriver.Chrome(executable_path=self.abspath, chrome_options=self.chrome_options)

    def parse(self, response):
        manga_page_url_list = response.xpath(
            '//div[@class="ph_r_tabs_con"]//div[@class="ph_r_con_li_c"]//div[@class="li_content_dec"]//span/h3/a')
        manga_cover_url_list = response.xpath(
            '//div[@class="ph_r_tabs_con"]//div[@class="ph_r_con_li_c"]//div[@class="li_content_dec"]//img')
        # 爬当前页漫画
        for i in range(len(manga_page_url_list)):
            item = ComicItem()
            item['comic_name'] = manga_page_url_list[i].attrib['title']
            item['detail_url'] = manga_page_url_list[i].attrib['href']
            item['cover_url'] = 'https:' + manga_cover_url_list[i].attrib['src']
            yield item
            # 进详情页
            # yield scrapy.Request(url=manga_page_url, callback=self.enter_manage_detail_page, meta=item)
        # 翻页爬下一页
        next_page = response.xpath('//div[@class="bottom_page page"]//a[@class="pg_next"]')
        if len(next_page) == 0:
            print("运行结束...")
            return
        next_page = self.base_url + next_page[0].attrib['href']
        yield scrapy.Request(url=next_page)
