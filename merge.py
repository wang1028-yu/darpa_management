import os
import pickle
from config import *
from utils.data_analyse_functions import *
from utils.data_store_functions import *

# 合并字典的函数
# 可以合并节点字典和relation字典
# def merge_dict(dict_list):
#     total_dict = {}
#     for dict in dict_list:
#         for key in dict:
#             value = dict[key]
#             total_dict[value] = value
#     return total_dict


# 合并字典的函数
# 可以合并节点字典和relation字典
def merge_dict(dict_list):
    total_dict = {}
    # node_set = set()
    for dict in dict_list:
        for key in dict:
            if key in total_dict:
                if total_dict[key].split("_")[0] == "null" and dict[key].split("_")[0] != "null":
                    total_dict[key] = dict[key]
            else:
                total_dict[key] = dict[key]
    return total_dict
            
# 生成节点字典
def generate_node_dict(node_dict):
    node_set = set()
    # 唯一id对应uuid的字典
    uuid_id_dict = dict()
    # uuid对应名称的字典
    uuid_name_dict = dict()
    # 唯一id对应name的字典
    id_name_dict = dict()
    count = 0
    for item in node_dict:
        key = item
        value = node_dict[item]
        if (value in node_set) == False:
            node_set.add(value)
            id_name_dict[value] = count
            count += 1
        uuid_name_dict[key] = value
        uuid_id_dict[key] = id_name_dict[uuid_name_dict[key]]
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
            if None in [name1, name2]:
                continue
            result_list.append("%s\t%s\t%s\t%s\t%s\t%s\t%s"%(id1, id2, relaiton_id, name1, name2, relation, timestamp))
    with open(save_path, "w") as file:
        for line in result_list:
            file.write(line)
    
