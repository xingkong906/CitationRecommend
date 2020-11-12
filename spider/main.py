# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     main.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          main.py
   Description :
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'

from spider.author_page_thread import AuthorPageThread
from spider.paper_page_thread import PaperPageThread
from util.dao import col_testPaper, col_paper, col_author, col_page
from time import time
from util.stringUtil import flatten


def author():
    things = []
    for p in col_paper.find():
        things += p['authors']
    things = list(set(things))
    au = AuthorPageThread(things, thread_num=56)
    s = time()
    au.start()
    e = time()
    print("The time spent on this program is %f s" % (e - s))


def paper():
    au = PaperPageThread(range(1, 40000), 128)
    s = time()
    au.start()
    e = time()
    print("The time spent on this program is %f s" % (e - s))


def train_paper():
    things = [p["in_citations"] for p in col_paper.find()]
    things = flatten(things, dtype="s")
    things = list(set(things))
    print(len(things))
    p = [y['url_id'] for y in col_paper.find()]
    # 剔除已经存在的部分
    things = [x for x in things if x not in p]
    # things = [x['_id'] for x in col_page.find({"used": False})]
    au = PaperPageThread(things, 56)
    s = time()
    au.start()
    e = time()
    print("The time spent on this program is %f s" % (e - s))


if __name__ == '__main__':
    # col_page.update_many({"used": True}, {'$set': {"used": False}}, True)
    train_paper()
