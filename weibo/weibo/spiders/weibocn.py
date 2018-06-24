# -*- coding: utf-8 -*-
import scrapy
import json
from weibo.items import *
import logging

class WeibocnSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']
    userdetail_url = 'https://m.weibo.cn/profile/info?uid={id}'
    followers_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{id}&page={page}'
    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{id}&since_id={page}'
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{id}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={page}'
    # start_users = ['1345566427']
    start_users = ['2343286617']

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
                                 meta={'page': 1, 'id': id})
            # 粉丝
            yield scrapy.Request(url=self.fans_url.format(id=id, page=1), callback=self.parse_fans,
                                 meta={'id': id, 'page': 1})
            # 微博
            yield scrapy.Request(url=self.weibo_url.format(id=id, page=1), callback=self.parse_weibo,
                                 meta={'id': id, 'page': 1})

    def parse_followers(self, response):
        result = json.loads(response.text)
        # logging.info(response.text)
        if result.get('ok') and result.get('data').get('cards')[-1].get('card_group') and len(
                result.get('data').get('cards')[-1].get('card_group')):
            followers = result.get('data').get('cards')[-1].get('card_group')
            for follow in followers:
                uid = follow.get('user').get('id')
                yield scrapy.Request(url=self.userdetail_url.format(id=uid), callback=self.parse_user)
            uid = response.meta.get('id')
            user_relation_item = UserRelationItem()
            follows = [{'id': follow.get('user').get('id'), 'name': follow.get('user').get('screen_name')} for
                       follow in followers]
            user_relation_item['id'] = uid
            user_relation_item['follows'] = follows
            user_relation_item['fans'] = []
            yield user_relation_item

            page = response.meta.get('page') + 1
            yield scrapy.Request(url=self.followers_url.format(id=uid, page=page), callback=self.parse_followers,
                                 meta={'page': page, 'id': uid})

    def parse_fans(self, response):
        result = json.loads(response.text)
        # logging.info(response.url)
        if result.get('ok') and result.get('data').get('cards')[-1].get('card_group') and len(
                result.get('data').get('cards')[-1].get('card_group')):
            fans = result.get('data').get('cards')[-1].get('card_group')
            for fan in fans:
                if fan.get('user'):
                    uid = fan.get('user').get('id')
                    yield scrapy.Request(url=self.userdetail_url.format(id=uid), callback=self.parse_user)
            uid = response.meta.get('id')
            user_relation_item = UserRelationItem()
            fans1 = [{'id': fan.get('user').get('id'), 'name': fan.get('user').get('screen_name')} for fan in fans if fan.get('user')]
            user_relation_item['id'] = uid
            user_relation_item['fans'] = fans1
            user_relation_item['follows'] = []
            yield user_relation_item
            page = response.meta.get('page') + 1
            yield scrapy.Request(url=self.fans_url.format(id=uid, page=page), callback=self.parse_fans,
                                 meta={'page': page, 'id': uid})

    def parse_weibo(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(
                result.get('data').get('cards')):
            weibos = result.get('data').get('cards')
            for weibo in weibos:
                if weibo.get('card_type') == 9:
                    mblog = weibo.get('mblog')
                    if mblog:
                        weibo_item = WeiboItem()
                        field_map = {
                            'id': 'id', 'attitude_count': 'attitudes_count', 'comments_count': 'comments_count',
                            'created_at': 'created_at', 'reposts_count': 'reposts_count', 'picture': 'original_pic',
                            'source': 'source', 'text': 'text'
                        }
                        for field, attr in field_map.items():
                            weibo_item[field] = mblog.get(attr)
                            yield weibo_item
                else:
                    pass
            uid = response.meta.get('id')
            page = response.meta.get('page') + 1
            yield scrapy.Request(url=self.weibo_url.format(id=uid, page=page), callback=self.parse_weibo,
                                 meta={'id': uid, 'page': page})
