# Guião de estudo do Projeto 1 (MINDD 2026/27)

Classificação de sessões de carregamento de veículos elétricos que terminam de forma anormal.
Grupo: Amir Masnavi, Inês Oliveira e Manuela Leite.

Versão em inglês: `docs/STUDY_GUIDE.md`. As duas têm o mesmo conteúdo, as mesmas secções e os mesmos números.

## Como usar este guião

Este guião explica o projeto desde o zero. Não é preciso saber data science para o seguir. Todos os números vêm do
relatório final (`docs/FINAL_REPORT.pdf`) e, ao lado de cada um, indicamos o capítulo ou a tabela de onde vem. Assim
qualquer pessoa pode confirmar. Quando escrevemos "Parte 4, Secção 9", referimo-nos ao notebook único
`MINDD_Project1.ipynb`: a Parte 4 é a Task 4 e a Secção 9 é a mesma Secção 9 que tinha o `Task4.ipynb`.

Todos começam pelo núcleo comum, que demora cerca de 15 minutos a ler, e pelo glossário, que serve para consulta.
Depois cada pessoa estuda a sua parte, em menos de 2 horas:

| Quem | Parte do projeto | Notebook | Relatório |
| --- | --- | --- | --- |
| Amir | Task 1: perceber, auditar e preparar os dados | Parte 1 | Capítulos 1 a 3 |
| Inês | Task 2: definir o problema e a avaliação; Task 3: ablação e modelos | Partes 2 e 3 | Capítulos 4 e 5 |
| Manuela | Task 4: otimização, threshold e teste; Task 5: análise final; modelo final | Partes 4 e 5 | Capítulos 6 a 9 |

Cada parte termina com uma lista "Se só tens 30 minutos" e com perguntas prováveis da professora, cada uma com uma
resposta modelo. As perguntas comuns, no fim, são para todos. O plano de ensaio, no fim do guião, explica como treinar
em pares.

Uma dica que vale para qualquer resposta oral: começar pela decisão, dar um número que a sustente e dizer o que não
fizemos e porquê. É a forma como o relatório está escrito, e é o que a professora vai procurar.

---

## Núcleo comum (para todos)

### O projeto num parágrafo

Uma empresa de carregamento de carros elétricos quer saber, no momento em que uma sessão de carregamento começa, se
essa sessão vai acabar mal: por exemplo, por avaria do posto, falha de comunicação ou problema na bateria do carro.
Se conseguir prever isso, pode vigiar melhor os postos com mais risco e mandar um técnico antes de os problemas se
acumularem. A pergunta do enunciado é até que ponto a informação disponível no início da sessão (onde, quando, o
tempo que faz, o histórico do posto e do utilizador) permite prever esse fim anormal. A nossa resposta curta é que
permite fazer uma boa ordenação dos postos que estão a falhar agora, sobretudo graças ao histórico recente de falhas
do posto, mas não permite ver falhas que surgem sem aviso.

### Os dados

O ficheiro tem 441.077 sessões de carregamento e 47 colunas, de 31 de dezembro de 2019 a 31 de dezembro de 2021, em 92
postos de carregamento, 13 estações e 3 distritos de Jiaxing, na China (capítulo 1). É uma versão educativa de um
dataset publicado por Zhang et al. (2025). As colunas dividem-se em grupos: identificação (utilizador, posto), local
(estação, distrito), transação (energia, custos, horas de início, fim e pagamento, causa de fim), tempo meteorológico
(temperatura, humidade, precipitação), tarifa e um conjunto de colunas de histórico já calculadas: quantas sessões e
quantas falhas teve o posto ou o utilizador nos últimos 1, 7, 30 dias, etc.

### O target

O ficheiro não trazia a coluna `is_Abnormal`, só a `end_cause` (causa de fim), com 15 valores. Decidimos que uma
sessão é normal quando acaba com "Charging ends normally" ou "User stops charging" (o utilizador parou porque quis).
As outras 13 causas são avarias, por isso contam como anormais. Com esta definição, 18,58% das sessões são anormais,
ou seja, cerca de 1 anormal para 4,4 normais (Tabela 1.1). Confirmámos a definição com as colunas de histórico do
próprio dataset: recontámos as falhas com a nossa regra e batem certo em 100,00% (posto) e 99,98% (utilizador) das
linhas.

### As cinco tasks numa linha cada

1. Task 1: conhecer os dados, verificar a qualidade, perceber o que muda no tempo, decidir o que pode ser usado e
   preparar os dados.
2. Task 2: definir exatamente o que se prevê e como se avalia (métricas, divisão temporal, baselines), antes de
   treinar qualquer modelo.
3. Task 3: medir que grupos de informação ajudam (ablação) e treinar modelos individuais e ensembles.
4. Task 4: afinar os melhores modelos, escolher o modelo final e o threshold, congelar tudo e avaliar uma única vez
   no teste.
5. Task 5: comparar o modelo final com a baseline no teste com todas as medidas pedidas, ver onde falha e explicar
   o que significa para o operador.

### O modelo final e os números que todos têm de saber

O modelo final é um gradient boosting (muitas árvores pequenas, cada uma a corrigir os erros das anteriores) com
profundidade 6, learning rate 0,1, 200 iterações e pelo menos 100 sessões por folha, sobre 27 features (Tabela 8.2).
O threshold é 0,490: é o valor que faz soar um alerta em 10% das sessões de desenvolvimento.

| Medida (fonte) | Modelo final | B1 (taxa de falhas do posto em 7 dias) | B0 (sem skill, ao acaso) |
| --- | --- | --- | --- |
| PR-AUC média nos 4 folds de desenvolvimento (Tabela 8.1) | 0,626 | 0,511 | 0,181 |
| PR-AUC no período de teste (Tabela 8.1) | 0,532 | 0,381 | 0,178 |
| Alertas no teste com o threshold congelado (Tabela 7.1) | 7,4% das sessões | | |
| Por cada 1.000 sessões de teste (Tabela 7.1) | 50,3 alertas certos, 24,0 falsos, 125,6 falhas não detetadas | | |

O modelo bate a B1 em todos os folds, em todos os distritos e em todas as estações do teste (capítulo 7).

### A regra do teste congelado

Guardámos os últimos três meses (outubro a dezembro de 2021, 80.081 sessões) como teste final e não lhes tocámos
durante o desenvolvimento. Escolhemos o modelo, as features, os hiperparâmetros e o threshold só com os dados
anteriores. Escrevemos essas escolhas num ficheiro a 27/10/2026, às 11:40:32, e só depois avaliámos o teste, uma vez.
Nada mudou depois de vermos o resultado. As corridas posteriores (a reprodução da Task 4, a Task 5 e a corrida do
notebook único) usaram o mesmo ficheiro congelado, deram os mesmos números e não serviram para escolher nada.

---

## Glossário

Os termos estão em inglês, como no relatório. Entre parênteses fica o termo em português quando é comum.

