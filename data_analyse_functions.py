import re
from data_store_functions import *
import datetime
import ujson
import json

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
    # node_dict = {}
    # res = re.findall(
    #     'NetFlowObject":{"uuid":"(.*?)"(.*?)"localAddress":"(.*?)","localPort":(.*?),"remoteAddress":"(.*?)","remotePort":(.*?),',
    #     line)[0]
    # node_dict["type"] = "netflow"
    # node_dict["uuid"] = res[0]   
    # node_dict["localAddress"] = res[2]
    # node_dict['localPort'] = res[3]
    # node_dict['remoteAddress'] = res[4]
    # node_dict["remotePort"]  = res[5]
    # return node_dict
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
        node_dict["type"] = data["type"]
    except:
        node_dict["type"] = "null"
    return node_dict

# 提取某种类型的数据
def extract_node_in_type(id_name_dict, node_type, save_path):
    node_dict = {}
    for item in id_name_dict:
        this_node_type = id_name_dict[item].split("_")[-1]
        if this_node_type == node_type:
            node_dict[item]  = id_name_dict[item]
    save_dict_to_local(node_dict, save_path, node_type)
    return 0

# 深度优先搜索
def dfs():
    pass

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