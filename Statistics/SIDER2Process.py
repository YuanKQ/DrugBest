# -*- coding: utf-8 -*-
"""
__title__ = 'SIDER2Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Oct 20,2017 11:39'
__mail__ = kq_yuan@outlook.com

__description__== 处理SIDER2的meddra_adverse_effects.tsv文件 (996 drugs, 4492 side effects)
                  每个side effect的IDF值(max 6.90476, min 0.1954):
                  药物(第4行, drug name)与side effect(第8行, MedDRA side effect name)的矩阵(996*4492)
                  ==> 序列化
                  "../Data/characters/SIDER/drug_SIDER.pickle": 字典结构, 长度为992, key为药物, 药物与副作用作用关系以长度为4492的np.array来表示, 每一bit代表一种副作用, 0表示不出现, 非零浮点数表示服用该种药物会出现该bit位所代表的副作用)
                  "../Data/characters/SIDER/SIDER_name.pickle": list结构,长度为4492, 指明上述的以长度为4492的np.array的每一bit所指代的副作用名称

"""
from Statistics.antibioticCount import read_from_splitFile
import numpy as np


def build_SIDER_matrix():
    index = 0
    SIDER_dict = dict()
    with open("../Data/draft/meddra_adverse_effects.tsv", "r") as f:
        lines = f.readlines()
        for line in lines:
            items = line.split("\t")
            if len(items) >= 8:
                drug = items[3].lower()
                side_effect = items[7].replace("\n", "").lower()
                if drug in SIDER_dict:
                    index = col_names.index(side_effect)
                    SIDER_dict[drug][index] = 1  # 此处将修改为IDF值
                else:
                    SIDER_dict[drug] = np.zeros(4492)
    return SIDER_dict


def calculate_TFIDF(input_dict, drug_size, feature_size):
    input_metric = np.zeros((drug_size, feature_size)) # input_metric = np.zeros((996, 4492))
    index = 0
    for key in input_dict:
        input_metric[index] = input_dict[key]
        index += 1
    big_metric = np.transpose(input_metric)
    print(big_metric)
    # DF(t, Drugs): the number of drugs with side effect
    df = big_metric.sum(1)  # 4492*1
    idf = np.log((drug_size + 1) / (df + 1))  # 4492*1
    print("idf:", np.max(idf), np.min(idf))
    return np.transpose(idf)  # 1*4492


def validate_pickle():
    print("-------------------")
    with open("../Data/characters/SIDER/drug_SIDER.pickle", 'rb') as rf:
        out_dict = pickle.load(rf)
    with open("../Data/characters/SIDER/SIDER_name.pickle", 'rb') as rf:
        cols = pickle.load(rf)
    tmp_index = 0
    for key in out_dict:
        if tmp_index == 0:
            print(key)
            index = 0
            for value in out_dict[key]:
                if value != 0:
                    print(cols[index], value)
                index += 1
        break


if __name__ == '__main__':
    SIDER_SIZE = 4492
    DRUG_SIZE = 996
    col_names = []  # 列: side_effect
    row_names = []  # 行: drug_name

    row_names = list(read_from_splitFile("../Data/draft/meddra_adverse_effects.tsv", "\t", [3, ]))
    col_names = list(read_from_splitFile("../Data/draft/meddra_adverse_effects.tsv", "\t", [7, ]))

    # 字母序
    row_names.sort()
    col_names.sort()

    print(row_names)
    print(col_names)

    SIDER_dict = build_SIDER_matrix()
    df_sider_drug = calculate_TFIDF(SIDER_dict, DRUG_SIZE, SIDER_SIZE)

    kindex = 0
    for key in SIDER_dict:
        SIDER_dict[key] = SIDER_dict[key] * df_sider_drug
        if kindex == 0:
            print(key)
            index = 0
            for value in SIDER_dict[key]:
                if value != 0:
                    print(col_names[index], value)

                index += 1
        kindex += 1

    # 序列化
    import pickle
    with open("../Data/characters/SIDER/drug_SIDER.pickle", "wb") as f:
        pickle.dump(SIDER_dict, f)
    with open("../Data/characters/SIDER/SIDER_name.pickle", "wb") as f:
        pickle.dump(col_names, f)

    validate_pickle()





