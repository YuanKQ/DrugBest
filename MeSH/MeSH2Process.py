# -*- coding: utf-8 -*-
"""
__title__ = 'MeSH2Process.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 03,2017 15:18'
__mail__ = kq_yuan@outlook.com

__description__== 处理MeSH的结构信息

"""
import random
import urllib.request

import time

if __name__ == '__main__':
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