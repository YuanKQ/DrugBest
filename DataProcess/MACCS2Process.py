# -*- coding: utf-8 -*-
"""
__title__ = 'MACCS2Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'May 02,2018 16:50'
__mail__ = kq_yuan@outlook.com

__description__== 抽取药物MACCS key:
                  从.sdf文件(all structure from drugbank)中抽取出药物名称(generic Name, 全部小写)
                  ==> 经过MAyaChemTools处理得到MACCS key与药物名称对应起来.
                  ==> 序列化
                  ""Data/drug_MACCS166.pickle": 长度为8176的dict结构, key为药名, value为MACCS key vector


"""
import re
import numpy as np
import DataProcess.util as util
import pickle
def extract_from_sdf():
    with open("../Data/draft/structures.sdf", "r") as f:
        content = f.read()
        drug_names = re.findall("(?<=<GENERIC_NAME>\n).*(?=\s)", content)
        drug_names = list(map(str.lower, drug_names))  # 转为小写字母
        print(drug_names[924])  # 序号为924的药物(ergoloid mesylate, 无关紧要, 并没有减少数据集)结构无法解析出MACCS key

    return drug_names, drug_names[924]


def extract_MACCSkey(drugs_list):
    MACCS_dict = {}
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/structures.csv", 'r') as rf:
        lines = rf.readlines()
        index = -1
        for line in lines:
            # 跳过第一行"解释说明": CompoundID", "MACCSKeysFingerprints
            index += 1
            if index == 0:
                continue

            tmp_array = line.split(";")
            bit_list = []
            if (len(line) > 0):
                bits = tmp_array[-1].replace('"', "").split()  # 去掉最后以为的双引号"
                bit_list = list(map(lambda x: int(x), bits))
            print(index)
            MACCS_dict[drugs_list[index - 1]] = np.array(bit_list)

        print(index)
    return MACCS_dict


def build_MACCS_ddi_matrix():
    drug_set = util.get_all_drugs_as_sets()
    drug_MACCS_ddi_dict = {}
    for drug in drug_set:
        if drug in drugs2MACCS_dict.keys():
            drug_MACCS_ddi_dict[drug] = drugs2MACCS_dict[drug]
    print(len(drug_MACCS_ddi_dict))
    return drug_MACCS_ddi_dict


if __name__ == '__main__':
    drugs_list, item = extract_from_sdf()
    drugs2MACCS_dict = extract_MACCSkey(drugs_list)
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/drug_MACCS166.pickle", "wb") as wf:
        pickle.dump(drugs2MACCS_dict, wf)