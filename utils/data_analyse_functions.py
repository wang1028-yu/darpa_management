import re
from data_store_functions import *
import datetime
import ujson
import pickle
import time

def load_json(line):
    return ujson.loads(line)
    # return json.loads(line)

# 提取节点类型
def extract_nodetype(line):
    data = ujson.loads(line)
    type = list(data["datum"].keys())[0]
    return type

# 处理Subject类型数据
def parse_subject_data(line):
    data = line["com.bbn.tc.schema.avro.cdm18.Subject"]
    node_dict = dict()
    # 提取json中的详细信息
    node_dict["type"] = "subject"
    try:
        node_dict['uuid'] = data["uuid"]
    except:
        node_dict["uuid"] = "null"
    try:
        node_dict['name'] = data['properties']['map']['name']
    except:
        node_dict["name"] = "null"
    try:
        node_dict['timestamp'] = data['startTimestampNanos']
    except:
        node_dict['timestamp'] = "null"
    try:
        node_dict['cid'] = data['cid']
    except:
        node_dict["cid"] = "null"
    try:
        node_dict['ppid'] = data['properties']['map']['ppid']
    except:
        node_dict['ppid'] = "null"
    try:
        node_dict['cwd'] = data['properties']['map']['cwd']
    except:
        node_dict["cwd"] = "null"
    try:
        node_dict["cmdLine"] = data["cmdLine"]["string"]
        if node_dict["cmdLine"] == None:
            node_dict["cmdLine"] = "null"
    except:
        node_dict["cmdLine"] = "null" 
    return node_dict
    
# 处理principal类型数据
def parse_principal_data(line):
    data = line["com.bbn.tc.schema.avro.cdm18.Principal"]
    node_dict = dict()
    node_dict["type"] = "principal"
    # 提取json中的详细信息
    try:
        node_dict['uuid'] = data["uuid"]
    except:
        node_dict["uuid"] = "null"
    try:
        node_dict['userId'] = data['userId']
    except:
        node_dict['userId'] = "null"
    try:
        node_dict['timestamp'] = data['startTimestampNanos']
    except:
        node_dict['timestamp'] = "null"
    return node_dict

# 提取netflow信息
def parse_netflow_data(line):
    data = line["com.bbn.tc.schema.avro.cdm18.NetFlowObject"]
    node_dict = dict()
    node_dict["type"] = "netflow"
    # 提取json中的详细信息
    try:
        node_dict['uuid'] = data["uuid"]
    except:
        node_dict["uuid"] = "null"
    try:
        node_dict['localAddress'] = data['localAddress']
    except:
        node_dict['localAddress'] = "null"
    try:
        node_dict['localPort'] = data['localPort']
    except:
        node_dict['localPort'] = "null"
    try:
        node_dict['remoteAddress'] = data['remoteAddress']
    except:
        node_dict['remoteAddress'] = "null"
    try:
        node_dict['remotePort'] = data['remotePort']
    except:
        node_dict["remotePort"] = "null"
    try:
        if "int" in data["fileDescriptor"]:
            node_dict["file_desc"] = data["fileDescriptor"]["int"]
        else:
            node_dict["file_desc"] = data["fileDescriptor"]
    except:
        node_dict["file_desc"] = "null"
    return node_dict
    
# 提取UnitDependency
def parse_unitdependency_data(line):
    data = line["com.bbn.tc.schema.avro.cdm18.UnitDependency"]
    node_dict = dict()  
    node_dict["type"] = "unitdependency"
    # 提取json中的详细信息
    try:
        node_dict['unit'] = data["unit"]
    except:
        node_dict["unit"] = "null"
    try:
        node_dict['dependentUnit'] = data['dependentUnit']
    except:
        node_dict['dependentUnit'] = "null"
    return node_dict
    
