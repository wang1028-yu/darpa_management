import os
import time
from config import *
from utils.data_store_functions import *
from utils.data_analyse_functions import *

def extract_dict_from_txt(file_path):
    node_dict = dict()
    with open(file_path, "r") as file:
        for line in file:
            details = line.split("\t")
            node_dict[details[0]] = details[3]
            node_dict[details[1]] = details[4]
    return node_dict

# 提取所有文件的各节点
def extract_all_file_nodes(file_dir_path):
    file_list = os.listdir(file_dir_path)
    for file in file_list:
        file_path = file_dir_path + "/" + file
        txt_file_path = file_path + "/encode_triple.txt"
        print("处理文件%s中"%(file_path))
        node_dict = extract_dict_from_txt(txt_file_path)
        extract_all_type_node(file_path, node_dict)
        print("文件%s处理完成"%(file_path))

# 数据压缩函数
def compress_data(file_path):
    distinct_set = set()
    with open(file_path + "/encode_triple.txt", "r") as file:
        for line in file:
            [id1, id2, relation_id, node1, node2, relation, timestamp] = line.split("\t")
            detail = "%s\t%s\t%s"%(id1, id2, relation_id)
            distinct_set.add(detail)
    return distinct_set

def distinct_single_data():
    # 去重
    for file_path in filter_attack_data():
        print("处理文件%s中"%(file_path))
        distinct_set = compress_data(file_path)
        print("文件%s处理完成"%(file_path))
        save_path = file_path + "/compress.txt"
        save_to_local(save_item = distinct_set, save_path = save_path)   
    return 0

# 过滤攻击数据文件，保留正常数据文件
def filter_attack_data():
    benign_data_list = []
    attack_file_list = ["ta1-trace-e3-official-1.json.3", "ta1-trace-e3-official-1.json.4", "ta1-trace-e3-official.json.125"]
    for file in os.listdir(splited_result_path):
        file_path = splited_result_path + "/" + file
        if file in attack_file_list:
            continue
        else:
            benign_data_list.append(file_path)
    return benign_data_list

# 处理异构图
def distinct_total_data_heterogeneous():
    total_set = set()
    for file in filter_attack_data():
        compress_data_path = file + "/compress.txt"
        print("处理文件%s中"%(compress_data_path))
        with open(compress_data_path, "r") as compress_data:
            for line in compress_data:
                total_set.add(line)
        print("文件%s处理完成"%(compress_data_path))
    save_to_local(save_item = total_set, save_path = total_result_path + "triple.txt") 

# 处理同构图数据
def distinct_total_data_homogeneous():
    total_set = set()
    for file in filter_attack_data():
        compress_data_path = file + "/compress.txt"
        print("处理文件%s中"%(compress_data_path))
        with open(compress_data_path, "r") as compress_data:
            for line in compress_data:
                total_set.add(line)
        print("文件%s处理完成"%(compress_data_path))
    save_to_local(save_item = total_set, save_path = total_result_path + "triple.txt") 
    
# 处理异构图数据
def process_heterogenous(file_path):
    types_line_dict = dict()
    with open(file_path, "r") as file:
        for line in file:
            id1, id2, relation_id, node1, node2, relation, timestamp = line.split("\t")
            type1 = node1.split("_")[-1]
            type2 = node2.split("_")[-1]
            timestamp = timestamp.replace("\n", "")
            details = "%s\t%s\t%s\t%s\t"%(id1, relation_id, id2, timestamp)
            line_type = "%s-%s-%s"%(type1,relation,type2)
            if line_type in types_line_dict:
                types_line_dict[line_type].append(details)
            else:
                types_line_dict[line_type] = [details]
    return types_line_dict

# 保存异构图中各种三元组的信息
def save_heterogenous(file_path, types_line_dict):
    hetero_triples_path = file_path + "/hetero_triples/"
    try:
        os.mkdir(hetero_triples_path)
    except:
        pass
    for key in types_line_dict:
        save_path = hetero_triples_path + key + ".txt"
        details = types_line_dict[key]
        save_to_local(details, save_path)

# 单线程处理文件
def extrace_types_triple_single(file):
    file_path = splited_result_path + file
    encoding_triple_path = file_path + "/encode_triple.txt"
    types_line_dict = process_heterogenous(encoding_triple_path)
    # 保存
    save_heterogenous(file_path, types_line_dict)
    print("%s处理完成"%(file_path))
    
# 多线程处理文件
def extract_types_triple_muti_process(file_dir_path, num_processes):
    process_pool = mp.Pool(num_processes)
    for file in os.listdir(file_dir_path):
        process_pool.apply_async(extrace_types_triple_single, args=(file,))
    process_pool.close()
    process_pool.join()
# 主要任务，压缩与处理
if __name__ == "__main__":
    extract_types_triple_muti_process(splited_result_path, num_processes)

        

    # distinct_single_data()
    # extract_all_file_nodes(splited_result_path)
    # distinct_total_data_heterogeneous()
    # distinct_total_data_homogeneous()
    
    # 深度优先搜索，放后面弄
    
    
    # file_dir_path = splited_result_path
    # test_file_path = splited_result_path + "ta1-trace-e3-official-1.json/encode_triple.txt"
    
    # file_path = splited_result_path + "ta1-trace-e3-official-1.json/"
    # encode_triple_path = file_path + "encode_triple.txt"
    # subject_node_path = file_path + "types/subject.pkl"
    
    # file_path = splited_result_path + "2.json/"
    # file_path = "./result/splited_result/ta1-trace-e3-official.json.1/"
    # encode_triple_path = file_path + "encode_triple.txt"
    # subject_node_path = file_path + "types/subject.pkl"
    # 生成邻接列表字典
    # adj_list_dict = generate_adj_list_dict(encode_triple_path)



    # subject_nodes = load_pickle(subject_node_path)    
    # subject_nodes_id = list(subject_nodes.keys())
    # for node in subject_nodes:
    #     # 深度优先搜索
    #     print(node)
    #     result = dfs(int(node), adj_list_dict)
    #     print(result)
        
    
    # adj_list_dict = dict()
    # file_path = "./test/test_triple.txt"
    # adj_list_dict = dict()
    # with open(file_path, "r") as file:
    #     for line in file:
    #         subject, object, relation, timestamp = line.replace("\n", "").split(" ")
    #         object_dict = {"relation":relation, "object":int(object), "timestamp":int(timestamp)}
    #         if int(subject) in adj_list_dict:
    #             adj_list_dict[int(subject)].append(object_dict)
    #         else:
    #             adj_list_dict[int(subject)] = []
    #             adj_list_dict[int(subject)].append(object_dict)
    # print(adj_list_dict)
    # result = dfs(1, adj_list_dict)
    # print(result) 