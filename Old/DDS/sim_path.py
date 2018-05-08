# -*- coding: utf-8 -*-
"""
__title__ = 'sim_path.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 18,2017 16:07'
__mail__ = kq_yuan@outlook.com

__description__== 构建DDS路径:
                  1-Step: 前6个
                  2-Step: 前4个
                  3-Step: 前2个
                  宽度优先算法咯~
                  ------------
                  随机游走: 走三步

                  序列化结果: "/home/yuan/Code/PycharmProjects/DrugBest/DDS/result/drug_sim_paths.pickle"
                  字典结构, 长度为557, key为药物, value为list, 为与key相近的药物列表

"""
import pickle
import queue


## Validate the method: bfs_path
# drug_top6_dict = {1: [11, 12, 13, 14],
#                   11: [111, 112, 113, 114],
#                   12: [121, 122, 123, 124],
#                   13: [131, 132, 133, 134],
#                   14: [141, 142, 143, 144],
#                   15: [151, 152],
#                   111: [1111, 1112, 113],
#                   112: [1121],
#                   1121: [11211]
#                   }
# drug_sim_path = {}
# level_size_dict = {1: 2, 2: 2, 3: 1}


def bfs_path(drug, target, level):
    if level not in level_size_dict.keys():
        return

    qlist = list()
    index = 0
    for item in drug_top6_dict[drug]:
        if index == level_size_dict[level]:
            break
        index += 1
        qlist.append(item)
        if target not in drug_sim_path:
            drug_sim_path[target] = set()
        drug_sim_path[target].add(item)
        # if target not in drug_sim_path:
        #     drug_sim_path[target] = list()
        # drug_sim_path[target].append(item)

    while len(qlist) > 0:
        item = qlist[0]
        qlist.remove(item)
        bfs_path(item, target, level+1)


if __name__ == '__main__':
    level_size_dict = {1: 6, 2: 2}
    # level_size_dict = {1: 6, 2: 5, 3: 4, 4: 3, 5:2, 6:1}
    # level_size_dict = {1: 6, 2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6, 11: 6, 12: 6}
    drug_sim_path = {}
    with open("result/drug_top6_drugs_dict.pickle", 'rb') as rf:
        drug_top6_dict = pickle.load(rf)

    validate_index = 0
    max_size = 0
    min_size = 100000
    for drug in drug_top6_dict.keys():
        bfs_path(drug, drug, 1)
        # if validate_index == 0:
        #     print(drug_top6_dict[drug], len(drug_sim_path[drug]))
        #     for item in drug_sim_path[drug]:
        #         print(item, ":", drug_top6_dict[item])
        # validate_index += 1
        sample_size = len(drug_sim_path[drug])
        max_size = sample_size if max_size < sample_size else max_size
        min_size = sample_size if min_size > sample_size else min_size

    print("max:", max_size)
    print("min:", min_size)

    with open("result/drug_sim_paths.pickle", "wb") as wf:
        pickle.dump(drug_sim_path, wf)


