from keras.layers import (
    Input,
    Dense,
    Activation,
    MultiHeadAttention,
    Softmax,
    TextVectorization,
    Embedding,
    GlobalAveragePooling1D,
    LSTM,
)
import os
from keras.models import Model, load_model
import keras
import numpy as np
import tensorflow as tf


class ContentGenerator:

    def __init__(self, vocab_size=5_000, n_grams=10, n_training_epochs=2) -> None:
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
        The y is last token of x.
        x is output of vectorization - last token.
        """
        x_ = self.vectorize_layer(x)
        y_ = x_[:,-1:]
        x_ = x_[:, :-1]
        return x_, y_

    def adapt_vectorization(self, dataset):
        self.vectorize_layer.adapt(dataset)
    
    def train(self, dataset):
        x, y = self.get_last_token(dataset)
        self.predictor.fit(x, y, epochs=self.n_training_epochs)
        self.predictor.save("models/CONTENT_GENERATOR")
    
    def predict(self, x: str):
        return self.predictor.predict(self.vectorize_layer([x])[:,:-1])

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
        count = 0
        while count < n_predictions:
            pred = self.predict(context)

            # Don't repeat words
            try:
                while True:
                    # Select k-best
                    k_best_predictions = tf.math.top_k(pred, k=10).indices[0,:]
                    idx = np.random.choice(k_best_predictions.numpy())
                    print(idx)

                    word = vocabulary[idx]
                    if word in phrase:
                        pred[0][idx] = 0
                    else:
                        break
            except IndexError as e:
                print(f"IDX: {idx} has caused error, ")
                print(e)
                continue
                    
            phrase.append(word)
            context = f"{context} {word}"
            context = ' '.join(context.split()[1:])
            count += 1
            print(word)
        return " ".join(phrase)