| Termo | O que quer dizer | Exemplo no nosso projeto |
| --- | --- | --- |
| Dataset | O conjunto de dados, uma tabela em que cada linha é um caso e cada coluna uma característica | Cada linha é uma sessão de carregamento |
| Feature (variável preditora) | Uma coluna que o modelo usa para prever | A hora de início, a temperatura, a taxa de falhas do posto |
| Target (variável alvo) | O que queremos prever | `is_Abnormal`: 1 se a sessão acaba mal, 0 se acaba bem |
| Classe positiva / negativa | Os dois valores do target. A positiva é a que procuramos | Positiva: sessão anormal. Negativa: sessão normal |
| Leakage (fuga de informação) | Usar informação que não estaria disponível no momento da previsão. Dá resultados falsamente bons | A energia carregada só se sabe no fim, por isso não pode prever o fim |
| Class imbalance (desequilíbrio de classes) | Uma classe é muito mais rara que a outra | 18,6% anormais contra 81,4% normais |
| Missing values (valores em falta) | Células vazias (NaN) | "Horas desde a última falha do posto" fica vazio se o posto nunca falhou |
| Outlier | Um valor muito afastado dos outros. Pode ser um erro ou um caso real | Uma conta com mais de 500 sessões (frota) |
| IQR | Intervalo interquartil, a regra das "cercas de Tukey" para detetar outliers | Usado na Parte 1, Secção 10.1 |
| Isolation Forest | Método que procura casos raros olhando para várias colunas ao mesmo tempo | As sessões que marcou eram 60% anormais |
| Encoding | Transformar categorias em números | Distrito A, B, C passam a 0, 1, 2, ou a três colunas 0/1 (one-hot) |
| Scaling (normalização) | Pôr as colunas numa escala parecida | Média 0 e desvio padrão 1 para a regressão logística |
| Log transform | Aplicar o logaritmo para "encolher" valores muito grandes | `log1p` nas contagens com cauda longa |
| VIF | Mede quanto uma variável é explicada pelas outras. Acima de 10 há redundância | As janelas de 180 e 730 dias do utilizador chegam a 65,4 |
| PCA | Junta variáveis correlacionadas em poucas componentes | Testada e não usada |
| Temporal split (divisão temporal) | Treinar com o passado e avaliar com o futuro, em vez de baralhar ao acaso | Treino até junho de 2021, teste de outubro a dezembro de 2021 |
| Burn-in | Período inicial que não se usa | Até 31/03/2020, porque o histórico ainda estava incompleto |
| Fold | Uma divisão treino/validação. Avaliar em vários folds dá uma ideia da estabilidade | Usámos 4 folds, um por trimestre |
| Expanding window | Cada fold treina com tudo o que veio antes da sua validação, por isso o treino vai crescendo | O fold 1 treina 6 meses, o fold 4 treina 15 |
| Purge gap (purga) | Retirar do treino sessões cujo resultado só se sabe depois da fronteira | 27 a 39 sessões por fold |
| Baseline | Uma referência simples. Um modelo só vale a pena se a bater | B0 ao acaso, B1 taxa de falhas do posto em 7 dias |
| Precision (precisão) | Dos alertas dados, quantos eram mesmo falhas | 0,677 no teste: 68 em cada 100 alertas são reais |
| Recall (sensibilidade) | Das falhas que houve, quantas apanhámos | 0,286 no teste: apanhámos 29 em cada 100 falhas |
| F1 | Média harmónica de precision e recall | 0,402 no teste |
| PR-AUC | Área debaixo da curva precision-recall. Resume a qualidade da ordenação em todos os thresholds. O valor "ao acaso" é a percentagem de positivos | 0,532 no teste contra 0,178 ao acaso |
| ROC-AUC | Probabilidade de uma sessão anormal ter score maior do que uma normal. 0,5 é o acaso | 0,794 no teste |
| Lift | Quantas vezes a PR-AUC está acima do acaso | 3,03 no teste |
| Balanced accuracy | Média do recall das duas classes. 0,5 é o acaso | 0,628 no teste |
| MCC | Correlação entre previsão e realidade, de −1 a 1. 0 é o acaso | 0,373 no teste |
| Threshold (cut-off, limiar) | Valor do score a partir do qual se dá alerta | 0,490 |
| Alert rate (taxa de alertas) | Percentagem de sessões com alerta | 10% em desenvolvimento, 7,4% no teste |
| Alert budget | Quantos alertas a equipa consegue tratar, em percentagem das sessões | Testámos 5%, 10% e 20% |
| Overfitting (sobreajuste) | O modelo decora o treino e falha em dados novos | Uma árvore de profundidade 16 com folhas de 50 sessões |
| Hyperparameter | Configuração escolhida antes de treinar | Profundidade da árvore, learning rate |
| Ensemble | Combinar vários modelos | Random forest, gradient boosting, stacking |
| Bagging / random forest | Muitas árvores treinadas em amostras diferentes, cuja média reduz a variância | 200 árvores |
| Boosting | Árvores em sequência, cada uma corrige os erros das anteriores, o que reduz o viés | O nosso modelo final |
| Stacking | Um meta-modelo aprende a combinar as previsões de outros modelos | Regressão logística sobre LR, Naive Bayes e árvore |
| Calibration (calibração) | Saber se o score se pode ler como probabilidade | Score 0,74 corresponde a cerca de 74% de falhas reais |
| Brier score | Erro médio das probabilidades. Quanto mais baixo, melhor | 0,103 em desenvolvimento |
| Permutation importance | Baralhar uma coluna e medir quanto o modelo piora | Baralhar o histórico do posto tira 0,366 de PR-AUC |
| Partial dependence | Como o score médio muda quando uma variável muda | O score sobe muito quando a taxa de 1 dia do posto passa 0,3 |
| Drift | Os dados mudam ao longo do tempo | A percentagem de anormais vai de 26,3% a 13,7% e depois a 22,9% |
| Cold start | Não há histórico para um caso novo | Utilizadores novos: o modelo tem menos informação sobre eles |
| Ablation (ablação) | Tirar ou pôr grupos de variáveis para medir o que cada um vale | S1 a S4 na Task 3 |
| Bootstrap | Reamostrar com reposição para estimar a incerteza | Erro padrão da PR-AUC de 0,004 a 0,006 |
| McNemar | Teste que compara dois classificadores nas mesmas sessões | O modelo acerta sozinho 4.283 vezes, a B1 sozinha 2.223 |

---

## Parte do Amir: Task 1, perceber, auditar e preparar os dados

Parte 1 do notebook, capítulos 1 a 3 do relatório.

Esta parte responde a duas perguntas: os dados são de confiança, e o que podemos usar para prever? Tudo o que as
outras tasks fazem assenta nas decisões tomadas aqui.

### Passo a passo

#### Secções 2 a 4: carregar, descrever e limpar

Lemos o ficheiro e olhámos para cada coluna: tipo, significado e
quando é conhecida. Depois fizemos as verificações de qualidade da Tabela 2.1. Encontrámos espaços (tabs) a mais no
fim de algumas datas e em 18.370 valores de local, e tirámo-los ao ler. Não há linhas repetidas. Há 17 pares em que a
mesma conta começa em dois postos no mesmo segundo; são contas de frota, por isso ficaram. Não há valores negativos
nem sessões que acabem antes de começar. As durações param nas 23,99 horas, o que parece um limite do sistema. Há
54.621 sessões com energia zero, mas a energia é uma coluna do fim da sessão, por isso não a usamos de qualquer forma.
A ideia geral é que os dados estão em bom estado e que, antes de corrigir alguma coisa, investigámos se era mesmo um
erro.

#### Secção 5: construir o target

