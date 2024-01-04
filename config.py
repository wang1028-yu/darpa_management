import multiprocessing as mp
source_data_path = "/home/wcy/workspace/source_data/darpa"
trace_source_data = source_data_path + "/trace"
cadets_source_data = source_data_path + "/cadets"
num_processes = int(mp.cpu_count()/2)
