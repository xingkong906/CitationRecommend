# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     paper.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          paper.py
   Description :
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'
from util.Log import get_logger
from util.dao import col_paper


class Paper:
    logger = get_logger(TAG=__name__, file_name=__name__)

    def __init__(self):
        # ACL ID
        self._id = ""
        self.url_id = ""
        self.title = ""
        self.authors = []
        self.authors_full_name = []
        self.venue = ""
        self.year = 0
        self.abstract = ""
        # 引用的文章-->paper._id
        self.out_citations = []
        # 被引用的文章-->paper._id
        self.in_citations = []
        # 每一个引文包含了paper_id,line,sentence
        # 字典类型，包含：paper_id(-->paper._id),line(所在行),sentence(引文句);
        self.citing_sentences = []
        self.session = ""

    def save(self):
        # 写入mongoDB数据库，只存一个
        try:
            col_paper.insert_one(self.__dict__)
            self.logger.info("写入\tid:" + self._id)
        except Exception as e:
            self.logger.error("id:%s\turl_id:%s\t%s" % (self._id, self.url_id, e))

