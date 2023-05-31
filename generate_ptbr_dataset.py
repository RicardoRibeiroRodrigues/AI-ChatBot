from translate import Translator
import concurrent.futures

# create a translator object
translator = Translator(to_lang="pt")


def traduzir_palavras(palavras):
    translator = Translator(to_lang="pt")
    resultados = []
    for palavra in palavras:
        resultado = translator.translate(palavra)
        print(resultado)
        resultados.append(resultado)
    return resultados


n_threads = 30

# Translate a sentence from English to Portuguese
# https://www.kaggle.com/datasets/nicapotato/bad-bad-words
with open("data/bad-words.csv", "r") as f:
    lines = f.readlines()

tamanho_parte = (len(lines) // n_threads) + 1
partes = [lines[i : i + tamanho_parte] for i in range(0, len(lines), tamanho_parte)]

# executando a tradução em paralelo
with concurrent.futures.ThreadPoolExecutor() as executor:
    resultados = executor.map(traduzir_palavras, partes)

# juntando os resultados
palavras_traduzidas = []
for resultado in resultados:
    palavras_traduzidas += resultado

english_words = set(map(lambda x: x.strip().replace("\n", ""), lines))

with open("data/bad-words-ptbr.csv", "w") as f:
    for word in palavras_traduzidas:
        word = word.strip().replace("\n", "")

        if word not in english_words and word != "-" and word != "":
            f.write(word + "\n")