# 编码三元组
def encode_triple_2(triple_file_path, uuid_name_dict, relation_dict, save_path):
    result_list = []
    # 静态编码
    static_file_node_set = set()
    static_subject_node_set = set()
    static_netflow_node_set = set()
    # 动态编码
    dynamic_file_node_set = set()
    dynamic_subject_node_set = set()
    dynamic_netflow_node_set = set()
    # 动静态结合字典
    static_dynamic_dict = dict()
    static_dynamic_subject_dict = dict()
    static_dynamic_file_dict = dict()
    static_dynamic_netflow_dict = dict()
    # 最后编码结果列表
    encode_result_list = []
    with open(triple_file_path, "r") as file:
        for triple in file:
            [node1, relation, node2, timestamp] = triple.split("\t")
            timestamp = int(timestamp.strip())
            name1 = uuid_name_dict.get(node1)
            name2 = uuid_name_dict.get(node2)
            if None in [name1, name2]:
                continue
            for node_name in [name1, name2]:
                type = node_name.split("_")[-1]
                if type == "subject":
                    static_subject_node_set.add(node_name)
                    dynamic_subject_node_set.add((node_name, timestamp))
                elif type == "file":
                    static_file_node_set.add(node_name)
                    dynamic_file_node_set.add((node_name, timestamp))
                elif type == "netflow":
                    static_netflow_node_set.add(node_name)
                    dynamic_netflow_node_set.add((node_name, timestamp))
            relaiton_id = relation_dict.get(relation)
            result_list.append([relaiton_id, name1, name2, relation, timestamp]) 
    # 静态字典
    static_subject_dict = dict(zip(list(static_subject_node_set), range(len(static_subject_node_set))))
    static_file_dict = dict(zip(list(static_file_node_set), range(len(static_file_node_set))))
    static_netflow_dict = dict(zip(list(static_netflow_node_set), range(len(static_netflow_node_set))))
    
    # 动态字典
    dynamic_subject_dict = dict(zip(list(dynamic_subject_node_set), range(len(dynamic_subject_node_set))))
    dynamic_file_dict = dict(zip(list(dynamic_file_node_set), range(len(dynamic_file_node_set))))
    dynamic_netflow_dict = dict(zip(list(dynamic_netflow_node_set), range(len(dynamic_netflow_node_set))))

    for item in result_list:
        [relaiton_id, name1, name2, relation, timestamp] = item
        if None in [name1, name2]:
            continue
        # 查询name1编码
        type1 = name1.split("_")[-1]
        if type1 == "subject":
            static_id1 = static_subject_dict.get(name1)
            dynamic_id1 = dynamic_subject_dict.get((name1, timestamp))
            static_dynamic_subject_dict[dynamic_id1] = (static_id1, timestamp)
        elif type1 == "file":
            static_id1 = static_file_dict.get(name1)
            dynamic_id1 = dynamic_file_dict.get((name1, timestamp))
            static_dynamic_file_dict[dynamic_id1] = (static_id1, timestamp)
        elif type1 == "netflow":
            static_id1 = static_netflow_dict.get(name1)
            dynamic_id1 = dynamic_netflow_dict.get((name1, timestamp))
            static_dynamic_netflow_dict[dynamic_id1] = (static_id1, timestamp)
        # 查询name2编码
        type2= name2.split("_")[-1]
        if type2 == "subject":
            static_id2 = static_subject_dict.get(name2)
            dynamic_id2 = dynamic_subject_dict.get((name2, timestamp))
            static_dynamic_subject_dict[dynamic_id2] = (static_id2, timestamp)
        elif type2 == "file":
            static_id2 = static_file_dict.get(name2)
            dynamic_id2 = dynamic_file_dict.get((name2, timestamp))
            static_dynamic_file_dict[dynamic_id2] = (static_id2, timestamp)
        elif type2 == "netflow":
            static_id2 = static_netflow_dict.get(name2)
            dynamic_id2 = dynamic_netflow_dict.get((name2, timestamp))
            static_dynamic_netflow_dict[dynamic_id2] = (static_id2, timestamp)
        
        key1 = (type1, static_id1, name1)
        key2 = (type2, static_id2, name2)
        # 添加到动静态组合字典
        if key1 in static_dynamic_dict:
            static_dynamic_dict[key1].add((dynamic_id1, timestamp))
        else:
            static_dynamic_dict[key1] = set()
            static_dynamic_dict[key1].add((dynamic_id1, timestamp))
        if key2 in static_dynamic_dict:
            static_dynamic_dict[key2].add((dynamic_id2, timestamp))
        else:
            static_dynamic_dict[key2] = set()
            static_dynamic_dict[key2].add((dynamic_id2, timestamp))
        # 添加到编码结果列表
        encode_result_list.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(dynamic_id1, dynamic_id2, static_id1, static_id2, relaiton_id, name1, name2, relation, timestamp))
    
    # 添加相同节点的时间关系边
    # for key in static_dynamic_dict:
    #     (type, static_id, name) = key
    #     edges = static_dynamic_dict[key]
    #     edges = sorted(list(edges), key=lambda x:x[1])
    #     for index in range(0, len(edges)-1, 2):
    #         node1 = edges[index]
    #         node2 = edges[index + 1]
    #         dynamic_id1 = node1[0]
    #         dynamic_id2 = node2[0]
    #         timestamp = node2[1]
    #         # TODO 后面再优化
    #         relaiton_id = 99
    #         relation = "EVENT_DYNAMIC"
    #         encode_result_list.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(dynamic_id1, dynamic_id2, static_id, static_id, relaiton_id, name, name, relation, timestamp))
        
    with open(save_path + "/encode_triple.txt", "w") as file:
        for line in encode_result_list:
            file.write(line)    
    os.mkdir(save_path + "/types/")
    
    # 字典保存到本地
    # dynamic_subject_list = [item[0]+"\t"+str(dynamic_subject_dict[item]) for item in dynamic_subject_dict]
    # dynamic_file_list = [item[0]+"\t"+str(dynamic_file_dict[item]) for item in dynamic_file_dict]
    # dynamic_netflow_list = [item[0]+"\t"+str(dynamic_netflow_dict[item]) for item in dynamic_netflow_dict]
    
    # save_list_to_local(dynamic_subject_list, save_path + "/types/", "subject")
    # save_list_to_local(dynamic_file_list, save_path + "/types/", "file")
    # save_list_to_local(dynamic_netflow_list, save_path + "/types/", "netflow")
    
    # 静态字典
    static_file_list = [item + "\t" + str(static_file_dict[item]) for item in static_file_dict]
    static_subject_list = [item + "\t" + str(static_subject_dict[item]) for item in static_subject_dict]
    static_netflow_list = [item + "\t" + str(static_netflow_dict[item]) for item in static_netflow_dict]
    
    save_list_to_local(static_subject_list, save_path + "/types/", "subject")
    save_list_to_local(static_file_list, save_path + "/types/", "file")
    save_list_to_local(static_netflow_list, save_path + "/types/", "netflow")
    
    static_dynamic_subject_dict = dict(sorted(static_dynamic_subject_dict.items(), reverse=False))
    static_dynamic_file_dict = dict(sorted(static_dynamic_file_dict.items(), reverse=False))
    static_dynamic_netflow_dict = dict(sorted(static_dynamic_netflow_dict.items(), reverse=False))
    # 格式
    save_dict_to_local(static_dynamic_subject_dict, save_path + "/types/", "dynamic_subject")
    save_dict_to_local(static_dynamic_file_dict, save_path + "/types/", "dynamic_file")
    save_dict_to_local(static_dynamic_netflow_dict, save_path + "/types/", "dynamic_netflow")
    
    