É a decisão mais importante da task, explicada no núcleo comum. Decidimos que
"User stops charging" conta como normal, porque foi o utilizador que quis parar. A prova é que, com esta regra, as
colunas de histórico do dataset batem certo em 100,00% e 99,98% das linhas. Com a alternativa (só "Charging ends
normally" é normal) batem em 0,26% e 35,85%, e a percentagem de anormais subiria para 53,93% (Tabela 1.1). Também
reparámos que as taxas de falha já vêm suavizadas, (falhas + 1) / (sessões + 5), e por isso um posto sem histórico
fica com 0,2. Há 9.058 sessões normais (2,5%) que não carregaram energia, quase sempre utilizadores que pararam ao fim
de um minuto. Ficaram como normais, porque para as tirar teríamos de usar a energia, que só se sabe no fim.

#### Secção 6: valores em falta

Só existem em 4 colunas do tipo "tempo desde a última sessão ou falha", e cada vazio
corresponde à sua flag de "sem histórico". O vazio quer dizer "isto nunca aconteceu", não "não sabemos". Decidimos não
apagar linhas nem pôr a média. Nas árvores deixamos o vazio, porque o modelo sabe tratá-lo. Na regressão logística
pomos o máximo do treino, ou seja, lemos "nunca aconteceu" como "aconteceu há muito tempo", e mantemos a flag.

#### Secção 7: mudanças ao longo do tempo

Os dados não são estáveis (Figura 2.3). O volume cai para 1.391 sessões em
fevereiro de 2020, provavelmente por causa da COVID-19, e chega a 25 a 28 mil por mês no outono de 2021. A percentagem
de anormais desce de 26,3% para 13,7% e volta a subir para 22,9%. O tipo de avaria também muda: as falhas de ligação
somam 7,1 pontos à percentagem de anormais no 1.º trimestre de 2020 e só 1 a 2 pontos a partir do 3.º trimestre. No
início do ficheiro o histórico ainda está incompleto, e por isso 31% das sessões de janeiro de 2020 parecem de
utilizadores novos, contra 9 a 15% depois. Há uma coisa estável: a percentagem de falhas de cada posto é parecida em
2020 e 2021 (Spearman 0,81), e é por isso que o histórico do posto funciona. Daqui decidimos dividir os dados por tempo
e não ao acaso. Uma divisão ao acaso misturaria períodos diferentes e daria resultados otimistas demais.

#### Secção 8: leakage, ou o que se sabe no início

Sete colunas só existem depois da sessão: energia, custo da
eletricidade, taxa de serviço, montante, pagamento efetivo, hora de fim e hora de pagamento. Sozinhas separam as
classes com ROC-AUC de 0,82 a 0,85, melhor do que qualquer variável do início (a melhor tem 0,77), e é precisamente
por isso que são perigosas: descrevem o resultado, não o preveem (Figura 2.1). As sessões anormais são curtas e
carregam pouco. Excluímo-las todas. A hora de criação da encomenda foi o caso difícil: aparece depois do início em 56%
das sessões, às vezes 16 horas depois, e a sua relação com o resultado é fraca (AUC 0,59). Como não temos a certeza de
que existe no momento da previsão, excluímo-la também. O tempo meteorológico só tem um valor por distrito e por dia;
seguimos o enunciado e tratamo-lo como uma previsão conhecida no início.

#### Secção 9: explorar os preditores (só no período de treino)

Medimos as relações apenas no treino, para que a
validação e o teste não influenciem as escolhas. A localização importa sobretudo ao nível do posto: os distritos vão
de 14,6% a 24,1% de anormais, as estações de cerca de 8% a 38% e os postos de 4,1% a 60,9%. Os 10 piores postos
geram 24,1% das falhas com só 10,2% das sessões. A hora e o dia da semana mexem pouco (14,7% a 20,5% e 17,0% a 18,9%) e
o tempo tem efeitos fracos. O histórico é o sinal mais forte (Figura 2.2): dividindo a taxa de falhas do posto em 7
dias em decis, a percentagem de anormais vai de cerca de 4% no decil mais baixo a cerca de 60% no mais alto. Um posto
que falhou há pouco tende a voltar a falhar. O histórico do utilizador também ajuda, mas menos (AUC 0,69 a 0,70 contra
0,75 a 0,77 do posto). Os utilizadores são muito desiguais: 45% das 34.294 contas do treino têm uma só sessão, mas o
1% de contas mais ativas faz 34% das sessões. Os novos utilizadores falham um pouco mais (20,2% contra 17,5%).

#### Secção 10: outliers

Primeiro aplicámos a regra do IQR, que mostrou caudas longas nas contagens e nos tempos
(assimetria de 3 a 9). Depois olhámos para os casos extremos um a um: postos parados mais de 14 dias (39% de falhas
quando voltam), 21 contas com mais de 500 sessões e dois dias de tempestade. Por fim corremos o Isolation Forest, e as
sessões que ele marcou eram 60% anormais. Os extremos são reais e informativos, por isso não tirámos nenhuma linha.
Para os modelos lineares aplicamos `log1p`, que encolhe as caudas sem apagar nada.

#### Secção 11: divisão temporal

Deixámos de fora o burn-in (até 31/03/2020, 14.017 sessões), porque o histórico
estava incompleto e o tipo de falhas dessa altura já não existe. O resto foi dividido por data (Tabela 3.1): treino de
abril de 2020 a junho de 2021 (271.182 sessões, 17,8% anormais), validação de julho a setembro de 2021 (75.769, 21,1%)
e teste de outubro a dezembro de 2021 (80.081, 17,6%). Purgámos 28 sessões do treino que acabavam depois da fronteira,
porque o resultado delas só se saberia depois. Esta divisão mostrou duas coisas. Primeiro, 39,9% das sessões de
validação e 61,3% das de teste são de contas que nunca aparecem no treino, por isso o `user_id` não pode ser feature.
Segundo, todos os postos da validação e do teste já estavam no treino, por isso não conseguimos testar um posto novo.

#### Secção 12: features e redução

Ficámos com 29 features em 7 grupos: calendário (hora e dia da semana), tarifa,
local (posto, estação, distrito), tempo (temperatura, humidade, precipitação e uma nova `rain_flag`), histórico do
posto (8), histórico do utilizador (10) e concorrência (1). Tirámos colunas redundantes (Tabela 3.2): o preço da
eletricidade, que é fixado pela tarifa, seis contagens de falhas que são funções exatas de outras colunas, duas flags
que valem sempre 0 depois do burn-in e uma flag repetida. Algumas features estão muito correlacionadas: as janelas do
utilizador chegam a VIF 65,4, porque as janelas de 180 e 730 dias contêm quase as mesmas sessões. As árvores e os
modelos regularizados lidam bem com isso. Para modelos lineares simples criámos um conjunto reduzido, de 19 das 23
variáveis numéricas, com VIF máximo de 8,6. Também testámos a PCA: precisa de 11 de 23 componentes para guardar 90% da
variância, e a primeira componente quase não separa as classes (AUC 0,51). Comprime pouco e mistura informação do
posto com a do utilizador, por isso não a usámos.

#### Secção 13: operações aprendidas e desequilíbrio

Preparámos duas versões dos dados. A versão para árvores mantém
os valores brutos, os vazios e os códigos das categorias. A versão linear aplica `log1p` a 8 colunas, enche os vazios
com o máximo do treino, normaliza, codifica a hora e o dia da semana com seno e cosseno (porque são circulares: a
hora 23 está perto da hora 0) e faz one-hot ao posto e à tarifa, o que dá 126 colunas. Tudo o que aprende algo com os
dados (médias, desvios, listas de categorias, valores de preenchimento) é aprendido só no treino (Tabela 3.3). Para
mostrar porque é que isto importa: se aprendêssemos com todos os períodos, o valor de preenchimento de "dias desde a
última falha do utilizador" passaria de 543 para 702 dias, o que é informação do futuro a entrar no treino. Quanto ao
desequilíbrio (1 para 4,4), não reamostrámos nem usámos pesos de classe. Os modelos aprendem a proporção real e são
avaliados com métricas que não se deixam enganar por ela. Também não usámos SMOTE, porque inventaria sessões
impossíveis, como meia flag ou uma mistura de dois postos.

#### Secções 14 e 15: ficheiros e síntese

O notebook grava os dados preparados, os grupos de features, o registo de
decisões e o ledger das operações aprendidas, e termina com a síntese pedida pelo enunciado. No relatório, essa
síntese foi integrada no capítulo 9.

### Se só tens 30 minutos

- O target vem da `end_cause`: 13 causas de avaria são anormais, e "user stops" é normal. Dá 18,58% de anormais e bate
  com o histórico do dataset em cerca de 100% das linhas.
- Sete colunas do fim da sessão mais a `end_cause` são leakage. A hora da encomenda também saiu, por ter uma data
  incerta.
- O tempo meteorológico é tratado como previsão, como diz o enunciado.
- Não tirámos nenhuma linha: não há duplicados verdadeiros, os vazios querem dizer "nunca aconteceu" e os extremos são
  reais.
- Os dados mudam no tempo (volume, % de anormais, tipo de avaria), por isso a divisão é temporal, com burn-in e purga.
- O sinal mais forte é o histórico recente de falhas do posto: dos 4% aos 60% de anormais entre o decil mais baixo e
  o mais alto.
- Ficaram 29 features em 7 grupos. A PCA foi testada e rejeitada. O VIF alto só aparece nas janelas do utilizador.
- Tudo o que aprende com os dados é aprendido só no treino (exemplo: 543 contra 702 dias).
- Não houve reamostragem nem SMOTE: os modelos aprendem a proporção real.
- O `user_id` não pode ser feature, porque 61,3% das sessões de teste são de contas novas.

### Liga com

A Task 2 usa as 29 features, a divisão temporal e a regra de "aprender só no treino" para montar os folds e o
protocolo. A Task 3 usa as duas versões dos dados, uma para árvores e outra para modelos lineares.

### Perguntas prováveis sobre a Task 1

1. **Como definiram o target e porque é que "User stops charging" é normal?**
   É normal porque parar é uma escolha do utilizador e não uma avaria. As outras 13 causas são falhas de
   equipamento, comunicação ou do veículo. Testámos esta definição recontando as falhas do histórico do dataset, e
   bate certo em 100,00% (posto) e 99,98% (utilizador) das linhas; a alternativa só bate em 0,26%. Ver capítulo 1.1.

2. **Porque é que não removeram nenhuma linha?**
   Porque investigámos cada problema antes de agir e nenhum era um erro. Não há duplicados verdadeiros (os 17 pares
   são contas de frota), os vazios querem dizer "nunca aconteceu" e os extremos são situações reais, como postos
   parados muito tempo ou contas de frota. As sessões que o Isolation Forest marcou como estranhas eram 60% anormais,
   por isso apagá-las seria apagar o sinal. Ver Tabela 2.1.

3. **Como trataram os valores em falta?**
   Os vazios só aparecem em 4 colunas de "tempo desde a última sessão ou falha", e cada um corresponde à flag "sem
   histórico". Nas árvores deixámo-los, porque o modelo encaminha-os para o lado certo de cada divisão. Na versão
   linear pusemos o máximo do treino e mantivemos a flag. Não usámos a média, porque "nunca aconteceu" não é um valor
   médio. Ver Secção 3.3.

4. **Como verificaram que não há leakage?**
   Classificámos cada coluna pelo momento em que é conhecida. As sete colunas do fim da sessão têm ROC-AUC de 0,82 a
   0,85, acima de tudo o que se sabe no início (0,77), porque descrevem o resultado. Saíram todas, e também a hora da
   encomenda, que aparece depois do início em 56% dos casos. Além disso, tudo o que aprende com os dados é aprendido
   só no treino. Ver Secção 2.1.

5. **Que mudanças no tempo encontraram e o que implicam para a avaliação?**
   O volume, a percentagem de anormais (26,3%, depois 13,7%, depois 22,9%) e o tipo de avaria mudam. Por isso não
   podemos baralhar os dados: avaliamos sempre no futuro em relação ao treino e lemos cada PR-AUC ao lado da
   percentagem de anormais do seu período. Ver Secção 2.4.

6. **Porque deixaram de fora os primeiros três meses?**
   No início do ficheiro o histórico ainda está a encher: 31% das sessões de janeiro de 2020 parecem de utilizadores
   novos, contra 9 a 15% depois. Além disso, as falhas de ligação desse período quase desapareceram mais tarde. Esses
   meses ensinariam ao modelo um padrão que já não existe. Ver Secção 3.1.

7. **O que é a purga e porque é precisa?**
   O resultado de uma sessão só se sabe quando ela acaba, até 24 horas depois. Uma sessão que começa antes da
   fronteira do treino e acaba depois tem um resultado "do futuro". Retirámos essas 28 sessões do treino para que esse
   resultado não entre no modelo. Ver Secção 3.1.

8. **Porque não usaram a PCA?**
   Testámo-la: precisa de 11 de 23 componentes para guardar 90% da variância, e a primeira componente quase não
   separa as classes (AUC 0,51). Comprimia pouco, misturava o histórico do posto com o do utilizador e tornava o modelo
   mais difícil de explicar. Ver Secção 3.2.

9. **Porque não equilibraram as classes com SMOTE ou undersampling?**
   O desequilíbrio é moderado (1 para 4,4) e avaliamos com PR-AUC e alertas por 1.000 sessões, que não se deixam
   enganar pela classe maioritária. O SMOTE criaria sessões impossíveis, como meia flag. Se usássemos reamostragem,
   seria só dentro do treino de cada fold, para a validação e o teste manterem a proporção real. Ver Secção 3.3.

10. **O tempo meteorológico pode mesmo ser usado no início?**
    Só existe um valor por distrito e por dia, por isso não é o tempo exato da sessão. O enunciado manda tratá-lo como
    previsão conhecida no início, e foi o que fizemos. Deixámos isso registado como limitação. De qualquer forma, o
    modelo quase não o usa (importância abaixo de 0,002). Ver Secções 2.1 e 6.6.

---

## Parte da Inês: Task 2 (problema e avaliação) e Task 3 (ablação e modelos)

Partes 2 e 3 do notebook, capítulos 4 e 5 do relatório.

A Task 2 fixa as regras do jogo antes de jogar: o que se prevê, com que variáveis, como se mede e contra quem se
compara. A Task 3 joga com essas regras: mede que informação ajuda e treina os primeiros modelos.

### Task 2 passo a passo (Parte 2)

#### Secção 3: o problema

A unidade é uma sessão de carregamento. A classe positiva é o fim anormal. A previsão faz-se
uma vez, no início da sessão, só com o que se sabe nesse momento. Pensámos o uso como vigilância preventiva e
prioridade de manutenção: as sessões que estão a começar, e através delas os postos, são ordenadas pelo risco, e o
operador, que tem capacidade limitada, olha primeiro para as mais arriscadas. Um alerta quer dizer "esta sessão, neste
posto, tem mais risco de acabar mal". Não é um diagnóstico e não diz qual será a avaria. No desenvolvimento (abril de
2020 a setembro de 2021) há 346.979 sessões, 18,5% anormais.

