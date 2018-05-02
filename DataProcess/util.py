# -*- coding: utf-8 -*-
"""
__title__ = 'util.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'May 02,2018 15:57'
__mail__ = kq_yuan@outlook.com

__description__== 定义一些常见操作

"""
import numpy as np

def get_all_drugs_as_sets():
    """
    获取drugbank5.0.9所有的药物名称（小写）
    :return: 所有药物名称的集合
    """
    drug_set = set()
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/allDrugName.txt", 'r') as rf:
        lines = rf.readlines()
    for line in lines:
        drug_set.add(line.split()[0])
    return drug_set

def calculate_TFIDF(input_dict, drug_size, feature_size):
    input_metric = np.zeros((drug_size, feature_size)) # input_metric = np.zeros((996, 4492))
    index = 0
    for key in input_dict:
        input_metric[index] = input_dict[key]
        index += 1
    big_metric = np.transpose(input_metric)
    # print(big_metric)
    # DF(t, Drugs): the number of drugs with side effect
    df = big_metric.sum(1)  # 4492*1
    idf = np.log((drug_size + 1) / (df + 1))  # 4492*1
    print("idf:", "max:", np.max(idf), "min:", np.min(idf))
    return np.transpose(idf)  # 1*4492

if __name__ == '__main__':
    get_all_drugs_as_sets()