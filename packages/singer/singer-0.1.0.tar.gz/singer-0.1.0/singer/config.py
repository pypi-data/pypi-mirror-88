# coding=utf-8
import os
import configparser
from singer.logger import logger


class SingerConfig():
    def __init__(self, path='config.ini', mode='default'):
        config = configparser.ConfigParser()
        config.read(path)
        self.__config = config
        self.__sections = config.sections()
        self.__mode = mode
        self.__logger = logger('SingerConfig')

    def __get_value(self, section, key):
        if section and section in self.__sections:
            return self.__config.get(section, key)
        return None

    def __get_section(self, key, section=''):
        if section:
            return (key, section)
        arr = key.split(':')
        if len(arr) > 1:
            section = arr[0]
            key = arr[1]
            return (key, section)
        if self.__mode:
            section = self.__mode
        elif len(self.__sections) > 0:
            section = self.__sections[0]
        return (key, section)

    def get_sections(self):
        '''获取Sections
        '''
        return self.__sections

    def get_items(self, section=''):
        '''获取Section
        '''
        if section and section in self.__sections:
            return self.__config.items(section)
        if self.__mode and self.__mode in self.__sections:
            return self.__config.items(self.__mode)
        return None

    def get_config(self, key, section='', env_key=''):
        '''获取配置
        '''
        key, section = self.__get_section(key, section)
        if not section:
            return None
        env_key = env_key or ('SINGER_%s_%s' % (section, key)).upper()
        self.__logger.debug('config env name: %s', env_key)
        return os.getenv(env_key) or self.__get_value(section, key)

    def set_config(self, key, value, section=''):
        key, section = self.__get_section(key, section)
        if not section:
            return False
        self.__config[section].set(key, value)
        return True
