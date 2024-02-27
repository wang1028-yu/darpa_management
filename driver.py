import merge
import preprocess_data
import features
import process_data
from config import *
import os

# 主函数
if __name__ == "__main__":
    try:
        os.rmdir("./finish")
    except:
        pass
    preprocess_data.run("./example", 1)
    # preprocess_data.run(trace_source_data, 1)
    # preprocess_data.run(trace_source_data, num_processes)
    merge.run()
    features.run()
    process_data.run()
    os.mkdir("./finish")