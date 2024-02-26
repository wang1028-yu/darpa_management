import multiprocessing as mp
import sys
sys.path.append("../requirements/OpenKE")
sys.path.append("./utils")

source_data_path = "/home/wcy/workspace/source_data/darpa"
trace_source_data = source_data_path + "/trace"
# trace_source_data = "./test_data/"
cadets_source_data = source_data_path + "/cadets"
little_test_data = source_data_path + "/little_test"
# num_processes = mp.cpu_count() - 1
num_processes = 30


# splited_result_path = "./result/splited_result/"
# total_result_path = "./result/total_result/"

splited_result_path = "./test/splited_result/"
total_result_path = "./test/total_result/"

node_path = "./result/total_result/types/"
memory_node_path = node_path + "memory.pkl"
file_node_path = node_path + "file.pkl"
netflow_node_path = node_path + "netflow.pkl"
principal_node_path = node_path + "principal.pkl"
srcsink_node_path = node_path + "srcsink.pkl"
subject_node_path = node_path + "subject.pkl"
unnamepipe_node_path = node_path + "unnamepipe.pkl"