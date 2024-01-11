import os
import time
from config import *

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


# 主要任务，压缩与处理
if __name__ == "__main__":
    # extract_all_file_nodes(splited_result_path)
    # file_dir_path = splited_result_path
    # test_file_path = splited_result_path + "ta1-trace-e3-official-1.json/encode_triple.txt"
    file_path = splited_result_path + "4.json/"
    encode_triple_path = file_path + "encode_triple.txt"
    subject_node_path = file_path + "types/subject.pkl"
    # 生成邻接列表字典
    adj_list_dict = generate_adj_list_dict(encode_triple_path)
    subject_nodes = load_pickle(subject_node_path)    
    subject_nodes_id = list(subject_nodes.keys())
    for node in subject_nodes:
        print(node)