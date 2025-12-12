import numpy as np
import pandas as pd
from math import log
from tqdm import tqdm

class SearchEngine:

    def __init__(self, corpus, mode="tfidf"):
        self.corpus = corpus
        self.mode = mode

        self.corpus.nettoyer_texte()
        self.corpus.build_vocab()
         
        if mode == "tfidf":
            self.matrix = self.build_tfidf_matrix()
        else:
            self.matrix = self.corpus.build_tf_matrix()

    def build_tfidf_matrix(self):
        tf = self.corpus.build_tf_matrix()
        df = self.corpus.document_frequency()["document_frequency"].to_dict()
        N = len(self.corpus.id2doc)

        idf = np.array([log(N / (df[word] + 1)) for word in self.corpus.vocab])
        return tf * idf


    def cosine(self, a, b):
        return np.dot(a, b) / (
            np.linalg.norm(a) * np.linalg.norm(b) + 1e-10
            )


    def search(self, query, top=10):
        query = query.lower().split()

        query_vec = np.zeros(len(self.corpus.vocab))
        for w in query:
            if w in self.corpus.vocab:
                query_vec[self.corpus.vocab.index(w)] += 1

        scores = []
        for i, (doc_id, doc) in tqdm(enumerate(self.corpus.id2doc.items()), total=len(self.corpus.id2doc)):
            score = self.cosine(query_vec, self.matrix[i])
            scores.append((doc_id, doc.titre, score))

        df = pd.DataFrame(scores, columns=["id", "titre", "score"])
        return df.sort_values(by="score", ascending=False).head(top)
