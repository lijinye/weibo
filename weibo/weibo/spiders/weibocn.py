# -*- coding: utf-8 -*-
import scrapy
import json
from weibo.weibo.items import UserItem


class WeibocnSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']
    userdetail_url = 'https://m.weibo.cn/profile/info?uid={id}'
    followers_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{id}&page={page}'
    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{id}&since_id={page}'
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{id}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={page}'
    start_users = ['1345566427']

    def start_requests(self):
        for user in self.start_users:
            yield scrapy.Request(url=self.userdetail_url.format(id=user), callback=self.parse_user)

    def parse_user(self, response):
        result = json.loads(response.text)
        if result.get('data').get('user'):
            user_info = result.get('data').get('user')
            user_item = UserItem()
            field_map = {
                'id': 'id', 'name': 'screen_name', 'cover': 'avatar_hd', 'gender': 'gender',
                'description': 'description',
                'fans_count': 'followers_count', 'follows_count': 'follow_count', 'weibos_count': 'statuses_count',
                'verified': 'verified', 'verified_reason': 'verified_reason'
            }
            for field, attr in field_map.items():
                user_item[field] = user_info.get(attr)
            yield user_item
        id = user_info.get('id')
        # 关注
        yield scrapy.Request(url=self.followers_url.format(id=id, page=1), callback=self.parse_followers,
                             meta={'page': '1', 'id': id})
        # 粉丝
        yield scrapy.Request(url=self.fans_url.format(id=id, page=1), callback=self.parse_fans,
                             meta={'id': id, 'page': 1})
        # 微博
        yield scrapy.Request(url=self.weibo_url.format(id=id, page=1), callback=self.parse_weibo,
                             meta={'id': id, 'page': 1})

    def parse_followers(self, response):
        pass

    def parse_fans(self, response):
        pass

    def parse_weibo(self, response):
        pass
