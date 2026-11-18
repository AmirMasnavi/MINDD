# Guião da apresentação do Projeto 1 (MINDD 2026/27)

Slides: `docs/MINDD_TP1_Presentation.pptx` (12 slides, cerca de 13 min mais perguntas). Versão em inglês:
`docs/PRESENTATION_SCRIPT.md`, com os mesmos slides, tempos e números. Os slides estão em inglês e o Amir não fala
português, por isso a apresentação é feita em inglês. Esta versão serve para perceber bem o que se diz em cada slide.

## Quem apresenta o quê

| Quem | Slides | Tempo | Conteúdo | Commits que a justificam |
| --- | --- | --- | --- | --- |
| Amir | 1 a 4 | cerca de 4:00 | Introdução e Task 1: target, leakage, histórico do posto, divisão temporal | `724de72` setup do projeto, `4c97b8b` EDA da Task 1, `beb9039` versão mínima, `99cc6aa` secções 0 a 6 da Task 1 |
| Inês | 5 a 8 | cerca de 4:30 | Task 2: folds temporais, PR-AUC, baselines. Task 3: ablação, seis modelos | `eb92ca6` primeira versão da Task 2, `ede6a52` correções à Task 2, `cb75870` primeira versão da Task 3 |
| Manuela | 9 a 12 | cerca de 4:45 | Task 4: tuning, cut-off 0,490, congelar. Task 5: teste 0,532 contra 0,381. Conclusão | `14db8b2` Task 4 refeita e `task4_frozen.json`, `8c7e7ac` Task 5 integrada no relatório, todos os commits do relatório |

A Inês também escreveu a primeira versão dos notebooks da Task 4 (`ede6a52`) e da Task 5 (`c093d9f`) e as secções 7 a
10 da Task 1 (`defc15a`). O Amir também corrigiu a avaliação temporal e o pré-processamento da Task 3 (`a5be2d8`,
`aa17d1b`).

Há duas passagens de vez: o Amir termina o slide 4 com "Over to Inês" e a Inês termina o slide 8 com "Over to
Manuela".

---

## Amir: slides 1 a 4

### Slide 1. Sessões de carregamento anormais (cerca de 45 s)

Apresentar o grupo. O projeto pergunta se a informação disponível quando uma sessão de carregamento começa permite
prever que ela vai acabar de forma anormal. Seguimos as cinco tasks por ordem: dados, protocolo de avaliação, modelos,
otimização e teste final.

Frase opcional sobre quem fez o quê: "A Inês fez a primeira versão dos notebooks das Tasks 2 a 5, eu fiz a primeira
versão da Task 1 e a correção do protocolo na Task 3, e a Manuela integrou as tasks e escreveu o relatório."

### Slide 2. O problema e os dados (cerca de 1 min)

Temos 441 mil sessões em dois anos, em 92 postos. O ficheiro não tem a coluna is_Abnormal, por isso construímo-la a
partir da causa de fim. Quando o utilizador para a sessão, conta como normal, porque foi escolha dele. A prova de que a
definição está certa: as contagens de falhas anteriores que vêm com o dataset batem com as nossas em cerca de 100% das
linhas, contra menos de 36% com a definição alternativa. Só 18,6% das sessões são anormais, por isso um modelo que diz
sempre "normal" já acerta 81%, e a accuracy não é uma métrica útil.

### Slide 3. Só o que se sabe no início (cerca de 1 min 15 s)

A primeira regra do projeto: uma variável só pode ser preditor se for conhecida quando a sessão começa. A energia, os
custos e a duração separam muito bem as classes, mas descrevem o resultado; usá-los seria leakage. A melhor variável
legítima chega a 0,77. Reparámos também em dois detalhes. As taxas de falha fornecidas estão suavizadas: juntam uma
falha imaginária em cinco sessões imaginárias, por isso um posto sem histórico tem sempre 0,2, e uma falha numa sessão
dá 0,33 em vez de 1. Confirmámos a fórmula recalculando-a nas seis janelas. E 9.058 sessões normais não entregaram
energia; mantivemo-las, porque a energia só se sabe no fim.

### Slide 4. O histórico do posto é o sinal mais forte (cerca de 1 min)

Este gráfico é o resultado principal da exploração: quando a taxa de falha do posto a 7 dias é dividida em decis, a
percentagem de anormais sobe de 4% para 60%. O histórico do utilizador também ajuda, mas menos. Os dados não são
estáveis ao longo do tempo, por isso a divisão é cronológica. A Task 1 termina com 29 features candidatas em 7 grupos,
construídas a partir de 27 colunas; a Task 3 reduz para 27 features. Passo à Inês.

---

## Inês: slides 5 a 8

### Slide 5. Avaliar como no uso real (cerca de 1 min 15 s)

