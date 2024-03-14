节点类型
'com.bbn.tc.schema.avro.cdm18.Subject'
'com.bbn.tc.schema.avro.cdm18.Principal'
'com.bbn.tc.schema.avro.cdm18.NetFlowObject'
'com.bbn.tc.schema.avro.cdm18.UnitDependency'
'com.bbn.tc.schema.avro.cdm18.FileObject'
'com.bbn.tc.schema.avro.cdm18.SrcSinkObject'
'com.bbn.tc.schema.avro.cdm18.UnnamedPipeObject'
'com.bbn.tc.schema.avro.cdm18.Event'
'com.bbn.tc.schema.avro.cdm18.MemoryObject'

边的类型
EVENT_WRITE	process --> file
EVENT_RECVMSG	netflow --> process
EVENT_SENDMSG	process --> netflow
EVENT_READ	file --> process
EVENT_MMAP	process --> memory
EVENT_LOADLIBRARY	file --> process
EVENT_FORK	process --> process
EVENT_UNIT	创建 process --> process
EVENT_CONNECT	process --> others
EVENT_CREATE_OBJECT	 process --> file
EVENT_RENAME	file --> file
EVENT_OPEN	process --> file
EVENT_EXECUTE	process --> process
EVENT_MPROTECT	修改内存 process --> memory
EVENT_EXIT	退出 process --> process
EVENT_CLOSE	process --> file
EVENT_CHANGE_PRINCIPAL  process --> process
EVENT_CLONE	process --> process
EVENT_UNLINK	process --> file
EVENT_ACCEPT	others --> process 
EVENT_MODIFY_FILE_ATTRIBUTES	process --> file
EVENT_TRUNCATE	process --> file
EVENT_LINK	 //// object 和 object2 同一种类型结构都不同我也是服了  file --> file
EVENT_UPDATE	file --> file
EVENT_OTHER	A --> B


结果存放在result中，其中splited_result是分开对每个文件进行处理，total_result是所有数据汇总的字典

使用方法
1. 运行data_preprocess.py 预处理单个文件的数据
2. 运行merge.py 整合所有文件的处理数据

config.py配置模型参数


start_time	2018-04-10 14:28:57
end_time	2018-04-10 16:23:18


tart_time	2018-04-13 16:21:16
end_time	2018-04-13 17:21:58

start_time	2018-04-13 17:21:58
end_time	2018-04-13 18:47:44