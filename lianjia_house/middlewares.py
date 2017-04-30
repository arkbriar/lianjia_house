# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json
import requests
from datetime import datetime, timedelta
from itertools import cycle
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

    proxy_pool = []
    proxy_update_time = None

    def __init__(self):
        self.update_proxy_pool()

    def update_proxy_pool(self):
        r = requests.get('http://localhost:8000/?types=0&count=40&country=国内')
        ip_ports = json.loads(r.text)
        global_proxy_list = []
        for ip_port in ip_ports:
            global_proxy_list.append('%s:%s' % (ip_port[0], ip_port[1]))
        assert len(global_proxy_list) == 40
        self.proxy_pool = cycle(global_proxy_list)
        self.proxy_update_time = datetime.utcnow()

    def process_request(self, request, spider):
        # update proxy pool every 20s
        if self.proxy_update_time + timedelta(seconds=20) < datetime.utcnow():
            self.update_proxy_pool()

        proxy_addr = next(self.proxy_pool)
        request.meta['proxy'] = 'http://' + proxy_addr
