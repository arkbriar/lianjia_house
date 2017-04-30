# -*- coding: utf-8 -*-
import scrapy
import json
import re

from lianjia_house.items import LianjiaHouseItem


class LianjiaShanghaiHouseSpider(scrapy.Spider):
    name = "lianjia_shanghai_house"
    allowed_domains = ["sh.lianjia.com"]
    start_urls = []

    def __init__(self):
        with open('lianjia_shanghai_url.json') as data_file:
            data = json.load(data_file)
        for house_url in data:
            yield scrapy.Request('http://sh.lianjia.com' + house_url['url'], self.parse)

    def parse(self, response):
        content = response.xpath(
            '/html/body/div[@class="zf-top"]/div[@class="cj-cun"]/div[@class="content forRent"]')
        house_info = content.xpath('./div[@class="houseInfo"]')
        around_info = content.xpath('./div[@class="aroundInfo"]')

        house_id_str = content.xpath(
            './div[@class="houseRecord"]/span[@class="houseNum"]/text()').extract()
        match = re.search('房源编号：(.+?)', house_id_str)
        assert match
        house_id = match.group(1)

        # extracting item
        house_item = LianjiaHouseItem()
        house_item['id'] = house_id
        house_item['price'] = house_info.xpath(
            './div[@class="price"]/div/text()').extract()
        house_item['room'] = house_info.xpath(
            './div[@class="room"]/div/text()').extract()[0]
        house_item['hall'] = house_info.xpath(
            './div[@class="room"]/div/text()').extract()[1]
        house_item['area'] = house_info.xpath(
            './div[@class="area"]/div/text()').extract()
        house_item['floor'] = around_info.xpath(
            './table/tbody/tr[1]/td[2]/text()').extract().strip()
        house_item['orientation'] = around_info.xpath(
            './table/tbody/tr[1]/td[4]/text()').extract().strip()
        house_item['region'] = around_info.xpath(
            './table/tbody/tr[2]/td[2]/text()').extract()
        house_item['time'] = around_info.xpath(
            './table/tbody/tr[2]/td[4]/text()').extract()
        house_item['community'] = around_info.xpath(
            './table/tbody/tr[3]/td[2]/p/a/text()').extract()
        house_item['address'] = around_info.xpath(
            './table/tbody/tr[4]/td[2]/p/text()').extract().strip()

        yield house_item
