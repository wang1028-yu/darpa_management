import csv,jieba
with open('data/cls/chn.csv') as f:
    reader=csv.reader(f)
    header = next(reader)  #表头
    data = [[int(row[0]),row[1]] for row in reader]  #每个元素是一个由字符串组成的列表，第一个元素是标签（01），第二个元素是评论文本。
    
tofiledir='data/cls'
with open(tofiledir+'/corpus.txt','w') as f:
    f.writelines([' '.join(jieba.cut(row[1]))+'\n' for row in data])
