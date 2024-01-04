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