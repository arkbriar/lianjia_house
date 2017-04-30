# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaHouseItem(scrapy.Item):
    id = scrapy.Field()
    price = scrapy.Field()
    room = scrapy.Field()
    hall = scrapy.Field()
    area = scrapy.Field()
    floor = scrapy.Field()
    orientation = scrapy.Field()
    region = scrapy.Field()
    time = scrapy.Field()
    community = scrapy.Field()
    address = scrapy.Field()


class LianJiaHouseUrl(scrapy.Item):
    url = scrapy.Field()
