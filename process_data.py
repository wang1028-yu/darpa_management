import os
from data_analyse_functions import *
from data_store_functions import *
import time

if __name__ == "__main__":
    mkdir_multi("./123/546")
    file_dir_path = "./result/splited_result/"
    file_list = os.listdir(file_dir_path)
    for file in file_list:
        txt_file_path = file_dir_path + "/" + file + "/triple.txt"
        min_time, max_time = extract_time(txt_file_path)
        print(max_time)
        print(min_time)
    
    # timestamp = 1523627788474000000
    # time_stamp = time.time()
    # print(timestamp)
    # print(time_stamp)
    # print(timestamp_to_date(time_stamp))