# -*- coding: utf-8 -*-
"""
__title__ = 'SIDER2Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'May 02,2018 21:42'
__mail__ = kq_yuan@outlook.com

__description__== 处理SIDER4+SIDER2
                  每个side effect的IDF值(max: 6.794586580876499 min: 0.001120448296489728):
                  ==> 序列化
                  "../Data/drug_SIDER.pickle": 字典结构, 长度为892, key为药物, 药物与副作用作用关系以长度为4876的np.array来表示, 每一bit代表一种副作用, 0表示不出现, 非零浮点数表示服用该种药物会出现该bit位所代表的副作用)
                  "../Data/characters/SIDER/SIDER_name.pickle": list结构,长度为4876, 指明上述的以长度为4876的np.array的每一bit所指代的副作用名称


"""
import numpy as np

from DataProcess.util import calculate_TFIDF


def build_SIDER_matrix():
    drug_SIDER_matrix = dict()
    for drug in drug_SIDER_dict.keys():
        drug_SIDER_matrix[drug] = np.zeros(col_len)
        for item in drug_SIDER_dict[drug]:
            drug_SIDER_matrix[drug][col_names.index(item)] = 1
    return drug_SIDER_matrix


if __name__ == '__main__':
    drug_SIDER_dict = dict()
    sider_set = set()
    with open("../Data/draft/drug_sider.tsv", "r") as f:
        lines = f.readlines()
        for line in lines:
            items = line.split("\t")
            if len(items) > 0:
                drug = items[0]
                drug_SIDER_dict[drug] = []
                for i in range(1, len(items)):
                    sider = items[i].replace("\n", "")
                    sider_set.add(sider)
                    drug_SIDER_dict[drug].append(sider)

    print(len(sider_set))
    col_len = len(sider_set)
    col_names = list(sider_set)
    col_names.sort()

    drug_SIDER_matrix = build_SIDER_matrix()
    df_sider_drug = calculate_TFIDF(drug_SIDER_matrix, len(drug_SIDER_matrix), col_len)

    kindex = 0
    for key in drug_SIDER_matrix:
        drug_SIDER_matrix[key] = drug_SIDER_matrix[key] * df_sider_drug
        if kindex == 0:
            print(key)
            index = 0
            for value in drug_SIDER_matrix[key]:
                if value != 0:
                    print(col_names[index], value)

                index += 1
        kindex += 1

    # 序列化
    import pickle

    with open("../Data/drug_SIDER.pickle", "wb") as f:
        pickle.dump(drug_SIDER_matrix, f)
    with open("../Data/SIDER_name.pickle", "wb") as f:
        pickle.dump(col_names, f)

    print("END")