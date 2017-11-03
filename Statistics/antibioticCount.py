# -*- coding: utf-8 -*-
"""
__title__ = 'antibioticCount.py'
__author__ = 'YuanKQ'
__mtime__ = '17-10-19'
__mail__ = kq_yuan@outlook.com

__description__== 统计抗感染药物在DDI中的数量及比例
                  Drugbank4-PDDIs         1199 drugs;
                  OpenKG                  691 drugs; & Drugbank4-PDDIs 269 drugs; & meddra_adverse_effects 229 drugs
                  meddra_adverse_effects  996 drugs; & Drugbank4-PDDIs 665 drugs; & Drugbank4-PDDIs & OpenKG 178 drugs


"""


def read_from_splitFile(filename, seperator, index_list):
    drugs_set = set()
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            items = line.split(seperator)
            index = 0
            max_index = max(index_list)
            for item in items:
                if index in index_list:
                    drugs_set.add(item.lower().replace("\n", ""))

                index += 1
            if index > max_index:
                continue

    # for item in drugs_set:
    #     print(item)
    print(filename, len(drugs_set))

    return drugs_set


def DDI_count(drug_set, filename):
    count = 0
    with open(filename, 'r') as rf:
        lines = rf.readlines()
        for line in lines:
            items = line.split("$")
            if len(items) >= 3:
                if items[1].lower() in drug_set and items[3].lower() in drug_set:
                    count += 1
    return count


if __name__ == '__main__':

    drugs_DDI = read_from_splitFile("../Data/draft/Drugbank4-PDDIs.csv", "$", [1, 3])
    drugs_KG = read_from_splitFile("../Data/draft/openKG_antibiotic.csv", ",", [1, ])
    side_effects = read_from_splitFile("../Data/draft/meddra_adverse_effects.tsv", "\t", [3, ])
    commons_1 = side_effects & drugs_KG
    commons_2 = side_effects & drugs_DDI
    # commons_all = side_effects & drugs_DDI & drugs_KG
    # print(len(commons_1), len(commons_2), len(commons_all))
    print(DDI_count(commons_1, "../Data/draft/Drugbank4-PDDIs.csv"))
    print(DDI_count(commons_2, "../Data/draft/Drugbank4-PDDIs.csv"))