#### Secção 4: que variáveis se podem usar

Pusemos cada uma das 47 colunas numa das quatro categorias do enunciado
(Tabela 4.1): 27 elegíveis, 1 só para construir o target (`end_cause`), 7 geradas durante ou depois da sessão e 12
excluídas por outra razão (o `UserID`, a hora da encomenda e 10 colunas redundantes). O notebook verifica em código que
cada coluna aparece exatamente uma vez. O `UserID` sai porque 35% a 46% das sessões de validação de cada fold vêm de
contas que não estão no treino: o modelo só decoraria contas e identificaria pessoas. O histórico do utilizador é o
substituto legítimo. O `post_id` também é um identificador, mas o posto é conhecido no início, por isso ficou nesta
fase (a Task 3 acabou por tirá-lo).

#### Secção 5: o custo dos dois erros

Um falso positivo é um alerta numa sessão que acaba bem; um falso negativo é uma
falha que passa sem alerta. Por evento, o falso negativo é pior: o alerta leva a uma ação barata (vigiar ou
inspecionar), enquanto uma falha não vista deixa um posto avariado em serviço, e as falhas aparecem em grupos no mesmo
posto. Mas o número de falsos alertas está limitado pela capacidade dos técnicos, e uma lista enorme de alertas não
serve para nada. Não sabemos o rácio de custos c = custo(FN) / custo(FP). Com probabilidades calibradas, o threshold
ótimo seria 1/(1+c): 0,50 para c = 1, 0,33 para c = 2 e 0,17 para c = 5. Como fixar um threshold nesta fase seria
arbitrário, escolhemos métricas que avaliam a ordenação e reportamos resultados para três orçamentos de alertas: 5%,
10% e 20% das sessões.

#### Secção 6: métricas

A métrica principal é a PR-AUC (Tabela 4.2). Mede quão precisos se mantêm os alertas à medida
que apanhamos mais falhas, e ignora os verdadeiros negativos, que são a maioria. A sua limitação é que o valor ao acaso
é a percentagem de anormais, que muda entre períodos; por isso lemo-la sempre ao lado dessa percentagem, ou como lift.
Como métricas complementares usamos a ROC-AUC, que não depende da percentagem de anormais e por isso se compara entre
períodos, e o Brier score e a log-loss, que medem a qualidade das probabilidades. As operacionais são precision,
recall e alertas certos, falsos e falhados por 1.000 sessões, para cada orçamento. Para a estabilidade olhamos para o
valor em cada fold, o desvio padrão, o pior fold, a tendência e os folds ganhos. Não usamos accuracy, porque prever
sempre "normal" acerta em 79% a 84% das sessões de cada fold e não apanha nenhuma falha. O F1 só aparece quando já há
threshold.

#### Secção 7: avaliação temporal

Dividimos o desenvolvimento em quatro folds de janela crescente, um por trimestre
(Tabela 4.3). O fold 1 treina até 30/09/2020 (111.470 sessões) e valida em out–dez 2020 (60.364). O fold 4 treina até
30/06/2021 (271.182) e valida em jul–set 2021 (75.769). As fronteiras são trimestres de calendário, fixadas antes de
ver qualquer resultado. Um trimestre é grande o suficiente para uma estimativa estável (cada um tem pelo menos 6.600
sessões anormais) e curto o suficiente para mostrar mudanças. Escolhemos quatro folds como compromisso: um fold antes
treinaria menos de seis meses, e folds mensais dariam 12 estimativas pequenas e ruidosas. Os folds têm tamanhos
diferentes, e os primeiros treinam com menos dados e sem um inverno completo, por isso esperamos que sejam um pouco
pessimistas. Em cada fold, as 27 a 39 sessões que ainda estavam a decorrer na fronteira são purgadas, e todo o
preprocessing é ajustado de novo dentro do treino desse fold. O teste é retirado logo a seguir a ler o ficheiro, e só
contamos as suas linhas.

#### Secção 8: agregar os folds

Ordenamos os modelos pela média simples da PR-AUC dos quatro folds, para que cada
período conte uma vez. Também reportamos a média ponderada pelo número de sessões e o valor pooled (todas as previsões
juntas), que é o que serve para escolher o threshold. Como a percentagem de anormais muda entre folds, não comparamos
folds entre si, mas comparamos dois modelos dentro do mesmo fold: diferenças emparelhadas e número de folds ganhos.
Não declaramos significância estatística, porque com quatro folds o menor p-valor possível de um teste de Wilcoxon
exato é 0,125, mesmo que um modelo ganhe todos os folds.

#### Secção 9: baselines

A B0 é o acaso: scores aleatórios. A sua PR-AUC é a percentagem de anormais de cada fold (média
0,181). A B1 usa uma coluna do dataset como score, a taxa de falhas do posto nos últimos 7 dias, e não aprende nada. Já
é forte: PR-AUC média de 0,511, ROC-AUC de 0,772 e pior fold de 0,456 no fold 2 (Tabela 4.4). Com um orçamento de 5%,
74% dos seus alertas são falhas reais, mas só apanha 21% das falhas (Tabela 4.5). Um modelo só compensa a complexidade
se apanhar mais falhas do que a B1 com o mesmo orçamento.

#### Secção 10: protocolo

A Tabela 4.6 resume tudo e o notebook grava-o em `prepared/task2_protocol.json`. As tasks
seguintes leem esse ficheiro e usam exatamente as mesmas features, folds e métricas.

### Task 3 passo a passo (Parte 3)

#### Secção 3: ablação dos grupos de features

Comparámos os quatro conjuntos pedidos pelo enunciado sempre com o mesmo
modelo de referência, um gradient boosting sem afinação. Assim, as diferenças vêm da informação e não da afinação.
Tratamos diferenças abaixo de 0,005 como desprezáveis; um bootstrap dá um erro padrão de 0,004 a 0,006 para uma PR-AUC,
o que dá a escala desta tolerância. Resultados (Tabela 5.1):

| Conjunto | Features | PR-AUC média | Ganho |
| --- | --- | --- | --- |
| S1 contexto e tempo | 9 | 0,290 | |
| S2 + tarifa | 10 | 0,290 | +0,0006 |
| S3 + histórico do posto | 18 | 0,584 | +0,294, nos 4 folds |
| S4 + histórico do utilizador | 29 | 0,615 | +0,031, nos 4 folds |
| Selecionado (S4 sem `post_id` e sem tarifa) | 27 | 0,626 | |
| Selecionado sem histórico do utilizador | 16 | 0,599 | |

Daqui saem as respostas às perguntas do enunciado. A tarifa não acrescenta nada além da hora, porque o período
tarifário é uma função da hora de início e o modelo consegue reconstruí-lo. O histórico do posto é, de longe, o grupo
que mais ajuda: sobe a PR-AUC de 0,290 para 0,584, com ganhos de +0,249 a +0,360 em cada trimestre, e com ele o modelo
já fica acima da B1 em todos os folds. O histórico do utilizador ajuda menos (+0,031), sempre no mesmo sentido, mas o
ganho encolhe de +0,044 no fold 1 para +0,018 no fold 4. Para utilizadores que voltam, a PR-AUC sobe de 0,609 para
0,640; para contas novas (cerca de 13% das sessões), quase não muda. A ordem dos conjuntos é a mesma em todos os
folds, por isso o efeito é consistente no tempo, embora o tamanho dos ganhos varie. Depois tirámos o `post_id` (a
PR-AUC sobe +0,0107 nos quatro folds, o que mostra que a identidade do posto não acrescenta nada quando há histórico)
e a tarifa (+0,0003). Ficámos com 27 features.

