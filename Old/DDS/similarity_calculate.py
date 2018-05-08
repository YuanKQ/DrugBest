# -*- coding: utf-8 -*-
"""
__title__ = 'similarity_calculate.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 11,2017 11:27'
__mail__ = kq_yuan@outlook.com

__description__== [V] 根据药物的特征, 就算余弦相似度和欧氏距离, 用小数据集加以验证: 基于余弦相似度的效果更好.
                  根据药物特征, 计算dataset中所有药物的最相近的Top6, 并将计算结果序列化.
                  - "/home/yuan/Code/PycharmProjects/DrugBest/DDS/result/drug_sim_drugs_dict.pickle": 字母全小写
                    字典结构, 长度为557, key1为药物名称, value1依然为list结构, list中的每个元素都是dict结构(key2为相似度, value2为药物药物列表, 这些药物与key1的相似度为key2)
                    举个例子:
                    drug_sim_drugs_dict["morphine"]=[{0.420381794109: 'oxycodone'}, {0.466841026533: 'hydromorphone'}, ...]
                  - "/home/yuan/Code/PycharmProjects/DrugBest/DDS/result/drug_top6_drugs_dict.pickle": 字母全小写
                    字典结构, 长度为557, key为药物名称, value1为list结构,为与key最相似的top6中药物列表, list的长度为6
                    举个例子:
                    drug_top6_drugs_dict["morphine"] = ['oxycodone', 'hydromorphone','codeine', 'buprenorphine', 'hydrocodone', 'fentanyl']
"""
import pickle
import numpy as np
import scipy.spatial.distance as distance

TOP_SIZE = 6


def calculate_cosine(drug_list, distance_func):
    drug_drug_similar_dict = {}
    for drug in drug_list:
        drug = drug.lower()
        threshold = 1000000.0
        sim_drugs_dict = {}
        for item in drug_all_dict.keys():
            if item != drug:
                cos = distance_func(drug_all_dict[drug], drug_all_dict[item])
                if len(sim_drugs_dict) < TOP_SIZE:
                    if cos not in sim_drugs_dict.keys():
                        sim_drugs_dict[cos] = [item, ]
                    else:
                        sim_drugs_dict[cos].append(item)

                    key_values = list(sim_drugs_dict.keys())
                    key_values.sort()
                    threshold = key_values.pop()

                elif cos <= threshold:
                    # 删除dict中最大的元素
                    key_values = list(sim_drugs_dict.keys())
                    key_values.sort()
                    maximum = key_values.pop()
                    sim_drugs_dict.pop(maximum)
                    # 添加新的元素
                    if cos not in sim_drugs_dict.keys():
                        sim_drugs_dict[cos] = [item, ]
                    else:
                        sim_drugs_dict[cos].append(item)

                    key_values = list(sim_drugs_dict.keys())
                    key_values.sort()
                    threshold = key_values.pop()

        drug_drug_similar_dict[drug] = sim_drugs_dict
    return drug_drug_similar_dict

def display_dict(result_dict):
    for key, item_dict in result_dict.items():
        print(key)
        sim_list = list(item_dict.keys())
        sim_list.sort()
        for sim in sim_list:
            print(item_dict[sim])
        print("----------------")


def dataset_validate():
    # 根据药物的特征, 就算余弦相似度和欧氏距离, 用小数据集加以验证: 基于余弦相似度的效果更好.
    painkillers = [
        "Morphine", "Codeine", "Oxycodone",
        "Ibuprofen", "Indomethacin", "Acetaminophen", "Phenylbutazone",
        "Tramadol",
        "Atropine", "Propantheline",
        "Estazolam", "Diazepam", "Alprazolam"
    ]

    antibiotics = [
        "Amoxicillin", "Piperacillin", "Ampicillin",
        "Cephalexin", "Ceftriaxone",
        "Kanamycin", "Amikacin",
        "Minocycline", "doxycycline",
        "Lincomycin", "Clindamycin", "Roxithromycin",
        "Norfloxacin"
    ]

    # 确认小数据集是否都存在

    # for antibiotic in antibiotics:
    #     if antibiotic.lower() not in drug_set:
    #         print(antibiotic)
    # print("===============")
    # for painkiller in painkillers:
    #     if painkiller.lower() not in drug_set:
    #         print(painkiller)

    print("painkillers:")
    display_dict(calculate_cosine(painkillers, distance.cosine))
    print("=================\nantibiotics:")
    display_dict(calculate_cosine(antibiotics, distance.cosine))

    print("\n\n\n")
    print("painkillers:")
    display_dict(calculate_cosine(painkillers, distance.euclidean))
    print("=================\nantibiotics:")
    display_dict(calculate_cosine(antibiotics, distance.euclidean))


if __name__ == '__main__':
    with open("after/drug_all_dict.pickle", 'rb') as rf:
        drug_all_dict = pickle.load(rf)
    drug_set = set(drug_all_dict.keys())

    drug_drug_similar_dict = calculate_cosine(list(drug_set), distance.cosine)

    drug_top6_drugs_dict = {}
    display_index = 0
    for key, item_dict in drug_drug_similar_dict.items():
        drug_top6_drugs_dict[key] = list()
        sims = list(item_dict.keys())
        sims.sort()
        sim_index = 0
        for sim in sims:
            if sim_index < 6:
                drug_top6_drugs_dict[key].extend(item_dict[sim])
            sim_index += 1

        display_index += 1
        if display_index < 11:
            print(key, drug_top6_drugs_dict[key])

    print("size of drug_top6_drugs_dict:", len(drug_top6_drugs_dict))
    print("size of drug_drug_similar_dict", len(drug_drug_similar_dict))

    with open("result/drug_sim_drugs_dict.pickle", "wb") as wf:
        pickle.dump(drug_drug_similar_dict, wf)
    with open("result/drug_top6_drugs_dict.pickle", "wb") as wf:
        pickle.dump(drug_top6_drugs_dict, wf)