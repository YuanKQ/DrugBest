# -*- coding: utf-8 -*-
"""
__title__ = 'NDFRT2Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 09,2017 19:52'
__mail__ = kq_yuan@outlook.com

__description__== 处理ndfrt("Data/draft/NDFRT_Public_2017.10.02_TDE.xml")的药物特征PHYSIOLOGIC_EFFECT, MECHANISM_OF_ACTION,
                  将处理后的结果序列化保存
                  序列化结果:
                  每一位, 0表示不出现, 非零浮点数表示服用该种药物会出现该位所代表的特征的IDF值
                  "Data/characters/ndfrt/drug_actionCode_matrix_dict.pickle": 字典结构, 长度为947, key为药物(全小写), actionCode用长度为626的np.array来表示
                  "Data/characters/ndfrt/drug_physiologicalCode_matrix_dict.pickle": 字典结构, 长度为947, key为药物(全小写), physiologicalCode用长度为1866的np.array来表示


"""
import xml.etree.cElementTree as ET

from Statistics.SIDER2Process import calculate_TFIDF
from Statistics.antibioticCount import read_from_splitFile
import numpy as np
import pickle


def extract_elements(file_name):
    """
    提取MECHANISM_OF_ACTION_KIND(C12), PHARMACOKINETICS_KIND(C14), Drug_KIND(C16)名字与id
    :param fileName: ndfrt的xml文件
    :return:
    """
    tree = ET.ElementTree(file=file_name)
    root = tree.getroot()
    for concept in root.findall("conceptDef"):
        name = concept.find("name").text.lower()
        id = concept.find("code").text
        kind = concept.find("kind").text
        if kind in {"C8", "C10"} and name in drugs_DDI:
            # drug infos extraction
            for role in concept.findall("definingRoles/role"):
                role_name = role.find("name").text
                if role_name in {"R92", "R82", "C28", "C30"}:
                    if name not in drug_actionID_dict.keys():
                        drug_actionID_dict[name] = []
                    drug_actionID_dict[name].append(role.find("value").text)
                if role_name in {"R93", "R83", "C20", "C22"}:
                    if name not in drug_physiologicalID_dict.keys():
                        drug_physiologicalID_dict[name] = []
                    drug_physiologicalID_dict[name].append(role.find("value").text)
        elif kind == "C12":
            # MECHANISM_OF_ACTION infos extraction
            action_set.add(id)
        elif kind == "C6":
            # PHARMACOKINETICS_KIND infos extraction
            physiological_set.add(id)


def build_idf_matrix(colID_list, drug_colID_dict):
    col_len = len(colID_list)
    drug_colID_matrix_dict = {}
    for drug in drug_colID_dict.keys():
        if drug not in drug_colID_matrix_dict.keys():
            drug_colID_matrix_dict[drug] = np.zeros(col_len)
        for code in drug_colID_dict[drug]:
            drug_colID_matrix_dict[drug][colID_list.index(code)] = 1

    # # for validate
    # print("Validate:")
    # key_validate = "rituximab"
    # drug_colID_dict[key_validate].sort()
    # print(len(drug_colID_dict[key_validate]), drug_colID_dict[key_validate])
    #
    # i = 0
    # for value in drug_colID_matrix_dict[key_validate]:
    #     if value == 1:
    #         print(colID_list[i])
    #     i += 1

    # 计算TF-IDF
    drug_size = len(drug_colID_matrix_dict)
    col_idf = calculate_TFIDF(drug_colID_matrix_dict, drug_size, col_len)
    for drug in drug_colID_matrix_dict.keys():
        drug_colID_matrix_dict[drug] *= col_idf

    # # for validate
    # i = 0
    # for value in drug_colID_matrix_dict[key_validate]:
    #     if value != 0:
    #         print(colID_list[i], value)
    #     i += 1
    # print("------------------\n")

    return drug_colID_matrix_dict


if __name__ == '__main__':
    action_set = set()
    physiological_set = set()
    drug_actionID_dict = {}
    drug_physiologicalID_dict = {}
    drugs_DDI = read_from_splitFile("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/Drugbank4-PDDIs.csv", "$", [1, 3])
    extract_elements("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/NDFRT_Public_2017.10.02_TDE.xml")
    print("id_action:", len(action_set))
    print("id_physiological:", len(physiological_set))
    print("drug_actionID_dict:", len(drug_actionID_dict))
    print("drug_physiologicalID_dict:", len(drug_physiologicalID_dict))

    actionID_list = list(action_set)
    actionID_list.sort()
    physiological_list = list(physiological_set)
    physiological_list.sort()

    drug_actionCode_matrix_dict = build_idf_matrix(actionID_list, drug_actionID_dict)
    drug_physiologicalCode_matrix_dict = build_idf_matrix(physiological_list, drug_physiologicalID_dict)
    print("action_matix: [row] ", len(drug_actionCode_matrix_dict), "[col] ", len(drug_actionCode_matrix_dict["rituximab"]))
    print("physiological_matix: [row] ", len(drug_physiologicalCode_matrix_dict), "[col] ",
          len(drug_physiologicalCode_matrix_dict["rituximab"]))

    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/ndfrt/drug_actionCode_matrix_dict.pickle", "wb") as wf:
        pickle.dump(drug_actionCode_matrix_dict, wf)
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/ndfrt/drug_physiologicalCode_matrix_dict.pickle", "wb") as wf:
        pickle.dump(drug_physiologicalCode_matrix_dict, wf)


    # # 验证pickle是否能够正确读写
    # with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/ndfrt/drug_actionCode_matrix_dict.pickle", 'rb') as rf:
    #     test1 = pickle.load(rf)
    # with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/characters/ndfrt/drug_physiologicalCode_matrix_dict.pickle", 'rb') as rf:
    #     test2 = pickle.load(rf)
    # print("action_matix: [row] ", len(test1), "[col] ",
    #       len(test1["rituximab"]))
    # print("physiological_matix: [row] ", len(test2), "[col] ",
    #       len(test2["rituximab"]))