Há também questões operacionais e éticas. O histórico do posto precisa de um registo ao vivo das sessões terminadas,
que tem sempre atraso. Se os alertas levarem a manutenção, as falhas podem diminuir e o histórico mudar. O histórico
do utilizador é um perfil de comportamento ligado a uma conta: um condutor que usou um posto avariado pode ficar com
um score mais alto e ser "culpado" por uma falha do equipamento. Mantivemo-lo porque melhora a ordenação, mas só para
ordenar sessões internamente, nunca para decidir sobre um condutor. O modelo sem histórico do utilizador (0,599) é a
alternativa de privacidade.

#### Secção 4: modelos individuais

O enunciado pede pelo menos três princípios. Escolhemos três famílias dos slides
(Tabela 5.2). A regressão logística é linear: a taxa de falhas sobe de forma suave com o histórico do posto, e o modelo
dá probabilidades. Precisa de log e normalização e sofre com variáveis correlacionadas, o que a penalização controla.
O Naive Bayes é probabilístico, tem poucos parâmetros e um viés diferente, mas assume que as variáveis são
independentes dada a classe, o que as janelas de 1, 7 e 30 dias violam. A árvore de decisão faz divisões sucessivas
por limiares, que é a forma das relações vistas na Task 1, e não precisa de normalização; em troca, é instável e
sobreajusta, por isso afinámos a profundidade e o tamanho mínimo das folhas. Deixámos de fora o kNN, que precisa de uma
distância entre contagens, taxas e categorias e compararia cada sessão de validação com até 271.000 sessões de treino,
e o SVM com kernel, cujo tempo cresce entre o quadrado e o cubo do número de sessões e que não dá probabilidades. Ambos
obrigariam a usar uma amostra e a deitar fora o histórico que tem o sinal. Resultados: árvore 0,597, regressão
logística 0,593 e Naive Bayes 0,525. Este último ordena razoavelmente (ROC-AUC 0,814), mas as suas probabilidades são
piores do que a constante (Brier 0,172 contra 0,148), o que é coerente com a independência violada. A árvore e a
regressão logística chegam quase ao mesmo valor apesar de serem tão diferentes, o que sugere que o limite está na
informação disponível e não no modelo.

#### Secção 5: ensembles

Escolhemos um ensemble por ideia. A random forest faz bagging: a média de 200 árvores
treinadas em amostras diferentes reduz a variância de uma árvore instável. O gradient boosting faz boosting: árvores
pequenas em sequência, cada uma a corrigir os erros das anteriores, reduzem o viés. O stacking combina a regressão
logística, o Naive Bayes e a árvore com uma regressão logística por cima, que aprende quanto confiar em cada um. Não
usámos voting com pesos iguais, porque um dos modelos é muito mais fraco. O enunciado avisa que o stacking não pode ter
leakage. Por isso construímos as previsões do meta-modelo por ordem temporal: dentro do treino de cada fold, cada
trimestre é previsto por modelos treinados só com sessões que começaram e acabaram antes dele (Figura 5.2). Os três
ensembles batem os seus componentes em todos os folds: a random forest fica +0,025 acima da árvore e o boosting
+0,028.

#### Secção 6: comparação e alertas

Ranking final (Tabela 5.3): gradient boosting 0,626, random forest 0,622, stacking
0,610, árvore 0,597, regressão logística 0,593, Naive Bayes 0,525, B1 0,511 e B0 0,181. O boosting e a random forest
estão dentro da tolerância. Preferimos o boosting porque ganha em três folds e é muito mais rápido a treinar de novo.
Bate a B1 em todos os folds, por +0,103 a +0,120 (+0,115 em média). Em alertas (Tabela 5.4), com um orçamento de 5%,
88% dos alertas do boosting são falhas reais, contra 74% na B1, mas o modelo ainda deixa passar 136 de cerca de 180
falhas por 1.000 sessões.

### Se só tens 30 minutos

- A previsão é um alerta de risco no início da sessão, para vigilância e manutenção, não um diagnóstico.
- 47 colunas: 27 elegíveis, 1 target, 7 do fim da sessão e 12 excluídas por outra razão. O `UserID` sai porque o modelo
  decoraria contas e identificaria pessoas.
- O falso negativo é pior por evento, mas a capacidade dos técnicos limita os falsos alertas. Por isso avaliamos a
  ordenação e usamos orçamentos de 5%, 10% e 20%.
- A PR-AUC é a métrica principal e lê-se sempre com a percentagem de anormais (o acaso). Accuracy não serve: prever
  sempre "normal" já acerta 79% a 84%.
- Quatro folds de janela crescente, um por trimestre, com purga. O teste fica fechado.
- Os modelos ordenam-se pela média simples dos folds, comparados fold a fold. Não há significância com 4 folds
  (Wilcoxon mínimo 0,125).
- B0 = 0,181 e B1 = 0,511. A B1 já é forte.
- Ablação: a tarifa não acrescenta nada, o histórico do posto dá +0,294 e o do utilizador +0,031. Ficaram 27 features
  (sem `post_id` e sem tarifa).
- Três individuais (regressão logística, Naive Bayes, árvore) e três ensembles (random forest, boosting, stacking
  temporal). O kNN e o SVM ficaram de fora por razões de escala.
- Vencedor: gradient boosting com 0,626, +0,115 acima da B1 e melhor nos 4 folds.

### Liga com

A Task 4 afina o boosting, a random forest e a árvore com os mesmos folds e a mesma regra de tolerância, e escolhe o
threshold com o orçamento de 10% definido aqui. A B1 da Task 2 é a baseline da Task 5.

### Perguntas prováveis sobre as Tasks 2 e 3

1. **Porque usaram PR-AUC e não accuracy?**
   A classe anormal é minoritária (cerca de 18%), por isso prever sempre "normal" já dá 79% a 84% de accuracy sem
   apanhar uma única falha. A PR-AUC mede quão precisos ficam os alertas à medida que apanhamos mais falhas, e ignora
   os verdadeiros negativos. A sua limitação é depender da percentagem de anormais, por isso lemo-la sempre com essa
   percentagem ou como lift. Ver Secção 4.4.

2. **Porque não usaram K-fold aleatório?**
   Os dados mudam no tempo e o modelo vai ser usado em sessões futuras. Com folds aleatórios, o modelo treinaria com
   sessões de depois daquelas em que é avaliado e veria o futuro, o que dá resultados otimistas demais. Usámos quatro
   folds de janela crescente em que o treino vem sempre antes da validação. Ver Secção 4.5.

3. **O que é a purga entre treino e validação?**
   O resultado de uma sessão só existe quando ela acaba. As 27 a 39 sessões por fold que começaram antes da fronteira e
   acabaram depois saem do treino, para que nenhum resultado "do futuro" entre no modelo. Ver Secção 4.5.

4. **Porque é que a B1 é uma boa baseline?**
   Porque é o que um operador poderia fazer hoje sem nenhum modelo: olhar para os postos que falharam na última
   semana. Não aprende nada, é conhecida no início da sessão e foi o sinal mais forte da Task 1. Já chega a 0,511 de
   PR-AUC contra 0,181 do acaso, por isso bater a B1 é uma exigência séria. Ver Secção 4.7.

5. **A tarifa acrescenta informação além da hora?**
   Não. Acrescentá-la muda a PR-AUC em +0,0006, e as diferenças por fold (−0,0033 a +0,0038) ficam todas dentro da
   tolerância de 0,005. O período tarifário é decidido pela hora de início, por isso um modelo que já tem a hora
   consegue reconstruí-lo. Ver Secção 5.1.

6. **Quanto vale o histórico do utilizador e que problemas levanta?**
   Acrescenta +0,031 de PR-AUC em todos os folds, sobretudo para quem volta (de 0,609 para 0,640), e o ganho encolhe
   com o tempo. É um perfil de comportamento de uma pessoa, por isso só o usamos para ordenar sessões internamente e
   nunca para decidir sobre um condutor. O modelo sem ele (0,599) fica como alternativa de privacidade. Ver
   Secção 5.1.

7. **Porque não usaram kNN ou SVM?**
   O enunciado pede três princípios e nós usámos linear, probabilístico e árvore. O kNN precisaria de uma distância
   entre contagens, taxas e categorias e compararia cada sessão de validação com até 271.000 de treino. O SVM com kernel
   cresce entre o quadrado e o cubo do número de sessões e não dá probabilidades. Os dois obrigariam a usar uma amostra
   e a perder o histórico que tem o sinal. Ver Secção 5.2.

8. **Como evitaram leakage no stacking?**
   Não usámos validação cruzada aleatória para gerar as previsões do meta-modelo. Dentro do treino de cada fold, cada
   trimestre foi previsto por modelos treinados só com sessões que começaram e acabaram antes dele. Depois o
   meta-modelo aprendeu com essas previsões, e há asserções no código que verificam as datas de cada ajuste. Ver
   Secção 5.3.

9. **Porque é que o Naive Bayes é o pior?**
   Assume que as variáveis são independentes dada a classe, mas as janelas de 1, 7 e 30 dias contam em parte as
   mesmas falhas. Ordena razoavelmente (ROC-AUC 0,814), mas as probabilidades ficam demasiado confiantes: o Brier é
   0,172, pior do que a constante 0,148. Ver Secção 5.2.

10. **Porque é que os ensembles podem melhorar os modelos individuais?**
    A random forest faz a média de muitas árvores em amostras diferentes, e isso cancela a instabilidade de uma árvore.
    O boosting corrige os erros passo a passo, o que reduz o viés de árvores pequenas. O stacking junta modelos que
    erram de formas diferentes. Nos nossos dados, todos ficaram acima dos seus componentes em todos os folds. Ver
    Secção 5.3.

