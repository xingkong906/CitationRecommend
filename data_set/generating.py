# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     generating.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          generating.py
   Description :    用于从数据库中读取数据生成本地数据文件
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'

from util.dao import col_author, col_paper, col_testAuthor, col_testPaper
import json


def bpr_train_data():
    # 生成bpr训练数据
    with open("../data_set/bpr_train.csv", "w", encoding='utf-8')as f:
        # 插入标题栏
        f.write("userId,paperId\n")
        for au in col_author.find():
            id = str(au['id'])
            publications = au['publications']
            for pub in publications:
                f.write("%s,%s\n" % (id, pub))
                f.flush()
    print("bpr_train.csv写入完成")


def ar_train_data():
    process = 0
    all = col_paper.count()
    papers = [x['url_id'] for x in col_paper.find()]
    with open("../data_set/ar_train.data", "w", encoding='utf-8')as f:
        for p in col_paper.find(no_cursor_timeout=True):
            authors = p['authors']
            r_authors = []
            in_citations = p['in_citations']
            in_citations = [x for x in in_citations if x in papers]
            for oc in in_citations:
                oc_paper = col_paper.find_one({'url_id': oc})
                r_authors += oc_paper['authors']
            r_authors = list(set(r_authors))
            sentence = " ".join(enlarge_author(authors, r_authors))
            f.write(sentence + '\n')
            f.flush()
            process += 1
            print("\rprocessing...\t%.2f%%" % (process / all * 100), end="")


def get_ar_authors(filter: {}):
    """
    根据相关条件查询文档中所有相关作者信息
    :param filter:
    :return:
    """
    rs = {}
    papers = [x['url_id'] for x in col_paper.find()]
    for p in col_paper.find(filter, no_cursor_timeout=True):
        authors = p['authors']
        r_authors = []
        in_citations = p['in_citations']
        in_citations = [x for x in in_citations if x in papers]
        for oc in in_citations:
            oc_paper = col_paper.find_one({'url_id': oc})
            r_authors += oc_paper['authors']
        r_authors = list(set(r_authors))
        ar_authors = list(set(r_authors + authors))
        rs[p['url_id']] = [authors, r_authors, ar_authors]
    if filter == {}:
        with open("../data_set/ar_author.json", "w", encoding='utf-8')as f:
            json.dump(rs, f)
    return rs


def get_ar_authors_local():
    return json.load(open("../data_set/ar_author.json"))


def pr_train_data():
    process = 0
    all = col_paper.count()
    with open("../data_set/pr_train.data", "w", encoding='utf-8')as f:
        for p in col_paper.find():
            url_id = [p['url_id']]
            in_citations = p['in_citations']
            sentence = " ".join(enlarge_author(url_id, in_citations))
            f.write(sentence + '\n')
            f.flush()
            process += 1
            print("\rprocessing...\t%.2f%%" % (process / all * 100), end="")


def enlarge_author(authors: list, r_auhors: list, window=3):
    rs = []
    if not r_auhors:
        return authors
    if len(r_auhors) <= window:
        for r in r_auhors:
            rs += authors
            rs.append(r)
        return rs
    index = [x for x in range(len(r_auhors))]
    for au in authors:
        for x in range(window):
            i = x
            while i < len(r_auhors):
                temp = [au]
                temp += r_auhors[i:i + window]
                i = i + window
                if len(temp) == window + 1:
                    rs += temp
    return rs


if __name__ == '__main__':
    print(get_ar_authors({}))
