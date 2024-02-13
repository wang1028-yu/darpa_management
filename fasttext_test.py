import os
import gensim
import collections

corpus_path = "./data/cls/corpus.txt"
corpus_path2 = "./data/cls/corpus2.txt"
def read_corpus(file_name, tokens_noly = False):
    with open(file_name, "r") as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_noly:
                yield tokens
            else:
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])

# 构造特征的函数
if __name__ == "__main__":
    data_set1 = list(read_corpus(corpus_path))
    data_set2 = list(read_corpus(corpus_path2))
    data_sets = [data_set1, data_set2]
    for data_set in data_sets:
        data_length = len(data_set)
        train_length = int(0.8 * data_length)
        train_corpus = data_set[:train_length]
        test_corpus = data_set[train_length:]
        model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count = 2, epochs= 100)
        model.build_vocab(train_corpus)
        model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
        doc = data_set[0][0]
        print(doc)
        print(model.dv[0])
    