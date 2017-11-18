# -*- coding: utf-8 -*-
"""
__title__ = 'MeSH2Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 03,2017 15:18'
__mail__ = kq_yuan@outlook.com

__description__== 处理MeSH的结构信息: 从MeSH的树状结构中提取出边关系, 并将处理结果序列化
                  序列化结果:
                  "MeSH_data/edges.txt": 每一列的格式为"nodeId\tnodeId\n", 保存了MeSH树状结构的每一条边, 共21155条边
                  "MeSH_data/drug_countId_dict.pickle": 字典结构, 长度为9353, key为药物(全小写), value为nodeId
"""
import glob
import pickle
import random
import re
import urllib.request
from bs4 import BeautifulSoup
import time

from Statistics.antibioticCount import read_from_splitFile


def crawl_MeSH():
    # crawl MeSH tree Structure online
    urls = ["https://www.nlm.nih.gov/mesh/2015/mesh_trees/D01.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D02.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D03.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D04.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D05.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D06.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D08.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D09.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D10.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D12.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D13.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D20.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D23.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D25.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D26.html",
                "https://www.nlm.nih.gov/mesh/2015/mesh_trees/D27.html",
                ]

    for url in urls:
        req = urllib.request.Request(url)
        file_name = url.split("/")[-1]
        try:
            text = urllib.request.urlopen(req).read().decode('utf-8')
        except:
            print("Error: The %s can't be read." % file_name)
        with open("MeSH_html/%s.html" % file_name, "w") as wf:
            wf.write(text)

        time.sleep(random.randint(5, 20))


def extract_MeSH_id(html_file):
    print(html_file)
    drugs_before = len(drug_countId_dict)
    edges_before = len(edge_list)
    with open(html_file, 'r') as rf:
        html_doc = rf.read()
    html = BeautifulSoup(html_doc, "lxml")
    level1 = html.find("ul", class_="Level1")
    level1_id = extract_id_from_text(level1.li.a.text)
    if level1_id is not None:
        edge_list.append([0, level1_id])
        a_tags = level1.find_all("a", attrs={"href":re.compile(r'^//www.nlm.nih.gov/cgi/mesh/2015/MB_cgi?')})
        for a_tag in a_tags:
            child_id = extract_id_from_text(a_tag.text)
            parent_id = extract_id_from_text(a_tag.parent.parent.parent.a.text)
            if child_id != level1_id:
                edge_list.append([parent_id, child_id])
    print(len(drug_countId_dict) - drugs_before, len(edge_list) - edges_before)
    # print(edge_list)
    # print(drug_countId_dict)


def extract_id_from_text(text):
    global drug_count
    array = re.findall(pattern, text)
    if len(array) > 0 and len(array[0]) >= 2:
        drug_name = array[0][0].lower()
        if drug_name not in drug_countId_dict.keys():
            drug_set.add(drug_name)
            drug_count += 1
            mesh_id = drug_count
            drug_countId_dict[drug_name] = mesh_id
        return drug_countId_dict[drug_name]
        # drug_set.add(array[0][0])
        # mesh_id = "".join(array[0][1])
        # if mesh_id not in drug_countId_dict.keys():
        #     drug_count += 1
        #     drug_countId_dict[mesh_id] = array[0][0]
        # return mesh_id

    return None


def find_key_by_value(value, ddict):
    ddict = {"hahah":"541"}
    count = 0
    for drug, id in ddict.items():
        count += 1
        if id == value:
            print(count)
            return drug


if __name__ == '__main__':
    # crawl_MeSH()

    drug_count = 0
    drug_set = set()
    drug_countId_dict = {}
    drug_countId_dict["root"] = 0
    edge_list = []
    pattern = re.compile("(.+)\s\[D0?(\d[\d\.]*)\]")
    # extract_MeSH_id("/home/yuan/Code/PycharmProjects/DrugBest/MeSH/MeSH_html/D27.html.html")
    for file in glob.glob(r"/home/yuan/Code/PycharmProjects/DrugBest/MeSH/MeSH_html/*.html.html"):
        extract_MeSH_id(file)
    print("---------------------")
    print("drugs:", len(drug_countId_dict))
    print("edges:", len(edge_list))

    with open("MeSH_data/drug_countId_dict.pickle", "wb") as wf:
        pickle.dump(drug_countId_dict, wf)
    with open("MeSH_data/edges.txt", "w") as wf:
        for edge in edge_list:
            line = "\t".join(str(i) for i in edge)
            line += "\n"
            wf.write(line)

    print("drug_count:", drug_count)

    # # 验证连接关系是否获取正确
    # print("drug_set:", len(drug_set))
    # for edge in edge_list:
    #     node1 = find_key_by_value(edge[0], drug_countId_dict)
    #     node2 = find_key_by_value(edge[1], drug_countId_dict)
    #     print(node1,"---", node2)
    # print("----------------")
    # # DDI中的药物与MeSH的交集: 630
    # drugs_DDI = read_from_splitFile("../Data/draft/Drugbank4-PDDIs.csv", "$", [1, 3])
    # # print(drugs_DDI)
    # print(len(drug_set & drugs_DDI))