---

## Parte da Manuela: Task 4, Task 5 e o modelo final

Partes 4 e 5 do notebook, capítulos 6 a 9 do relatório.

A Task 4 transforma o melhor modelo num sistema de alertas: afina-o, escolhe o threshold, congela tudo e só depois
abre o teste. A Task 5 estuda esse modelo congelado no teste: contra a baseline, ao longo do tempo, por grupos, nos
erros e na prática do operador. O capítulo 8 junta as escolhas finais e o 9 responde à pergunta do projeto.

### Task 4 passo a passo (Parte 4)

#### Secções 2 a 4: que modelos afinar e como

Afinámos três modelos: o gradient boosting, a random forest e a árvore
de decisão. São os dois melhores ensembles e o melhor individual da Task 3, e cobrem três princípios (boosting, bagging
e uma árvore só). O boosting e a random forest estavam a 0,003 um do outro, dentro da tolerância, e por isso os dois
precisavam de afinação antes de escolher. Deixámos de fora o stacking (0,015 atrás e muito caro de afinar), a regressão
logística (as duas penalizações já davam o mesmo) e o Naive Bayes (o seu único parâmetro não mexe no problema da
independência). Cada modelo foi procurado numa grelha explícita (Tabela 6.1): 39, 13 e 41 configurações, 37 minutos
no total. Cada configuração foi treinada no treino de cada fold e avaliada no trimestre seguinte, por isso a procura
respeita o tempo e nunca vê o teste. O objetivo é a média simples da PR-AUC dos 4 folds. A regra de escolha, entre as
configurações a 0,005 da melhor, é ficar com a mais simples. Quando a escolha caía na ponta de uma grelha, alargámos
essa grelha uma vez. Usámos grid search porque permite declarar exatamente o espaço e o procedimento, como pede o
enunciado.

#### Secção 5: otimizado contra o inicial

Só adotávamos uma configuração nova se batesse a da Task 3 por mais de 0,005
em média (ganho relevante) e em pelo menos 3 dos 4 folds (estável). Nenhuma passou (Tabela 6.2). No boosting, a escolha
da procura é −0,002 e ganha 1 fold; na random forest, +0,001 nos 4 folds; na árvore, +0,002 em 3 folds. Os resultados
são planos: 31 das 39 configurações do boosting ficam a 0,005 da melhor. A procura confirmou as configurações da
Task 3, que já estavam no planalto. O modelo final é o gradient boosting da Task 3 (profundidade 6, learning rate 0,1,
200 iterações, folha mínima 100). Como estava a 0,003 da random forest, aplicámos o desempate fixado antes da procura,
o melhor pior fold: 0,575 contra 0,567. Também é cerca de quatro vezes mais rápido a treinar.

#### Secção 6: o threshold

O score só vira alerta quando há um threshold. Dos critérios do enunciado, usámos a
restrição de taxa de alertas: o threshold faz soar alerta em 10% das sessões, ou seja, o operador inspeciona cerca de
100 em cada 1.000. Não usámos uma função de custo porque não temos os custos reais, e teríamos de inventar um rácio.
Também não maximizámos o F1, porque ele dá o mesmo peso a precision e recall sem razão operacional, nem impusemos um
recall mínimo, que deixaria a carga de trabalho em aberto. O orçamento de alertas é a única quantidade que um operador
consegue fixar diretamente. O threshold foi calculado nas previsões out-of-fold juntas: cada uma das 235.472 sessões
de validação foi pontuada pelo modelo treinado no treino do seu próprio fold. O percentil 90 desses scores é 0,490. A
Tabela 6.3 compara-o com o threshold por defeito, 0,50: em desenvolvimento são quase iguais (alertas 9,7% contra
10,0%, precision 0,747 contra 0,740, recall 0,395 contra 0,403, F1 0,517 contra 0,522). Isto acontece porque os scores
deste modelo são quase probabilidades, e cerca de 10% das sessões têm risco acima de 0,5. O F1 seria máximo perto de
0,3, mas aí o modelo marcaria muito mais do que 10% das sessões. Para o operador, 10% quer dizer 74,0 falhas reais e
26,0 falsos alertas em cada 100 inspeções, enquanto 109,8 de 183,8 falhas por 1.000 sessões passam sem alerta. Lido
como probabilidade, 0,490 equivale a dizer que uma falha não detetada custa mais ou menos o mesmo que uma inspeção
inútil (rácio 1,04).

#### Secção 7: calibração

O threshold só usa o score como ordem, mas um operador pode lê-lo como risco, por isso
verificámos. O Brier score é 0,103, contra 0,150 de uma constante. Em dez faixas, o score médio e a percentagem real de
falhas diferem no máximo 0,015, e na faixa de cima, onde estão os alertas, 0,738 previsto bate com 0,740 observado.
Não acrescentámos calibração, porque uma calibração que mantém a ordem dos scores marcaria exatamente as mesmas 10%
das sessões.

#### Secções 8 e 9: congelar e avaliar o teste uma vez

Escrevemos o modelo, as 27 features e o threshold no ficheiro
`prepared/task4_frozen.json` a 27/10/2026 às 11:40:32, antes de ler o teste. Depois treinámos o modelo em todas as
346.931 sessões de desenvolvimento cujo resultado já se sabia antes de 1/10/2021 e avaliámos o teste (80.081 sessões,
17,6% anormais) uma vez (Tabela 6.4). O modelo tem PR-AUC 0,532, três vezes o acaso e +0,152 acima da B1 (0,381); a
B0 tem 0,178. A margem sobre a B1 é maior do que em desenvolvimento, mas o valor absoluto desce 0,128 em relação ao
fold 4 (0,660), cerca de 27 erros padrão, por isso é uma mudança real nesse trimestre e não ruído. A B1 desce ainda
mais. Com o threshold sem mudanças, o modelo marca 7,4% das sessões em vez de 10%, com precision 0,677 e recall 0,286.
Reportámos isto tal como saiu e não mudámos nada.

#### Secção 10: o que o modelo usa

Medimos a importância por permutação: baralhamos as colunas de um grupo e vemos
quanto a PR-AUC cai, nos trimestres de validação. O histórico do posto domina (cai 0,366), o do utilizador vem a
seguir (0,097, e o seu papel diminui de 0,108 no fold 1 para 0,067 no fold 4), o local custa 0,012 e o calendário, a
concorrência e o tempo menos de 0,002 cada (Figura 6.3). A variável mais importante é a taxa de falhas do posto no
último dia (0,196). A ordem bate com a ablação da Task 3, embora os tamanhos sejam diferentes, porque os dois métodos
respondem a perguntas diferentes: a permutação mede quanto este modelo usa um grupo, e a ablação mede o que se perde
quando se treina de novo sem ele. Há três limites. Variáveis correlacionadas dividem a importância entre si. O método
mede uso, não causa. E descreve o modelo na validação, antes da mudança vista no teste.

#### Secções 11 a 13

Conclusões, ficheiros gravados e, na Secção 13, a tabela final de comparação e a descrição do
modelo que aparecem no capítulo 8.

### Task 5 passo a passo (Parte 5)

#### Secção 2: escolher o modelo final e a baseline

A escolha usa só os resultados de desenvolvimento. Só a random
forest (0,622) fica a menos de 0,005 do boosting (0,626), por isso a decisão vem da estabilidade e do custo: o boosting
tem melhor pior fold (0,575 contra 0,567), menor variação entre folds (0,038 contra 0,042) e um treino quatro vezes
mais barato (3,3 s contra 12,4 s por fold, Secção 6.2). A interpretabilidade não os separa, porque os dois são
ensembles de árvores, e o modelo mais legível, a árvore, está 0,028 atrás, mais de cinco vezes a tolerância. Para o
operador a escolha não muda nada no trabalho diário, porque o mesmo threshold de 10% transforma qualquer um dos dois
rankings em alertas. A baseline é a B1: conhecida no início, não aprende nada e é o que um operador podia usar hoje.

#### Secções 3 e 4: refit e teste

Treinámos o modelo de novo em todo o desenvolvimento com as decisões fixas e
pontuámos o teste com o mesmo ficheiro congelado. Os números da Task 4 voltaram exatamente iguais. Tudo o que vem a
seguir é descritivo: usa as etiquetas do teste para descrever o modelo congelado e não muda nenhuma escolha.

#### Secção 5: o modelo final contra a baseline

A Tabela 7.1 tem todas as medidas pedidas. A B1 também precisa de um
threshold, por isso demos-lhe o mesmo critério do modelo (10% em desenvolvimento, o que dá 0,393). Como os dois
thresholds dão números de alertas diferentes no teste, a tabela também mostra a B1 e a B0 com o mesmo número de
alertas do modelo:

| Medida | Modelo final | B1 (threshold 0,393) | B1 (mesmos alertas) | B0 (mesmos alertas) |
| --- | --- | --- | --- | --- |
| PR-AUC | 0,532 | 0,381 | 0,381 | 0,178 |
| Precision / recall | 0,677 / 0,286 | 0,504 / 0,225 | 0,509 / 0,215 | 0,180 / 0,076 |
| F1 | 0,402 | 0,311 | 0,302 | 0,107 |
| Balanced accuracy / MCC | 0,628 / 0,373 | 0,589 / 0,251 | 0,585 / 0,248 | 0,501 / 0,003 |
| Alertas | 7,4% | 7,8% | 7,4% | 7,4% |
| Certos / falsos / falhados por 1.000 | 50,3 / 24,0 / 125,6 | 39,5 / 38,9 / 136,4 | 37,8 / 36,4 / 138,1 | 13,4 / 60,9 / 162,5 |

