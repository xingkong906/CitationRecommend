# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     dao.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          dao.py
   Description :
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'
import pymongo

client = pymongo.MongoClient('120.77.157.222', 27017)
db = client['test_data']
col_paper = db["paper"]
col_author = db["author"]
col_page = db["page"]
col_testPaper = db["testPaper"]
col_testAuthor = db["testAuthor"]
