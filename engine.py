# -*- coding: utf-8 -*-
import nltk
import gensim
import numpy as np
from scipy import spatial


class XReadingAI(object):
    def __init__(self, model_file):
        self.model = gensim.models.Doc2Vec.load(model_file)

    def similar_words(self, word):
        # -----*----- 類似単語の取得 -----*-----
        try:
            print(self.model.most_similar(word))
        except:
            pass

    def sentence_similarity(self, *sentences):
        # -----*----- 2文の類似度を算出 -----*-----
        num_features = 300
        sentence_1_avg_vector = self.avg_feature_vector(sentences[0], num_features)
        sentence_2_avg_vector = self.avg_feature_vector(sentences[1], num_features)
        # １からベクトル間の距離を引いてあげることで、コサイン類似度を計算
        with np.errstate(invalid='ignore'):
            return 1 - spatial.distance.cosine(sentence_1_avg_vector, sentence_2_avg_vector)

    def avg_feature_vector(self, sentence, num_features):
        # -----*----- 文中の単語の特徴ベクトルの平均を算出 -----*-----
        words = nltk.word_tokenize(sentence)
        # 特徴ベクトルの入れ物を初期化
        feature_vec = np.zeros(num_features, dtype="float32")

        for word in words:
            try:
                feature_vec = np.add(feature_vec, self.model[word])
            except:
                pass
        if len(words) > 0:
            feature_vec = np.divide(feature_vec, len(words))

        return feature_vec
