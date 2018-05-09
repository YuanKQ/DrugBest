# -*- coding: utf-8 -*-
"""
__title__ = 'util.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'May 02,2018 15:57'
__mail__ = kq_yuan@outlook.com

__description__== 定义一些常见操作

"""
import numpy as np
import xml.etree.cElementTree as ET
import pickle
def get_all_drugs_as_sets():
    """
    获取drugbank5.0.9所有的药物名称（小写）
    :return: 所有药物名称的集合
    """
    drug_set = set()
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/allDrugName.txt", 'r') as rf:
        lines = rf.readlines()
    for line in lines:
        drug_set.add(line.split()[0])
    return drug_set

def calculate_TFIDF(input_dict, drug_size, feature_size):
    input_metric = np.zeros((drug_size, feature_size)) # input_metric = np.zeros((996, 4492))
    index = 0
    for key in input_dict:
        input_metric[index] = input_dict[key]
        index += 1
    big_metric = np.transpose(input_metric)
    # print(big_metric)
    # DF(t, Drugs): the number of drugs with side effect
    df = big_metric.sum(1)  # 4492*1
    idf = np.log((drug_size + 1) / (df + 1))  # 4492*1
    print("idf:", "max:", np.max(idf), "min:", np.min(idf))
    return np.transpose(idf)  # 1*4492

def extract_drugbankId_drugname():
    id_drug_dict = {}
    tree = ET.ElementTree(file="/data/home/Code/DDI-DataSource/drugbank-5-0-9.xml")
    # tree = ET.ElementTree(file="/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/simple_drugbank_example.xml")
    for drug_elem in tree.findall("drug"):
        id = drug_elem.find("drugbank-id").text
        drug_name = drug_elem.find("name").text.lower()
        if id not in id_drug_dict.keys():
            id_drug_dict[id] = drug_name
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/drugbankID_drug.pickle", "wb") as wf:
        pickle.dump(id_drug_dict, wf)


def get_drugbankId_drugname():
    drugbankId_drugName_dict = {}
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/drugbankID_drug.pickle", 'rb') as rf:
        drugbankId_drugName_dict = pickle.load(rf)
    return drugbankId_drugName_dict


def get_ddi_drugs():
    drugs_ddi = set()
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/relation.txt", 'r') as rf:
        lines = rf.readlines()
    for line in lines:
        items = line.split("$")
        # print(line)
        if len(items) > 0:
            drugs_ddi.add(items[0])
            drugs_ddi.add(items[1])
    return drugs_ddi


def process_relations(drug_file="/home/yuan/Code/PycharmProjects/DrugBest/Data/after/drugs_ddi.pickle",
                      rel_file="/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/relation.txt",
                      target_file="/home/yuan/Code/PycharmProjects/DrugBest/Data/after/ddi_pairs_v5.txt"):
    """
    去掉重复的ddi，去掉某一维特征向量为0的药物的ddi
    :return:
    """
    with open(drug_file, 'rb') as rf:
        drugs = pickle.load(rf)
    with open(rel_file, 'r') as rf:
        lines = rf.readlines()
    print("all ddi pairs: ", len(lines))
    line_set = set()
    positive_count = 0
    negetive_count = 0
    with open(target_file, "w") as wf:
        for line in lines:
            items = line.split("$")
            if len(items) >= 3:
                head = items[0]
                tail = items[1]
                rel = items[2].split()[0]
                if head in drugs and tail in drugs:
                    if line not in line_set:
                        line_set.add(line)
                        wf.write(line)
                        if "increase" in rel:
                            positive_count += 1
                        if "decrease" in rel:
                            negetive_count += 1
    print("filtered: ", len(line_set))
    print("increase: ", positive_count)
    print("decrease: ", negetive_count)


def get_relations(file="/home/yuan/Code/PycharmProjects/DrugBest/Data/after/ddi_pairs_v5.txt",
                  target_file="/home/yuan/Code/PycharmProjects/DrugBest/Data/after/ddi_rel_v5.pickle"):
    with open(file, 'r') as rf:
        lines = rf.readlines()
    ddi_increase = list()
    ddi_decrease = list()
    for line in lines:
        items = line.split("$")
        if len(items) > 3:
            head = items[0]
            tail = items[1]
            rel = items[2].split()[0]
            tmp = []
            tmp.append(head)
            tmp.append(tail)
            tmp.append(rel)
            if "increase" in rel:
                ddi_increase.append(tmp)
            if "decrease" in rel:
                ddi_decrease.append(tmp)
    with open(target_file, "wb") as wf:
        pickle.dump(ddi_increase, wf)
        pickle.dump(ddi_decrease, wf)

if __name__ == '__main__':
    # drugs_ddi = get_ddi_drugs()
    # print("all drugs of ddi: ", len(drugs_ddi))
    # process_relations()
    get_relations()
    print("end")
