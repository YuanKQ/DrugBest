# -*- coding: utf-8 -*-
"""
__title__ = 'wordembeding2Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 06,2017 09:01'
__mail__ = kq_yuan@outlook.com

__description__== 将python2序列化结果"/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/drug_word2vec_dict.pickle"
                  以python3重新序列化, 保存至"/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/Word2Vec/drug_word2vec_dict.pickle"
                  序列化结果:
                  "/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/Word2Vec/drug_word2vec_dict.pickle":
                  字典结构, size=1065, key为药物名称(全小写), value为训练得到的词向量(长度为200的np.ndarray)

"""
import pickle

from Statistics.antibioticCount import read_from_splitFile

with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/drug_word2vec_dict.pickle" , 'rb') as rf:
    drug_word2vec_dict = pickle.load(rf, encoding="latin1")

print(drug_word2vec_dict["cilazapril"], len(drug_word2vec_dict), len(drug_word2vec_dict["cilazapril"]), type(drug_word2vec_dict["cilazapril"]))
# print(drug_word2vec_dict["amikacin"])

# with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/Word2Vec/drug_word2vec_dict.pickle", "wb") as wf:
#     pickle.dump(drug_word2vec_dict, wf)

drugs_DDI = read_from_splitFile("../Data/draft/Drugbank4-PDDIs.csv", "$", [1, 3])
drug_word2vec_ddi_dict = {}
for drug in drugs_DDI:
    if drug in drug_word2vec_dict.keys():
        drug_word2vec_ddi_dict[drug] = drug_word2vec_dict[drug]

print("ddi length:", len(drug_word2vec_ddi_dict)) # len(drug_word2vec_ddi_dict) = len(drug_word2vec_dict)

with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/Word2Vec/drug_word2vec_ddi_dict.pickle", "wb") as wf:
    pickle.dump(drug_word2vec_ddi_dict, wf)
