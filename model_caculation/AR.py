# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     AR.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          AR.py
   Description :    作者相关度
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'
from gensim.models.word2vec import Word2Vec, LineSentence
from util.dao import col_testPaper, col_paper
import time
from data_set.generating import get_ar_authors_local
from util.model_caculate import *


class AR:
    data_path = "../data_set/ar_train.data"
    model_path = "AR/AR.model"  # 模型参数缓存文件路径
    vector_path = "AR/AR.vector"  # 词向量缓存路径
    model = None
    sims = None  # 目标文档与系统文档的相关性大小
    topn = 100  # 返回的结果数
    sort_sim = None  # 相关性排序结果，只有文档idy
    sys_doc_au = {}  # 系统文档相关作者
    sys_doc_map = {}
    sys_doc_ar = []  # 保存系统中所有文档的ar模型表示,key为url_id

    def __init__(self):
        self.sys_doc_au = get_ar_authors_local()
        i = 0
        for key, _ in self.sys_doc_au.items():
            self.sys_doc_map[key] = i
            i += 1

    def init_data_net(self):
        """
        生成ar.text文件
        :return:
        """
        pass

    def init_data_local(self):
        self.sys

    def train(self):
        start = time.time()
        # 直接从文本文件中读取数据集
        sentences = LineSentence(self.data_path)
        self.model = Word2Vec(sentences, min_count=3, size=100, window=5, workers=4)

        self.model.save(self.model_path)
        self.model.wv.save_word2vec_format(self.vector_path, binary=False)
        print("模型已保存，训练共花时间：", time.time() - start)

    def get_model(self):
        if not self.model:
            self.model = Word2Vec.load("CR.model")
        return self.model

    def most_similar(self, aim_author: list):
        """
        获取推荐结果集
        :param aim_author:
        :return:
        """
        tv = sent2vec(self.model, aim_author)
        r = sim(tv, self.get_sys_doc_ar())
        r = np.argsort(-r)
        return r[:self.topn]

    def get_sys_doc_ar(self):
        if self.sys_doc_ar:
            return self.sys_doc_ar
        for _, value in self.sys_doc_au.items():
            self.sys_doc_ar.append(sent2vec(self.model, value[2]))
        return self.sys_doc_ar

    def test(self):
        test_paper = [x['url_id'] for x in col_testPaper.find()]
        true = 0
        total = 0
        for t in test_paper:
            au = self.sys_doc_au[t]
            pubs = col_testPaper.find_one({'url_id': t})['in_citations']
            total += len(pubs)
            recall = self.most_similar(au[2])
            pubs = [self.sys_doc_map[x] for x in pubs if x in self.sys_doc_map.keys()]
            true += len([x for x in recall if x in pubs])
        r_rate = float(true / total)
        t_rate = float(true / (len(test_paper) * self.topn))
        print("召回率：%.2f%%" % r_rate)
        print("准确率：%.2f%%" % t_rate)


if __name__ == '__main__':
    ar = AR()
    ar.train()
    ar.test()
