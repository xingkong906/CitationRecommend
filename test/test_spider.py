# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     test_spider.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          test_spider.py
   Description :
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'
from lxml import etree
from util.downloader import Downloader
from util.stringUtil import deep_select

# content = open("data.html", "r", encoding='utf-8').read()
content = Downloader(url='http://aan.how/browse/author/publications/3835')()
selector = etree.HTML(content)
# f = open("data.html", "w", encoding="utf-8")
# f.write(etree.tostring(selector).decode("utf-8"))
# f.close()
author = "//tr[@class='gradeA']/td[2]/a/@href"
print(len(deep_select(selector, return_type="list", xpath=author)))