# 提取FileObject
def parse_fileobject_data(line):
    data = line["com.bbn.tc.schema.avro.cdm18.FileObject"]
    node_dict = dict()  
    node_dict["type"] = "file"
    # 提取json中的详细信息
    try:
        node_dict['uuid'] = data["uuid"] 
    except:
        node_dict["uuid"] = "null"
    try:
        node_dict['path'] = data["baseObject"]['properties']['map']['path']
    except:
        node_dict["path"] = "null"
    try:
        if "int" in data["fileDescriptor"]:
            node_dict["file_desc"] = data["fileDescriptor"]["int"]
        else:
            node_dict["file_desc"] = data["fileDescriptor"]
    except:
        node_dict["file_desc"] = "null"
    return node_dict
    
# 提取SrcSinkObject
def parse_srcsinkobject_data(line):
    data = line["com.bbn.tc.schema.avro.cdm18.SrcSinkObject"]
    node_dict = dict()  
    node_dict["type"] = "srcsink"
    # 提取json中的详细信息
    try:
        node_dict['uuid'] = data["uuid"] 
    except:
        node_dict["uuid"] = "null"
    try:
        node_dict['base_pid'] = data['baseObject']['properties']['map']['pid']
    except:
        node_dict["base_pid"] = "null"
    try:
        if "int" in data["fileDescriptor"]:
            node_dict["file_desc"] = data["fileDescriptor"]["int"]
        else:
            node_dict["file_desc"] = data["fileDescriptor"]
    except:
        node_dict["file_desc"] = "null"
    return node_dict

# 提取UnnamedPipeObject
def parse_unnamedpipeobject_data(line):
    data = line["com.bbn.tc.schema.avro.cdm18.UnnamedPipeObject"]
    node_dict = dict()  
    node_dict["type"] = "unnamedpipe"
    # 提取json中的详细信息
    try:
        node_dict['uuid'] = data["uuid"]
    except:
        node_dict["uuid"] = "null"
    try:
        node_dict['pid'] = data["baseObject"]['properties']['map']['pid']
    except:
        node_dict["pid"] = "null"
    try:
        node_dict["source_file"] = data["sourceFileDescripto"]["int"]
    except:
        node_dict["source_file"] = "null"
    try:
        node_dict["sink_file"] = data["sinkFileDescripto"]["int"]
    except:
        node_dict["sink_file"] = "null"
    return node_dict

# 提取MemoryObject
def parse_memoryobject_data(line):
    data = line["com.bbn.tc.schema.avro.cdm18.MemoryObject"]
    node_dict = dict()
    node_dict["type"] = "memory"
    try:
        node_dict['uuid'] = data["uuid"]
    except:
        node_dict["uuid"] = "null"
    try:
        node_dict['memoryAddress'] = data['memoryAddress']
    except:
        node_dict["memoryAddress"] = "null"
    return node_dict

