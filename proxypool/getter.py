# -*- coding:utf-8 -*-
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
from proxypool.setting import *


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        if self.redis.get_count() < MAX_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        if self.is_over_threshold():
            for i in range(self.crawler.__CrawlCount__):
                proxies = self.crawler.get_proxies(self.crawler.__CrawlFunc__[i])
                for proxy in proxies:
                    self.redis.add(proxy)
