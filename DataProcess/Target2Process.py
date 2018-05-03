# -*- coding: utf-8 -*-
"""
__title__ = 'Target2Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'May 02,2018 21:45'
__mail__ = kq_yuan@outlook.com

__description__==

"""
import pickle
import re
import numpy as np
from DataProcess.util import calculate_TFIDF, get_drugbankId_drugname


def extract_drug_target(id_drug_dict, target_file, key_validate=None):
    """
    先提取药物靶向蛋白质的名称, 并排序 ==> 构建药物与靶向蛋白质的one-hot coding
    :return:
    """
    drug_target_dict = {}
    target_name_set = set()
    line_pattern = re.compile(r"(>drugbank_\w+\|\w+\s)(.*)\s(\(.*\))")
    id_pattern = re.compile(r"DB\d+")

    with open(target_file, 'r') as rf:
        lines = rf.readlines()
        for line in lines:
            line_array = line_pattern.split(line)
            if len(line_array) >= 5:
                id_array = id_pattern.findall(line_array[3])
                for drugbank_id in id_array:
                    if drugbank_id in id_drug_dict.keys():
                        target_name_set.add(line_array[2])
                        if id_drug_dict[drugbank_id] in drug_target_dict:
                            drug_target_dict[id_drug_dict[drugbank_id]].append(line_array[2])
                        else:
                            drug_target_dict[id_drug_dict[drugbank_id]] = [line_array[2], ]

    # For valiate whether the process is correct
    if key_validate is not None:
        drug_target_dict[key_validate].sort()
        print(len(drug_target_dict[key_validate]), drug_target_dict[key_validate])


    # 将药物靶向蛋白质按字母序排列
    target_name_list = list(target_name_set)
    target_name_list.sort()

    # 构建药物与靶向蛋白质的one-hot coding
    matrix_size = len(target_name_list)
    print("matrix size:", matrix_size, " drug:", len(drug_target_dict))
    drug_target_matrix_dict = {}
    for key in drug_target_dict.keys():
        if key not in drug_target_matrix_dict.keys():
            drug_target_matrix_dict[key] = np.zeros(matrix_size)
        for value in drug_target_dict[key]:
            drug_target_matrix_dict[key][target_name_list.index(value)] = 1

    # For valiate whether the process is correct
    if key_validate is not None:
        index = 0
        for one in drug_target_matrix_dict[key_validate]:
            if one == 1:
                print(target_name_list[index])
            index += 1

    return drug_target_matrix_dict, matrix_size, target_name_list


if __name__ == '__main__':
    id_drug_dict = get_drugbankId_drugname()
    drug_size = len(id_drug_dict)

    # 药物靶向蛋白质
    drug_target_matrix_dict, target_size, target_name_list = extract_drug_target(id_drug_dict,
                                                                                 "/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/drug_target_protein.txt",
                                                                                 "miconazole")
    target_idf = calculate_TFIDF(drug_target_matrix_dict, drug_size, target_size)
    print(np.max(target_idf), np.min(target_idf))

    kindex = 0
    for key in drug_target_matrix_dict:
        drug_target_matrix_dict[key] *= target_idf
        if kindex == 0:
            print(key)
            index = 0
            for value in drug_target_matrix_dict[key]:
                if value != 0:
                    print(target_name_list[index], value)
                index += 1
            print('--------------')
        kindex += 1

    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/drug_target.pickle", "wb") as wf:
        pickle.dump(drug_target_matrix_dict, wf)

    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/target_name.pickle", "wb") as wf:
        pickle.dump(target_name_list, wf)
    print("end")

    ## 药作用酶
    # drug_enzyme_matrix_dict, enzyme_size, enzyme_name_list = extract_drug_target(id_drug_dict,
    #                                                                              "../Data/draft/drug_enzyme_protein.txt",
    #                                                                              "Doxorubicin")
    # enzyme_idf = calculate_TFIDF(drug_enzyme_matrix_dict, drug_size, enzyme_size)
    # print(np.max(enzyme_idf), np.min(enzyme_idf))
    # kindex = 0
    # for key in drug_enzyme_matrix_dict:
    #     drug_enzyme_matrix_dict[key] *= enzyme_idf
    #     if kindex == 0 or kindex == len(drug_enzyme_matrix_dict) - 1:
    #         print(key)
    #         index = 0
    #         for value in drug_enzyme_matrix_dict[key]:
    #             if value != 0:
    #                 print(enzyme_name_list[index], value)
    #             index += 1
    #         print('--------------')
    #     kindex += 1
    # with open("../Data/characters/Target_DDI-v4/enzyme_name.pickle", "wb") as wf:
    #     pickle.dump(enzyme_name_list, wf)