# 处理event事件
def parse_event_data(line):
    data = line['com.bbn.tc.schema.avro.cdm18.Event']
    node_dict = dict()
    # 在溯源图中的方向是A指向B
    A_B_list = ["EVENT_WRITE", "EVENT_SENDMSG", "EVENT_MMAP", "EVENT_FORK", "EVENT_UNIT", "EVENT_CONNECT", "EVENT_CREATE_OBJECT", "EVENT_OPEN", "EVENT_EXECUTE", "EVENT_MPROTECT", "EVENT_EXIT", "EVENT_CLOSE", "EVENT_CHANGE_PRINCIPAL", "EVENT_CLONE", "EVENT_UNLINK", "EVENT_MODIFY_FILE_ATTRIBUTES", "EVENT_TRUNCATE", "EVENT_OTHER"]
    # 在溯源图中的方向是B指向A
    B_A_list = ["EVENT_RECVMSG", "EVENT_READ", "EVENT_LOADLIBRARY", "EVENT_ACCEPT"]
    # 自己对自己操作，有两个object
    triple_list = ["EVENT_RENAME", "EVENT_LINK", "EVENT_UPDATE"]
    try:
        node_dict["type"] = data["type"]
    except:
        node_dict["type"] = "null"
        
    if node_dict["type"] in triple_list:
        try:
            node_dict["subject"] = data["subject"]["com.bbn.tc.schema.avro.cdm18.UUID"]
        except:
            node_dict["subject"] = "null"
        try:
            node_dict["predicateObject"] = data["predicateObject"]["com.bbn.tc.schema.avro.cdm18.UUID"]
        except:
            node_dict["predicateObject"] = "null"
        try:
            node_dict["timestamp"] = data["timestampNanos"]
        except:
            node_dict["timestampNanos"] = "null"
        try:
            node_dict["predicateObject2"] = data["predicateObject2"]["com.bbn.tc.schema.avro.cdm18.UUID"]
        except:
            node_dict["predicateObject2"] = "null"
        node_dict["sub"] = node_dict["predicateObject"]
        node_dict["obj"] = node_dict["predicateObject2"]
    else:
        try:
            node_dict["subject"] = data["subject"]["com.bbn.tc.schema.avro.cdm18.UUID"]
        except:
            node_dict["subject"] = "null"
        try:
            node_dict["predicateObject"] = data["predicateObject"]["com.bbn.tc.schema.avro.cdm18.UUID"]
        except:
            node_dict["predicateObject"] = "null"
        try:
            node_dict["timestamp"] = data["timestampNanos"]
        except:
            node_dict["timestampNanos"] = "null"
        if node_dict["type"] in A_B_list:
            node_dict["sub"] = node_dict["subject"]
            node_dict["obj"] = node_dict["predicateObject"]
        elif node_dict["type"] in B_A_list:
            node_dict["sub"] = node_dict["predicateObject"]
            node_dict["obj"] = node_dict["subject"]  
    return node_dict


# 深度优先搜索
# 输入：进程节点， 邻接列表字典
def dfs(node, adj_list_dict):
    # 深搜栈
    stack = []
    # 深搜结果
    result = []
    edges = adj_list_dict[node]
    for adj_edge in edges:
        stack.append(adj_edge)
        while len(stack) > 0:
            current_edge = stack.pop()
            current_node = int(current_edge["object"])
            current_time = int(current_edge["timestamp"])
            if current_node in adj_list_dict.keys():
                next_edges = adj_list_dict[current_node]
                for next_edge in next_edges:
                    next_time = int(next_edge["timestamp"])
                    if next_time > current_time:
                        stack.append(next_edge)
            result.append(current_edge)
    return result

# 找到文件的最小时间和最大时间
def extract_time(file_path):
    time_set = set()
    for line in open(file_path, "r"):
        time = int(line.split("\t")[-1]) / 1000000000
        time_set.add(time)
    time_list = list(time_set)
    return timestamp_to_date(min(time_list)), timestamp_to_date(max(time_list))

# 时间戳转日期
def timestamp_to_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

def date_to_timestamp(date):
    time_array = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    return time.mktime(time_array)

# 节点去重
def node_distinct(node_path):
    with open(node_path, "rb") as file:
        node_list = pickle.load(file)
        print(len(node_list))
        distinct_set = set()
        for item in node_list:
            distinct_set.add(node_list[item])
        print(len(distinct_set))
        
# 生成邻接表字典
def generate_adj_list_dict(file_path):
    adj_list_dict = dict()
    with open(file_path, "r") as file:
        for line in file:
            details = line.split("\t")
            contain_none = any(item == "None" for item in details)
            if contain_none:
                continue
            subject = int(details[0])
            object = int(details[1])
            relation = int(details[2])
            # subject_node = details[4]
            # if "file" in subject_node:
            #     print(line)
            timestamp = int(details[-1].replace("\n", ""))
            object_dict = {"relation":relation, "object":object, "timestamp":timestamp}
            if subject in adj_list_dict:
                adj_list_dict[subject].append(object_dict)
            else:
                adj_list_dict[subject] = []
                adj_list_dict[subject].append(object_dict)
    return adj_list_dict

def generate_ancestor_list():
    pass