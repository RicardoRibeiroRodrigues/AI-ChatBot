from keras.layers import (
    Input,
    Dense,
    MultiHeadAttention,
    Softmax,
    TextVectorization,
    Embedding,
    LSTM,
)
from transformers import pipeline, set_seed
import os
from keras.models import Model, load_model
import keras
import numpy as np
import tensorflow as tf

N_NOT_REPEATED_TRIALS = 50


class ContentGenerator:
    def __init__(self, vocab_size=5_000, n_grams=10, n_training_epochs=20) -> None:
        self.vocab_size = vocab_size
        self.vectorize_layer = TextVectorization(
            max_tokens=vocab_size, output_sequence_length=n_grams
        )
        self.n_training_epochs = n_training_epochs

        if os.path.exists("models/CONTENT_GENERATOR"):
            print("[INFO] Loading content generator...")
            self.predictor = load_model("models/CONTENT_GENERATOR")
        else:
            self.build_model()

        set_seed(42)
        self.gpt_generator = pipeline("text-generation", model="gpt2")

    def build_model(self):
        self.predictor, latent = self._predict_word_model(10, 15, self.vocab_size)
        opt = keras.optimizers.Nadam(learning_rate=0.1)
        loss_fn = keras.losses.SparseCategoricalCrossentropy(
            ignore_class=1,
            name="sparse_categorical_crossentropy",
        )
        self.predictor.compile(loss=loss_fn, optimizer=opt, metrics=["accuracy"])
        print(self.predictor.summary())

    def get_last_token(self, x):
        """
        Function to map the dataset to (x, y) pairs.

        Y is last token of X.
        X is output of vectorization minus the last token.
        """
        vectorized = self.vectorize_layer(x)
        x_ = vectorized[:, :-1]
        y_ = vectorized[:, -1:]
        return x_, y_

    def adapt_vectorization(self, dataset):
        self.vectorize_layer.adapt(dataset)

    def train(self, dataset):
        train_dataset = tf.data.Dataset.from_tensor_slices(dataset).batch(64)
        train_dataset = train_dataset.map(self.get_last_token)

        self.predictor.fit(train_dataset, epochs=self.n_training_epochs)
        self.predictor.save("models/CONTENT_GENERATOR")

    def predict(self, x: str):
        return self.predictor.predict(self.vectorize_layer([x])[:, 1:])

    def _predict_word_model(self, seq_len, latent_dim, vocab_size):
        input_layer = Input(shape=(seq_len - 1,))
        x = input_layer
        x = Embedding(vocab_size, latent_dim, name="embedding", mask_zero=True)(x)
        x = MultiHeadAttention(num_heads=3, key_dim=2)(x, value=x)
        x = LSTM(latent_dim, kernel_initializer="glorot_uniform")(x)
        latent_rep = x
        x = Dense(vocab_size)(x)
        x = Softmax()(x)
        return Model(input_layer, x), Model(input_layer, latent_rep)

    def generate_content(self, pages, n_predictions=20):
        phrase = []
        # Sliding context
        context = pages
        vocabulary = self.vectorize_layer.get_vocabulary()
        for _ in range(n_predictions):
            pred = self.predict(context)
            word = ""
            for _ in range(N_NOT_REPEATED_TRIALS):
                # Select k-best (10)
                k_best_predictions = tf.math.top_k(pred, k=10).indices[0, :]
                top_idxs = k_best_predictions.numpy()
                idx = np.random.choice(top_idxs)

                if idx > len(vocabulary) - 1:
                    pred[0][idx] = 0
                    continue

                word = vocabulary[idx]
                if word not in phrase:
                    break
                pred[0][idx] = 0

            phrase.append(word)
            context = context.split()[1:]
            context.append(word)
            context = " ".join(context)
        return " ".join(phrase)

    def gpt_generate(self, page):
        prompt = f"Generate a content for this page: \n" + page[:500]
        res = self.gpt_generator(prompt, max_new_tokens=50)
        # Returns only the generated text, without the prompt
        return "\n".join(res[0]["generated_text"].split("\n")[1:])
