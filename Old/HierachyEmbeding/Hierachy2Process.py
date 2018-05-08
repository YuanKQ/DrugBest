# -*- coding: utf-8 -*-
"""
__title__ = 'Hierachy2Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Apr 29,2018 11:14'
__mail__ = kq_yuan@outlook.com

__description__== 根据Hierarchy of drugbank提取edgelist
                  从ChemOnt中提取 根节点 到 direct parent的edgelist
                  从Drugbank中提取 direct parent 到 drug 子节点的edgelist

"""
import pickle
import re
import xml.etree.cElementTree as ET


# def extrct_id_drug():
#     with open("/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/structures.sdf") as f:
#     # with open("structure_sdf_example.txt") as f:
#         content = f.read()
#     drug_infos = content.split("$$$$")
#     id_pattern = re.compile("(?<=DRUGBANK_ID>\s)DB\d{5}")
#     name_pattern = re.compile("(?<=GENERIC_NAME>\s).*(?=\s)")
#
#     count = 0
#     for info in drug_infos:
#         if len(info) > 0:
#            ids = re.findall(id_pattern, info)
#            names = re.findall(name_pattern, info)
#            if len(ids) > 0 and len(names) > 0:
#               id = ids[0]
#               name = names[0].lower()
#               if name not in id_drugAndchem_dict.keys():
#                     id_drugAndchem_dict[name] = id
#               print(id, name)



def extract_chemitry_relation():
    with open("/home/yuan/Code/PycharmProjects/DrugBest/Old/Data/draft/ChemOnt_2_1.obo") as f:
        content = f.read()
    chem_infos = content.split("[Term]")
    id_pattern = re.compile("(?<=id:\sCHEMONTID:)\d{7}")
    name_pattern = re.compile("(?<=name:\s).+(?=\s)")
    tail_pattern = re.compile("(?<=is_a: CHEMONTID:)\d{7}(?=\s)")
    count = -1
    for info in chem_infos:
        count += 1
        if len(info) > 0 and count > 0:  # 第一个info为文件头，不含任何信息
            ids = re.findall(id_pattern, info)
            names = re.findall(name_pattern, info)
            tails = re.findall(tail_pattern, info)
            if len(ids) > 0 and len(names) > 0:
                id = "CHEM" + ids[0]
                name = names[0].lower()
                if name not in id_drugNchem_dict.keys():
                    id_drugNchem_dict[name] = id
                if id not in drugNchem_id_dict.keys():
                    drugNchem_id_dict[id] = name
                if len(tails) > 0:
                    tail_id = "CHEM" + tails[0]
                    edge_list.append([id, tail_id])
                # print(id, name)



def extract_parent_drug():
    tree = ET.ElementTree(file="/data/home/Code/DDI-DataSource/drugbank-5-0-9.xml")
    # tree = ET.ElementTree(file="/home/yuan/Code/PycharmProjects/DrugBest/Data/draft/simple_drugbank_example.xml")
    for drug_elem in tree.findall("drug"):
        id = drug_elem.find("drugbank-id").text
        drug_name = drug_elem.find("name").text.lower()
        parent = drug_elem.find("classification/direct-parent")
        if parent is not None:
            pname = parent.text.lower()
            if drug_name not in id_drugNchem_dict.keys() and len(id) > 0:
                id_drugNchem_dict[drug_name] = id
            if len(id) > 0 and id not in drugNchem_id_dict.keys():
                drugNchem_id_dict[id] = drug_name
            if drug_name in id_drugNchem_dict.keys() and pname in id_drugNchem_dict.keys():
                edge_list.append([id_drugNchem_dict[drug_name], id_drugNchem_dict[pname]])



if __name__ == '__main__':
    id_drugNchem_dict = {}
    drugNchem_id_dict = {}
    edge_list = []
    extract_chemitry_relation()
    extract_parent_drug()
    print(len(edge_list))
    with open("hierarchy.edgelist", "w") as wf:
        for edge in edge_list:
            wf.write(edge[0])
            wf.write(" ")
            wf.write(edge[1])
            wf.write("\n")
    with open("hierarchyEmbeding_id_drugName.pickle", "wb") as wf:
        pickle.dump(drugNchem_id_dict, wf)

