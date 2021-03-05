# -*- coding: utf-8 -*-
import jieba
import numpy as np


# 返回分词后的数组
def get_cut_words(t):
    cuts = jieba.cut(t)

    return list(cuts)


# 将两段文本向量化
def get_vectors(t1, t2):
    # 分词
    words1 = get_cut_words(t1)
    words2 = get_cut_words(t2)

    # 取去重后的所有词
    words_all = list(set(words1 + words2))
    len_all = len(words_all)

    # 初始化向量（0矩阵）
    v1 = np.zeros(len_all)
    v2 = np.zeros(len_all)

    # 计算词频（确定向量的每个位置的值）
    for i in range(len_all):
        word = words_all[i]

        v1[i] = words1.count(word)
        v2[i] = words2.count(word)

    print("分词结果，句1：{}".format(words1))
    print("分词结果，句2：{}".format(words2))
    print("汇总去重结果：{}".format(words_all))
    print("向量1：{}".format(v1))
    print("向量2：{}".format(v2))

    return v1, v2


# 计算两个向量的余弦相似度
def get_dist(v1, v2):
    d = float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    return d


if __name__ == '__main__':
    title1 = "腾讯今天发布去年Q4财报"
    title2 = "腾讯今天发布今年Q4财报"
    vec1, vec2 = get_vectors(title1, title2)
    dist = get_dist(vec1, vec2)

    print("相似度：{}".format(dist))
