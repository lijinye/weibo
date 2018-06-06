# -*- coding:utf-8 -*-
from proxypool.setting import *
import redis
from random import choice


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, pwd=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=pwd, decode_responses=True)

    def add(self, proxy, initial_score=INITIAL_SCORE):
        if not self.db.zscore(REDIS_KEY, proxy):
            self.db.zadd(REDIS_KEY, initial_score, proxy)
        else:
            pass

    def exists(self, proxy):
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def get_random(self):
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if result:
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if result:
                return choice(result)
            else:
                pass

    def set_max_score(self, proxy):
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def decrease(self, proxy):
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            return self.db.zrem(REDIS_KEY, proxy)

    def get_count(self):
        return self.db.zcard(REDIS_KEY)

    def get_all(self):
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
