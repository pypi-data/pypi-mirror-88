# coding=utf-8

class SingerCache():
    def __init__(self):
        self.__cache = {}

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
