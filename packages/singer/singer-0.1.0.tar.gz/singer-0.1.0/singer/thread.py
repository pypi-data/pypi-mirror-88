# coding=utf-8
from concurrent.futures import ThreadPoolExecutor, as_completed


class SingerThread(object):
    def __init__(self, max_workers=5):
        self.__executor = ThreadPoolExecutor(max_workers=max_workers)
        self.__task_list = []

    def start(self, fn, args=...):
        task = self.__executor.submit(fn, args)
        self.__task_list.append(task)

    def completed(self, fn):
        for future in as_completed(self.__task_list):
            fn(future)

    def cancel(self):
        '''取消执行
        '''
        for task in reversed(self.__task_list):
            task.cancel()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__executor.shutdown(wait=True)
        return False
