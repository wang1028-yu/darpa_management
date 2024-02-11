import os
import gensim
import collections

corpus_path = "./data/cls/corpus.txt"
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
    data_set = list(read_corpus(corpus_path))
    data_length = len(data_set)
    train_length = int(0.8 * data_length)
    train_corpus = data_set[:train_length]
    test_corpus = data_set[train_length:]
    model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count = 2, epochs= 100)
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    ranks = []
    second_ranks = []
    for doc_id in range(len(train_corpus)):
        inferred_vector = model.infer_vector(train_corpus[doc_id].words)
        sims = model.dv.most_similar([inferred_vector], topn=len(model.dv))
        rank = [docid for docid, sim in sims].index(doc_id)
        ranks.append(rank)
        second_ranks.append(sims[1])
    counter = collections.Counter(ranks)
    print(counter)
    print('Document ({}): «{}»\n'.format(doc_id, ' '.join(train_corpus[doc_id].words)))
    print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    for label, index in [('MOST', 0), ('SECOND-MOST', 1), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
        print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))
    