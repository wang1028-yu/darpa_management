from utils.data_analyse_functions import *
from utils.data_store_functions import *

# 分割darpa数据集
if __name__=="__main__":
    origin_file_path = "/home/wcy/workspace/source_data/darpa/trace"
    for file in range(211):
        file_path = "ta1-trace-e3-official.json." + str(file)
        