# -*- coding:utf-8 -*-
import requests
from requests.exceptions import ConnectionError

base_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}


def get_page(url, options={}):
    headers = dict(base_headers, options)
    try:
        response = requests.get(url, headers=base_headers)
        if response.status_code == 200:
            return response.text
    except  ConnectionError:
        return None
