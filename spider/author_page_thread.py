# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     paper_page_thread.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          paper_page_thread.py
   Description :    对author_page的多线程
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.
-------------------------------------------------
"""
import threading
from time import time
from spider.author_page import AuthorPage
from util.Log import get_logger
from logging import Logger


class AuthorPageThread(object):

    def __init__(self, things, thread_num=6):
        """

        :param things: 作者页的链接list
        :param thread_num:
        """
        self.thread_num = thread_num
        self.things = things
        self.loggers = [get_logger(__name__ + str(x), __name__ + str(x)) for x in range(1, thread_num + 1)]

    def get_range(self):
        # 完成范围的均分
        ranges = []
        length = len(self.things)
        n = self.thread_num
        t = 0
        for i in range(0, n):
            offset = int(length / n)
            obj = None
            if i == (n - 1):
                obj = self.things[t:]

            else:
                obj = self.things[t:t + offset]
            ranges.append(obj)
            t += offset
        return ranges

    @staticmethod
    def do_something(things, logger: Logger):
        for i in things:
            logger.info("开始处理author:" + i)
            try:
                author_page = AuthorPage(i)
                author_page.run()

            except Exception as e:
                logger.error("发生错误:%s\t%s" % (i, e))
            logger.info("完成处理author：" + i)

    def start(self):
        thread_list = []
        n = 1
        for ran in self.get_range():
            thread = threading.Thread(target=self.do_something, args=(ran, self.loggers[n - 1]))
            n += 1
            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            i.join()
        print("进程执行完成")


if __name__ == '__main__':
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    #
    # print("all over %s" % ctime())
    s = time()
    down = AuthorPageThread(range(3), 10)
    print(down.get_range())
    down.start()
    e = time()
    print("The time spent on this program is %f s" % (e - s))
