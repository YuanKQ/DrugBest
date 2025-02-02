# -*- coding: utf-8 -*-
"""
__title__ = 'DDS.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 10,2017 09:52'
__mail__ = kq_yuan@outlook.com

__description__== 删除特征向量全为0的药物, 去掉不曾使用的特征
                  单个特征:
                  drug_actionCode_matrix_dict 557 188
                  drug_phyCode_matrix_dict    557 320
                  drug_SIDER_matrix_dict      557 3304
                  drug_enzyme_matrix_dict     557 141
                  drug_target_matrix_dict     557 773
                  drug_atc_matrix_dict        557 619
                  drug_MACCS_matrix_dict      557 158
                  drug_MeSH_matrix_dict       557 127
                  drug_word2vec_matrix_dict   557 100
                  ------------------------------------
                  total: drug_all_dict        557 5730

"""
from Statistics.antibioticCount import read_from_splitFile
import pickle
import numpy as np


def read_pickle_to_dict(file):
    drug_character_dict = {}
    with open(file, 'rb') as rf:
        old_drug_character_dict = pickle.load(rf)

    # 记得将dict中的key值全部转化为小写
    for drug in old_drug_character_dict.keys():
        drug_character_dict[drug.lower()] = old_drug_character_dict[drug]
    return drug_character_dict


def write_dict_to_pickle(drug_character_dict, file_name):
    print(file_name, len(drug_character_dict), len(drug_character_dict[list(drug_character_dict.keys()).pop()]))
    with open("after/%s.pickle" % file_name, "wb") as wf:
        pickle.dump(drug_character_dict, wf)


def complete_zeros_vector(file):
    old_drug_character_dict = read_pickle_to_dict(file)
    exclusion_count = 0
    temp_key = list(old_drug_character_dict.keys()).pop()
    vector_size = len(old_drug_character_dict[temp_key])
    drug_character_dict = {}
    exclusion_set = set()
    for drug in total_drug_set:
        if drug not in old_drug_character_dict.keys():
            drug_character_dict[drug] = np.zeros(vector_size)
            exclusion_count += 1
            exclusion_set.add(drug)
        else:
            drug_character_dict[drug] = old_drug_character_dict[drug]
    print(file, exclusion_count)
    return drug_character_dict, exclusion_set


def filter_zero_character(old_drug_character_dict, character=None):
    """
    过滤掉冗余特征
    :param old_drug_character_dict:
    :return:
    """
    print("-----------------\ncharacter:", character)
    old_vector_size = len(old_drug_character_dict[list(old_drug_character_dict.keys()).pop()])
    print("old vector size:", old_vector_size)
    drug_size = len(old_drug_character_dict)
    old_metrix = np.zeros((drug_size, old_vector_size))
    key_list = list(old_drug_character_dict.keys())
    index = 0
    for key in key_list:
        old_metrix[index] = old_drug_character_dict[key]
        index += 1
    new_metrix = old_metrix[:, ~np.all(old_metrix == 0, axis=0)]
    # #---------------------------
    # sum_matrix = old_metrix.sum(axis=0)
    # sum_matrix[np.all(sum_matrix==0, axis=0)]
    # print(sum_matrix)
    # #---------------------------
    new_vector_size = len(new_metrix[0])
    print("delete vectors:", (old_vector_size - new_vector_size))
    drug_character_dict = {}

    index = 0
    for key in key_list:
        drug_character_dict[key] = new_metrix[index]
        index += 1
        if index == 1:
            print("new vector size:", len(drug_character_dict[key]))

    return drug_character_dict


