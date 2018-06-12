# -*-coding:utf-8 -*-
import time
from multiprocessing import Process

from proxypool.api import app
from proxypool.getter import Getter
from proxypool.setting import *
from proxypool.tester import Tester


class Scheduler(object):
    def schedule_tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        app.run(API_HOST, API_PORT)

    def run(self):
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
