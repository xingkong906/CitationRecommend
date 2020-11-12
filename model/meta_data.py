# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     meta_data.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          meta_data.py
   Description :
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.
-------------------------------------------------
"""
__author__ = 'Carl'
from util.dao import col_paper, col_author
from util.Log import get_logger
import re

logger = get_logger(TAG="paper", file_name="paper")


class MetaData:
    def __init__(self):
        self.paper_id = None
        self.title = None
        self.authors = None
        self.venue = None
        self.year = None


def write_data():
    with open("../data_set/acl-metadata.txt", "r", encoding='UTF-8') as f:
        while True:
            try:
                row = MetaData()
                pattern = re.compile(".*{(.*)}.*")
                line=f.readline()
                if not line:
                    break
                row.paper_id = pattern.findall(line)[0]
                line = f.readline()
                authors = pattern.findall(line)[0].strip().replace(", ", ",")
                # 多名作者的处理
                row.authors = str(authors).split("; ")
                for author in row.authors:
                    try:
                        au = col_author.find_one({"full_name": author})
                        papers =set([])
                        if "papers" in au.keys():
                            papers = set(au["papers"])
                        papers.add(row.paper_id)
                        col_author.update_one({"full_name": author}, {"$set": {"papers": list(papers)}})
                    except Exception as e:
                        logger.error("id:%s\tauthor:%s\t%s" % (row.paper_id,author, e))
                        logger.error("line:" + line)
                line = f.readline()
                row.title = pattern.findall(line)[0]
                line=f.readline()
                row.venue = pattern.findall(line)[0]
                line = f.readline()
                row.year = int(pattern.findall(line)[0])
                col_paper.insert_one(row.__dict__)
                logger.info("插入："+row.paper_id)
                f.readline()
            except Exception as e:
                logger.error("id:%s\t\t%s" % (row.paper_id, e))
                logger.error("line:" + line)


if __name__ == '__main__':
    write_data()
