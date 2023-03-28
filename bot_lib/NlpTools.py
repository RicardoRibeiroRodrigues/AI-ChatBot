import re
import os
import json
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class NlpTools:
    TOKEN_REGEX = r"(?u)\b\w\w+\b"
    INDEX_PATH = "data/index.json"

    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer()
        self.tfidf = None

        if os.path.exists(self.INDEX_PATH):
            print("[INFO] Loading index...")
            self.load_index()
        else:
            self.index = {"[__CURR_ID__]": 0}

    def get_inc_curr_id(self) -> int:
        curr_id = self.index["[__CURR_ID__]"]
        self.index["[__CURR_ID__]"] += 1
        return curr_id

    def load_index(self) -> None:
        with open(self.INDEX_PATH, "r") as f:
            self.index = json.load(f)

    def add_document(self, text: str) -> None:
        tokens = self.tokenize(text)
        doc_id = self.get_inc_curr_id()

        for token in tokens:
            term_f = self.vectorizer.vocabulary_[token]
            if token not in self.index:
                self.index[token] = {}
            if doc_id not in self.index[token]:
                self.index[token][doc_id] = self.tfidf[doc_id, term_f]
        
        self.save_index()
        return doc_id

    def tokenize(self, text: str) -> list[str]:
        return re.findall(self.TOKEN_REGEX, text.lower())

    def save_index(self) -> None:
        with open(self.INDEX_PATH, "w") as f:
            json.dump(self.index, f)

    def search(self, query: str) -> list[int]:
        """
        Using OR aproach (sum of tfidfs)
        """
        tokens = self.tokenize(query)
        ret = dict()

        for token in tokens:
            if token in self.index:
                for doc in self.index[token]:
                    if doc in ret:
                        ret[doc] += self.index[token][doc]
                    else:
                        ret[doc] = self.index[token][doc]
        return ret 

    def wn_search(self, search_word: str) -> tuple[str, dict]:
        search_word_syn = wordnet.synsets(search_word)
        if not search_word_syn:
            return None, None
        
        search_word_syn = search_word_syn[0]
        biggest_similarity = 0
        best_match = None
        for word in self.index:
            word_syn = wordnet.synsets(word)
            if not word_syn:
                continue

            word_syn = word_syn[0]
            if word_syn.wup_similarity(search_word_syn) > biggest_similarity:
                biggest_similarity = word_syn.wup_similarity(search_word_syn)
                best_match = word
        
        return best_match, self.index[best_match]
    
    def fit_transform(self, docs: list[str]) -> None:
        self.tfidf = self.vectorizer.fit_transform(docs)


