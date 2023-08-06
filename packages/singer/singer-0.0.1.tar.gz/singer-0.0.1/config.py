# coding=utf-8
import os
import configparser
from main import Singer


class SingerConfig():
    def __init__(self, path='config.ini', mode=''):
        config = configparser.ConfigParser()
        config.read(path)
        self.__config = config
        self.__sections = config.sections()
        self.__mode = mode
        self.__logger = Singer.get_logger('SingerConfig')

    def __get_value(self, section, key):
        if section and section in self.__sections:
            return self.__config[section].get(key)
        return None

    def get_sections(self):
        return self.__config.sections()

    def get_config(self, key, section='', env_key=''):
        arr = key.split(':')
        if len(arr) > 1 and not section:
            section = arr[0]
            key = arr[1]
        if not section:
            section = self.__mode or self.__sections[0]
        env_key = env_key or ('%s_%s' % (section, key)).upper()
        self.__logger.debug('config env name: %s', env_key)
        return os.getenv(env_key) or self.__get_value(section, key)
