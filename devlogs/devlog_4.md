## DevLog 4 - Content generation from the crawled database

The goal of this delivery was to add a `!generate` functionality to use the content from the database to generate new content using a language model. This feature is particularly interesting as it brings in a very current topic: language models for content generation. With the popularization of GPT and the advancement of similar technologies, this topic has become highly relevant.

The adopted solution was to train a simple language model at each `!crawl` command and save the model whenever it is trained. Content generation uses the top_k method for word search during generation, and methods were created to prevent word repetition.

The biggest challenges in this stage were dealing with bugs in the content generation algorithm and assembling, compiling, and training the neural network and the vectorization layer. The main sources of reference were class materials and the [TensorFlow documentation](https://www.tensorflow.org/api_docs/python/tf/all_symbols).