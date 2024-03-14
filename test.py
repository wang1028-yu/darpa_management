import json
import os
from multiprocessing import Pool, Manager, Process
import sys
sys.path.append("..")
from config import *
from data_analyse_functions import *
import pandas as pd
from data_store_functions import *

# 测试
def test_output(file_name):
    with open(file_name) as file:
        key = 0
        for line in file:
            line = json.loads(line)
            print(line["datum"])
            print()
            if key ==2:
                break
            key += 1
            
def test_process_single_file(word_set, file_path):
    with open(file_path, "r") as file:
        for line in file:
            for item in line.split(" "):
                word_set.append(item)
       
def test_mutiprocess():
    word_set = Manager().list()
    file_dir = "./test_file"
    process = []
    for file in os.listdir(file_dir):
        file_path = file_dir + "/" + file
        p = Process(target=test_process_single_file, args=(word_set,file_path))
        p.start()
        process.append(p)
    for p in process:
        p.join()
    print(set(word_set))

def test_chunk_file(file_path):
    with open(file_path, "r") as file:
        file.seek(10)
        data = file.read(40 - 10)
        print(data)


if __name__ =="__main__":
    netflow_features_path = "./result/splited_result/ta1-trace-e3-official.json.64/types/netflow_features.pkl"
    netflow_features = load_pickle(netflow_features_path)
    for key in netflow_features:
        print(len(netflow_features[key]))
        print(key)
    
    print(netflow_features[867])
    
    
