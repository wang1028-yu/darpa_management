import gensim
from utils.data_store_functions import *
import re
import collections
import binascii
from config import *

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
    
# 处理进程
def process_subject(file_path, distinct_save_path):
    pattern = r'_(\d+)_'
    distinct_set = set()
    with open(file_path, "r") as f:
        for line in f:
            detail, id = line.split("\t")
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
            distinct_set.add(result)
    # 保存到本地
    save_to_local(distinct_set, distinct_save_path)
    print("进程保存完成")

# 处理文件
def process_file(file_path, distinct_save_path):
    distinct_set = set()
    with open(file_path, "r") as f:
        for line in f:
            detail, id = line.split("\t")
            detail = detail.replace("_file", "").replace("\n", "")
            result = detail.split("/")
            result = ["tmp.xxxx" if "tmp." in item else item for item in result]
            details = " ".join(result)
            details = details.strip()
            distinct_set.add(details)
    # 保存到本地
    save_to_local(distinct_set, distinct_save_path)
    print("文件保存完成")

# 处理IP
def process_netflow(file_path, distinct_save_path):
    pattern = r'\.|\:|->'
    distinct_set = set()
    with open(file_path, "r") as f:
        for line in f:
            detail, id = line.split("\t")
            detail = detail.replace("_netflow", "").replace("\n", "")
            details = re.split(pattern=pattern, string=detail)
            result = " ".join(details)
            result = result.strip()
            distinct_set.add(result)
    # 保存到本地
    save_to_local(distinct_set, distinct_save_path)
    print("netflow保存完成")

# 读取语料库
def read_corpus(file_name, tokens_noly = False):
    distinct_set = set()
    with open(file_name, "r") as f:
        # for i, line in enumerate(f):
        counter = 0
        for line in f:
            tokens = gensim.utils.simple_preprocess(line)
            tokens_line = " ".join(tokens).strip()
            # print(tokens_line)
            if (tokens_line in distinct_set) == False:
                distinct_set.add(tokens_line)
                if tokens_noly:
                    yield tokens
                    # print(tokens)
                else:
                    yield gensim.models.doc2vec.TaggedDocument(tokens, [counter])
                    counter += 1

def read_corpus_netflow(file_name, tokens_noly = False):
    distinct_set = set()
    with open(file_name, "r") as f:
        # for i, line in enumerate(f):
        counter = 0
        for line in f:
            tokens = line.replace("\n", "").split(" ")
            tokens_line = " ".join(tokens).strip()
            # print(tokens_line)
            if (tokens_line in distinct_set) == False:
                distinct_set.add(tokens_line)
                if tokens_noly:
                    yield tokens
                    # print(tokens)
                else:
                    yield gensim.models.doc2vec.TaggedDocument(tokens, [counter])
                    counter += 1

# doc2vec构造特征
def doc2vec(file_path, vector_size, min_count, epochs, start_lr, end_lr, netflow):
    # 读取语料库
    if netflow:
        data_set = list(read_corpus_netflow(file_path))
    else:
        data_set = list(read_corpus(file_path))
    train_corpus = data_set[:1000]
    # train_corpus = data_set
    print(len(train_corpus))
    model = gensim.models.doc2vec.Doc2Vec(
        vector_size = vector_size, 
        min_count = min_count, 
        epochs = epochs
        )
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    
    # 评估
    ranks = []
    second_ranks = []
    for doc_id in range(len(train_corpus)):
        inferred_vector = model.infer_vector(train_corpus[doc_id].words)
        sims = model.dv.most_similar([inferred_vector], topn=len(model.dv))
        rank = [docid for docid, sim in sims].index(doc_id)
        ranks.append(rank)
        second_ranks.append(sims[1])
    counter = collections.Counter(ranks)
    print(counter)
    # sum = 0
    # for item in counter:
    #     sum = sum + counter[item]
    #     print(item, end=":")
    #     print(counter[item])
    # print(sum)
    print('Document ({}): «{}»\n'.format(doc_id, ' '.join(train_corpus[doc_id].words)))
    print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for label, index in [('MOST', 0), ('SECOND-MOST', 1), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
        print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))

# 构造特征的函数
if __name__ == "__main__":
    for file in os.listdir(splited_result_path):
        print(file)
        types_path = splited_result_path + file + "/types"
        file_path = types_path + "/file.txt"
        netflow_path = types_path + "/netflow.txt"
        subject_path = types_path + "/subject.txt"
        distinct_file_path = types_path + "/file_corpus.txt"
        distinct_subject_path = types_path + "/subject_corpus.txt"
        distinct_netflow_path = types_path + "/netflow_corpus.txt"
        print(types_path)
        # 处理文件，进程，netflow
        process_file(file_path, distinct_file_path)
        process_subject(subject_path, distinct_subject_path)
        process_netflow(netflow_path, distinct_netflow_path)
        break
    
    # file_corpus = "./graph_data/distinct_data/file.txt"
    # subject_corpus = "./graph_data/distinct_data/subject.txt"
    # netflow_corpus = "./graph_data/distinct_data/netflow.txt"
    
    # data_set = list(read_corpus_netflow(netflow_corpus))
    # print(len(data_set))
    # print(data_set)
    
    # 文件转化成向量
    # doc2vec(
    #     file_path=file_corpus, 
    #     vector_size=100, 
    #     min_count=1, 
    #     epochs=700,
    #     start_lr=1e-4,
    #     end_lr=1e-4,
    #     netflow = False
    # )
    
    # netflow转化为向量
    # doc2vec(
    #     file_path=netflow_corpus,
    #     vector_size=100,
    #     min_count=1,
    #     epochs=2000,
    #     start_lr=1e-4,
    #     end_lr=1e-4,
    #     netflow = True
    # )
    
    # 进程转化成向量
    # doc2vec(
    #     file_path=subject_corpus, 
    #     vector_size=100, 
    #     min_count=1,  
    #     epochs=1000,
    #     start_lr=1e-4,
    #     end_lr=1e-4
    # )