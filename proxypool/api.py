# -*- coding:utf-8 -*-
from flask import Flask, g
from proxypool.db import RedisClient

__all__ = ['app']
app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome</h2>'


@app.route('/random')
def get_proxy():
    conn = get_conn()
    return conn.get_random()


@app.route('/count')
def get_count():
    conn = get_conn()
    return conn.get_count()


if __name__ == '__main__':
    app.run()
