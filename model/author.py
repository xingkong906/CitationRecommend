# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     processor.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          processor.py
   Description :
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'
from util.Log import get_logger
from util.dao import col_author


class Author:
    logger = get_logger(TAG=__name__, file_name=__name__)

    def __init__(self, _id=None, full_name=None):
        """

        :param _id: id为字符串类型
        :param full_name:
        """
        self._id = str(_id)
        self.full_name = full_name
        self.papers_count = 0
        # 为了便于计算，合作者包括自己
        self.partners_full_name = []
        self.partners_id = []
        self.affiliations = []
        self.collaborators = []
        # 作者所发表的文章-->paper.url_id
        self.publications = []
        self.insert_flag = True
        self.search()

    def search(self):
        """
        根据ID查询数据库中的信息
        :return:
        """
        try:
            au = col_author.find_one({"_id": self._id})
            if au is not None:
                if not self.full_name:
                    self.full_name = au["full_name"]
                self.partners_full_name = au['partners_full_name']
                self.partners_id = au['partners_id']
                self.papers_count = au['partners_id']
                self.partners_id = au['partners_id']
                self.affiliations = au['affiliations']
                self.collaborators = au['collaborators']
                # 作者所发表的文章-->paper.url_id
                self.publications = au['publications']
                self.insert_flag = False
        except Exception as e:
            self.logger.error("id:%s\t%s" % (self._id, e))

    def add_partner_full_name(self, authors_name: list):
        rs = set(self.partners_full_name)
        rs = rs.union(authors_name)
        self.partners_full_name = list(rs)

    def add_partner_id(self, _id: list):
        rs = set(self.partners_id)
        rs = rs.union(_id)
        self.partners_id = list(rs)

    def save(self):
        # 写入mongoDB数据库
        try:
            if self.insert_flag:
                col_author.insert_one(self.__dict__)
            else:
                col_author.replace_one({"_id": self._id}, self.__dict__)
            self.logger.info("写入\tid:" + self._id)
        except Exception as e:
            self.logger.error("id:%s\t%s" % (self._id, e))


if __name__ == '__main__':
    a = Author(10, "1")
    print(a.publications)
    a.save()
    print(a.publications)
