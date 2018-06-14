# -*- coding:utf-8 -*-

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

INITIAL_SCORE = 10
MAX_SCORE = 100
MIN_SCORE = 0

MAX_THRESHOLD = 10000
TESTER_CYCLE = 20
GETTER_CYCLE = 20

API_HOST = '0.0.0.0'
API_PORT = 5555

TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

TEST_URL = 'www.baidu.com'
STATUS_CODE = [200]
BATCH_TEST_COUNT = 100
