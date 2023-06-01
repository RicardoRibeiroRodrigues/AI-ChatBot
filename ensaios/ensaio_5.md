# Ensaio da entrega da aps 5

Nessa etapa foi implementada a feature de geração de conteúdo "!gptgenerate" utilizando o GPT-2 treinado, baixado do huggingface. Não foi possível o uso da API do GPT da openAI, já que esta API se tornou paga recentemente, exigindo colocar o cartão de crédito para criar uma conta. 

No entanto, usar o GPT-2 localmente tem algumas desvantagens, como o fato que de só temos acesso ao GPT-2, ao invés do GPT-3 e GPT-4, que tiveram grandes saltos na performance do modelo, criando textos muito mais coesos, além de que a inferência em geral é mais rápida quando faz-se o uso da API, já que o modelo está rodando as inferências em hardware dedicado, e geralmente máquinas com maior poder computacional. Porém, mesmo com o GPT-2 sendo um tendo sua performance inferior aos outros GPTs, ele ainda aprensenta resultados melhores do que o modelo de linguagem treinado usado no '!generate', isso é esperado, já que o GPT foi treinado com muito mais dados, e trata-se de uma rede neural mais complexa.

Nessa etapa foi consultado principalmente a [documentação oficial do modelo GPT-2 no huggingface](https://huggingface.co/gpt2). A principal dificuldade nessa etapa foi acertar acertar o input das páginas dentro modelo, já que existem limites e um formato certo de os dados entrarem no modelo.
