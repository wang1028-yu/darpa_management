from config import *
import os
from multiprocessing import Pool, Manager, Process
import multiprocessing as mp
from tqdm import tqdm
import pandas as pd
import time
from utils.data_analyse_functions import *
from utils.data_store_functions import *

# 分割darpa数据集
# if __name__=="__main__":
def run():
    # origin_file_path = "/home/wcy/workspace/source_data/darpa/trace"
    # for file in range(211):
    #     file_path = "ta1-trace-e3-official.json." + str(file)
    # origin_file_path = "./test/splited_result/"
    origin_file_path = "./result/splited_result/"
    total_node_dict_path = "./result/total_result/uuid_name_dict.pkl"
    total_count_id = 0
    # for index in range(1):
    timestamp0 = 1522703644
    for index in range(211):
        # file_path = origin_file_path + "%s.json/"%(index)
        file_path = origin_file_path + "ta1-trace-e3-official.json.%s/"%(index)
        triple_path = file_path + "triple.txt"
        node_path = file_path + "uuid_name_dict.pkl"
        relation_path = file_path + "id_relation_dict.pkl"
        time_path = file_path + "time.txt"
        # # 节点字典
        # node_dict = load_pickle(node_path)
        # # 边字典
        # relation_dict = load_pickle(relation_path)
        # 第一行数据
        start_time = open(time_path, "r").readlines()[0].split("\t")[1].strip()
        origin_f  = open(triple_path).readlines()
        splited_triple= []
        for line in origin_f:
            line_time_stamp = line.split("\t")[-1].strip()
            line = line.strip().split("\t")
            splited_triple.append(line)
            # # 查找节点名称
            # id1 = line.split("\t")[0]
            # id2 = line.split("\t")[1]
            
            if int(line_time_stamp) >= (timestamp0 + 3600):
                triple_save_path = origin_file_path + str(total_count_id) + ".json"
                time_dict = {"start_time": timestamp_to_date(int(timestamp0)),"end_time":timestamp_to_date(int(line_time_stamp))}
                # 清空文件夹
                clean_folder(triple_save_path)
                save_triple_to_local(triple = splited_triple, save_path = triple_save_path, file_name = "triple")
                save_dict_to_local(save_item= time_dict,save_path=triple_save_path, file_name="time")
                # 保存节点和边的字典
                
                print(file_path + str(total_count_id) + "保存完成")
                timestamp0 = int(line_time_stamp)
                # 清空三元组和字典
                splited_triple.clear()
                total_count_id += 1
                
        print(triple_path)
        
        
        