O modelo bate a B1 em todas as medidas. Com o mesmo número de alertas, dá mais 12,4 alertas certos e menos 12,4 falsos
por 1.000 sessões. O ganho em PR-AUC é de 0,152, com intervalo bootstrap de 95% entre 0,145 e 0,158, e no teste de
McNemar o modelo acerta sozinho em 4.283 sessões, contra 2.223 da B1. Como sessões do mesmo posto e do mesmo dia não
são independentes, estes números mostram o tamanho do ganho e não um p-valor exato. A balanced accuracy e o MCC estão
bem acima do acaso, mas são moderados, porque a especificidade alta (0,971) esconde um recall baixo.

#### Secção 6: ao longo do tempo

O teste parece muito pior do que o desenvolvimento (0,532 contra 0,635 pooled e
0,660 no fold 4), mas a maior parte da queda é aritmética. A PR-AUC sobe com a percentagem de anormais, que era 21,1%
no fold 4 e é 17,6% no teste. Aplicando o lift do fold 4 à percentagem do teste, esperaríamos 0,550, por isso 87% da
queda vem da percentagem e 13% de um lift mais baixo. A ordenação enfraqueceu um pouco, como mostra a ROC-AUC, que não
depende da percentagem: 0,794 no teste contra 0,825 a 0,844 nos folds. Por mês, o modelo dá 0,553, 0,483 e 0,551, sem
tendência de descida dentro do trimestre (Figura 7.2).

#### Secção 7: por grupos

O modelo fica acima da B1 nos três distritos (ganhos de 0,144 a 0,189) e nas 12 estações do
teste (0,083 a 0,269). Tongxiang, com 47,9% das sessões e só 12,0% anormais, tem a PR-AUC mais baixa (0,474). Os alertas
seguem os postos que mais falham: os nove postos com mais alertas recebem 46,4% deles. O grupo mais fraco são os
utilizadores novos (12,9% do teste), com PR-AUC 0,394 contra 0,551 dos que voltam e recall 0,146 contra 0,307. O modelo
dá-lhes menos alertas porque não tem histórico deles. É o problema do cold start.

#### Secção 8: onde o modelo falha

No teste há 4.026 verdadeiros positivos, 1.921 falsos positivos, 10.062 falsos
negativos e 64.072 verdadeiros negativos. Os falsos positivos parecem verdadeiros positivos, e as falhas não detetadas
parecem sessões normais. Nos dois tipos de alerta, a sessão mediana começa cerca de um minuto e meio depois de uma
sessão anormal no mesmo posto; nas falhas não detetadas, 6,9 horas depois. As sessões que começam menos de 6 horas
depois de uma falha no posto (38,3% do teste) têm 91,7% dos falsos alertas e recall 0,445. Depois de 6 horas, o recall
cai para 0,02 a 0,05, e esses períodos calmos têm 52,9% das falhas não detetadas (Figura 7.3). Usámos a `end_cause` só
para descrever os erros, nunca como preditor: o recall vai de 0,19 nas falhas de control loop a 0,50 nas de DC
switching. Em resumo, o modelo reage a um posto que está a falhar agora e não vê falhas que chegam sem aviso.

#### Secção 9: interpretação

Repetimos a importância por permutação no teste e a ordem mantém-se: o histórico do posto
tira 0,271, o do utilizador 0,114, o local 0,009 e o resto menos de 0,001. Também usámos partial dependence, que não
está nos slides e usámos como versão "com modelo" das curvas por decis da Task 1: o score médio sobe muito quando a taxa
de 1 dia do posto passa 0,3. Os dois métodos descrevem como o modelo usa as entradas, não o que causa as falhas, e
dividem a importância entre janelas correlacionadas.

#### Secção 10: o threshold na prática

Num dia médio do teste, o threshold dá 65 alertas em 870 sessões, dos quais 21
são falsos, e 109 sessões anormais passam sem alerta. Os alertas vêm de cerca de 20 postos por dia, por isso o número
de inspeções é menor do que o de alertas, mas varia de 18 a 210 alertas por dia, acompanhando as falhas. Se um falso
alerta custa 1 e uma falha não detetada custa c, o modelo sai mais barato do que não dar alertas quando c > 0,48 e
mais barato do que alertar tudo quando c < 6,4, por isso é útil numa gama larga de custos. Também descrevemos o que
dariam outros orçamentos (5%, 10%, 20%), mas só como descrição: o threshold 0,490 ficou e nenhum threshold saiu dali.

### Capítulo 8: o modelo final e a reprodutibilidade

A Tabela 8.1 junta todos os modelos avaliados nos quatro trimestres, com as baselines. Só três linhas têm valor de
teste (modelo final, B1, B0), porque o teste foi usado uma vez. A Tabela 8.2 descreve o que é preciso para reconstruir
o modelo. Dados: desenvolvimento de 1/4/2020 a 30/9/2021 em quatro folds com purga, treino final em 346.931 sessões e
teste de outubro a dezembro de 2021. Preprocessing: códigos ordinais para local e distrito aprendidos no treino, o
resto sem transformação, sem imputação, sem reamostragem e sem pesos. Features: 27 (histórico do posto 8, utilizador
10, tempo 4, calendário 2, local 2, concorrência 1). Hiperparâmetros: os do boosting acima, seed 42. Threshold: 0,490.
Calibração: nenhuma. O reproducibility statement (Secção 8.3) diz como repetir tudo: Python 3.12.3, as versões fixadas
em `requirements.txt`, o CSV com o seu SHA-256, seed 42 e o notebook corrido do início ao fim. Também diz que as
corridas de reprodução pontuaram o teste outra vez com o mesmo ficheiro congelado, deram os mesmos números e não
serviram para escolher nada.

### Capítulo 9: a síntese

Responde à pergunta do projeto: a informação do início da sessão permite uma ordenação útil dos postos que estão a
falhar agora, sobretudo graças ao histórico do posto, mas não vê falhas sem aviso, e a força do sinal muda no tempo.
As limitações incluem o tempo diário tratado como previsão, os postos novos que ficaram sem teste, a privacidade do
histórico do utilizador, os scores de desenvolvimento otimistas, o teste de um só trimestre, os custos desconhecidos e
as 13 causas juntas. As recomendações são três: pedir ao operador os custos reais e a capacidade diária antes de mudar
o threshold (sempre em dados de desenvolvimento), treinar o modelo de novo com regularidade e vigiar a ordenação, e
juntar dados que o ficheiro não tem, como o registo de manutenção dos postos ou telemetria, para apanhar falhas depois
de períodos calmos.

### Se só tens 30 minutos

- Afinámos três modelos (boosting, random forest, árvore) com grid search nos mesmos 4 folds. Nenhuma afinação ganhou
  mais de 0,005 de forma estável, por isso ficou a configuração da Task 3.
- O modelo final é o gradient boosting (profundidade 6, lr 0,1, 200 iterações, folha 100), com 27 features. Ganhou à
  random forest pelo melhor pior fold (0,575 contra 0,567).
- O threshold 0,490 faz soar alerta em 10% das sessões de desenvolvimento, escolhido nas previsões out-of-fold. Quase
  igual a 0,50, porque os scores estão bem calibrados (Brier 0,103).
- Congelado a 27/10 às 11:40:32. O teste foi avaliado uma vez: 0,532 contra 0,381 (B1) e 0,178 (B0).
- No teste: 7,4% de alertas, precision 0,677, recall 0,286, F1 0,402, balanced accuracy 0,628, MCC 0,373. Por 1.000
  sessões: 50,3 alertas certos, 24,0 falsos e 125,6 falhas não detetadas.
- A queda face ao desenvolvimento é 87% aritmética (menos anormais no teste). A ROC-AUC mostra uma pequena perda real
  (0,794 contra 0,825 a 0,844).
- Acima da B1 em todos os distritos e estações. O grupo mais fraco são os utilizadores novos (recall 0,146).
- Erros: o modelo apanha falhas logo a seguir a outra falha no posto e falha as que chegam depois de períodos calmos
  (52,9% das falhas não detetadas).
- O histórico do posto domina a importância. A permutação mede uso, não causa.
- É útil para custos de falha entre 0,48 e 6,4 vezes o custo de um falso alerta. Recomendações: custos reais, refit
  regular, dados de manutenção.

### Liga com

Esta parte usa tudo o que veio antes: as features e a regra "aprender só no treino" da Task 1, os folds, as métricas e
a B1 da Task 2, e o vencedor e a tolerância da Task 3.

### Perguntas prováveis sobre as Tasks 4 e 5

1. **Porque é que nenhuma configuração afinada ficou?**
   Só aceitávamos uma configuração nova se ganhasse mais de 0,005 em média e em pelo menos 3 dos 4 folds. Nenhuma
   passou: o boosting afinado ficou −0,002, a random forest +0,001 e a árvore +0,002. Os resultados são planos (31 das
   39 configurações do boosting estão a 0,005 da melhor), por isso a Task 3 já estava no planalto. Ver Secção 6.2.

