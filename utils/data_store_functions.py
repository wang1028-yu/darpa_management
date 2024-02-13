import pickle
import os
import shutil

# 保存的函数
def save_dict_to_local(save_item, save_path, file_name):
    # 存两份，pickle一份，txt一份
    with open(save_path + "/" + file_name + ".pkl", 'wb') as f:
        pickle.dump(save_item, f)
    try:
        # 存txt一份
        with open(save_path + "/" + file_name +".txt", "w") as f:
            for item in save_item:
                f.write(str(item) + "\t" + str(save_item[item]) + "\n")
    except:
        os.remove(save_path + "/" + file_name +".txt")

        
# 把三元组存储到本地
def save_triple_to_local(triple, save_path, file_name):
    with open(save_path + "/" + file_name + ".txt",  "w") as file:
        for item in triple:
            line = item[0] + "\t" + item[1] + "\t" + item[2] + "\t" + str(item[3])
            file.write(line + "\n")

def save_to_local(save_item, save_path):
    try:
        os.remove(save_path)
    except:
        pass
    with open(save_path, "a+") as file:
        for line in save_item:
            file.write(line + "\n")
        file.close()
    save_path = save_path.replace(".txt", ".pkl")
    with open(save_path, 'wb') as f:
        pickle.dump(save_item, f)

# 清除文件夹
def clean_folder(file_path):
    folders = os.path.exists(file_path)
    if not folders:
        os.makedirs(file_path)
    else:
        shutil.rmtree(file_path)
        os.makedirs(file_path)
        
def mkdir_multi(path):
    # 判断路径是否存在
    isExists=os.path.exists(path)
    if not isExists:
        # 如果不存在，则创建目录（多层）
        os.makedirs(path) 
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

# 加载pickle文件
def load_pickle(pickle_path):
    with open(pickle_path, "rb") as file:
        result = pickle.load(file)
    return result

# 提取某种类型的数据
def extract_node_in_type(id_name_dict, node_type, save_path):
    node_dict = {}
    for item in id_name_dict:
        this_node_type = item.split("_")[-1]
        if this_node_type == node_type:
            # node_dict[item]  = id_name_dict[item]
            node_dict[item] = id_name_dict[item]
    save_dict_to_local(node_dict, save_path, node_type)
    return 0

# 提取某种类型的数据
def extract_node_in_type_with_total_dict(id_name_dict, node_type, save_path):
    node_dict = {}
    for item in id_name_dict:
        this_node_type = item.split("_")[-1]
        if this_node_type == node_type:
            node_dict[item] = id_name_dict[item]
    save_dict_to_local(node_dict, save_path, node_type)
    return 0

# 提取所有类型的节点
def extract_all_type_node(save_path, dict):
    try:
        os.mkdir(save_path + "/types/")
    except:
        pass
    # 提取各种类型的节点
    node_type_list = ["subject", "principal", "netflow", "file", "srcsink", "unnamedpipe", "memory"]
    for node_type in node_type_list:
        node_type_save_path = save_path + "/types/"
        extract_node_in_type(dict, node_type, node_type_save_path)