if __name__ =="__main__":
# def run():
    # 节点字典列表
    node_list = []
    # 关系字典列表
    relation_list = []
    # for file in os.listdir(splited_result_path):
    for index in range(211):
        file = "ta1-trace-e3-official.json.%s/"%(index)
        node_path = splited_result_path + file + "/uuid_name_dict.pkl"
        relation_path = splited_result_path + file + "/id_relation_dict.pkl"
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
    # 清理主文件夹
    print("保存字典中。。。")
    clean_folder(total_result_path)
    # 编码节点, 关系
    save_dict_to_local(save_item = uuid_name_dict, save_path = total_result_path, file_name = "uuid_name_dict") 
    save_dict_to_local(save_item = relation_dict, save_path = total_result_path, file_name = "id_relation_dict")
    print("保存字典完成")
    
    # 编码三元组 nodeid1, nodeid2, relaitonid, node1, node2, relation, timestamp
    # for file in os.listdir(splited_result_path):
    #     print(file)
    #     triple_path = splited_result_path + file + "/triple.txt"
    #     save_path = splited_result_path + file       
    #     print("处理%s中。。。。"%(file))
    #     encode_triple_2(triple_path, uuid_name_dict, relation_dict, save_path)
    #     print("%s处理完成"%(file))
    
    
    # 编码三元组 nodeid1, nodeid2, relaitonid, node1, node2, relation, timestamp
    for i in range(263):
        file = "%s.json"%(i)
        triple_path = splited_result_path + file + "/triple.txt"
        save_path = splited_result_path + file
        print("处理%s中。。。。"%(file))
        encode_triple_2(triple_path, uuid_name_dict, relation_dict, save_path)
        print("%s处理完成"%(file))
    
    file_node_set = set()
    netflow_node_set = set()
    subject_node_set = set()
    
    # 生成去重原始语料库
    for i in range(263):
        file = "%s.json"%(i)
        single_file_node_path = splited_result_path + file + "/types/file.txt"
        single_netflow_node_path = splited_result_path + file + "/types/netflow.txt"
        single_subject_node_path = splited_result_path + file + "/types/subject.txt"
        with open(single_file_node_path, "r") as f:
            for line in f:
                name, id = line.split("\t")
                file_node_set.add(name)
        with open(single_netflow_node_path, "r") as f:
            for line in f:
                name, id = line.split("\t")
                netflow_node_set.add(name)
        with open(single_subject_node_path, "r") as f:
            for line in f:
                name, id = line.split("\t")
                subject_node_set.add(name)
    
    # 保存原始语料库
    file_node_dict = dict(zip(list(file_node_set), range(len(file_node_set))))
    subject_node_dict = dict(zip(list(subject_node_set), range(len(subject_node_set))))
    netflow_node_dict = dict(zip(list(netflow_node_set), range(len(netflow_node_set))))
    
    file_node_list = [item + "\t" + str(file_node_dict[item]) for item in file_node_dict]
    subject_node_list = [item + "\t" + str(subject_node_dict[item]) for item in subject_node_dict]
    netflow_node_list = [item + "\t" + str(netflow_node_dict[item]) for item in netflow_node_dict]
    # 保存到本地
    save_list_to_local(subject_node_list, "./result/total_result/", "subject")
    print("subject保存完成")
    save_list_to_local(file_node_list,  "./result/total_result/", "file")
    print("file保存完成")
    save_list_to_local(netflow_node_list, "./result/total_result/", "netflow")
    print("netflow保存完成")