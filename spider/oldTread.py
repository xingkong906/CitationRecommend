# -*- coding:utf8 -*-
import threading
from time import ctime, time
from spider.paper_page2 import PaperPage
from util.Log import get_logger
from logging import Logger

logger = get_logger("mutil_thread_paper")
lock = threading.Lock()


class PageThread(object):

    def __init__(self, length, thread_num=6):
        self.thread_num = thread_num
        self.length = length
        self.loggers = [get_logger(__name__ + str(x), __name__ + str(x)) for x in range(1, thread_num + 1)]
        logger.info("任务数：%s\t线程数：%s" % (str(length), str(thread_num)))

    def get_range(self):
        # 完成范围的均分
        ranges = []
        length = self.length
        offset = int(int(length) / self.thread_num)
        for i in range(self.thread_num):
            if i == (self.thread_num - 1):
                ranges.append((i * offset, length))
            else:
                ranges.append((i * offset, (i + 1) * offset))
        print(range)
        return ranges

    @staticmethod
    def do_something(start, end, logger: Logger):
        for i in range(start, end):
            logger.info("开始处理page:" + str(i))
            try:
                page = PaperPage(i)
                page.run()
                if not page.valid:
                    # 网页无效时不进行存储
                    return
                # 引用锁机制
                lock.acquire()
                page.paper.save()
                for au in page.authors:
                    au.save()
                lock.release()
            except Exception as e:
                logger.info("发生错误:%s\t%s" % (str(i), e))
            logger.info("完成处理page：" + str(i))

    def start(self):
        thread_list = []
        n = 1
        for ran in self.get_range():
            s1, s2 = ran
            thread = threading.Thread(target=self.do_something, args=(s1, s2, self.loggers[n - 1]))
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
    down = PageThread(30001, 512)
    down.start()
    e = time()
    print("The time spent on this program is %f s" % (e - s))
