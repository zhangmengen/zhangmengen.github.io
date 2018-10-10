import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from proxypool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice
import re


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
    
    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):  # http://redisdoc.com/sorted_set/zscore.html   db.zscore返回REDIS_KEY中的proxy的值
            return self.db.zadd(REDIS_KEY, score, proxy)  # 如果不在这个redis key中，那么就添加，score为评分满分10分，
    
    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)  # 返回键为name的zset中score在给定区间的元素， 也就是返回rediskey中的 MAX_SCORE分数，100分
        if len(result):  # 如果result为真
            return choice(result)  # 从序列中随机选取一个元素，
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)   # db.zrevrange  返回键为name的zset（按score从大到小排序）中index从start到end的所有元素
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError  # 利用重写Exception， 返回代理池已经枯竭
    
    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)  # db.zscore返回REDIS_KEY中的proxy的值
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)  # db.zincrby 将这个redis key 中的proxy的分值减少1
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)  # 删除键为name的zset中的元素，
    
    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None
    
    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)
    
    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)  # 返回键为name的zset的元素个数
    
    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)   # 返回键为name的zset中score在给定区间的元素
    
    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)  # # db.zrevrange  返回键为name的zset（按score从大到小排序）中index从start到end的所有元素


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)  # 调用batch方法
    print(result)
