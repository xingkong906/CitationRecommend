# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     paper_page.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          paper_page.py
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
from model.paper import Paper
from util.stringUtil import *
from util.dao import col_paper
from lxml import etree

logger = get_logger("paper_page", "paper_page")
host = "http://aan.how/browse/paper/"


class PaperPage(object):
    valid = False  # 网页数据的有效性，无效则不进行解析与储存

    def __init__(self, _id, content=None, **kwargs):
        self._id = str(_id)
        self.paper = Paper()
        page_data = col_paper.find_one({"url_id": self._id})
        if page_data:
            # 数据库中已经存在，直接返回
            return
        if content is None:
            self.content = Downloader(host + self._id)()
            if self.content:
                self.valid = True
            else:
                logger.error("当前网页为空，无法进行解析\turl_id:"+self._id)
                self.valid=False
                return
        else:
            self.valid=True
            self.content = content
        self.selector = etree.HTML(self.content)
        self.paper.url_id = self._id

    def run(self):
        if not self.valid:
            logger.info("该paper已存在\turl_id:" + self._id)
            return
        self.main_page()
        self.get_in_citation()
        if len(self.paper.in_citations) < 1:
            logger.info("该paper参考文献小于1，已进行排除\turl_id:" + self._id)
            return
        self.get_citing_sentence()
        self.get_out_citation()
        self.paper.save()
        logger.info("完成解析\turl:%s\tpaper_id:%s" % (self._id, self.paper._id))

    def main_page(self):
        try:
            self.paper.year = to_int(deep_select(self.selector, 0, "//table//tr[5]/td/text()"))
            # if self.paper.year < 2013:
            #     # 对数据集进行筛选
            #     return
            # 列出所有作者
            authors = deep_select(self.selector, return_type="list", xpath="//table//tr[6]/td//a/@href")
            if not authors:
                # 如果self.paper中无作者，则直接剔除数据
                self.valid = False
                return
            authors_id = [to_num(x) for x in authors]
            self.paper.authors_full_name = deep_select(self.selector, return_type="list",
                                                       xpath="//table//tr[6]/td//a/text()")
            self.paper.authors = authors_id
            self.paper._id = deep_select(self.selector, 0, "//table//tr[1]/td/text()")
            if not self.paper._id:
                self.valid = False
                return
            self.paper.title = deep_select(self.selector, 0, "//table//tr[2]/td/text()")
            self.paper.venue = deep_select(self.selector, 0, "//table//tr[3]/td/text()")
            self.paper.session = deep_select(self.selector, 0, "//table//tr[4]/td/text()")

            self.paper.abstract = clean(deep_select(self.selector, 0, '//div[@id="abstract"]/p/text()'))
        except Exception as e:
            logger.error("id:%s\t%s" % (self._id, e))

    def get_out_citation(self):
        if not self.valid:
            return
        self.selector = etree.HTML(Downloader('http://aan.how/browse/outgoing_citations/' + self._id)())
        out_citations = deep_select(self.selector, return_type="list", xpath='//a/@href')
        if out_citations:
            self.paper.out_citations = [to_num(x) for x in out_citations]

    def get_in_citation(self):
        if not self.valid:
            return
        self.selector = etree.HTML(Downloader('http://aan.how/browse/incoming_citations/' + self._id)())
        in_citations = deep_select(self.selector, return_type="list",
                                   xpath='//a/@href')
        if in_citations:
            self.paper.in_citations = [to_num(x) for x in in_citations]

    def get_citing_sentence(self):
        if not self.valid:
            return
        self.selector = etree.HTML(Downloader('http://aan.how/browse/citing_sentences/' + self._id)())
        paper_id = deep_select(self.selector, return_type="list", xpath='//a/text()')
        sentence = deep_select(self.selector, return_type="list", xpath="//tr/td[4]/div/text()")
        line = deep_select(self.selector, return_type="list", xpath="//tr/td[3]/text()")
        if paper_id and sentence:
            for x in range(len(paper_id)):
                citing_sentences = {"paper_id": paper_id[x], "sentence": clean(sentence[x]), "line": line[x]}
                self.paper.citing_sentences.append(citing_sentences)


if __name__ == '__main__':
    item = PaperPage(31007)
    # item.lab_notes()
    item.run()
