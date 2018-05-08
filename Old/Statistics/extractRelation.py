# -*- coding: utf-8 -*-
"""
__title__ = 'extractRelation.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'May 01,2018 10:25'
__mail__ = kq_yuan@outlook.com

__description__== drugbank中所有的药物名称都保存至allDrugName.txt,
                  所有的药物关系描述保存至allRelations.txt,
                  (药物1， 药物2， 关系）的关系对儿保存至relation.txt
"""
"""
先提取药物名称，再提取关系
"""
import xml.etree.cElementTree as ET
def extract_relation_to_txt():
    """
    提取relation description和drug name, 并且将保存至文件
    :return:
    """
    tree = ET.ElementTree(file="/data/home/Code/DDI-DataSource/drugbank-5-0-9.xml")
    # tree = ET.ElementTree(file="/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/simple_drugbank_example.xml")
    drugs_name = {}
    with open("allDrugName.txt", "w") as wf:
        with open("allRelations.txt", "w") as wf1:
            for drug_elem in tree.findall("drug"):
                drug_name = drug_elem.find("name").text.lower()
                relations = drug_elem.findall("drug-interactions/drug-interaction/description")
                if drug_name is not None:
                    wf.write(drug_name)
                    wf.write("\n")
                    print(drug_name)
                for relation in relations:
                    if relation is not None:
                        description = relation.text.lower()
                        wf1.write(description)
                        wf1.write("\n")
                        print(description)

import re
def extraction_relation():
    drugs = []
    relations = []
    with open("allDrugName.txt", 'r') as rf:
        lines = rf.readlines()
        for line in lines:
            drugs.append(re.sub("\n", "", line))

    with open("allRelations.txt", "r") as rf:
        lines = rf.readlines(10000)
        while len(lines) > 0:
            for line in lines:
                relation = []
                for drug in drugs:
                    if drug in line:
                        relation.append(drug)
                if "increase" in line:
                    relation.append("increase")
                elif "decrease" in line or "reduce" in line:
                    relation.append("decrease")
                else:
                    print(len(relations), line)
                relations.append(relation)

            lines = rf.readlines(10000)

    with open("relation.txt", "w") as wf:
        for relation in relations:
            if len(relation) == 3:
                wf.write(relation[0])
                wf.write("$")
                wf.write(relation[1])
                wf.write("$")
                wf.write(relation[2])
                wf.write("\n")



if __name__ == '__main__':
    extraction_relation()

