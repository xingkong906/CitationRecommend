# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     author_page.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          author_page.py
   Description :
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'
from util.downloader import Downloader
from util.Log import get_logger
# from spider.paper_page_thread import PaperPageThread
from model.author import Author
from util.stringUtil import *
from lxml import etree
from util.dao import col_paper, col_page

host = "http://aan.how/browse/author/"


class AuthorPage(object):
    valid = False  # 网页数据的有效性，无效则不进行解析与储存
    logger = get_logger(__name__, __name__)

    def __init__(self, _id, content=None, **kwargs):
        self._id = str(_id)
        self.author = Author(_id=self._id)
        if not self.author.full_name:
            self.valid = True
        else:
            return
        if self.author.insert_flag:
            if content is None:
                self.content = Downloader(host + self._id)()
                if self.content:
                    self.valid = True
                else:
                    self.logger.error("当前网页为空，无法进行解析\t_id:" + self._id)
                    self.valid = False
                    return
            else:
                self.valid = True
                self.content = content
            self.selector = etree.HTML(self.content)

    def run(self):
        if not self.valid:
            self.logger.info("该author已存在\t_id:" + self._id)
            return
        self.logger.info("开始解析author：" + self._id)
        self.main_page()
        if not self.author.insert_flag:
            self.logger.info("无效网页，已剔除:" + self._id)
            return
        self.get_partners()
        self.get_papers()
        self.author.save()
        self.save_publications()
        self.logger.info("完成author：" + self._id)

    def main_page(self):
        self.author.full_name = deep_select(self.selector, 0, xpath="//head/title/text()").replace("AAN: ", "")
        if "ValueError" in self.author.full_name:
            self.author.insert_flag = False
            self.valid = False
            return
        self.author.publications = deep_select(self.selector, 0, xpath="//table/tbody/tr[1]/td/text()")
        self.author.affiliations = deep_select(self.selector, return_type="list",
                                               xpath="//table/tbody/tr[5]/td/ul/li/text()")

    def get_partners(self):
        if not self.valid:
            return
        self.selector = etree.HTML(Downloader('http://aan.how/browse/author/collaborators/' + self._id)())
        name = deep_select(self.selector, return_type="list",
                           xpath="//tr[@class='gradeA']/td[1]/a/text()")
        self.author.partners_full_name = name
        # 合作文章数量
        num = deep_select(self.selector, return_type="list",
                          xpath="//tr[@class='gradeA']/td[2]/text()")
        for x in range(len(name)):
            papers_id = deep_select(self.selector, return_type="list",
                                    xpath="//tr[@class='gradeA'][" + str(x + 1) + "]/td[3]/a/text()")
            self.author.collaborators.append({"author": name[x], "num": num[x], "papers_id": papers_id})

        partners_id = deep_select(self.selector, return_type="list",
                                  xpath="//tr[@class='gradeA']/td[1]/a/@href")
        self.author.partners_id = [to_num(x) for x in partners_id]

    def get_papers(self):
        if not self.valid:
            return
        self.selector = etree.HTML(Downloader('http://aan.how/browse/author/publications/' + self._id)())
        papers_url_id = deep_select(self.selector, return_type="list",
                                    xpath="///tr[@class='gradeA']/td[2]/a/@href")
        self.author.papers_count = len(papers_url_id)
        self.author.publications = [to_num(x) for x in papers_url_id]
        # 使用多线程爬取网页
        # paper_thread = PaperPageThread(self.author.publications, 10)
        # paper_thread.start()

    def save_many(self, papers: []):
        # 一次存多个对象
        ids = [x for x in papers._id]
        try:
            col_paper.insert_many([x.__dict__ for x in papers])
        except Exception as e:
            self.logger.error("ids:%s\t%s" % (ids, e))

    def save_publications(self):
        for x in self.author.publications:
            col_page.update_one({"_id": x}, {'$set': {"used": False}}, True)


if __name__ == '__main__':
    a = AuthorPage(24724)
    a.run()