if __name__ == '__main__':
    # 确定数据集total_drug_set规模: 557
    drugs_DDI = read_from_splitFile("../Data/draft/Drugbank4-PDDIs.csv", "$", [1, 3])
    drug_atc_dict = read_pickle_to_dict("before/drug_atc_dict.pickle")
    drug_MACCS_dict = read_pickle_to_dict("before/drug_MACCS_ddi_dict.pickle")
    drug_MeSH_dict = read_pickle_to_dict("before/drug_MeSH_ddi_dict.pickle")
    drug_word2vec_dict = read_pickle_to_dict("before/drug_word2vec_ddi_dict.pickle")
    total_drug_set = drugs_DDI & drug_atc_dict.keys()& drug_MACCS_dict.keys() & drug_MeSH_dict.keys() & drug_word2vec_dict.keys()
    print("total_drug:", len(total_drug_set))  # 557

    # 过滤掉不在数据集total_drug_set中的药物
    drug_actionCode_matrix_dict, action_set = complete_zeros_vector("before/drug_actionCode_matrix_dict.pickle")
    drug_phyCode_matrix_dict, phy_set = complete_zeros_vector("before/drug_physiologicalCode_matrix_dict.pickle")
    drug_SIDER_matrix_dict, SIDER_set = complete_zeros_vector("before/drug_SIDER.pickle")
    drug_enzyme_matrix_dict, enzyme_set = complete_zeros_vector("before/drug_enzyme.pickle")
    drug_target_matrix_dict, target_set = complete_zeros_vector("before/drug_target.pickle")

    exclusion_set = action_set & phy_set & SIDER_set & enzyme_set & target_set
    print("exclusion_set:", len(exclusion_set), exclusion_set)

    drug_atc_matrix_dict, tmp = complete_zeros_vector("before/drug_atc_dict.pickle")
    drug_MACCS_matrix_dict, tmp = complete_zeros_vector("before/drug_MACCS_ddi_dict.pickle")
    drug_MeSH_matrix_dict, tmp = complete_zeros_vector("before/drug_MeSH_ddi_dict.pickle")
    drug_word2vec_matrix_dict, tmp = complete_zeros_vector("before/drug_word2vec_ddi_dict.pickle")

    # 过滤掉冗余特征
    drug_actionCode_matrix_dict = filter_zero_character(drug_actionCode_matrix_dict, "action")
    drug_phyCode_matrix_dict = filter_zero_character(drug_phyCode_matrix_dict, "physiologicalCode")
    drug_SIDER_matrix_dict = filter_zero_character(drug_SIDER_matrix_dict, "side effect")
    drug_enzyme_matrix_dict = filter_zero_character(drug_enzyme_matrix_dict, "enzyme")
    drug_target_matrix_dict = filter_zero_character(drug_target_matrix_dict, "target")
    drug_atc_matrix_dict = filter_zero_character(drug_atc_matrix_dict, "atc")
    drug_MACCS_matrix_dict = filter_zero_character(drug_MACCS_matrix_dict, "MACCS")
    drug_MeSH_matrix_dict = filter_zero_character(drug_MeSH_matrix_dict, "MeSH")
    drug_word2vec_matrix_dict = filter_zero_character(drug_word2vec_matrix_dict, "Word2Vec")

    # 将处理后的数据重新保存到pickle文件中
    write_dict_to_pickle(drug_actionCode_matrix_dict, "drug_actionCode_matrix_dict")
    write_dict_to_pickle(drug_phyCode_matrix_dict, "drug_phyCode_matrix_dict")
    write_dict_to_pickle(drug_SIDER_matrix_dict, "drug_SIDER_matrix_dict")
    write_dict_to_pickle(drug_enzyme_matrix_dict, "drug_enzyme_matrix_dict")
    write_dict_to_pickle(drug_target_matrix_dict, "drug_target_matrix_dict")
    write_dict_to_pickle(drug_atc_matrix_dict, "drug_atc_matrix_dict")
    write_dict_to_pickle(drug_MACCS_matrix_dict, "drug_MACCS_matrix_dict")
    write_dict_to_pickle(drug_MeSH_matrix_dict, "drug_MeSH_matrix_dict")
    write_dict_to_pickle(drug_word2vec_matrix_dict, "drug_word2vec_matrix_dict")

    # 将特征矩阵拼接在一块儿
    drug_all_dict = {}
    i = 0
    for drug in total_drug_set:
        drug_all_dict[drug] = np.concatenate((drug_actionCode_matrix_dict[drug], drug_phyCode_matrix_dict[drug],
                                              drug_SIDER_matrix_dict[drug], drug_enzyme_matrix_dict[drug],
                                              drug_target_matrix_dict[drug], drug_atc_matrix_dict[drug],
                                              drug_MACCS_matrix_dict[drug], drug_MeSH_matrix_dict[drug],
                                              drug_word2vec_matrix_dict[drug]))
        i += 1
        if i == 1:
            print("all character vector size: ", len(drug_all_dict[drug]))

    print(len(drug_all_dict))
    write_dict_to_pickle(drug_all_dict, "drug_all_dict")
"""
## Output: /home/yuan/Code/research_code/DDI/DrugDrugInteraction/bin/python /home/yuan/Code/PycharmProjects/DrugBest/DDS/DDS.py
../Data/draft/Drugbank4-PDDIs.csv 1199
total_drug: 557
before/drug_actionCode_matrix_dict.pickle : [exclusion_count] 53
before/drug_physiologicalCode_matrix_dict.pickle : [exclusion_count] 64
before/drug_SIDER.pickle : [exclusion_count] 174
before/drug_enzyme.pickle : [exclusion_count] 217
before/drug_target.pickle : [exclusion_count] 28
exclusion_set: 5 {'methacycline', 'kaolin', 'metrizamide', 'troleandomycin', 'sulfadimethoxine'}
before/drug_atc_dict.pickle : [exclusion_count] 0
before/drug_MACCS_ddi_dict.pickle : [exclusion_count] 0
before/drug_MeSH_ddi_dict.pickle : [exclusion_count] 0
before/drug_word2vec_ddi_dict.pickle : [exclusion_count] 0
-----------------
character: action
old vector size: 626
delete vectors: 438
new vector size: 188
-----------------
character: physiologicalCode
old vector size: 1866
delete vectors: 1546
new vector size: 320
-----------------
character: side effect
old vector size: 4492
delete vectors: 1188
new vector size: 3304
-----------------
character: enzyme
old vector size: 174
delete vectors: 33
new vector size: 141
-----------------
character: target
old vector size: 1220
delete vectors: 447
new vector size: 773
-----------------
character: atc
old vector size: 738
delete vectors: 119
new vector size: 619
-----------------
character: MACCS
old vector size: 166
delete vectors: 8
new vector size: 158
-----------------
character: MeSH
old vector size: 127
delete vectors: 0
new vector size: 127
-----------------
character: Word2Vec
old vector size: 100
delete vectors: 0
new vector size: 100
"""
