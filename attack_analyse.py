# import igraph
import os
# def judge(tuple_list, tuple2):
#     for tuple1 in tuple_list:
#         # print(tuple1)
#         if (tuple1[0] in tuple2[0] and tuple1[1] in tuple2[1]) or (tuple1[1] in tuple2[0] and tuple1[0] in tuple2[1]):
#             if tuple1[1] == "180.156.107.146":
#                 print(tuple2)
#             return True
#         else:
#             return False

def judge(tuple1, tuple2):
    if (tuple1[0] in tuple2[0] and tuple1[1] in tuple2[1]) or (tuple1[1] in tuple2[0] and tuple1[0] in tuple2[1]):
        return True
    else:
        return False

if __name__ =="__main__":
    
    # attack_file_path = "./result/splited_result/ta1-trace-e3-official.json.125/triple.txt"
    # encode_attack_file_path = "./result/splited_result/ta1-trace-e3-official.json.125/encode_triple.txt"
    # attack_tuple_list = [
    #     ("/etc/passwd", "cache"),
    #     ("/etc/passwd","firefox"), 
    #     ("cache","/proc/sys/vm/overcommit_memory"), 
    #     ("cache", "/etc/group"), 
    #     ("cache","180.156.107.146"), 
    #     ("cache", "/home/admin/cache"), 
    #     ("cache", "/var/log/xtmp")
    #     ]
    # result_path = "./result/label_125.txt"
    
    
    # attack_file_path = "./result/splited_result/ta1-trace-e3-official-1.json.3/triple.txt"
    # encode_attack_file_path = "./result/splited_result/ta1-trace-e3-official-1.json.3/encode_triple.txt"
    # attack_tuple_list = [
    #     ("gtcache", "pass_mgr"),
    #     ("/etc/passwd","gtcache"), 
    #     ("/dev/urandom","gtcache"), 
    #     ("gtcache", "146.153.68.151"), 
    #     ("sh","gtcache"), 
    #     ("/tmp/ztmp", "ztmp"), 
    #     ("ztmp", "uname"),
    #     ("ztmp","128.55.12.73"),
    #     ("ztmp","162.66.239.75")
    #     ]
    # result_path = "./result/label_1-3.txt"
    
    
    attack_file_path = "./result/splited_result/ta1-trace-e3-official-1.json.4/triple.txt"
    encode_attack_file_path = "./result/splited_result/ta1-trace-e3-official-1.json.4/encode_triple.txt"
    attack_tuple_list = [
        ("/home/admin/Desktop/tcexec", "chmod"),
        ("/home/admin/Desktop/tcexec", "thunderbird"), 
        ("chmod", "bash"), 
        ("/home/admin/Desktop/tcexec", "chmod"), 
        ("/home/admin/Desktop/tcexec","tcexec"), 
        ("/tmp/tcexec", "pine"), 
        ("/tmp/tcexec", "tcexec"),
        ("tcexec","sh"),
        ("tcexec","162.66.239.75"),
        ("tcexec","128.55.12.1"),
        ("tcexec","128.55.12.110")
        ]
    result_path = "./result/label_1-4.txt"
    
    try:
        os.remove(result_path)
    except:
        pass
    with open(encode_attack_file_path, "r") as file:
        for line in file:
            [id1, id2, relation_id, node1, node2, relation, timestamp] = line.split("\t")
            for tuple1 in attack_tuple_list:
                if judge(tuple1, (node1, node2)):
                    with open(result_path, "a+") as result_file:
                        result_file.write(line)
                        result_file.flush()
                    continue