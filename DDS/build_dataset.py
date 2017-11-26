# -*- coding: utf-8 -*-
"""
__title__ = 'build_dataset.py'
__IDE__ = 'PyCharm'
__author__ = 'YuanKQ'
__mtime__ = 'Nov 18,2017 22:03'
__mail__ = kq_yuan@outlook.com

__description__== 构建数据集, 三种关系, sim, ddi, other
                  将空格转为下划线
                  实体数量请以drug_sim_drugs_dict.keys()为准
                  想要重新构造数据集， 请先运行sim_path.py

"""
import pickle
from random import shuffle


def build_ddi_dict():
    drug_ddi_drugs_dict = {}
    with open("../Data/draft/Drugbank4-PDDIs.csv", 'r') as rf:
        lines = rf.readlines()

    count = 0
    for line in lines:
        items = line.split("$")
        if len(items) >= 3:
            head = items[1].lower()
            tail = items[3].lower()
            if head in drug_set and tail in drug_set:
                count += 1
                if head not in drug_ddi_drugs_dict.keys():
                    drug_ddi_drugs_dict[head] = set()
                if tail not in drug_ddi_drugs_dict.keys():
                    drug_ddi_drugs_dict[tail] = set()
                drug_ddi_drugs_dict[head].add(tail)
                drug_ddi_drugs_dict[tail].add(head)

    print("count:", count)
    print("drug_set:", len(drug_set))
    print("drug_ddi_drugs_dict:", len(drug_ddi_drugs_dict)), count_pairs(drug_ddi_drugs_dict)
    print(drug_set - set(drug_ddi_drugs_dict.keys()))
    # {'daunorubicin', 'dronabinol', 'mechlorethamine', 'streptozocin', 'phenoxybenzamine', 'estramustine', 'proguanil', 'deferoxamine', 'dinoprostone', 'papaverine', 'mannitol', 'mitoxantrone', 'hydroxyurea', 'minoxidil', 'lomustine', 'barbital', 'amsacrine', 'misoprostol', 'metipranolol', 'epoprostenol', 'quinacrine', 'phentolamine', 'iloprost', 'idarubicin', 'azacitidine', 'yohimbine', 'doxazosin', 'cyclandelate', 'ondansetron', 'levobunolol', 'bupivacaine', 'dactinomycin', 'mifepristone', 'nitroprusside'

    return drug_ddi_drugs_dict


def count_pairs(result_dict):
    pairs = 0
    for key in result_dict.keys():
        for item in result_dict[key]:
            pairs += 1
    print("before:", pairs, pairs / 2)


def build_other_dict(sim_dict, ddi_dict):
    drug_other_drugs_dict = {}
    max_size = 0
    min_size = 10000
    for drug in drug_set:
        sim_set = sim_dict[drug] if drug in sim_dict else set()
        ddi_set = ddi_dict[drug] if drug in ddi_dict else set()
        if drug not in drug_other_drugs_dict.keys():
            drug_other_drugs_dict[drug] = drug_set - (sim_set | ddi_set)
            # print(drug, len(drug_other_drug_dict[drug]))
            max_size = len(drug_other_drugs_dict[drug]) if max_size < len(drug_other_drugs_dict[drug]) else max_size
            min_size = len(drug_other_drugs_dict[drug]) if min_size > len(drug_other_drugs_dict[drug]) else min_size

    print("max:", max_size, "min:", min_size)
    return drug_other_drugs_dict


def build_pair_list(target_dict):
    pair_list = []
    for key in target_dict.keys():
        for item in target_dict[key]:
            pair = set([key, item])
            if pair not in pair_list:
                pair_list.append(pair)
                # print(key, item)
    print("len:", len(target_dict), "pairs:", len(pair_list))
    return pair_list