2. **Porque é que o threshold vem de um orçamento de 10% e não do máximo de F1?**
   O F1 dá o mesmo peso a precision e recall sem razão operacional, e o seu máximo, perto de 0,3, marcaria muito mais
   do que 10% das sessões. O orçamento é a quantidade que o operador consegue controlar: quantas inspeções pode fazer.
   O valor de 10% é o do meio dos três orçamentos do protocolo e o último em que os alertas a mais acertam mais do que
   falham. Ver Secção 6.3.

3. **Porque é que 0,490 é quase igual a 0,50?**
   Porque os scores do modelo estão próximos de probabilidades (Brier 0,103, desvios até 0,015) e cerca de 10% das
   sessões têm risco acima de 0,5. É uma coincidência deste modelo, não uma propriedade do 0,50. Ver Secções 6.3 e 6.4.

4. **Precisaram de calibrar o modelo?**
   Verificámos e não. Na faixa de cima, onde estão os alertas, o score médio é 0,738 e a percentagem real 0,740. Além
   disso, uma calibração que mantém a ordem marcaria as mesmas 10% de sessões, por isso não mudaria os alertas. Ver
   Secção 6.4.

5. **Porque é que a PR-AUC do teste é mais baixa do que a de desenvolvimento?**
   Sobretudo porque o teste tem menos anormais (17,6% contra 21,1% no fold 4), e a PR-AUC sobe com essa percentagem.
   Com o lift do fold 4 esperávamos 0,550, por isso 87% da queda vem daí. A ROC-AUC, que não depende da percentagem,
   mostra uma pequena perda real (0,794 contra 0,825 a 0,844). Ver Secção 7.3.

6. **Garantem que o teste foi usado uma vez só, se o voltaram a pontuar?**
   A avaliação oficial é a de 27/10, feita depois de congelar as escolhas no ficheiro. As corridas seguintes usaram o
   mesmo ficheiro congelado sem mudanças, deram exatamente os mesmos números, estão declaradas no reproducibility
   statement e não serviram para escolher nada. O que o enunciado proíbe é mudar modelos, features, hiperparâmetros ou
   thresholds depois de ver o teste, e isso não aconteceu. Ver Secções 6.5 e 8.3.

7. **Que falhas é que o modelo não apanha e porquê?**
   As que chegam depois de um período calmo no posto. Depois de 6 horas sem falhas, o recall cai para 0,02 a 0,05, e
   esses períodos têm 52,9% das falhas não detetadas. O modelo apoia-se no histórico recente do posto, e sem uma falha
   recente não há aviso. Também falha mais com utilizadores novos (recall 0,146). Ver Secções 7.3 e 7.4.

8. **O que é que a importância por permutação pode e não pode dizer?**
   Diz quanto este modelo usa cada grupo de variáveis: o histórico do posto domina. Não diz o que causa as falhas, e
   variáveis correlacionadas dividem a importância entre si, por isso uma janela isolada parece menos importante do
   que é. Por isso baralhámos grupos inteiros. Ver Secções 6.6 e 7.5.

9. **O modelo é útil para um operador?**
   Sim, como ordenação dos postos que estão a falhar agora. Num dia médio dá 65 alertas em 870 sessões, 21 deles
   falsos, vindos de cerca de 20 postos. Sai mais barato do que não dar alertas ou alertar tudo para custos de falha
   entre 0,48 e 6,4 vezes o de um falso alerta. Não é um detetor completo: deixa passar 109 falhas por dia. Ver
   Secção 7.6.

10. **Porque escolheram o gradient boosting e não a random forest, se estão empatados?**
    Estavam dentro da tolerância (0,626 contra 0,622), por isso aplicámos o desempate fixado antes: o melhor pior fold
    (0,575 contra 0,567). O boosting também varia menos entre folds e treina cerca de quatro vezes mais depressa, o que
    facilita treinar de novo com regularidade. Ver Secções 6.2 e 7.1.

---

## Perguntas comuns (todos têm de saber responder)

1. **Qual é a pergunta do projeto e qual é a vossa resposta, em duas frases?**
   A pergunta é até que ponto a informação disponível no início de uma sessão permite prever que ela vai acabar mal. A
   nossa resposta é que permite uma ordenação útil dos postos que estão a falhar agora (PR-AUC de 0,532 no teste,
   contra 0,381 da melhor regra simples), mas não deteta falhas que chegam sem aviso no histórico do posto. Ver
   capítulo 9.

2. **Porque só usam informação do início da sessão?**
   Porque a previsão é feita quando a sessão começa, e o enunciado só permite o que se sabe nesse momento. As colunas
   do fim (energia, custos, hora de fim) separam muito bem as classes (ROC-AUC 0,82 a 0,85), mas é por descreverem o
   resultado; usá-las seria leakage e os resultados seriam falsos. Ver Secção 2.1.

3. **Porque dividiram os dados pelo tempo e não ao acaso?**
   Porque o volume, a percentagem de anormais e o tipo de avaria mudam ao longo dos dois anos, e porque o modelo vai
   ser usado em sessões futuras. Ao acaso, o modelo veria o futuro durante o treino e pareceria melhor do que é. Ver
   Secções 2.4 e 4.5.

4. **Porque é que a PR-AUC é a métrica principal?**
   Porque as falhas são a minoria (cerca de 18%) e o que interessa é que os alertas no topo da lista sejam falhas
   reais. A PR-AUC mede exatamente isso e ignora os verdadeiros negativos. O seu valor ao acaso é a percentagem de
   anormais, por isso lemo-la sempre ao lado dela. Ver Secção 4.4.

5. **Que modelo ganhou e por quanto?**
   O gradient boosting com 27 features. Em desenvolvimento tem 0,626 contra 0,511 da B1 (+0,115, melhor nos quatro
   folds). No teste tem 0,532 contra 0,381 (+0,152), e bate a B1 em todos os distritos e estações. Ver Tabela 8.1.

6. **Como garantiram que o teste foi usado uma só vez?**
   Retirámos o teste logo depois de ler o ficheiro, em todas as tasks. Escolhemos tudo com os quatro folds de
   desenvolvimento, gravámos as escolhas num ficheiro a 27/10 às 11:40:32 e só depois avaliámos o teste. Nada mudou a
   seguir. As corridas de reprodução usaram o mesmo ficheiro e deram os mesmos números. Ver Secções 6.5 e 8.3.

7. **Porque entregaram um só notebook?**
   O enunciado pede notebook(s) completo(s) e reprodutível(is), e a mensagem da professora fala de "notebook e
   relatório". Juntámos as cinco tasks por ordem num notebook único, sem mudar nenhuma célula de código, e corremo-lo
   do início ao fim num ambiente novo. Os números de teste ficaram iguais aos de 27/10. Ver Secção 8.3.

8. **Quais são as principais limitações?**
   O tempo meteorológico é diário e foi tratado como previsão. Não pudemos testar postos novos, porque todos os postos
   do teste já existiam no treino. O teste é um só trimestre. Os custos reais dos erros e a capacidade do operador não
   estão nos dados, por isso o orçamento de 10% é uma escolha nossa. As 13 causas de avaria estão juntas e o modelo
   deteta algumas muito pior do que outras. Ver capítulo 9.

9. **O que recomendam para melhorar?**
   Pedir ao operador os custos reais e a capacidade diária antes de mudar o threshold, e fazê-lo sempre em dados de
   desenvolvimento. Treinar o modelo de novo com regularidade e vigiar a ordenação, porque a ROC-AUC desceu no teste.
   Juntar dados que o ficheiro não tem, como o registo de manutenção dos postos ou telemetria, para apanhar falhas
   depois de períodos calmos. Ver capítulo 9.

10. **E um posto novo, sem histórico?**
    Não o conseguimos avaliar, porque todos os postos de validação e teste já estavam no treino. Esperamos que o modelo
    funcione pior, como acontece com os utilizadores novos (recall 0,146 contra 0,307), porque o sinal principal é o
    histórico do posto. É uma limitação declarada. Ver Secções 3.1 e 7.3.

11. **Porque não usaram uma rede neuronal ou outro modelo mais avançado?**
    O enunciado valoriza uma comparação pequena e bem justificada mais do que muitos algoritmos, e os métodos vêm dos
    slides da disciplina. Além disso, a regressão logística (0,593) e a árvore (0,597) chegam quase ao mesmo valor
    sendo muito diferentes, e a afinação não ajudou. Isso sugere que o limite está na informação disponível e não na
    complexidade do modelo. Ver Secções 5.2 e 6.2.

12. **O que fariam com mais tempo?**
    O mesmo que recomendamos: obter custos e capacidade reais, testar o modelo em mais trimestres e, se possível, em
    postos novos, e separar as causas de avaria para ver se alguns tipos se preveem melhor sozinhos. Tudo sem tocar no
    teste atual. Ver capítulo 9.

---

## Plano de ensaio (30 minutos, em pares)

1. Cada pessoa lê em voz alta o núcleo comum de outra, em 5 minutos, e a outra corrige se algo estiver errado.
2. Durante 10 minutos, a pessoa A faz 10 perguntas da parte da pessoa B (escolhidas ao acaso, misturando as da
   parte dela com as comuns). B responde sem notas. A confere com a resposta modelo e aponta o que faltou.
3. Trocam de papéis durante mais 10 minutos.
4. Nos últimos 5 minutos, cada um escreve as perguntas em que hesitou e volta a ler essa parte do guião.

A meta é responder bem a pelo menos 8 de 10 perguntas da própria parte e 7 de 10 das comuns. Se uma pergunta é sobre
a parte de outra pessoa, a resposta modelo diz onde ler.
