import re
import os
import json
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
import tensorflow as tf
from bot_lib.ContentGenerator import ContentGenerator


class NlpTools:
    TOKEN_REGEX = r"(?u)\b\w\w+\b"
    INDEX_PATH = "data/index.json"

    def __init__(self, scrapper_ref) -> None:
        self.vectorizer = TfidfVectorizer()
        self.tfidf = None
        self.content_generator = ContentGenerator()
        self.scrapper_ref = scrapper_ref

        if os.path.exists(self.INDEX_PATH):
            print("[INFO] Loading index...")
            self.load_index()
            self.content_generator.adapt_vectorization(self.scrapper_ref.contents)
        else:
            self.index = {"[__CURR_ID__]": 0}

        print("[INFO] Loading classifier...")
        self.classifier = tf.keras.models.load_model("models/CLASS_MODEL")
        print("[INFO] Done initializing NlpTools.")

    def get_inc_curr_id(self) -> int:
        curr_id = self.index["[__CURR_ID__]"]
        self.index["[__CURR_ID__]"] += 1
        return curr_id

    def load_index(self) -> None:
        with open(self.INDEX_PATH, "r") as f:
            self.index = json.load(f)

    def add_document(self, text: str, negative_amount: float) -> None:
        tokens = self.tokenize(text)
        doc_id = self.get_inc_curr_id()

        for token in tokens:
            term_f = self.vectorizer.vocabulary_[token]
            if token not in self.index:
                self.index[token] = {}
            if doc_id not in self.index[token]:
                self.index[token][doc_id] = [
                    self.tfidf[doc_id, term_f],
                    negative_amount,
                ]

        self.save_index()
        return doc_id

    def tokenize(self, text: str) -> list:
        return re.findall(self.TOKEN_REGEX, text.lower())

    def save_index(self) -> None:
        with open(self.INDEX_PATH, "w") as f:
            json.dump(self.index, f)

    def search(self, query: str) -> dict:
        """
        Using OR aproach (sum of tfidfs)

        returns:
            dict: {doc_id: [tfidf_sum, negative_amount]}
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

    def wn_search(self, search_word: str) -> tuple:
        """
        Using WordNet to find the best match for the search_word

        returns:
            tuple: (best_match, [tfidf_sum, negative_amount])
        """
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
        if not best_match:
            return None, None

        return best_match, self.index[best_match]

    def fit_transform(self) -> None:
        print("[INFO] Fitting and transforming vectorizer...")
        self.tfidf = self.vectorizer.fit_transform(self.scrapper_ref.contents)
        print("[INFO] Fitting and transforming vectrorization...")
        self.content_generator.adapt_vectorization(self.scrapper_ref.contents)
        print("[INFO] Training content generator...")
        self.content_generator.train(self.scrapper_ref.contents)

    def _convert_scale(self, value: float) -> float:
        return 1 - (value * 2)

    def get_negative_amount_texts(self, texts: list) -> list:
        classification = self.classifier.predict(texts)
        # The classifier returns a confidence that goes from 0 to 1, but we need it -1 to 1
        # Using the value[1] because the value[0] is the positive confidence, and we need the negative one
        classification = [self._convert_scale(value[1]) for value in classification]
        return classification
    
    def generate_text(self, query: str, model: str) -> str:
        docs = self.search(query)
        if not docs:
            docs = self.wn_search(query)
            docs = docs[1]
            print(docs)
            if docs is None:
                return None
    
        docs = max(docs, key=lambda x: docs[x][0])
        if model == 'inhouse':
            content = self.scrapper_ref.contents[int(docs)]
            processed_string = re.sub(r'\s+', ' ', content)
            res = self.content_generator.generate_content(processed_string)
        elif model == 'gpt':
            content = self.scrapper_ref.contents[int(docs)]
            processed_string = re.sub(r'\s+', ' ', content)
            res = self.content_generator.gpt_generate(processed_string)
        return res
    