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

结果存放在result中，其中splited_result是分开对每个文件进行处理，total_result是所有数据汇总的字典

使用方法
1. 运行data_preprocess.py 预处理单个文件的数据
2. 运行merge.py 整合所有文件的处理数据

config.py配置模型参数