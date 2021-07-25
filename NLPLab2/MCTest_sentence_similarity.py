# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/11 10:52
# @Author  : chengp
# @File    : sentence_similarity.py
# @Funtionality

" a class for calculating sentence similarity"

import nltk
import numpy as np
from gensim import corpora, models, similarities
from collections import defaultdict

class SentenceSimilarity():
    def __init__(self, seg):
        self.seg = seg

    def set_sentences(self, sentences):
        self.sentences = sentences



    # obtain tokenized sentences
    def get_cuted_sentences(self):
        cuted_sentences = []


        for sentence in self.sentences:
            cuted_sentences.append(nltk.word_tokenize(sentence))
        return cuted_sentences

    # for high-level complicated model
    def simple_model(self, min_frequency=0):
        self.texts = self.get_cuted_sentences()

    # remove low-frequent words
        frequency = defaultdict(int)
        for text in self.texts:
            for token in text:
                frequency[token] += 1
        self.texts = [[token for token in text if frequency[token] > min_frequency]
                      for text in self.texts]
        self.dictionary = corpora.Dictionary(self.texts)
        self.corpus_simple = [self.dictionary.doc2bow(text) for text in self.texts]

    # tfidf
    def TfidfModel(self):
        self.simple_model(min_frequency=0)

    # transform model
        self.model = models.TfidfModel(self.corpus_simple)
        self.corpus = self.model[self.corpus_simple]
    # create similarity matrix
        self.index = similarities.MatrixSimilarity(self.corpus)

    # lsi
    def LsiModel(self):
        self.simple_model()

    # transform model
        self.model = models.LsiModel(self.corpus_simple)
        self.corpus = self.model[self.corpus_simple]
    # create similarity matrix
        self.index = similarities.MatrixSimilarity(self.corpus)

    # lda
    def LdaModel(self):
        self.simple_model()

    # transform model
        self.model = models.LdaModel(self.corpus_simple)
        self.corpus = self.model[self.corpus_simple]
    # create similarity matrix
        self.index = similarities.MatrixSimilarity(self.corpus)

    # preprocessing new sentences
    def sentence2vec(self, sentence):

        vec_bow = self.dictionary.doc2bow(nltk.word_tokenize(sentence))

        return self.model[vec_bow]

    def bow2vec(self):
        vec = []

        length = max(self.dictionary) + 1
        for content in self.corpus:
            sentence_vectors = np.zeros(length)
        for co in content:
            sentence_vectors[co[0]] = co[1]
        vec.append(sentence_vectors)
        return vec

    # find the most similar sentences
    # input: test sentence
    def similarity(self, sentence):
        sentence_vec = self.sentence2vec(sentence)

        sims = self.index[sentence_vec]
        sim = max(enumerate(sims), key=lambda item: item[1])
        index = sim[0]
        score = sim[1]
        res={}
        res['sent'] = self.sentences[index]
        res['score']=score
        return res

    def similarity_k(self, sentence, k):
        sentence_vec = self.sentence2vec(sentence)

        sims = self.index[sentence_vec]
        sim_k = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)[:k]
        indexs = [i[0] for i in sim_k]
        scores = [i[1] for i in sim_k]
        return indexs, scores