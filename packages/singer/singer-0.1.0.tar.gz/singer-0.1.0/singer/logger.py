# coding=utf-8
import logging

logging.basicConfig(
    format='%(asctime)s  [%(levelname)s] - %(pathname)s[line:%(lineno)d]  -> %(name)s: %(message)s',
    level=logging.DEBUG)


def logger(name=''):
    '''获取日志记录器
    '''
    return logging.getLogger(name)
