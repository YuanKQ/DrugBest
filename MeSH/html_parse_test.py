# -*- coding: utf-8 -*-
"""
__title__ = 'html_parse_test.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 04,2017 21:17'
__mail__ = kq_yuan@outlook.com

__description__==

"""
import glob
import re
import os

from bs4 import BeautifulSoup

def extract_id_from_text(tag):
    text = tag.li.a.txt
    array = re.findall(pattern, text)
    if len(array) >= 2:
        if array[1] in drug_MeSH_id_dict.keys():
            drug_MeSH_id_dict[array[1]] = array[0]
        else:
            print(array)
        return array[1]
    else:
        return None


drug_MeSH_id_dict = {}
drug_MeSH_id_dict["0"] = "root"
edge_list = []
pattern = re.compile("([\w\s]+)\s\[D0?(\d+)\]")

with open("/home/yuan/Code/PycharmProjects/DrugBest/MeSH/MeSH_html/test.html", 'r') as rf:
    html_doc = rf.read()
html = BeautifulSoup(html_doc, "lxml")
# level1 = html.find("ul", class_="Level1")
li = html.find("li", class_="Test")
print(li)
a_tags = html.find_all("a", attrs={"href":re.compile(r'^//www.nlm.nih.gov/cgi/mesh/2015/MB_cgi?')})
for a in a_tags:
    print(a.text + "--" + a.parent.parent.parent.a.text)  # a li ul li.a.text
# if level1 is not None:
#     level2_set = level1.find_all("ul", class_=re.compile("Level\d+"))
#     print(len(level2_set))
#     for level2 in level2_set:
#         count = 0
#         for child in level2.find_all("li"):
#                 print(child.parent)
#                 print("--------------")
#         print(count)
for file in glob.glob(r"/home/yuan/Code/PycharmProjects/DrugBest/MeSH/MeSH_html/*.html.html"):
        print(file, os.path.isfile(file))



