from config import *
import os
from multiprocessing import Pool, Manager, Process
import multiprocessing as mp
from tqdm import tqdm
import pandas as pd
import time
from utils.data_analyse_functions import *
from utils.data_store_functions import *
                
# 处理所有的文件
def process_all_file_miti_processes(file_dir_path, num_processes):
    process_pool = mp.Pool(num_processes)
    for file in os.listdir(file_dir_path):
        file_path = file_dir_path + "/" + file
        process_pool.apply_async(process_single_file_single_process, args=(file_path,))
    process_pool.close()
    process_pool.join()

# 单进程，单文件
def process_single_file_single_process(file_path):
    print("开始处理文件%s"%(file_path))
    time_list = list()
    node_set = list()
    relation_set = list()
    triple_list = list()
    with open(file_path, "r") as file:
        for line in file:
            type  = extract_nodetype(line)
            line = load_json(line)["datum"]
            if type == 'com.bbn.tc.schema.avro.cdm18.Event':
                # 说明这行是event
                node = parse_event_data(line)
                second_timestamp = node["timestamp"] // 1000000000
                # 添加到三元组
                triple_list.append([node['sub'], node['type'], node["obj"], second_timestamp])
                # 添加到relation字典
                relation_set.append(node["type"])
                time_list.append(second_timestamp)
            else:
                if type == "com.bbn.tc.schema.avro.cdm18.Subject":
                    node = parse_subject_data(line)
                    node_set.append((node["uuid"], node["name"] + "_" + str(node["cid"]) + "_" + str(node["cmdLine"]) + "_" + node["type"]))
                elif type == 'com.bbn.tc.schema.avro.cdm18.NetFlowObject':
                    node = parse_netflow_data(line)
                    node_set.append((node["uuid"], str(node["localAddress"])+":"+str(node["localPort"]) + "->" + str(node["remoteAddress"]) + ":" + str(node["remotePort"]) + "_" + node["type"]))
                elif type == 'com.bbn.tc.schema.avro.cdm18.FileObject':
                    node = parse_fileobject_data(line)
                    node_set.append((node["uuid"], str(node["path"]) + "_" + node["type"]))
    file_name = file_path.split("/")[-1]
    save_path = splited_result_path + "/" + file_name
    node_set = set(node_set)
    relation_set = set(relation_set)
    uuid_name_dict = generate_node_dict_2(node_set)
    id_relation_dict = generate_relation_dict_2(relation_set)
    clean_folder(save_path)
    time_dict = {"start_time": timestamp_to_date(min(time_list)),"end_time":timestamp_to_date(max(time_list))}
    # 保存节点集，关系集，细节，三元组, 时间
    save_dict_to_local(save_item = uuid_name_dict, save_path = save_path, file_name = "uuid_name_dict")   
    save_dict_to_local(save_item = id_relation_dict, save_path = save_path, file_name = "id_relation_dict")
    save_dict_to_local(save_item= time_dict,save_path=save_path, file_name="time")
    save_triple_to_local(triple = triple_list, save_path = save_path, file_name = "triple")
    
    print("文件%s处理完成"%(file_path))
    
# 单进程处理文件
def process_all_file_single_processes(file_dir_path):
    for file in os.listdir(file_dir_path):
        file_path = file_dir_path + "/" + file
        process_single_file_single_process(file_path)
        
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

# if __name__=="__main__":
def run(file_path, num_processes):
    mkdir_multi(splited_result_path)
    mkdir_multi(total_result_path)
    process_all_file_miti_processes(file_path, num_processes)