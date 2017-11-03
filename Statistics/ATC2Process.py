# -*- coding: utf-8 -*-
"""
__title__ = 'ATC2Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 02,2017 14:50'
__mail__ = kq_yuan@outlook.com

__description__== 处理drugbank("../Data/draft/drugbank_all_infos_v_5_0_9.xml")的药物相应的atc-code, 将处理结果保存至.pickle文件中
                  序列化的结果为:
                  "../Data/characters/ATC_DDI-v4/drug_code_dict.pickle":  字典结构, 长度为1191, key为药物, 药物与靶向作用酶关系以长度为738的np.array来表示, 每一位代表一种atc-code, 0表示不出现, 非零浮点数表示服用该种药物会出现该位所代表的atc-code的IDF值)
                  "../Data/characters/ATC_DDI-v4/atc_code_name.pickle": list结构,长度为738, 指明上述的以长度为738的np.array的每一位所指代的atc-code的名称

"""
import pickle
import xml.etree.cElementTree as ET
import numpy as np
from Statistics.SIDER2Process import calculate_TFIDF

"""
倘若使用XPath, 需要将xml进行修改:
<drugbank xmlns="http://www.drugbank.ca" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.drugbank.cahttp://www.drugbank.ca/docs/drugbank.xsd" version="5.0" exported-on="2017-10-02">
 ==>
<drugbank xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.drugbank.cahttp://www.drugbank.ca/docs/drugbank.xsd" version="5.0" exported-on="2017-10-02">
"""


def extract_drug_atc():
    with open("../Data/draft/id2drug_v4.pickle", 'rb') as rf:
        id_drug_dict = pickle.load(rf)
    drug_size = len(id_drug_dict)
    drug_set = set(id_drug_dict.values())
    code_set = set()
    drug_code_dict = {}

    tree = ET.ElementTree(file="../Data/draft/drugbank_all_infos_v_5_0_9.xml")
    count = 0
    for drug_elem in tree.findall("drug"):
        drug_name = drug_elem.find("name").text
        if drug_name in drug_set:
            for code_elem in drug_elem.findall("atc-codes/atc-code/level"):
                code_name = code_elem.text
                code_set.add(code_name)
                if drug_name not in drug_code_dict:
                    drug_code_dict[drug_name] = []
                drug_code_dict[drug_name].append(code_name)

    # 字母序排列
    atc_code_list = list(code_set)
    atc_code_list.sort()


    drug_code_dict[key_validate].sort()
    print(key_validate, len(drug_code_dict[key_validate]), drug_code_dict[key_validate])

    matrix_size = len(atc_code_list)
    drug_code_matrix_dict = {}
    for key in drug_code_dict:
        if key not in drug_code_matrix_dict:
            drug_code_matrix_dict[key] = np.zeros(matrix_size)
        for code in drug_code_dict[key]:
            drug_code_matrix_dict[key][atc_code_list.index(code)] = 1

    i = 0
    for value in drug_code_matrix_dict[key_validate]:
        if value == 1:
            print(atc_code_list[i])
        i += 1

    return drug_code_matrix_dict, drug_size, matrix_size, atc_code_list



if __name__ == '__main__':
    key_validate = "Rituximab"

    drug_code_matrix_dict, drug_size, matrix_size, atc_code_list = extract_drug_atc()
    code_idf = calculate_TFIDF(drug_code_matrix_dict, drug_size, matrix_size)
    print("drug size:", drug_size, "  matrix_size:", matrix_size)

    # one-hot coding ==> idf matrix
    for key in drug_code_matrix_dict.keys():
        drug_code_matrix_dict[key] *= code_idf

    i = 0
    for value in drug_code_matrix_dict[key_validate]:
        if value != 0:
            print(atc_code_list[i], value)
        i += 1

    with open("../Data/characters/ATC_DDI-v4/drug_code_dict.pickle", "wb") as wf:
       pickle.dump(drug_code_matrix_dict, wf)

    with open("../Data/characters/ATC_DDI-v4/atc_code_name.pickle", "wb") as wf:
       pickle.dump(atc_code_list, wf)