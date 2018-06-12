# -*- coding:utf-8 -*-
import asyncio
import aiohttp
from proxypool.db import RedisClient
from proxypool.setting import *
import time


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                real_proxy = 'http://' + proxy
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as res:
                    if res.status in STATUS_CODE:
                        self.redis.set_max_score(proxy)
                    else:
                        self.redis.decrease(proxy)
            except:
                pass

    def run(self):
        try:
            count = self.redis.get_count()
            for i in range(0, count, BATCH_TEST_COUNT):
                start = i
                stop = min(count, i + BATCH_TEST_COUNT)
                proxies = self.redis.get_batch(start, stop - 1)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)
