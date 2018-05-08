# -*- coding: utf-8 -*-
"""
__title__ = 'SIDER4Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'May 01,2018 19:46'
__mail__ = kq_yuan@outlook.com

__description__== 从pubchem根据compoundID获取drugName，从sider2，sider4中获取Drug所有可能的副作用

"""

# 现获取compoundID
import time

CIDs = set()
def extract_compoundID(filename):
    with open(filename, 'r') as rf:
        lines = rf.readlines()
        for line in lines:
            items = line.split("\t")
            if len(items) >= 2:
                items[0] = items[0].replace("CID1", "0")
                items[0] = items[0].replace("-1", "")
                items[1] = items[1].replace("CID", "")
                items[1] = items[1].replace("-", "")
                CIDs.add(items[0])
                CIDs.add(items[1])
    with open("cids.txt", "w") as wf:
        for cid in CIDs:
            wf.write(cid)
            wf.write("\n")

import pubchempy as pcp
def fetch_name_from_pubchem(source_file="cid1.txt", target_file="cid_drug_1.txt", leftFile = "leftFile"):
    cids = []
    # source_file = "cids.txt"
    # target_file = "drug_cid.txt"
    with open(source_file, 'r') as rf:
        lines = rf.readlines()
    for line in lines:
        cids.append(line.split()[0])
    drugs = set()
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/allDrugName.txt", 'r') as rf:
        lines = rf.readlines()
    for line in lines:
        drugs.add(line.split()[0])
    with open(target_file, "w") as wf:
        for cid in cids:
            try:
                c = pcp.Compound.from_cid(cid)
                time.sleep(1)
                synonyms = set(c.synonyms)
                time.sleep(1)
                drug = drugs & synonyms
                print(drug, cid)
                if (len(drug) > 0):
                    wf.write(drug.pop())
                    wf.write("&")
                    wf.write(cid)
                    wf.write("\n")
            except Exception as e:
                print(e)
                with open(leftFile, "w") as wf:
                    wf.write(cid)
                    wf.write("\n")


def extract_drug_siders():
    drugs = set()
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/allDrugName.txt", 'r') as rf:
        lines = rf.readlines()
    for line in lines:
        drugs.add(line.split()[0])
    drug_siders = {}

    with open("/data/home/Code/DDI-DataSource/SIDER2_meddra_adverse_effects.tsv", 'r') as rf:
        lines = rf.readlines()
    for line in lines:
        items = line.split("\t")
        if len(items) == 8:
            if items[3] in drugs:
                if items[3] not in drug_siders.keys():
                    drug_siders[items[3]] = set()
                    drug_siders[items[3]].add(items[2])
                else:
                    drug_siders[items[3]].add(items[2])

    id_drug_dict = {}
    with open("cid_drug.txt", "r") as rf:
        lines = rf.readlines()
    for line in lines:
        items = line.split("&")
        if len(items) == 2:
            drug = items[0]
            cid = items[1].split()[0]
            if cid not in id_drug_dict.keys():
                id_drug_dict[cid] = drug
    with open("/data/home/Code/DDI-DataSource/meddra_all_se.tsv", "r") as rf:
        lines = rf.readlines()
    for line in lines:
        items = line.split("\t")
        if len(items) == 6:
            cid = items[0].replace("CID1", "")
            cid1 = items[1].replace("CID", "")
            if cid in id_drug_dict.keys():
                drug = id_drug_dict[cid]
                if drug not in drug_siders.keys():
                    drug_siders[drug] = set()
                    drug_siders[drug].add(items[2])
                else:
                    drug_siders[drug].add(items[2])
            if cid1 in id_drug_dict.keys():
                drug = id_drug_dict[cid1]
                if drug not in drug_siders.keys():
                    drug_siders[drug] = set()
                    drug_siders[drug].add(items[2])
                else:
                    drug_siders[drug].add(items[2])
    with open("drug_sider.tsv", "a") as wf:
        for drug in drug_siders.keys():
            wf.write(drug)
            wf.write("\t")
            for sider in drug_siders[drug]:
                wf.write(sider)
                wf.write("\t")
            wf.write("\n")

import sys
if __name__ == '__main__':
    ## 提取compoundID
    # extract_compoundID("/data/home/Code/DDI-DataSource/SIDER2_meddra_adverse_effects.tsv")
    # extract_compoundID("/data/home/Code/DDI-DataSource/meddra_all_se.tsv")

    ## 从PubChem中根据compoundID来获取drugName
    # print(sys.argv[-3])
    # print(sys.argv[-2])
    # print(sys.argv[-1])
    # fetch_name_from_pubchem(sys.argv[-3], sys.argv[-2], sys.argv[-1])

    ## drugName-sider
    extract_drug_siders()
    print("END")
