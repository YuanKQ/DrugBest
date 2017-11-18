# -*- coding: utf-8 -*-
"""
__title__ = 'similarity_assess.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 15,2017 10:59'
__mail__ = kq_yuan@outlook.com

__description__== 处理数据

"""
import re



def extract_label_result(filename, threshold=10):
    with open(filename, "r") as rf:
        contents = rf.read().split("----------------")
    total_sum = 0
    content_count = 0

    for content in contents:
        if content != "":
            content_count += 1
            lines = content.split("\n")
            index = 0
            count = 0
            for line in lines:
                if line != "":
                    if index > threshold:
                        break
                    # if index == 0:
                    #     print(re.split(r"[\u4E00-\u9FA5]+", line)[0])
                    if index >= 1:
                        # print(line)
                        count = count+1 if re.findall(r"\d", line)[-1] <= "4" else count
                        # print("[" + str(index) + "]", re.findall(r"\d", line)[-1])

                    index += 1
            # print("count:", count)
            total_sum += count / threshold
            # print("----------------")
    print(filename.split("/")[-1], "hits@%d:" % threshold, total_sum/content_count)



if __name__ == '__main__':
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/cosine.txt", 4)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/euclidean.txt", 4)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/cosine.txt", 5)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/euclidean.txt", 5)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/cosine.txt", 6)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/euclidean.txt", 6)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/cosine.txt", 7)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/euclidean.txt", 7)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/cosine.txt", 8)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/euclidean.txt", 8)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/cosine.txt", 9)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/euclidean.txt", 9)
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/cosine.txt")
    extract_label_result("/home/yuan/Code/PycharmProjects/DrugBest/DDS/label/euclidean.txt")
