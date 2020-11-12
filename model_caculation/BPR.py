# -*- coding: utf-8 -*-
# !/usr/bin/python3
"""
-------------------------------------------------
   File Name：     BPR.py
   Author :        Carl
   Author_email:   xingkong906@outlook.com
   date：          BPR.py
   Description :
-------------------------------------------------
#  If this run wrong, don't ask me , I don't know why;
#  If this run right, thank god, and I don't know why.
#  Maybe the answer, my friend, is blowing in the wind.                 
-------------------------------------------------
"""
__author__ = 'Carl'
from pandas import DataFrame, read_csv
import numpy as np
import tensorflow as tf
import random
from collections import defaultdict


class BPR(object):
    testing_data = []
    X_user = None
    X_pos_item = None
    X_neg_item = None
    X_predict = None
    loss = None
    optimizer = None
    predict = None
    topn = 100

    def __init__(self, data: DataFrame, n_epochs=10, batch_size=32,
                 train_sample_size=10,
                 test_sample_size=50,
                 num_k=100, evaluation_at=10):
        """
        BPR算法实现
        :param train_data: 训练集
        :param test_data: 测试集
        :param n_epochs: 隐藏层层数
        :param batch_size:
        :param train_sample_size: 训练时，正样本个例对应多少个负样本
        :param test_sample_size: 测试时，正样本个例对应多少个负样本
        :param num_k: item embedding的维度
        :param evaluation_at: 返回多少个结果
        """
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.train_sample_size = train_sample_size
        self.test_sample_size = test_sample_size
        self.num_k = num_k
        self.evaluation_at = evaluation_at

        self.data = data
        self.num_user = len(self.data['userId'].unique())
        self.num_item = len(self.data['paperId'].unique())
        self.num_event = len(self.data)
        self.all_item = set(self.data['paperId'].unique())
        self.experiment = []

        # Because the id is not always continuous , we build a map to normalize id . For example:[1,3,5,156]->[0,1,2,3]
        user_id = self.data['userId'].unique()
        self.user_id_map = {user_id[i]: i for i in range(self.num_user)}
        item_id = self.data['paperId'].unique()
        self.item_id_map = {item_id[i]: i for i in range(self.num_item)}
        training_data = self.data.loc[:, ['userId', 'paperId']].values
        self.training_data = [[self.user_id_map[training_data[i][0]], self.item_id_map[training_data[i][1]]] for i in
                              range(self.num_event)]  # 数据格式为：[[userId,itemId],[],[]]
        self.data_dic = defaultdict(set)
        for t in self.training_data:
            self.data_dic[t[0]].add(t[1])
        # data preprocess
        self.split_data()
        self.sample_dict = self.negative_sample()

        self.build_model()  # build TF graph
        self.sess = tf.Session()  # create session
        self.sess.run(tf.global_variables_initializer())

    def split_data(self):
        # 将data 切分为training_data and testing_data
        # testing_data生成过程为从user中随机选择一个其对应的item
        # 按照userId对paperId进行分组，并使用set进行去重user_session=[{},{},{}...]
        user_session = self.data.groupby('userId')['paperId'].apply(set).reset_index().loc[:,
                       ['paperId']].values.reshape(-1)
        for index, session in enumerate(user_session):
            random_pick = self.item_id_map[random.sample(session, 1)[0]]
            self.training_data.remove([index, random_pick])
            self.testing_data.append([index, random_pick])

    def negative_sample(self):
        # 生成负样本，每个user对应train_sample_size个负样本，默认大小为10
        # 生成的过程为随机从其非对应的item中选取10个
        user_session = self.data.groupby('userId')['paperId'].apply(set).reset_index().loc[:,
                       ['paperId']].values.reshape(-1)
        sample_dict = {}

        for td in self.training_data:
            sample_dict[tuple(td)] = [self.item_id_map[s] for s in
                                      random.sample(self.all_item.difference(user_session[td[0]]),
                                                    self.train_sample_size)]

        return sample_dict

    def build_model(self):
        self.X_user = tf.placeholder(tf.int32, shape=(None, 1))
        self.X_pos_item = tf.placeholder(tf.int32, shape=(None, 1))
        self.X_neg_item = tf.placeholder(tf.int32, shape=(None, 1))
        self.X_predict = tf.placeholder(tf.int32, shape=(1))

        user_embedding = tf.Variable(tf.truncated_normal(shape=[self.num_user, self.num_k], mean=0.0, stddev=0.5))
        item_embedding = tf.Variable(tf.truncated_normal(shape=[self.num_item, self.num_k], mean=0.0, stddev=0.5))

        embed_user = tf.nn.embedding_lookup(user_embedding, self.X_user)
        embed_pos_item = tf.nn.embedding_lookup(item_embedding, self.X_pos_item)
        embed_neg_item = tf.nn.embedding_lookup(item_embedding, self.X_neg_item)

        pos_score = tf.matmul(embed_user, embed_pos_item, transpose_b=True)
        neg_score = tf.matmul(embed_user, embed_neg_item, transpose_b=True)

        self.loss = tf.reduce_mean(-tf.log(tf.nn.sigmoid(pos_score - neg_score)))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(self.loss)

        predict_user_embed = tf.nn.embedding_lookup(user_embedding, self.X_predict)
        self.predict = tf.matmul(predict_user_embed, item_embedding, transpose_b=True)

    def fit(self):
        self.experiment = []
        for epoch in range(self.n_epochs):
            np.random.shuffle(self.training_data)
            total_loss = 0
            for i in range(0, len(self.training_data), self.batch_size):
                training_batch = self.training_data[i:i + self.batch_size]
                user_id = []
                pos_item_id = []
                neg_item_id = []
                for single_training in training_batch:
                    for neg_sample in list(self.sample_dict[tuple(single_training)]):
                        user_id.append(single_training[0])
                        pos_item_id.append(single_training[1])
                        neg_item_id.append(neg_sample)

                user_id = np.array(user_id).reshape(-1, 1)
                pos_item_id = np.array(pos_item_id).reshape(-1, 1)
                neg_item_id = np.array(neg_item_id).reshape(-1, 1)

                _, loss = self.sess.run([self.optimizer, self.loss],
                                        feed_dict={self.X_user: user_id, self.X_pos_item: pos_item_id,
                                                   self.X_neg_item: neg_item_id}
                                        )
                total_loss += loss

            num_true = 0
            for test in self.testing_data:
                result = self.sess.run(self.predict, feed_dict={self.X_predict: [test[0]]})
                result = result.reshape(-1)
                # if (result[[self.item_id_map[s] for s in random.sample(self.all_item, self.test_sample_size)]] > result[
                #     test[1]]).sum() + 1 <= self.evaluation_at:
                #     num_true += 1

                # print("epoch:%d , loss:%.2f , recall:%.2f" % (epoch, total_loss, num_true / len(self.testing_data)))
                # self.experiment.append([epoch, total_loss, num_true / len(self.testing_data)])

    def test(self, topn=100):
        true = 0
        total = 0
        user_grop = self.data.groupby("userId")
        for t in self.testing_data:
            result = self.sess.run(self.predict, feed_dict={self.X_predict: [t[0]]})
            items = self.data_dic[t[0]]
            total = len(items)
            result = result.reshape(-1)
            index = np.argsort(result)[:topn]
            total += len(self.training_data)
            true = len([x for x in items if x in result])
        r_rate = float(true / total)
        t_rate = float(true / (len(self.testing_data) * self.topn))
        print("召回率：%.2f%%" % r_rate)
        print("准确率：%.2f%%" % t_rate)


if __name__ == '__main__':
    data = read_csv("../data_set/bpr_train.csv")
    bpr = BPR(data)
    bpr.fit()
    bpr.test()
