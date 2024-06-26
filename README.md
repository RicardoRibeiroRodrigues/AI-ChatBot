# Discord ChatBot with Natural Language Processing and Crypto Data Features

This project creates a chatbot for Discord with multiple advanced features, integrating real-time cryptocurrency data and various Natural Language Processing (NLP) capabilities.

## Features

1. **Crypto Information Retrieval**:
   - `!run` command to provide users with real-time and historical cryptocurrency data.

2. **Web Crawling and Search**:
   - Implementation of web crawling capabilities to build a comprehensive database for information retrieval.

3. **Content Filtering**:
   - Development of a filtering mechanism to exclude negative content from the downloaded web pages using a trained Neural Network negativity classifier.

4. **Content Generation**:
   - Implementation of a neural network trained on the crawled data to generate content (GenAI).

5. **Advanced Content Generation**:
   - Enhanced content generation utilizing GPT-2 via HuggingFace transformers.

## DevLogs - Short texts explaining the development process for each of the feature iterations of the chatbot.

- [DevLog 0](devlogs/devlog_0.md) - Starting the bot structure!
- [DevLog 1](devlogs/devlog_1.md) - Adding the `!run` command to send crypto information to the user.
- [DevLog 2](devlogs/devlog_2.md) - Adding web crawling and search functions to the formed database.
- [DevLog 3](devlogs/devlog_3.md) - Filter by negativity on the content of downloaded pages.
- [DevLog 4](devlogs/devlog_4.md) - Content generation from the crawled database.
- [DevLog 5](devlogs/devlog_5.md) - Content generation with GPT (Gpt-2 using HuggingFace transformers)

## How to Run Locally

1. Clone the repository:
   ```sh 
   git clone https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot
   ```

2. Install the dependencies:
   ```sh 
   pip install -r requirements.txt
   ```

3. Add the bot's token and the CoinCap API token to a `.env` file in the following format:
   ```.env
   export TOKEN=bot_token_here
   export API_KEY=api_key_here
   ```

4. Run the setup script (this script will download WordNet):
   ```sh
   python3 manager_script.py setup
   ```

5. Run the bot:
   ```sh 
   python3 main.py
   ```

   ```PS: The file `manager_script.py` has a cleanup function to clean all generated data in `data/` and `models/`.```

## Author

- [Ricardo Ribeiro Rodrigues](https://github.com/RicardoRibeiroRodrigues) - ricardorr7@al.insper.edu.br
