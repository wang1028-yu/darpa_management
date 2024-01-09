import os
from data_analyse_functions import *
from data_store_functions import *
import time
from config import *


# 主要任务，压缩与处理
if __name__ == "__main__":
    # mkdir_multi("./123/546")
    # file_dir_path = "./result/splited_result/"
    # file_list = os.listdir(file_dir_path)
    # for file in file_list:
    #     txt_file_path = file_dir_path + "/" + file + "/triple.txt"
    #     min_time, max_time = extract_time(txt_file_path)
    # node_distinct(netflow_node_path)
    # node_distinct(subject_node_path)
    node_distinct(srcsink_node_path)