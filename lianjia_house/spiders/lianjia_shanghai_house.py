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
        LianjiaShanghaiHouseSpider.start_urls = []
        with open('lianjia_shanghai_url.json') as data_file:
            data = json.load(data_file)
        for house_url in data:
            LianjiaShanghaiHouseSpider.start_urls.append(
                'http://sh.lianjia.com' + house_url['url'])

    def parse(self, response):
        content = response.xpath(
            '/html/body/div[@class="zf-top"]/div[@class="cj-cun"]/div[contains(@class, "content")]')
        house_info = content.xpath('./div[contains(@class, "houseInfo")]')
        around_info = content.xpath('./table[contains(@class, "aroundInfo")]')

        match = re.search(
            u'^http://sh.lianjia.com/zufang/(.+)\\.html$', response.url)
        assert match
        house_id = match.group(1)

        # extracting item
        house_item = LianjiaHouseItem()
        house_item['id'] = house_id
        house_item['price'] = int(house_info.xpath(
            './div[@class="price"]/div/text()').extract()[0])
        house_item['price_unit'] = house_info.xpath(
            './div[@class="price"]/div/span[@class="unit"]/text()').extract()[0]
        house_item['room'] = int(house_info.xpath(
            './div[@class="room"]/div/text()').extract()[0])
        house_item['hall'] = int(house_info.xpath(
            './div[@class="room"]/div/text()').extract()[1].strip())
        house_item['area'] = float(house_info.xpath(
            './div[@class="area"]/div/text()').extract()[0])
        house_item['floor'] = around_info.xpath(
            './tr[1]/td[2]/text()').extract()[0].strip()
        house_item['orientation'] = around_info.xpath(
            './tr[1]/td[4]/text()').extract()[0].strip()
        house_item['region'], house_item['plate'] = around_info.xpath(
            './tr[2]/td[2]/text()').extract()[0].split(' ', 2)
        house_item['time'] = around_info.xpath(
            './tr[2]/td[4]/text()').extract()[0]
        house_item['community'] = around_info.xpath(
            './tr[3]/td[2]/p/a/text()').extract()[0]
        house_item['address'] = around_info.xpath(
            './tr[4]/td[2]/p/@title').extract()[0].strip()

        # extract latitude and longtitude from zone map
        house_item['longitude'] = float(response.xpath(
            '//*[@id="zoneMap"]/@longitude').extract()[0])
        house_item['latitude'] = float(response.xpath(
            '//*[@id="zoneMap"]/@latitude').extract()[0])

        yield house_item
