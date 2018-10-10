import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.setting import *


# schedule.py
#
# 调度器模块
#
# class proxypool.schedule.ValidityTester
#
# 异步检测类，可以对给定的代理的可用性进行异步检测。
#
# class proxypool.schedule.PoolAdder
#
# 代理添加器，用来触发爬虫模块，对代理池内的代理进行补充，代理池代理数达到阈值时停止工作。
#
# class proxypool.schedule.Schedule
#
# 代理池启动类，运行RUN函数时，会创建两个进程，负责对代理池内容的增加和更新。

class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)
    
    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()   # 调用getter中封装的run方法，获取代理
            time.sleep(cycle)
    
    def schedule_api(self):
        """
        开启API
        """
        app.run(API_HOST, API_PORT)  # 开启flask,默认是运行localhost 5555
    
    def run(self):
        print('代理池开始运行')
        
        if TESTER_ENABLED:  # 开启三个进程
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
