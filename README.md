=============================
**必须**
- ATC_DDI-v4/drug_code_dict.pickle: dict, 1191 * 738, idf
- MACCS166/durg_MACCS_ddi_dict.pickle: dict, 1069 * 166, 0-1
- MeSH/drug_MeSH_ddi_dict.pickle: dict, 630 * 128, embeding
- Word2Vec/drug_word2vec_ddi_dict.pickle: dict, 1065 * 100, embeding

**特征向量可以为0**
- ndfrt/drug_actionCode_matrix_dict.pickle: dict, 947*626, idf
- ndfrt/drug_physiologicalCode_matrix_dict.pickle: dict, 947*1866, idf
- SIDER/drug_SIDER.pickle: dict, 992*4492, idf

- Target_DDI-v4/drug_enzyme.pickle: dict, 580*174, idf
- Target_DDI-v4/drug_target.pickle: dict, 1097*1220, idf
==============================


## data_cleaning
处理完毕后的数据进行清洗:
- 删除特征向量全为0的药物
- 去掉不曾使用的特征

# Data
存放待处理数据和处理完毕后的数据
## after
存放处理后的数据

drugbank-v5.0.9所有药物相应的特征矩阵，可以直接提取不同年份的药物的药物关系
**必须**
- drug_code_dict.pickle: dict, 9697 * 867, idf
- durg_MACCS_dict.pickle: dict, 8176 * 166, 0-n, n可能因为所取的值太大导致结果误差
- drug_$hierarchy_dict.pickle: dict, 14333 * 127, embeding
- drug_word2vec_ddi_dict.pickle: dict, 1054 * 100, embeding
- ndfrt/drug_actionCode_matrix_dict.pickle: dict, 1388*626, idf
- ndfrt/drug_physiologicalCode_matrix_dict.pickle: dict, 1388*1866, idf
- SIDER/drug_SIDER.pickle: dict, 892*4876, idf
- Target_DDI-v4/drug_target.pickle: dict, 6837*3880, idf


- drugs_ddi.pickle: 以上特征矩阵的keys集合（药物名称），eg.drug_actionCode_matrix_dict.keys()
- ddi_rel_v5.pickle: 三元组列表：[ [drug1, drug2, "increase"], ...], [[drug1, drug2, "decreae"], ...]

# Statistic
从结构化,半结构化, 非结构化数据中抽取有用信息, 构建关于药物的特征向量

# 数据源
- DrugBank 5.0.9
- ChemOnt_2_1.obo.zip
  > Djoumbou Feunang Y, Eisner R, Knox C, Chepelev L, Hastings J, Owen G, Fahy E, Steinbeck C, Subramanian S, Bolton E, Greiner R, and Wishart DS. ClassyFire: Automated Chemical Classification With A Comprehensive, Computable Taxonomy. Journal of Cheminformatics, 2016, 8:61.
DOI: 10.1186/s13321-016-0174-y
- ndf-rt
- word2vec的语料: pubmed 2018.1.1: abstract, tile

===============================
2018-05-09:
某一维的特征向量都是0的药物全部filter掉
单个药物特征维度：6641
所有的ddi: 45955
increase:  30020
decrease:  15935

===============================
for 毕设：
increase/decrease具体的方面
