# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     model_caculate.py
   Author :        Administrator
   Author_email:   xingkong906@outlook.com
   date：          model_caculate.py
   Description :    模型计算相关函数
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Administrator'
import numpy as np


def sent2vec(model=None, words=[]):
    """
    从词列表构建文档向量
    :param model:  word2vec模型
    :param words:
    :return:
    """
    vect_list = []
    for w in words:
        try:
            vect_list.append(model.wv[w])
        except:
            continue
    vect_list = np.array(vect_list)
    vect = vect_list.sum(axis=0)
    rs=vect / np.sqrt((vect ** 2).sum())
    return rs


def similarity(a_vect, b_vect):
    """
    计算余弦相似度
    :param b_vect:
    :return:
    """
    dot_val = 0.0
    a_norm = 0.0
    b_norm = 0.0
    cos = None
    for a, b in zip(a_vect, b_vect):
        dot_val += a * b
        a_norm += a ** 2
        b_norm += b ** 2
    if a_norm == 0.0 or b_norm == 0.0:
        cos = -1
    else:
        cos = dot_val / ((a_norm * b_norm) ** 0.5)

    return cos


def cosine(_vec1, _vec2):
    a = float(np.sum(_vec1 * _vec2))
    b = (np.linalg.norm(_vec1) * np.linalg.norm(_vec2))
    rs = a / b
    return rs


def sim(vec1, vecs: list):
    """
    计算一个变量与多个变量的相关度
    :param vec1:
    :param vecs:
    :return:
    """
    rs = np.zeros(len(vecs))
    for i in range(len(vecs)):
        rs[i] = cosine(vec1, vecs[i])

    return rs