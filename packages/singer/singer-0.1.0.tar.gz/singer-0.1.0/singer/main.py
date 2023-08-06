
# coding=utf-8
from singer.logger import logger
from singer.config import SingerConfig
from singer.cache import SingerCache
from singer.thread import SingerThread


class Singer():
    def __init__(self):
        self.__guid = 0

    @property
    def guid(self):
        self.__guid += 1
        return self.__guid

    @staticmethod
    def logger(name=''):
        '''日志
        '''
        return logger(name)

    @staticmethod
    def config(path='config.ini', mode='default'):
        '''配置
        '''
        return SingerConfig(path, mode)

    @staticmethod
    def cache():
        '''缓存
        '''
        return SingerCache()

    @staticmethod
    def executor(max_workers=5):
        '''多线程执行器
        '''
        return SingerThread(max_workers)
