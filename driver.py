import merge
import preprocess_data
from config import *
# 主函数
if __name__ == "__main__":
    preprocess_data.run("./example", 1)
    # preprocess_data.run(trace_source_data, 1)
    # preprocess_data.run(trace_source_data, num_processes)
    merge.run()