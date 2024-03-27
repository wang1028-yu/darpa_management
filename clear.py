from utils.data_store_functions import *
from config import *
if __name__ =="__main__":
    # for i in range(526):
    for i in range(211):
        file_name = "ta1-trace-e3-official.json.%s"%(i)
        file_path = "./result/splited_result/" + file_name
        # file_path = "./interim_folder/result/splited_result/%s.json"%(i)
        # clean_folder(file_path)
        # os.remove(file_path)
        # shutil.rmtree(file_path)
        # print(file_path)
        # shutil.move(file_path, "./result/splited_result/%s.json"%(i))
        shutil.move(file_path, "./interim_folder/" + file_name)