# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     strings.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          strings.py
   Description :
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'

# 函数默认返回值
func_return = {"str": "", "list": [], "set": {}, "int": 0, "bool": False}


def get_stop_words():
    rs = []
    with open("../util/ENstopwords.txt", "r", encoding='utf-8')as f:
        for line in f.readlines():
            rs.append(line.strip())
    return rs


_stop_words = get_stop_words()
