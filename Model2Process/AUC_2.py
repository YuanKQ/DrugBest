# -*- coding: utf-8 -*-
"""
__title__ = 'AUC_2.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 25,2017 22:55'
__mail__ = kq_yuan@outlook.com

__description__==

"""
import numpy as np
import re
import sklearn.metrics as metrics


def softmax(x):
    return np.exp(x)/np.sum(np.exp(x))


with open("output.txt", "r") as rf:
    content = rf.read()
items = re.split("\d+-+", content)

print_index = 0
total_ddi = 0
total_sim = 0
ddi_predict_ddi = 0
ddi_predict_sim = 0
sim_predict_sim = 0
sim_predict_ddi = 0
true_label = []
predict_lable = []
predict_score = []
filter_count = 0
hit_count = 0
filter_sim = 0
filter_ddi = 0
hit_sim = 0
hit_ddi = 0
for item in items:
    if "rel" not in item:
        print(item)
        continue
    if print_index < 10:
        lines = item.split("\n")
        avalues = []
        for line in lines:
            if "$$" in line:
                avalues.append(float(line.split()[-1]))
    print_index += 1
    class_predict = softmax(avalues)

    if "rel: 1" in item:
        true_label.append(1)
        total_ddi += 1
        if "a[1]1" in item:
            predict_lable.append(1)
            ddi_predict_ddi += 1
            predict_score.append(np.max(class_predict))
        elif "a[1]0" in item:
            predict_lable.append(0)
            ddi_predict_sim += 1
            predict_score.append(np.min(class_predict))

    elif "rel: 0" in item:
        true_label.append(0)
        total_sim += 1
        if "a[1]1" in item:
            predict_lable.append(1)
            sim_predict_ddi += 1
            predict_score.append(np.max(class_predict))
        elif "a[1]0" in item:
            predict_lable.append(0)
            sim_predict_sim += 1
            predict_score.append(np.min(class_predict))


print("total sim: ", total_sim, "predict_true_sim: ", sim_predict_sim, "fail_to_predict_sim: ", sim_predict_ddi)
print("total ddi: ", total_ddi, "predict_true_ddi: ", ddi_predict_ddi, "fail_to_predict_ddi: ", ddi_predict_sim)
# p, r, t = metrics.precision_recall_curve(true_label, predict_score)
# print("aupr: ", metrics.auc(r, p))
# fpr, tpr, thresholds = metrics.roc_curve(true_label, predict_score, pos_label=1)
# print("auroc: ", metrics.auc(fpr, tpr))

print("filter_count:", filter_count, "hit_count:", hit_count)
print("filter_sim:", filter_sim, "filter_ddi:", filter_ddi)
print("hit_sim:", hit_sim, "hit_ddi:", hit_ddi)



