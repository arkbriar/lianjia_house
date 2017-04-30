# -*- coding: utf-8 -*-
import scrapy
from lianjia_house.items import LianJiaHouseUrl


class LianjiaShanghaiUrlSpider(scrapy.Spider):
    name = "lianjia_shanghai_url"
    allowed_domains = ["sh.lianjia.com"]
    start_urls = ['http://sh.lianjia.com/zufang/']

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.page_no = 1

    def next_url(self):
        self.page_no += 1
        return '%s/d%d' % ('http://sh.lianjia.com/zufang', self.page_no)

    def parse(self, response):
        house_link_list = response.xpath(
            '//*[@id="house-lst"]//li/div[@class="info-panel"]/h2/a/@href').extract()
        for house_link in house_link_list:
            url_item = LianJiaHouseUrl()
            url_item['url'] = house_link
            yield url_item

        if len(house_link_list) > 0:
            yield scrapy.Request(self.next_url(), callback=self.parse)