def write_txt():
    #relation2id.txt
    with open("dataset/relation2id.txt", "w") as wf:
        wf.write("sim\t0\n")
        wf.write("ddi\t1\n")

    # entity2id.txt
    entity_id_dict = {}
    with open("dataset/entity2id.txt", "w") as wf:
        entity_id = 0
        for drug in drug_set:
            entity = drug.replace(" ", "_")
            wf.write(entity + "\t" + str(entity_id) + "\n")
            entity_id += 1
            entity_id_dict[entity] = entity_id

    # e1_e2.txt
    with open("dataset/e1_e2.txt", "w") as wf:
        for drug1 in drug_set:
            e1 = drug1.replace(" ", "_")
            for drug2 in drug_set:
                e2 = drug2.replace(" ", "_")
                wf.write(str(entity_id_dict[e1]) + "\t" + str(entity_id_dict[e2]) + "\n")

    # train.txt
    sim_train_size = int(len(sim_pairs) * dataset_ratio["train"])
    ddi_train_size = int(len(ddi_pairs) * dataset_ratio["train"])
    train_str_list = build_line_list(0, sim_train_size, "sim", sim_pairs)
    train_str_list.extend(build_line_list(0, ddi_train_size, "ddi", ddi_pairs))
    shuffle(train_str_list)
    print("train_str_list:", len(train_str_list), train_str_list[:50])
    # validate_ddi(train_str_list)
    with open("dataset/train.txt", "w") as wf:
        for line in train_str_list:
            wf.write(line + "\n")

    # valid.txt
    sim_valid_size = int(len(sim_pairs) * dataset_ratio["valid"])
    ddi_valid_size = int(len(ddi_pairs) * dataset_ratio["valid"])
    valid_str_list = build_line_list(sim_train_size, sim_train_size + sim_valid_size, "sim", sim_pairs)
    valid_str_list.extend(build_line_list(ddi_train_size, ddi_train_size + ddi_valid_size, "ddi", ddi_pairs))
    shuffle(valid_str_list)
    print("valid_str_list:", len(valid_str_list), valid_str_list[:50])
    with open("dataset/valid.txt", "w") as wf:
        for line in valid_str_list:
            wf.write(line + "\n")

    # test.txt
    test_str_list = build_line_list(sim_train_size + sim_valid_size, len(sim_pairs), "sim", sim_pairs)
    test_str_list.extend(build_line_list(ddi_train_size + ddi_valid_size, len(ddi_pairs), "ddi", ddi_pairs))
    shuffle(test_str_list)
    print("test_str_list:", len(test_str_list), test_str_list[:50])
    with open("dataset/test.txt", "w") as wf:
        for line in test_str_list:
            wf.write(line + '\n')


def build_line_list(head_index, tail_index, rel_type, pairs):
    line_list = []
    for i in range(head_index, tail_index):
        if len(pairs[i]) >= 2:
            line = ""
            for entity in pairs[i]:
                line += (entity + "\t")
            line += rel_type
            line_list.append(line)

    return line_list


if __name__ == '__main__':
    """
    ## 构造 drug_ddi_drugs_dict, drug_others_dict
    # with open("after/drug_all_dict.pickle", 'rb') as rf:
    #     drug_all_dict = pickle.load(rf)
    # drug_set = set(drug_all_dict.keys())
    # with open("result/drug_sim_paths.pickle", 'rb') as rf:
    #     drug_sim_drugs_dict = pickle.load(rf)
    # print("drug_sim_drugs_dict:"), count_pairs(drug_sim_drugs_dict)  # 6359
    # 
    # drug_ddi_drugs_dict = build_ddi_dict()  # 4065
    # 
    # drug_others_dict = build_other_dict(drug_sim_drugs_dict, drug_ddi_drugs_dict) 
    # print("drug_others_dict:"), count_pairs(drug_others_dict)  #144940.5
    # 
    # with open("result/drug_ddi_drugs_dict.pickle", "wb") as wf:
    #     pickle.dump(drug_ddi_drugs_dict, wf)
    # with open("result/drug_others_dict.pickle", "wb") as wf:
    #     pickle.dump(drug_others_dict, wf)
    """

    with open("after/drug_all_dict.pickle", 'rb') as rf:
        drug_all_dict = pickle.load(rf)
    drug_set = set(drug_all_dict.keys())
    with open("result/drug_sim_paths.pickle", 'rb') as rf:
        drug_sim_drugs_dict = pickle.load(rf)
    with open("result/drug_ddi_drugs_dict.pickle", "rb") as rf:
        drug_ddi_drugs_dict = pickle.load(rf)
    with open("result/drug_others_dict.pickle", "rb") as rf:
        drug_others_dict = pickle.load(rf)

    print("drug_sim_drugs_dict:"), count_pairs(drug_sim_drugs_dict)  # 6359
    sim_pairs = build_pair_list(drug_sim_drugs_dict)
    print("drug_ddi_drugs_dict:"), count_pairs(drug_ddi_drugs_dict)
    ddi_pairs = build_pair_list(drug_ddi_drugs_dict)

    dataset_ratio = {"train":0.8, "valid": 0.1, "test": 0.1}

    write_txt()