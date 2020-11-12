# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     PR.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          PR.py
   Description :    文档ID相关度
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
import time

from gensim.models.word2vec import LineSentence, Word2Vec

from util.dao import col_testPaper, col_paper

__author__ = 'Carl'


class PR:
    """
    输出模型文件：
    PR.model：模型参数
    PR.vector:词向量
    """
    data_path = "../data_set/pr_train.data"
    model_path = "PR/PR.model"  # 模型参数缓存文件路径
    vector_path = "PR/PR.vector"  # 词向量缓存路径
    model = None
    sims = None  # 目标文档与系统文档的相关性大小
    topn = 100  # 返回的结果数
    sort_sim = None  # 相关性排序结果，只有文档idy
    sys_docs = [x["url_id"] for x in col_paper.find()]

    def __init__(self, topn=100):
        self.topn = topn

    def init_data_net(self):
        """
        生成ar.text文件
        :return:
        """
        pass

    def train(self):
        start = time.time()
        # 直接从文本文件中读取数据集
        sentences = LineSentence(self.data_path)
        self.model = Word2Vec(sentences, min_count=2, sg=1, hs=1, size=100, window=5, workers=4, iter=20)

        self.model.save(self.model_path)
        self.model.wv.save_word2vec_format(self.vector_path, binary=False)
        print("模型已保存，训练共花时间：", time.time() - start)

    def test(self):
        test_paper = [x['url_id'] for x in col_testPaper.find()]
        in_citations = [x['in_citations'] for x in col_paper.find()]
        total = 0
        true = 0
        for t in range(len(test_paper)):
            mode_sim = self.model.wv.most_similar(test_paper[t], topn=self.topn)
            call = [x[0] for x in mode_sim]
            inc = [x for x in in_citations[t] if x in self.sys_docs]
            total += len(inc)
            true = len([x for x in call if x in inc])
        r_rate = float(true / total)
        t_rate = float(true / (len(test_paper) * self.topn))
        print("召回率：%.2f%%" % r_rate)
        print("准确率：%.2f%%" % t_rate)

    def get_model(self):
        if not self.model:
            self.model = Word2Vec.load("PR.model")
        return self.model


if __name__ == '__main__':
    pr = PR()
    pr.train()
    pr.test()
