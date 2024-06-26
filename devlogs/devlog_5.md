## DevLog 5 - Content generation with GPT (GPT-2 using HuggingFace transformers)

In this stage, the `!gptgenerate` feature was implemented using a pre-trained GPT-2 model downloaded from HuggingFace.

However, using GPT-2 locally has some disadvantages, such as only having access to GPT-2 instead of GPT-3 and GPT-4, which have seen significant performance improvements and create much more cohesive texts. Additionally, inference is generally faster when using the GPT-3 API, as the model runs on dedicated hardware with typically higher computational power. Nonetheless, even though GPT-2 has inferior performance compared to newer GPT models, it still produces better results than the custom-trained language model used in the `!generate` command. This is expected since GPT has been trained on much more data and is a more complex model.

In this stage, the [official GPT-2 documentation on HuggingFace](https://huggingface.co/gpt2) was the primary source of reference. The main difficulty was correctly formatting the input pages for the model, as there are limits and specific formats required for the data to be input into the model.