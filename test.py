import json
import os
from multiprocessing import Pool, Manager, Process
import sys
sys.path.append("..")
from config import *
from data_analyse_functions import *
import pandas as pd

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
    with open("./example/1.json", "r") as file:
        data = pd.read_json(file, lines=True)
        print(data[1:4])
    # data = pd.read_json("./example/1.json", lines=True)
    # for line in data.itertuples():
    #     print(line)