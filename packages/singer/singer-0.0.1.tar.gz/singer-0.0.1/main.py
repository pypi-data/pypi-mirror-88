# coding=utf-8
import logging

logging.basicConfig(
    format='%(asctime)s  [%(levelname)s] - %(pathname)s[line:%(lineno)d]  -> %(name)s: %(message)s',
    level=logging.DEBUG)


class Singer():
    def __init__(self):
        self.__cache = {}

    @staticmethod
    def get_logger(name):
        '''获取日志记录器
        '''
        return logging.getLogger(name)

    def set_cache(self, key, value):
        '''设置缓存
        :param key      key
        :param value    value
        '''
        self.__cache[key] = value

    def get_cache(self, key):
        ''' 获取缓存
        :param key      key
        '''
        if key in self.__cache:
            return self.__cache[key]
        return None
