# -*- coding:utf-8 -*-
from pyquery import PyQuery
from proxypool.utils import get_page
import json


class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if k.startswith('crawl_'):
                count += 1
                attrs['__CrawlFunc__'].append(k)
        attrs['__CrawlCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaClass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            res = get_page(url)
            if res:
                doc = PyQuery(res)
                trs = doc('.containerbox boxindex table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_ip181(self):
        """
        获取ip181
        :return: 代理
        """
        start_url = 'http://www.ip181.com/'
        print('Crawling', start_url)
        html = get_page(start_url)
        if html:
            res = json.loads(html)
            results = res.get('RESULT')
            if results:
                for result in results:
                    ip = result.get('ip')
                    port = result.get('port')
                    yield ':'.join([ip, port])
