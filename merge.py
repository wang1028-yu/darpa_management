import os
import pickle
from data_analyse_functions import *
from data_store_functions import *

# 合并字典的函数
# 可以合并节点字典和relation字典
def merge_dict(dict_list):
    total_dict = {}
    for dict in dict_list:
        total_dict.update(dict)
    return total_dict

# 生成节点字典
def generate_node_dict(node_set):
    # 唯一id对应uuid的字典
    uuid_id_dict = dict()
    # uuid对应名称的字典
    uuid_name_dict = dict()
    # 唯一id对应name的字典
    id_name_dict = dict()
    count = 0
    for item in node_set:
        key = item
        value = node_set[item]
        uuid_id_dict[key] = count
        uuid_name_dict[key] = value
        id_name_dict[count] = value
        count += 1
    return uuid_id_dict, uuid_name_dict, id_name_dict

# 生成关系字典
def generate_relation_dict(relation_set):
    id_relation_dict = dict()
    count = 0
    for item in relation_set:
        id_relation_dict[item] = count
        count += 1
    return id_relation_dict

# 编码三元组
def encode_triple(triple_file_path, uuid_id_dict, uuid_name_dict, relation_dict, save_path):
    result_list = []
    with open(triple_file_path, "r") as file:
        for triple in file:
            [node1, relation, node2, timestamp] = triple.split("\t")
            id1 = uuid_id_dict.get(node1)
            name1 = uuid_name_dict.get(node1)
            id2 = uuid_id_dict.get(node2)
            name2 = uuid_name_dict.get(node2)
            relaiton_id = relation_dict.get(relation)
            result_list.append("%s\t%s\t%s\t%s\t%s\t%s\t%s"%(id1, id2, relaiton_id, name1, name2, relation, timestamp))
    with open(save_path, "w") as file:
        for line in result_list:
            file.write(line)

if __name__ =="__main__":
# def run():
    result_path = "./result/splited_result/"
    # 节点字典列表
    node_list = []
    # 关系字典列表
    relation_list = []
    for file in os.listdir(result_path):
        node_path = result_path + file + "/uuid_name_dict.pkl"
        relation_path = result_path + file + "/id_relation_dict.pkl"
        with open(node_path, "rb") as f:
            node_dict = pickle.load(f)
            node_list.append(node_dict)
        with open(relation_path, "rb") as f:
            relation_dict = pickle.load(f)
            relation_list.append(relation_dict)
            
    # 获取去重后的关系字典和节点字典
    relation_dict = generate_relation_dict(merge_dict(relation_list))
    uuid_id_dict, uuid_name_dict, id_name_dict = generate_node_dict(merge_dict(node_list))
    # 保存统一的字典
    total_save_path = "./result/total_result/"
    # 清理主文件夹
    print("保存字典中。。。")
    clean_folder(total_save_path)
    # 编码节点, 关系
    save_dict_to_local(save_item = uuid_id_dict, save_path = total_save_path, file_name = "id_uuid_dict")
    save_dict_to_local(save_item = uuid_name_dict, save_path = total_save_path, file_name = "uuid_name_dict") 
    save_dict_to_local(save_item = id_name_dict, save_path = total_save_path, file_name = "id_name_dict")    
    save_dict_to_local(save_item = relation_dict, save_path = total_save_path, file_name = "id_relation_dict")
    print("保存字典完成")
    # 节点压缩， 压缩临时文件， 要不要弄？？？
    # TODO
    
    # 提取各种类型的节点
    node_type_list = ["subject", "principal", "netflow", "file", "srcsink", "unnamepipe", "memory"]
    os.mkdir("./result/total_result/types/")
    for node_type in node_type_list:
        node_type_save_path = "./result/total_result/types/"
        extract_node_in_type(id_name_dict, node_type, node_type_save_path)
    
    # 编码三元组 nodeid1, nodeid2, relaitonid, node1, node2, relation, timestamp
    for file in os.listdir(result_path):
        triple_path = result_path + file + "/triple.txt"
        save_path = result_path + file +"/encode_triple.txt"
        print("处理%s中。。。。"%(file))
        encode_triple(triple_path, uuid_id_dict, uuid_name_dict, relation_dict, save_path)
        print("%s处理完成"%(file))