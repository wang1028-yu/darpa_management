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
            dynamic_id1, dynamic_id2, static_id1, static_id2, relation_id, node1, node2, relation, timestamp = line.split("\t")
            # id1, id2, relation_id, node1, node2, relation, timestamp = line.split("\t")
            type1 = node1.split("_")[-1]
            type2 = node2.split("_")[-1]
            timestamp = timestamp.replace("\n", "")
            details = [int(dynamic_id1),int(dynamic_id2), int(static_id1), int(static_id2), int(relation_id), int(timestamp)]
            line_type = "%s-%s-%s"%(type1,relation,type2)
            if line_type in types_line_dict:
                types_line_dict[line_type].append(details)
            else:
                types_line_dict[line_type] = [details]
    return types_line_dict

# 保存异构图中各种三元组的信息
def save_heterogenous(file_path, types_line_dict):
    hetero_triples_path = file_path + "/hetero_triples.pkl"
    with open(hetero_triples_path, 'wb') as f:
        pickle.dump(types_line_dict, f)

# 单线程处理文件
def extrace_types_triple_single(file):
    file_path = splited_result_path + file
    print(file_path)
    encoding_triple_path = file_path + "/encode_triple.txt"
    types_line_dict = process_heterogenous(encoding_triple_path)
        
    # 保存
    save_heterogenous(file_path, types_line_dict)
    print("%s处理完成"%(file_path))
    
# 多线程处理文件
def extract_types_triple_muti_process(file_dir_path, num_processes):
    process_pool = mp.Pool(num_processes)
    
    for file in os.listdir(file_dir_path):
        print(file)
        process_pool.apply_async(extrace_types_triple_single, args=(file,))
    
    # for file in file_dir_path:
    #     print(file)
    #     process_pool.apply_async(extrace_types_triple_single, args=(file))
    
    process_pool.close()
    process_pool.join()
    
    
# 处理动态图数据
def process_dynamic_graph():
    pass

# 主要任务，压缩与处理
# if __name__ == "__main__":
def run():
    # 提取
    # file_path = [str(i) + ".json" for i in range(526)]
    # extract_types_triple_muti_process(file_path, num_processes)
    extract_types_triple_muti_process(splited_result_path, num_processes)