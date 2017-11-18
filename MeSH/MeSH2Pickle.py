# -*- coding: utf-8 -*-
"""
__title__ = 'MeSH2Pickle.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 05,2017 20:54'
__mail__ = kq_yuan@outlook.com

__description__== 将graph embeding的结果序列化:
                  "/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/MeSH/drug_MeSH_embeding_dict.pickle":
                  字典结构, 字典结构, 长度为9353, key为药物(全小写), value为经过node2vec训练后的128w维向量(np.arrays(128)类型)

"""
import pickle
import numpy as np

from MeSH.MeSH2Process import find_key_by_value
from Statistics.antibioticCount import read_from_splitFile

def build_all_MeSH_matrix():
    drug_MeSH_embeding_dict = {}

    with open("/home/yuan/Code/PycharmProjects/DrugBest/MeSH/MeSH_data/drug_countId_dict.pickle", 'rb') as rf:
        drug_countId_dict = pickle.load(rf)

    drug_list = ["l"] * 10000
    for key, value in drug_countId_dict.items():
        drug_list[value] = key

    line_count = -1
    with open("/home/yuan/Code/PycharmProjects/DrugBest/MeSH/MeSH_data/MeSH.emd", 'r') as rf:
        lines = rf.readlines()
        for line in lines:
            line_count += 1
            if line_count == 0:
                continue
            line_list = line.split()
            if len(line_list) > 0:
                node_id = line_list[0]
                node_name = drug_list[int(node_id)]  # find_key_by_value(node_id, drug_countId_dict)
                if node_name not in drug_MeSH_embeding_dict.keys():
                    embeding_list = [float(i) for i in line_list[1: -1]]
                    drug_MeSH_embeding_dict[node_name] = np.array(embeding_list)

    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/MeSH/drug_MeSH_embeding_dict.pickle", "wb") as wf:
        pickle.dump(drug_MeSH_embeding_dict, wf)


def build_ddi_MeSH_matrix():
    # only extract ddi drugs from mesh graph embeding
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/MeSH/drug_MeSH_embeding_dict.pickle", 'rb') as rf:
        drug_MeSH_embeding_dict = pickle.load(rf)
    drugs_DDI = read_from_splitFile("../Data/draft/Drugbank4-PDDIs.csv", "$", [1, 3])
    # print("drugs_DDI: ", drugs_DDI)
    drug_MeSH_embeding_dict_ddi_dict = {}
    for drug in drugs_DDI:
        if drug in drug_MeSH_embeding_dict.keys():
            drug_MeSH_embeding_dict_ddi_dict[drug] = drug_MeSH_embeding_dict[drug]
    print(len(drug_MeSH_embeding_dict_ddi_dict))
    # print("drug_MeSH_embeding_dict.keys(): ", drug_MeSH_embeding_dict.keys())
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/MeSH/drug_MeSH_ddi_dict.pickle", "wb") as wf:
        pickle.dump(drug_MeSH_embeding_dict_ddi_dict, wf)

if __name__ == '__main__':
    build_ddi_MeSH_matrix()