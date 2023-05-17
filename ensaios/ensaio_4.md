# Ensaio da entrega da aps 4

O objetivo dessa entrega era adicionar uma funcionalidade '!generate' para utilizar os conteúdos do banco de dados para gerar novo conteúdo usando um modelo de linguagem. Essa funcionalidade é particularmente interessante por conta de trazer um tópico muito atual: os modelos de linguagem para geração de conteúdo, com a popularização do GPT e o avanço de outras tecnologias parecidas, esse tópico se torna muito relevante.

A solução adotada foi simplesmente treinar um modelo de linguagem simples a cada comando "!crawl", e salvar o modelo sempre que for treinado. A geração de conteúdo usa o método do top_k para busca das palavras para geração, e foram feitos métodos para impedir repetição de palavras.

As maiores dificuldades nessa etapa foram com bugs no algoritmo de fazer a geração de conteúdo, e na hora de montar, compilar e treinar a rede neural e a camada de vetorização. A principal fonte de consulta foram os materiais de aula e a [documentação do tensorflow](https://www.tensorflow.org/api_docs/python/tf/all_symbols).
