# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     processor.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          processor.py
   Description :    对数据库中的数据集进行相关操作
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'
from util.dao import col_author, col_paper


def idx():
    """
    重新对数据库中的所有作者赋予id值
    :return:
    """
    i = 1
    for au in col_author.find():
        col_author.update_one({'_id': au['_id']}, {"$set": {'id': i}})
        print("\r正在处理：", i, end='')
        i += 1
    print("\n完成id重新赋值")


def idx_paper():
    """
        重新对数据库中的所有文档赋予id值
        :return:
        """
    i = 1
    for au in col_paper.find():
        col_author.update_one({'_id': au['_id']}, {"$set": {'id': i}})
        print("\r正在处理：", i, end='')
        i += 1
    print("\n完成id重新赋值")


if __name__ == '__main__':
    idx_paper()
