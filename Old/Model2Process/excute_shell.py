# -*- coding: utf-8 -*-
"""
__title__ = 'excute_shell.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 24,2017 15:07'
__mail__ = kq_yuan@outlook.com

__description__== 模型自动运行的脚本文件

"""
n = [500, 200, 100, 50]
rate = [0.1, 0.01, 0.001, 0.0001, 0.00005]
margin = [1, 2, 3, 5, 10]

version = 1

with open("run.sh", "w") as wf:
    for n_i in n:
        for rate_i in rate:
            for margin_i in margin:

                wf.write("./Train_TransE_path %d %d %f %f >> log.txt\n" % (version, n_i, rate_i, margin_i))
                wf.write("./Test_TransE_path %d >> log.txt\n" % version)
                version += 1