Antes de treinar qualquer modelo, fixámos como ia ser avaliado. Um K-fold aleatório misturava semanas de treino e de
validação e dava resultados otimistas, por isso usamos quatro folds de janela crescente: o treino cresce e valida sempre
no trimestre seguinte. Os primeiros três meses são um burn-in, porque as colunas de histórico ainda estão incompletas.
O último trimestre de 2021 é o teste e não serve para nenhuma escolha. A métrica principal é a PR-AUC, porque a classe
positiva é a minoritária. Não sabemos a razão de custos c, por isso o cut-off ótimo 1/(1+c) ainda não pode ser fixado;
em vez disso, mostramos orçamentos de alertas fixos.

### Slide 6. Primeiro, duas baselines (cerca de 1 min)

Definimos duas baselines. A B0 é o "sem skill": a PR-AUC dela é igual à percentagem de anormais de cada fold, entre
0,16 e 0,21, o que mostra que o "sem skill" não é um número fixo. A B1 usa só a taxa de falha do posto a 7 dias como
score, não ajusta nada e já chega a 0,511 em média. É essa a fasquia que os modelos têm de passar.

### Slide 7. Que informação ajuda? (cerca de 1 min)

Para ver que informação vale a pena, juntámos os grupos de features um a um e medimos o ganho com o mesmo modelo de
referência. O histórico do posto faz quase toda a diferença: a PR-AUC passa de 0,29 para 0,58. O histórico do
utilizador junta 0,03. A tarifa não acrescenta nada além da hora. Tirar o identificador do posto até ajuda, porque o
histórico já diz o que importa e o modelo deixa de decorar postos. O conjunto final tem 27 features: as 29 candidatas
sem post_id e sem a tarifa.

### Slide 8. Seis modelos, três princípios (cerca de 1 min 15 s)

Treinámos três classificadores com princípios diferentes, regressão logística, Naive Bayes e uma árvore de decisão, e
três ensembles: random forest, gradient boosting e um stacking construído por ordem temporal para não haver leakage.
Todos batem a B1 em todos os folds, menos o Naive Bayes. O gradient boosting fica à frente com 0,626, mas a random
forest fica só 0,003 atrás, dentro da nossa tolerância de 0,005, por isso os dois passam para a otimização. Passo à
Manuela.

---

## Manuela: slides 9 a 12

### Slide 9. Afinar e congelar antes do teste (cerca de 1 min 15 s)

Afinámos o gradient boosting, a random forest e a árvore com uma grid search, sempre nos mesmos quatro folds e por
ordem temporal. Nenhuma configuração melhorou mais do que a tolerância, por isso o modelo final é o gradient boosting
da Task 3. O cut-off foi escolhido nos dados de desenvolvimento para que 10% das sessões deem alerta, o que dá 0,490,
quase o 0,5 por defeito. Verificámos a calibração e não foi preciso corrigir nada. Todas estas escolhas ficaram
gravadas num ficheiro antes de o teste ser lido.

### Slide 10. Resultado no teste: outubro a dezembro de 2021 (cerca de 1 min 15 s)

Só depois de congelar tudo avaliámos o teste, uma única vez. O modelo chega a uma PR-AUC de 0,532, contra 0,381 da B1
e 0,178 do "sem skill". Com o cut-off congelado, dá alerta em 7,4% das sessões, e 68% desses alertas são falhas reais.
Por cada mil sessões: 50 alertas certos, 24 falsos e 126 falhas sem alerta. Com o mesmo número de alertas, a B1 acerta
38 e erra 36. O desempenho desce em relação ao desenvolvimento, mas a maior parte da descida vem da menor percentagem
de anormais nesse trimestre.

### Slide 11. Onde funciona e onde falha (cerca de 1 min)

A vantagem sobre a B1 mantém-se em todos os distritos e estações. A permutation importance confirma que o modelo vive
do histórico do posto. A análise de erros mostra o limite: as sessões que começam poucas horas depois de uma falha no
mesmo posto ficam com quase todos os alertas, enquanto as falhas que chegam depois de um período calmo quase nunca são
assinaladas; são metade das falhas sem alerta. Os utilizadores novos, sem histórico, também são pior servidos.

### Slide 12. Conclusão (cerca de 1 min 15 s, depois perguntas)

Respondendo à pergunta: em parte, sim. A informação do início da sessão dá uma boa ordenação dos postos que estão a
falhar agora, bem acima da regra simples, mas não consegue ver falhas que não dão sinal no histórico recente. As
principais limitações: não sabemos os custos nem a capacidade de resposta, o sinal enfraquece com o tempo e o
histórico do utilizador levanta questões de privacidade. Recomendamos obter os custos reais, voltar a treinar o modelo
com regularidade e juntar dados de manutenção. Tudo é reprodutível: cada notebook corre sozinho, com seed 42 e versões
fixas. Obrigado; ficamos à disposição para perguntas.

---

## Perguntas

Cada um responde às perguntas sobre os seus slides. As perguntas prováveis e as respostas modelo estão no
`docs/GUIAO_ESTUDO.md` (partes do Amir, da Inês e da Manuela, e as perguntas comuns no fim).
