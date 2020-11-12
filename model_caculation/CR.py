# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     CR.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          CR.py
   Description :    文档相关度
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'

import numpy as np
import time
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pickle
from util.dao import col_paper, col_testPaper
from util.stringUtil import segment
from util.model_caculate import sent2vec, cosine, sim


class LabeledLineSentence(object):

    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield TaggedDocument(doc, [self.labels_list[idx]])


class CR:
    data = []
    data_label = []
    paper_count = 0
    model = None
    sims = None  # 目标文档与系统文档的相关性大小
    topn = 100  # 返回的结果数
    sort_sim = None  # 相关性排序结果，只有文档id
    sys_docs = [x["url_id"] for x in col_paper.find()]
    sys_docs_cr = []

    def __init__(self, topn=100, doc=None):
        """

        :param topn:返回相关结果数
        :param doc: 目标文档，包含标题与摘要组成的字符串
        """
        self.topn = topn
        if doc:
            self.aim_doc = segment(doc)
            self.aim_doc_vec = sent2vec(words=self.aim_doc)

    def init_data_net(self):
        # 从远程数据库中将文档的标题以及引文纳入训练
        for p in col_paper.find():
            sentence = segment(p['abstract']) + segment(p['title'])
            if sentence:
                self.data.append(sentence)
                self.data_label.append(p['url_id'])
        with open("CR/CR_data_lable.bin", 'wb')as f:
            # 将系统数据进行本地缓存，读取时可用data,data_label=pickle.load(open("CR_data_lable.bin", 'wb'))
            pickle.dump([self.data, self.data_label], f)
        self.paper_count = len(self.data_label)

    def init_data_local(self):
        """
        当本地已缓存有数据时，直接读取
        :return:
        """
        self.data, self.data_label = pickle.load(open("CR/CR_data_lable.bin", 'rb'))

    def get_sys_docs_cr(self):
        if self.sys_docs_cr:
            return self.sys_docs_cr
        for d in self.data:
            self.sys_docs_cr.append(sent2vec(self.model, d))
        return self.sys_docs_cr

    def get_model(self):
        if not self.model:
            self.model = Doc2Vec.load("CR/CR.model")
        return self.model

    def train(self):
        sentences = LabeledLineSentence(self.data, self.data_label)
        # 迭代20次
        self.model = Doc2Vec(size=100, window=10, min_count=3,
                             workers=10, iter=20)
        self.model.build_vocab(sentences)
        print("开始训练...")
        # 训练模型
        start = time.time()
        self.model.train(sentences, total_examples=self.model.corpus_count, epochs=12)

        self.model.save("CR/CR.model")
        self.model.save_word2vec_format("CR/CR.vector")
        print("模型已保存，共花时间：", time.time() - start)

    def most_sim(self, doc_vec):
        # 建立相关性索引
        sims = sim(doc_vec, self.get_sys_docs_cr())
        # 对相关度进行排序
        call = np.argsort(-sims)
        return call[:self.topn]

    def test(self):
        test_paper = [x['url_id'] for x in col_testPaper.find()]
        in_citations = [x['in_citations'] for x in col_paper.find()]
        true = 0
        total = 0
        for i in range(len(test_paper)):
            t_vec = sent2vec(self.model, self.data[self.data_label.index(test_paper[i])])
            call=self.most_sim(t_vec)
            inc = [x for x in in_citations[i] if x in self.sys_docs]
            inc_index = [self.data_label.index(x) for x in inc]
            total += len(inc)
            true += len([x for x in inc_index if x in call])
        r_rate = float(true / total)
        t_rate = float(true / (len(test_paper) * self.topn))
        print("召回率：%.2f%%" % r_rate)
        print("准确率：%.2f%%" % t_rate)


if __name__ == '__main__':
    cr = CR()
    cr.init_data_net()
    cr.train()
    cr.test()
