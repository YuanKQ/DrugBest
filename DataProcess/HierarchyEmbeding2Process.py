# -*- coding: utf-8 -*-
"""
__title__ = 'HierarchyEmbeding2Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'May 02,2018 17:19'
__mail__ = kq_yuan@outlook.com

__description__== 将graph embeding的结果序列化: "/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/drug_$hierarchy_embeding_dict.pickle":
                  字典结构, 字典结构, 长度为14333, key为药物(全小写), value为经过node2vec训练后的127维向量(np.arrays(128)类型)

"""
import pickle
import numpy as np

def build_drug_matrix(fileName, feature_name):
    line_count = -1
    drug_hierarchy_embeding_dict = {}
    with open(fileName, 'r') as rf:
        lines = rf.readlines()
    for line in lines:
        line_count += 1
        if line_count == 0:
            continue
        line_list = line.split()
        if len(line_list) > 0:
            node_id = line_list[0]
            node_name = id_drugs[node_id]  # find_key_by_value(node_id, drug_countId_dict)
            if node_name not in drug_hierarchy_embeding_dict.keys():
                embeding_list = [float(i) for i in line_list[1: -1]]
                drug_hierarchy_embeding_dict[node_name] = np.array(embeding_list)

    print(len(drug_hierarchy_embeding_dict), len(drug_hierarchy_embeding_dict['amoxicillin']))
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/drug_%s_embeding_dict.pickle"%feature_name, "wb") as wf:
        pickle.dump(drug_hierarchy_embeding_dict, wf)

if __name__ == '__main__':
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/hierarchyEmbeding_id_drugName.pickle", 'rb') as rf:
        id_drugs = pickle.load(rf)

    build_drug_matrix("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/deepwalk_vec.txt", "deepwalk")
    build_drug_matrix("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/LINE_vec.txt", "LINE")
    build_drug_matrix("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/node2vec_vec.txt", "node2vec")
    print("END")