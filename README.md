# Bot para discord utilizando NLP
Bot para discord desenvolvido como APS da disciplina de natural language processing.

## Ensaios - Textos curtos explicando o processo de desenvolvimento para cada iteração do chatbot.
- [Ensaio 0](https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot/blob/main/ensaios/ensaio_0.md) - Iniciando o esqueleto do bot!
- [Ensaio 1](https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot/blob/main/ensaios/ensaio_1.md) - Adicionando comando !run para mandar informações sobre cryptomoedas para o usuário.
- [Ensaio 2](https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot/blob/main/ensaios/ensaio_2.md) - Adicionando webcrawling e funcões de busca.
- [Ensaio 3](https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot/blob/main/ensaios/ensaio_3.md) - Filtro por negatividade das páginas baixadas.
- [Ensaio 4](https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot/blob/main/ensaios/ensaio_4.md) - Geração de conteúdo a partir do banco de dados.

## Como rodar local
1. Clone o repositório com o seguinte comando:
```sh 
git clone https://github.com/RicardoRibeiroRodrigues/NLP-DiscordBot
```
2. Baixe as dependências do bot:
```sh 
pip install -r requirements.txt
```
3. Coloque o token do bot e [chave da API da coincap](https://coincap.io/api-key) em um arquivo .env no seguinte formato:
```.env
export TOKEN=token_do_bot_aqui
export API_KEY=api_key_aqui
```
4. Rode o script de start up (esse script vai baixar a wordnet)
```sh
python3 manager_scripy.py setup
```
5. Rode o bot com o seguinte comando:
```sh 
python3 main.py
```

```OBS: O [manager_script.py] tem uma função de cleanup para limpar os arquivos de dados em testes locais do bot.```

## Autor:
- [Ricardo Ribeiro Rodrigues](https://github.com/RicardoRibeiroRodrigues) - ricardorr7@al.insper.edu.br
