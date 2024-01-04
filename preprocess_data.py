from config import *
import os
from data_analyse_functions import *
from multiprocessing import Pool, Manager, Process
import multiprocessing as mp
from tqdm import tqdm
import pandas as pd
from data_store_functions import *

# 处理单个文件
def process_single_file(json_silence, node_set, relation_set, detail_set,  triple_list):
    for line in json_silence.itertuples(): 
        line = line[1]     
        type = list(line.keys())[0]
        if type == 'com.bbn.tc.schema.avro.cdm18.Event':
            # 说明这行是event
            node = parse_event_data(line)
            # 添加到三元组
            triple_list.append([node['subject'], node['type'], node["predicateObject"], node["timestamp"]])
            # 添加到relation字典
            relation_set.append(node["type"])
        else:
            if type == "com.bbn.tc.schema.avro.cdm18.Subject":
                node = parse_subject_data(line)
                node_set.append((node["uuid"], str(node["name"]) + "_" + node["type"]))
                detail_set.append((node["uuid"],node))
            elif type == "com.bbn.tc.schema.avro.cdm18.Principal":
                node = parse_principal_data(line)
                node_set.append((node['uuid'], str(node['userId']) + "_" + node["type"]))
                detail_set.append((node["uuid"],node))
            elif type == 'com.bbn.tc.schema.avro.cdm18.NetFlowObject':
                node = parse_netflow_data(line)
                node_set.append((node["uuid"], str(node["localAddress"])+":"+str(node["localPort"]) + "->" + str(node["remoteAddress"]) + ":" + str(node["remotePort"]) + "_" + node["type"]))
                detail_set.append((node["uuid"], node))
            elif type == 'com.bbn.tc.schema.avro.cdm18.FileObject':
                node = parse_fileobject_data(line)
                node_set.append((node["uuid"], str(node["path"]) + "_" + node["type"]))
                detail_set.append((node["uuid"], node))
            elif type == 'com.bbn.tc.schema.avro.cdm18.SrcSinkObject':
                node = parse_srcsinkobject_data(line)
                node_set.append((node["uuid"], str(node["base_pid"]) + "_" + node["type"]))
                detail_set.append((node["uuid"], node))
            elif type == 'com.bbn.tc.schema.avro.cdm18.UnnamedPipeObject':
                node = parse_unnamedpipeobject_data(line)
                node_set.append((node["uuid"], str(node["pid"]) + "_" + node["type"]))
                detail_set.append((node["uuid"], node))
            elif type == 'com.bbn.tc.schema.avro.cdm18.MemoryObject':
                node = parse_memoryobject_data(line)
                node_set.append((node["uuid"], str(node["memoryAddress"]) + "_" + node["type"]))
                detail_set.append((node["uuid"], node))
                
# 处理所有的文件
def process_all_file(file_dir_path, num_processes):
    for file in os.listdir(file_dir_path):
        file_path = file_dir_path + "/" + file
        # 多进程处理文件
        parallel_process_single_data(file_path, num_processes)

# 生成的字典有三个，id-uuid， uuid-name, id-name
def generate_node_dict(node_set):
    # 唯一id对应uuid的字典
    id_uuid_dict = dict()
    # uuid对应名称的字典
    uuid_name_dict = dict()
    # 唯一id对应name的字典
    id_name_dict = dict()
    count = 0
    for item in node_set:
        id_uuid_dict[count] = item[0]
        uuid_name_dict[item[0]] = item[1]
        id_name_dict[count] = item[1]
        count += 1
    return id_uuid_dict, uuid_name_dict, id_name_dict

def generate_node_dict_2(node_set):
    # uuid对应名称的字典
    uuid_name_dict = dict()
    for item in node_set:
        uuid_name_dict[item[0]] = item[1]
    return uuid_name_dict

def generate_relation_dict(relation_set):
    id_relation_dict = dict()
    count = 0
    for item in relation_set:
        id_relation_dict[count] = item
        count += 1
    return id_relation_dict

def generate_relation_dict_2(relation_set):
    id_relation_dict = dict()
    for item in relation_set:
        id_relation_dict[item] = item
    return id_relation_dict

# 多个进程处理同一个文件
# 一个进程处理一个文件太慢了
def parallel_process_single_data(file_path, num_processes):
    file_name = file_path.split("/")[-1]
    print("处理文件%s中....."%(file_name))
    # 存储节点与编号的字典
    node_set = Manager().list()
    relation_set = Manager().list()
    detail_set = Manager().list()
    triple_list = Manager().list()
    process = mp.Pool(num_processes)
    results = []
    with open(file_path, "r") as file:
        lines = pd.read_json(file, lines=True)
        step = int(len(lines) / num_processes) 
        # 多进程处理文件
        with tqdm(total = num_processes) as pbar:
            for i in range(0, len(lines), step):
                result = process.apply_async(process_single_file, args=(lines[i:i+step], node_set, relation_set, detail_set, triple_list,))
                result.get()
                results.append(result)
                pbar.update(1)
            process.close()
            process.join()
    
    save_path = "./result/splited_result/" + file_name
    node_set = set(node_set)
    relation_set = set(relation_set)
    uuid_name_dict = generate_node_dict_2(node_set)
    id_relation_dict = generate_relation_dict_2(relation_set)
    clean_folder(save_path)
    # 保存节点集，关系集，细节，三元组
    save_dict_to_local(save_item = uuid_name_dict, save_path = save_path, file_name = "uuid_name_dict")   
    save_dict_to_local(save_item = id_relation_dict, save_path = save_path, file_name = "id_relation_dict")
    save_dict_to_local(save_item = detail_set, save_path = save_path, file_name = "details")
    save_triple_to_local(triple = triple_list, save_path = save_path, file_name = "triple")
    print("文件%s处理完成"%(file_name))

# 文件编号转名称
def uuid_to_nameid(file_path, save_path, id_uuid_dict, uuid_name_dict):
    pass

if __name__=="__main__":
    mkdir_multi("./result/splited_result/")
    mkdir_multi("./result/total_result/")
    process_all_file(cadets_source_data, num_processes)
    # process_all_file("./example", 1)