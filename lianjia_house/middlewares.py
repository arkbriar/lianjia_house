# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
import random
import requests
from datetime import datetime, timedelta
from scrapy import signals


class LianjiaHouseSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):

    global_proxy_list = []
    proxy_list = []
    update_time = None
    start_index = 0

    def __init__(self):
        # update global proxy list
        r = requests.get('http://localhost:8000/?types=0&count=200')
        ip_ports = json.loads(r.text)
        for ip_port in ip_ports:
            self.global_proxy_list.append('%s:%s' % (ip_port[0], ip_port[1]))
        assert len(self.global_proxy_list) == 200

        if len(self.proxy_list) == 0:
            self.update_proxy_list()

    def update_proxy_list(self):
        self.proxy_list = self.global_proxy_list[self.start_index:self.start_index + 50]
        self.update_time = datetime.utcnow()
        self.start_index += 50
        if self.start_index >= 200:
            self.start_index -= 200

    def proxy_list_expired(self):
        # expire every 30s
        return datetime.utcnow() > self.update_time + timedelta(seconds=30)

    def process_request(self, request, spider):
        # update proxy list if it is expired
        if self.proxy_list_expired():
            self.update_proxy_list()

        proxy_addr = random.choice(self.proxy_list)
        request.meta['proxy'] = 'http://' + proxy_addr
