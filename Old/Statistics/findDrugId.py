# -*- coding: utf-8 -*-
"""
__title__ = 'findDrugId.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 01,2017 08:52'
__mail__ = kq_yuan@outlook.com

__description__== 抽取药物名称以及对应drugbankID (1199, all drugs in Drugbank4-PDDIs.csv are found.)
                  ==> 逐行读取Drugbank4-PDDIs.csv, 抽取药物名称以及对应drugbankID
                  ==> 保存至./Data/draft/id2drug_v4.pickle中, 长度为1199的dict, key为DBxxxxx(drugbankID), value为药物名称

"""
import pickle
import re

id2drug_dict = {}

pattern = re.compile(r"DB\d{5}")


with open("../Data/draft/Drugbank4-PDDIs.csv", 'r') as rf:
    lines = rf.readlines()
    for line in lines:
        arry = line.split("$")
        if len(arry) > 4:
            # id2drug_dict[arry[0]] = arry[1]
            id2drug_dict[pattern.findall(arry[0])[0]] = arry[1]
            id2drug_dict[pattern.findall(arry[2])[0]] = arry[3]

print(len(id2drug_dict))

with open("../Data/draft/id2drug_v4.pickle", "wb") as wf:
    pickle.dump(id2drug_dict, wf)