import gensim
from utils.data_store_functions import *
import re
import collections
import binascii
from config import *
import numpy as np

# 单独处理一行数据
def process_single_line(detail, type):
    if(type == "file"):
        detail = detail.replace("_file", "").replace("\n", "")
        detail = detail.split("/")
        result = [re.sub(r'^[0-9A-F]+',"xxxx",item) for item in detail]
        result = [check_temp_file(item) for item in result]
        details = " ".join(result)
        result = details.strip()
        return gensim.utils.simple_preprocess(result)
    elif (type == "subject"):
        pattern = r'_(\d+)_'
        detail = detail.replace("_subject", "").replace("\n", "")
        details = re.split(pattern=pattern, string=detail)
        name, ppid, cmdLine = details
        if cmdLine == "null":
            result = [name]
        else:
            # 处理键值对
            result = re.sub(r'(\d+):(\d+)\|', "", cmdLine)
            result = re.sub(r"tmp\.[A-Za-z0-9]+", "tmp.XXXX", result)
            result = result.split(" ")
            # 处理乱码值 
            result = ["" if len(item) > 700 else item for item in result]
            result = ["" if is_hex(item) else item for item in result]
        result = " ".join(result)
        result = result.strip() 
        return gensim.utils.simple_preprocess(result)
    elif (type == "netflow"):
        detail = detail.replace("_netflow", "").replace("\n", "")
        if len(detail.split("->")[-1][0]) == 1:
            details = detail.split("->")[0]
        else:
            details = detail.split("->")[-1]
        details = re.split(r'\.|\:', details)
        return details

# 评估doc2vec
def evaluate_doc2vec(train_corpus, model):
    # 评估
    ranks = []
    second_ranks = []
    for doc_id in range(len(train_corpus)):
        inferred_vector = model.infer_vector(train_corpus[doc_id].words)
        # inferred_vector = model.dv[doc_id]
        sims = model.dv.most_similar([inferred_vector], topn=len(model.dv))
        rank = [docid for docid, sim in sims].index(doc_id)
        ranks.append(rank)
        second_ranks.append(sims[1])
    counter = collections.Counter(ranks)
    print(counter)
    print('Document ({}): «{}»\n'.format(doc_id, ' '.join(train_corpus[doc_id].words)))
    print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for label, index in [('MOST', 0), ('SECOND-MOST', 1), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
        print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))

def is_hex(s):
    if s != "":
        try:
            # 尝试将字符串解码为十六进制
            binascii.unhexlify(s)
            return True
        except binascii.Error:
            return False
    else:
        return False

def decode_hex(s):
    try:
        # 解码十六进制字符串
        decoded = binascii.unhexlify(s)
        return decoded.decode('utf-8')
    except binascii.Error:
        return None
    
# 转化成语料库
# distinct_XXX_corpus 中，id是原始文件的id，而值是经过gensim预处理之后的值
def trans_corpus_distinct(file_path, distinct_save_path, features_path, type):
    distinct_set = set()
    origin_corpus = dict()
    # origin_data = []
    with open(file_path, "r") as f:
        for line in f:
            detail, id = line.split("\t")
            result = process_single_line(detail, type)
            result = " ".join(result).strip()
            distinct_set.add(result)
            origin_corpus[int(id)] = result
            # origin_data.append(str(detail) + "---->" + str(result) + "\n")
    # 文件名
    feature_file_name = features_path.split("/")[-1]
    feature_file_path = features_path.replace(feature_file_name, "")
    feature_file_name = feature_file_name.replace(".txt", "")
    # 保存到本地
    save_to_local(distinct_set, distinct_save_path)
    # if type == "netflow":
    #     save_to_local(origin_data, "./test/netflow.txt")
    # 语料保存到本地
    save_dict_to_local(origin_corpus, feature_file_path, feature_file_name)

# 检查是否是临时文件
def check_temp_file(item):
    result = item
    if "tmp." in item:
        result = "tmp.xxxx"
    elif ".default" in item:
        result = "xxxx.default"
    elif "org.chromium." in item:
        result = "org.chromium.xxxx"
    elif ".png.tmp" in item:
        result = "xxxx.png.tmp"
    return result

# 读取语料库
# 区别处理netflow，netflow只需要按照/分割就行了
def read_corpus(file_name, tokens_noly = False):
    distinct_set = set()
    with open(file_name, "r") as f:
        counter = 0
        for line in f:
            if len(line) == 0:
                continue
            line = line.replace("\n", "")
            tokens = line.split(" ")
            tokens_line = " ".join(tokens).strip().replace("\n", "")
            if (tokens_line in distinct_set) == False:
                distinct_set.add(tokens_line)
                if tokens_noly:
                    yield tokens
                else:
                    yield gensim.models.doc2vec.TaggedDocument(tokens, [counter])
                    counter += 1

