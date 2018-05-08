# -*- coding: utf-8 -*-
"""
__title__ = 'drug_interaction_count.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 14,2017 20:53'
__mail__ = kq_yuan@outlook.com

__description__==

"""
import pickle

from Statistics.antibioticCount import DDI_count


def ddi_in_dataset(filename):
    count = 0
    with open(filename, 'r') as rf:
        lines = rf.readlines()
        for line in lines:
            drugs = line.split()
            if len(drugs) >= 2:
                if drugs[0] in drug_set and drugs[1] in drug_set:
                    count += 1
                    # if drugs[0] not in drug_ddi_drugs_dict.keys():
                    #     drug_ddi_drugs_dict[drugs[0]] = set()
                    # if drugs[1] not in drug_ddi_drugs_dict.keys():
                    #     drug_ddi_drugs_dict[drugs[1]] = set()
                    # drug_ddi_drugs_dict[drugs[0]].add(drugs[1])
                    # drug_ddi_drugs_dict[drugs[1]].add(drugs[0])

    print(count)


with open("after/drug_all_dict.pickle", 'rb') as rf:
    drug_all_dict = pickle.load(rf)

drug_ddi_drugs_dict = {}
drug_set = set(drug_all_dict.keys())
print(DDI_count(drug_set, "../Data/draft/Drugbank4-PDDIs.csv"))  # 8123
ddi_in_dataset('/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/drugbank_200901.dat')  # 5411
ddi_in_dataset('/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/drugbank_201204.dat')  # 8079

# print("drug_set:", len(drug_set))
# print("drug_ddi_drugs_dict:", len(drug_ddi_drugs_dict))
# pair_count = 0
# for key in drug_ddi_drugs_dict.keys():
#     for item in drug_ddi_drugs_dict[key]:
#         pair_count += 1
# print(pair_count, pair_count/2)