# doc2vec构造特征
def doc2vec(corpus_path, file_path, vector_size, min_count, epochs, start_lr, end_lr, type, dv_save_path):
    id_dv_dict = dict()
    # 读取语料库
    data_set = list(read_corpus(corpus_path))
    train_corpus = data_set
    if len(train_corpus) == 0:
        return 
    
    # 模型的训练与重载
    model = gensim.models.doc2vec.Doc2Vec(
        vector_size = vector_size, 
        min_count = min_count, 
        epochs = epochs
        )
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    
    doc_2_vec_dict = dict()
    # doc2vec dict中，键是语料，值是向量
    for doc_id in range(len(train_corpus)):
        doc = train_corpus[doc_id].words
        infer_vector = model.dv[doc_id]    
        doc_2_vec_dict[" ".join(doc)] = np.array(infer_vector)
    # id_dv中，键是原始文件中的id，值是向量
    with open(file_path, "r") as file:
        for line in file:
            # 分离id与值
            detail, id = line.split("\t")
            # 将值处理成语料
            corpus = process_single_line(detail, type)
            corpus = " ".join(corpus)
            # 从语料-向量字典中查询
            vector = doc_2_vec_dict.get(corpus)
            id_dv_dict[int(id)] = vector
    
    # print(id_dv_dict)
    # 特征保存到本地
    with open(dv_save_path, 'wb') as f:
        pickle.dump(id_dv_dict, f)
    
    # 评估
    # evaluate_doc2vec(train_corpus, model)

# 处理单个文件
def doc2vec_single_file(file):
    print("%s开始doc2vec"%(file))
    types_path = splited_result_path + file + "/types"
    file_file_path = types_path + "/file.txt"
    netflow_path = types_path + "/netflow.txt"
    subject_path = types_path + "/subject.txt"
    
    # 去重后语料库
    distinct_file_corpus_path = types_path + "/distinct_file_corpus.txt"
    distinct_subject_corpus_path = types_path + "/distinct_subject_corpus.txt"
    distinct_netflow_corpus_path = types_path + "/distinct_netflow_corpus.txt"
    
    # 原始文件转化为语料
    file_features_path = types_path + "/file_corpus.txt"
    subject_features_path = types_path + "/subject_corpus.txt"
    netflow_features_path = types_path + "/netflow_corpus.txt"
    
    # 语料特征 doc2vec
    file_dv_save_path = types_path + "/file_features.pkl"
    subject_dv_save_path = types_path + "/subject_features.pkl"
    netflow_dv_save_path = types_path + "/netflow_features.pkl"
    
    # 处理文件，进程，netflow
    trans_corpus_distinct(file_file_path, distinct_file_corpus_path, file_features_path, "file")
    trans_corpus_distinct(subject_path, distinct_subject_corpus_path, subject_features_path, "subject")
    trans_corpus_distinct(netflow_path, distinct_netflow_corpus_path, netflow_features_path, "netflow")
    
    # 进程转化成向量
    doc2vec(
        corpus_path=distinct_subject_corpus_path, 
        file_path=subject_path,
        vector_size=100, 
        min_count=1,  
        epochs=1000,
        start_lr=1e-4,
        end_lr=1e-4,
        type = "subject",
        dv_save_path = subject_dv_save_path
    )
    
    # netflow转化为向量
    doc2vec(
        corpus_path=distinct_netflow_corpus_path,
        file_path=netflow_path,
        vector_size=100,
        min_count=1,
        epochs=2000,
        start_lr=1e-4,
        end_lr=1e-4,
        type = "netflow",
        dv_save_path=netflow_dv_save_path
    )
    
    # 文件转化成向量
    doc2vec(
        corpus_path=distinct_file_corpus_path, 
        file_path=file_file_path,
        vector_size=100, 
        min_count=1, 
        epochs=1000,
        start_lr=1e-4,
        end_lr=1e-4,
        type = "file",
        dv_save_path=file_dv_save_path 
    )
    print("%s处理完成"%(file))

# 多进程处理doc2vec
def doc2vec_muti_process(file_dir_path, num_processes):
    process_pool = mp.Pool(num_processes)
    for file in os.listdir(file_dir_path):
        process_pool.apply_async(doc2vec_single_file, args=(file,))
    process_pool.close()
    process_pool.join()
    
    
    # for file in os.listdir(file_dir_path):
    #     doc2vec_single_file(file)

# 构造特征的函数
# if __name__ == "__main__":
def run():
    doc2vec_muti_process(splited_result_path, num_processes)
    # doc2vec_muti_process(splited_result_path, 1)