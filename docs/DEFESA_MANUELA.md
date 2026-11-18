# Defesa do Projeto 1: a parte da Manuela (Tasks 4 e 5)

Preparação para a defesa individual. O guião dos slides 9 a 12 está em `docs/GUIAO_APRESENTACAO.md`, e a explicação
completa das Tasks 4 e 5, com 10 perguntas e respostas, está em `docs/GUIAO_ESTUDO.md` (Parte da Manuela). Este
ficheiro junta o que o professor pediu, o que o enunciado exige nas tuas tasks, onde está cada coisa no código e as
perguntas que vêm do código. A Secção 8 explica os conceitos de ML que aparecem nestas tasks, do mais simples
ao mais técnico, e a Secção 9 faz o mesmo para os conceitos do resto do trabalho (Tasks 1 a 3).

## 1. O que o professor pediu

Pela mensagem dele:

- **Os slides não são obrigatórios.** O que conta é o código: vamos projetar os notebooks e ele faz perguntas a cada
  um sobre o que fez.
- **Como temos slides,** ele vai fazendo perguntas enquanto apresentamos, em conversa informal. Pode interromper a
  meio de um slide e pedir para ver o código desse ponto.
- **Cerca de 10 minutos de perguntas por pessoa.** Os teus slides duram cerca de 4:45, por isso a maior parte do tempo
  vai ser conversa e código. Ele não vai ouvir o guião de seguida.
- **As perguntas são sobre o que tu fizeste.** Tens de saber dizer, sem hesitar, qual foi o teu trabalho e explicar
  qualquer célula das Partes 4 e 5.

Na prática, ele vai querer ver três coisas:

1. **Que percebes o código e não só o resultado.** Ele aponta para uma célula e pergunta "o que faz isto?" ou "porque
   é que está assim?".
2. **Que cada decisão tem uma razão e um número.** Responde sempre por esta ordem: a decisão, o número que a sustenta e
   o que não fizemos e porquê.
3. **Que cumpriram as regras do enunciado,** sobretudo a do teste usado uma só vez e a do threshold escolhido sem ver o
   teste. São os pontos em que ele mais vai insistir na Task 4.

## 2. O que fizeste, segundo os commits

O professor vai perguntar "o que é que fizeste?". Convém responderes com a mesma frase que os teus colegas usam para
ti, por isso combinem-na antes. Os commits mostram isto:

| Commit | Data | O que mostra |
| --- | --- | --- |
| `ede6a52` (Inês) | 26/10 | Primeira versão do `Task4.ipynb` (84 células) |
| `14db8b2` (tu) | 27/10 | Task 4 reestruturada (71 células), procura corrida, `task4_frozen.json` gravado às 11:40:32, figuras e capítulo 6 do relatório |
| `7e5c9b1` (tu) | 28/10 | Task 4 final (75 células, Secção 13 com a tabela final), revisão das Tasks 1 a 4 e do relatório |
| `c093d9f` (Inês) | 28/10 | Primeira versão do `Task5.ipynb` |
| `8c7e7ac` (tu) | 29/10 | Task 5 corrida e integrada no relatório (capítulos 7 a 9) e reprodutibilidade verificada |
| vários (tu) | 02/10 a 29/10 | Relatório (`main.tex`), figuras, decision log e integração das 5 tasks |

Uma resposta honesta: *"A Inês fez a primeira versão dos notebooks das Tasks 4 e 5. Eu reestruturei a Task 4: a procura
em grelha, a regra para aceitar uma configuração nova, o threshold, a calibração e o ficheiro congelado antes do teste.
Depois corri e integrei a Task 5 no relatório e escrevi o relatório final."* Ajusta a frase ao que fizeste mesmo:
ele vai perguntar pormenores sobre aquilo que disseres que foi teu.

## 3. O que o enunciado exige e onde está no código

Tem os notebooks abertos no `Task4.ipynb` e no `Task5.ipynb`. Os números das secções são os mesmos no
`MINDD_Project1.ipynb` (Partes 4 e 5).

### Task 4

| O enunciado pede | Onde está | O que respondes |
| --- | --- | --- |
| Escolher 2 ou 3 modelos promissores | Secção 3 | Gradient boosting, random forest e árvore: os dois melhores ensembles e o melhor modelo individual, com três princípios diferentes. Fora: stacking (0,015 atrás e caro), regressão logística (as penalizações davam o mesmo) e Naive Bayes (o único parâmetro não resolve o problema da independência) |
| A procura usa só treino e validação | Secção 4.1, `run_search` → `cv_run` | Cada configuração é treinada no treino de cada fold e avaliada no trimestre seguinte. O teste nem está carregado: `assert df["start_time"].max() < TEST_START` |
| Respeitar a ordem temporal | Secção 2.1, `temporal_folds` | Os mesmos 4 folds de janela crescente da Task 2. Não há splits aleatórios nem early stopping interno (`early_stopping=False` em `make_boosting`), porque o early stopping separa uma validação aleatória |
| Espaço de procura explícito | Secção 4.1, `GRID_VALUES` | Grelha completa: 36, 12 e 40 configurações. Quando a escolhida fica na ponta de um intervalo, `extend_if_on_edge` acrescenta um valor além dessa ponta uma vez (`EDGE_VALUES`). No fim ficam 39, 13 e 41, 37 minutos no total |
| Métrica adequada à classe positiva | Secção 2.2 | Média simples da PR-AUC dos 4 folds, a métrica principal da Task 2 |
| Mostrar a configuração escolhida e o procedimento | Secções 4.2 a 4.5, `select_simplest` | Entre as configurações a 0,005 da melhor, fica a mais simples (`ORDER`, `SORT_KEY`) |
| Otimizado contra inicial: ganho relevante e estável? | Secção 5, célula com `VERDICTS` | `meaningful = ganho médio > 0,005` e `stable = ganhou em pelo menos 3 de 4 folds`. Nenhuma passou: −0,002, +0,001 e +0,002. Fica o boosting da Task 3 (profundidade 6, lr 0,1, 200 iterações, folha 100) |
| Um critério de threshold | Secção 6.1 | Restrição de taxa de alertas: 10% das sessões. Não usámos custo (custos desconhecidos), máximo de F1 (pesa igual precision e recall sem razão operacional, e o máximo perto de 0,3 dá muito mais alertas) nem recall mínimo (deixa a carga de trabalho em aberto) |
| Threshold escolhido em previsões de dados não usados no treino | Secção 6.2, `OOF_P`, `CUT_OFF` | Previsões out-of-fold: cada uma das 235.472 sessões de validação é pontuada pelo modelo do seu fold. `CUT_OFF` é o k-ésimo maior score, com k = 10% de 235.472, e dá 0,4899 |
| Default 0,50 contra o escolhido: precision, recall, F1, alertas, certos, falsos e falhados por 1.000 | Secção 6.3 | Quase iguais em desenvolvimento: alertas 9,7% contra 10,0%, precision 0,747 contra 0,740, recall 0,395 contra 0,403 |
| Consequências operacionais | Secção 6.4 | Em cada 100 inspeções há 74 falhas reais e 26 falsos alertas. Lido como probabilidade, 0,490 corresponde a um rácio de custos de 1,04 |
| Calibração, se o score for lido como probabilidade | Secção 7, `calibration_curve` | Brier 0,103 contra 0,150 de uma constante, desvio máximo 0,015, faixa de cima 0,738 previsto contra 0,740 observado. Não calibrámos, porque uma calibração que mantém a ordem marcaria as mesmas 10% |
| Fixar e aplicar sem mudanças ao teste | Secção 8, `FROZEN_CHOICES` → `prepared/task4_frozen.json` | Gravado a 27/10 às 11:40:32, antes de ler o teste: modelo, hiperparâmetros, 27 features, cut-off, sem calibração |
| Avaliar o teste uma vez | Secção 9 | Carrega o JSON congelado, treina de novo nas 346.931 sessões com resultado conhecido antes de 1/10/2021 e pontua o teste. `assert "TEST_SCORED" not in globals()` impede uma segunda avaliação na mesma sessão |
| Interpretar o modelo e dizer os limites | Secção 10, `permutation_drop` | Permutação por grupos nos trimestres de validação: histórico do posto 0,366, do utilizador 0,097, local 0,012, o resto < 0,002. Limites: variáveis correlacionadas dividem a importância, o método mede uso e não causa, e descreve a validação, antes da mudança do teste |

### Task 5

| O enunciado pede | Onde está | O que respondes |
| --- | --- | --- |
| Escolher o modelo final só com treino e validação: desempenho, estabilidade temporal, custo, interpretabilidade, consequências operacionais | Secções 2.1 e 2.2 | Só a random forest (0,622) fica a menos de 0,005 do boosting (0,626). Desempate pelo melhor pior fold (0,575 contra 0,567), menor variação (0,038 contra 0,042) e treino 4 vezes mais barato (3,3 contra 12,4 s por fold). A interpretabilidade não os separa; a árvore está 0,028 atrás |
| Escolher uma baseline adequada | Secção 2.4 | B1: a taxa de falha do posto a 7 dias. É conhecida no início, não aprende nada e é o que um operador podia usar hoje |
| Treinar de novo em todo o desenvolvimento, com tudo fixo | Secção 3 | Mesmo ficheiro congelado. O SHA-256 do JSON é verificado nas Secções 1, 3, 4 e 12, e o refit dos 4 folds devolve 0,6258 e o cut-off 0,489886, iguais aos da Task 4 |
| Comparar com a baseline: PR-AUC, precision, recall, F1, balanced accuracy, MCC, alertas, certos/falsos/falhados por 1.000 | Secção 5.1, `confusion_metrics`, `top_k_flags` | Modelo 0,532 contra B1 0,381 e B0 0,178. Precision 0,677, recall 0,286, F1 0,402, BA 0,628, MCC 0,373, 7,4% de alertas, 50,3 / 24,0 / 125,6 por 1.000. A B1 também é mostrada com o mesmo número de alertas (`top_k_flags`), para a comparação ser justa |
| A diferença é fiável? | Secção 5.2 | Bootstrap de 95% do ganho: 0,145 a 0,158. McNemar: o modelo acerta sozinho em 4.283 sessões, contra 2.223 da B1. Sessões do mesmo posto e dia não são independentes, por isso isto mostra o tamanho do ganho e não um p-valor exato |
| Variação no tempo | Secção 6 | Teste 0,532 contra 0,660 no fold 4. 87% da queda vem da percentagem de anormais (21,1% para 17,6%); com o lift do fold 4 esperávamos 0,550. A ROC-AUC mostra uma pequena perda real: 0,794 contra 0,825 a 0,844. Por mês: 0,553, 0,483 e 0,551 |
| Variação por grupos (distritos, postos) | Secção 7 | Acima da B1 nos 3 distritos (+0,144 a +0,189) e nas 12 estações (+0,083 a +0,269). 9 postos recebem 46,4% dos alertas. Utilizadores novos: recall 0,146 contra 0,307 (cold start) |
| Análise de erros: falsos positivos e falsos negativos | Secção 8 | TP 4.026, FP 1.921, FN 10.062, TN 64.072. Alertas certos e falsos começam cerca de 1,5 min depois de uma falha no posto; falhas sem alerta, 6,9 h depois. Depois de 6 h sem falhas o recall cai para 0,02 a 0,05, e estes períodos têm 52,9% das falhas sem alerta. A `end_cause` só serve para descrever os erros |
| Interpretar o modelo e os limites | Secção 9 | Permutação no teste: posto 0,271, utilizador 0,114, local 0,009. Partial dependence: o score sobe muito quando a taxa de 1 dia do posto passa de 0,3. Mede uso, não causa |
| Consequências do threshold e utilidade | Secção 10 | Num dia médio há 65 alertas em 870 sessões (21 falsos), vindos de cerca de 20 postos. O modelo é mais barato do que não dar alertas para c > 0,48 e do que alertar tudo para c < 6,37 |
| Conclusões, limitações e recomendações | Secção 11 e capítulo 9 do relatório | Em parte, sim. Recomendações: custos reais, refit regular, dados de manutenção |

## 4. Percurso no código (se ele pedir para mostrar)

Tem estas células prontas para ires lá diretamente:

1. `Task4.ipynb` Secção 4.1: `GRID_VALUES` e `extend_if_on_edge`. Mostra que o espaço de procura é explícito.
2. Secção 5: a célula com `meaningful` e `stable`. É a regra que decidiu manter a Task 3.
3. Secção 6.2: `OOF_P` e `CUT_OFF`. Mostra que o threshold vem de previsões out-of-fold.
4. Secção 8: `FROZEN_CHOICES` e o `write_text` do JSON. Abre também o `prepared/task4_frozen.json` e mostra o `frozen_at`.
5. Secção 9: o `assert "TEST_SCORED" not in globals()`, o JSON lido e `dev_train = df[df["end_time"] < TEST_START]`.
6. `Task5.ipynb` Secção 5.1: a tabela final contra a B1.
7. Secção 8.3: onde se concentram os erros (as 6 horas).

## 5. Perguntas que vêm do código

Estas não estão no guião de estudo. Juntas com as 10 perguntas da tua parte no `GUIAO_ESTUDO.md`.

1. **Porque não usaram o `GridSearchCV` do scikit-learn?**
   Os folds são de janela crescente, com burn-in e purga, e precisávamos de guardar as previsões de cada fold para
   escolher o threshold out-of-fold e para a regra dos 3 em 4 folds. O nosso `cv_run` faz o mesmo que uma grid search
   com splits fixos, mas guarda a PR-AUC por fold, o tempo e as previsões. A grid search não foi dada nas aulas; foi
   pesquisa nossa, e o relatório diz isso.

2. **Porque `early_stopping=False` no boosting?**
   O early stopping do `HistGradientBoostingClassifier` separa uma parte aleatória do treino para validar, o que mistura
   tempos e muda o número de iterações de fold para fold. Com ele desligado, o número de iterações é um hiperparâmetro
   da grelha, igual em todos os folds.

3. **Porque `HistGradientBoostingClassifier` e não o `GradientBoostingClassifier`?**
   Aceita valores em falta (NaN) diretamente, por isso não precisamos de imputação, trata as categorias com
   `categorical_features` e é muito mais rápido com 350 mil linhas. As colunas de histórico têm NaN quando ainda não há
   histórico; imputar seria inventar um valor.

4. **Que pré-processamento tem o modelo final?**
   Só o `tree_view`: códigos ordinais para `location` e `district`, aprendidos no treino de cada fold (categoria nova
   = −1, tratada como em falta). O resto passa sem mudanças: sem scaling, sem imputação, sem reamostragem e sem pesos. As
   árvores não precisam de scaling, e o desequilíbrio é tratado no threshold, não nos dados.

5. **Como calculas o cut-off, linha a linha?**
   Junto as previsões out-of-fold dos 4 folds (235.472 sessões), ordeno os scores do maior para o menor e fico com o
   k-ésimo, com k = 10% do total. Um alerta é score ≥ cut-off, e isso dá 0,4899. Aplicado a cada fold, dá entre 7,7% e
   12,2% de alertas, porque a percentagem de anormais muda de fold para fold.

6. **Porque é que no teste o modelo só marca 7,4% e não 10%?**
   Porque o cut-off é fixo e o teste tem menos anormais (17,6%) e uma ordenação um pouco mais fraca, por isso há menos
   sessões acima de 0,490. O enunciado diz para aplicar o threshold sem mudanças, e por isso não o reajustámos. Mostrámos
   outros orçamentos só como descrição.

7. **O que é a purga em `dev_train`?**
   Uma sessão de desenvolvimento só entra no treino final se acabou antes de 1/10/2021. Se acabasse depois, o resultado
   dela só se sabia já dentro do período de teste. A regra é a mesma dos folds da Task 2.

8. **Como provas que o ficheiro congelado não foi mexido depois do teste?**
   O `frozen_at` diz 2026-10-27T11:40:32, e o commit `14db8b2` desse dia já tem o ficheiro. A Task 5 verifica o SHA-256
   do JSON em quatro secções. As corridas de reprodução pontuaram o teste outra vez com o mesmo ficheiro, deram os
   mesmos números e não serviram para escolher nada; o reproducibility statement (Secção 8.3 do relatório) declara-o.

9. **A importância por permutação foi calculada em que dados?**
   Na Task 4, nos trimestres de validação, com os modelos de cada fold. Na Task 5, no teste, com o modelo final, só para
   descrever. Baralhamos grupos inteiros de colunas juntos (`permutation_drop`), porque as janelas de 1, 7 e 30 dias
   estão correlacionadas e, baralhadas uma a uma, cada uma parecia pouco importante.

10. **Porque o 10% e não o 5% ou o 20%?**
    São os três orçamentos do protocolo da Task 2, e escolhemos o do meio. O 10% é o último em que os alertas a mais
    ainda acertam mais vezes do que falham. Os outros dois aparecem na Secção 6.4 só como contexto, para um operador
    com mais ou menos capacidade.

## 6. Pontos fracos: assume-os antes que ele os aponte

- **A otimização não melhorou nada.** É um resultado, não uma falha: a grelha é plana (31 das 39 configurações do
  boosting estão a 0,005 da melhor), por isso a Task 3 já estava no planalto. A regra para aceitar foi fixada antes da
  procura.
- **O teste foi pontuado mais de uma vez.** A avaliação oficial é a de 27/10. As outras foram reproduções com o mesmo
  ficheiro e os mesmos números, e nenhuma escolha mudou. O enunciado proíbe mudar modelo, features, hiperparâmetros ou
  threshold depois de ver o teste, e isso não aconteceu.
- **Recall baixo (0,286).** O modelo deixa passar 125,6 falhas em cada 1.000 sessões. Isto vem do orçamento de 10%, que
  é uma escolha, e das falhas sem aviso, que nenhuma variável do início da sessão consegue ver.
- **Com c = 10, o valor do laboratório de avaliação, alertar tudo sai mais barato** (824,1 contra 1.280,5 por 1.000
  sessões). O modelo é útil para custos de falha entre 0,48 e 6,37 vezes o de um falso alerta, e por isso a primeira
  recomendação é pedir os custos reais ao operador.
- **Ensembles, grid search, permutation importance e partial dependence não foram dados nas aulas.** O relatório diz
  isso em cada caso ("not covered in class; our research led us to it"). Explica-os com conceitos das aulas: o
  bagging está no MINDD-04 (bootstrap) e a permutação é uma ablação sem treinar de novo.
- **Só um trimestre de teste.** Uma única janela de 3 meses não mostra a variação sazonal. Por isso recomendamos treinar
  de novo com regularidade e vigiar a ordenação.

## 7. Os números de bolso

| | |
| --- | --- |
| Modelo final | HistGradientBoosting, profundidade 6, lr 0,1, 200 iterações, folha 100, seed 42, 27 features |
| Desenvolvimento (média dos 4 folds) | PR-AUC 0,626; pior fold 0,575; ROC-AUC 0,825 a 0,844 por fold |
| Cut-off | 0,4899 (10% das 235.472 previsões out-of-fold) |
| Calibração | Brier 0,103, sem calibrador |
| Congelado | 27/10/2026 às 11:40:32, `prepared/task4_frozen.json` |
| Treino final / teste | 346.931 sessões / 80.081 sessões (17,6% anormais), outubro a dezembro de 2021 |
| Teste | PR-AUC 0,532 (B1 0,381, B0 0,178), ROC-AUC 0,794 |
| No cut-off | 7,4% de alertas, precision 0,677, recall 0,286, F1 0,402, BA 0,628, MCC 0,373 |
| Por 1.000 sessões | 50,3 certos, 24,0 falsos, 125,6 falhados (B1 com os mesmos alertas: 37,8 / 36,4 / 138,1) |
| Erros | 52,9% das falhas sem alerta chegam depois de mais de 6 h sem falhas no posto |
| Utilidade | Mais barato do que as alternativas para c entre 0,48 e 6,37 |

## 8. Conceitos de ML, do simples ao técnico

Cada conceito tem três níveis. **Simples** é o que dizes a alguém que nunca ouviu falar de ML. **A fundo** é a
resposta normal na defesa. **Técnico** é para quando o professor insistir. No fim de cada um, **No projeto** liga o
conceito aos nossos números. Se ficares bloqueada, começa pelo nível simples e sobe a partir daí.

### 8.1 As bases

#### Classificador e score

- **Simples:** é um programa que olha para uma sessão e diz "isto vai correr mal" ou "isto vai correr bem".
- **A fundo:** o modelo não dá logo um sim ou não. Dá um número entre 0 e 1, o score, que diz quão arriscada é a
  sessão. Só depois, com um threshold, esse número passa a ser um alerta.
- **Técnico:** é uma função aprendida f(x) → [0, 1], com x as 27 features da sessão no início, treinada para
  minimizar a log-loss. Se o score estiver bem calibrado, pode ler-se como P(anormal | x).
- **No projeto:** o score do boosting, e o alerta quando score ≥ 0,4899.

#### Treino, validação e teste

- **Simples:** é como estudar para um exame. Estudas com os exercícios (treino), testas-te com exercícios que não viste
  (validação) e no fim fazes o exame a sério, uma vez (teste).
- **A fundo:** o treino serve para o modelo aprender. A validação serve para nós escolhermos: que modelo, que
  hiperparâmetros, que threshold. O teste só serve para medir no fim, e se o usássemos para escolher, o resultado
  ficava otimista.
- **Técnico:** cada vez que um conjunto de dados influencia uma escolha, o erro medido nele deixa de ser uma estimativa
  sem viés do erro em dados novos. Por isso o teste fica fechado até tudo estar congelado.
- **No projeto:** desenvolvimento de 1/4/2020 a 30/9/2021, em 4 folds; teste de outubro a dezembro de 2021, avaliado
  uma vez depois do `task4_frozen.json`.

#### Overfitting

- **Simples:** é decorar as respostas em vez de perceber a matéria. Corre bem nos exercícios conhecidos e mal no exame.
- **A fundo:** um modelo muito complexo aprende o ruído do treino. Por isso limitamos a profundidade das árvores e
  exigimos um mínimo de sessões por folha.
- **Técnico:** é o compromisso entre viés e variância. Mais complexidade reduz o viés e aumenta a variância. Os
  hiperparâmetros de regularização (`max_depth`, `min_samples_leaf`, `learning_rate`) controlam esse compromisso.
- **No projeto:** tirar o `post_id` melhorou a PR-AUC (+0,011), porque o modelo deixou de decorar postos.

#### Leakage

- **Simples:** é fazer batota sem querer: usar informação que, na vida real, ainda não existe no momento da previsão.
- **A fundo:** a energia, o custo e a duração separam muito bem as classes, mas só se sabem quando a sessão acaba. Usá-los
  daria um modelo ótimo no papel e inútil na prática.
- **Técnico:** há dois tipos. Leakage de features: variáveis que dependem do resultado. Leakage de pré-processamento:
  aprender algo (códigos, thresholds, médias) com dados de validação ou de teste. Evitamos o segundo pondo tudo num
  `Pipeline`, ajustado só no treino de cada fold.
- **No projeto:** só entram variáveis do início da sessão; o `OrdinalEncoder` é aprendido no treino de cada fold.

#### Parâmetros e hiperparâmetros

- **Simples:** os parâmetros são o que o modelo aprende sozinho. Os hiperparâmetros são os botões que nós rodamos
  antes de ele aprender.
- **A fundo:** num boosting, as regras de cada árvore são parâmetros. A profundidade máxima, o número de árvores e a
  learning rate são hiperparâmetros, e foram esses que procurámos na Task 4.
- **Técnico:** os parâmetros saem da otimização da função de perda no treino. Os hiperparâmetros escolhem-se fora
  dela, por validação. Por isso a procura usa os folds e não o treino.

### 8.2 Avaliar no tempo

#### Divisão temporal e folds de janela crescente

- **Simples:** o modelo vai ser usado no futuro, por isso testamo-lo sempre com dados que vêm depois dos de treino.
- **A fundo:** um K-fold aleatório punha sessões de outubro no treino e de setembro na validação. Como sessões próximas
  no tempo se parecem (o mesmo posto avariado), o resultado ficava otimista. Usamos 4 folds em que o treino começa
  sempre em abril de 2020 e vai crescendo, e a validação é sempre o trimestre seguinte.
- **Técnico:** é validação "expanding window" (forward chaining). Fold 1: treino de abril a setembro de 2020,
  validação no 4.º trimestre de 2020. Fold 2: validação no 1.º trimestre de 2021. Fold 3: no 2.º trimestre de 2021.
  Fold 4: no 3.º trimestre de 2021. Os resultados são resumidos pela média simples, pelo desvio padrão e pelo pior fold.
- **No projeto:** 235.472 sessões de validação ao todo; PR-AUC média 0,626, pior fold 0,575.

#### Burn-in e purga

- **Simples:** o burn-in é deitar fora o início, em que os dados ainda estão "frios". A purga é tirar as sessões que
  estão a meio quando muda o período.
- **A fundo:** de janeiro a março de 2020 as colunas de histórico ainda estão incompletas, porque há poucas sessões
  para trás. A purga tira do treino as sessões que começaram antes do corte mas acabaram depois, porque o resultado
  delas ainda não se sabia no momento do corte.
- **Técnico:** sem purga, o rótulo de uma sessão de treino seria conhecido depois do início da validação, o que é
  leakage pelo rótulo. A regra é `end_time < início da validação` (ou `< TEST_START` no treino final).
- **No projeto:** entre 27 e 39 sessões purgadas por fold; treino final em 346.931 sessões.

#### Previsões out-of-fold

- **Simples:** é a nota que o modelo tem em exercícios que nunca viu.
- **A fundo:** cada sessão de validação recebe o score do modelo treinado só com o passado desse fold. Juntando os 4
  folds, temos um score "honesto" para 235.472 sessões, e é com ele que escolhemos o threshold.
- **Técnico:** se escolhêssemos o threshold com scores de sessões usadas no treino, eles estariam inflacionados
  (o modelo já as viu) e o threshold ficava mal posto. O enunciado exige previsões de dados não usados para ajustar
  o modelo.
- **No projeto:** `OOF_P` na Secção 6.2 da Task 4.

### 8.3 As métricas

#### Matriz de confusão

- **Simples:** uma tabela com os quatro casos possíveis: avisei e era falha (TP), avisei e não era (FP), não avisei e
  era falha (FN), não avisei e não era (TN).
- **A fundo:** todas as métricas com threshold (precision, recall, F1, BA, MCC) saem destes quatro números.
- **No projeto:** no teste, TP 4.026, FP 1.921, FN 10.062, TN 64.072.

#### Accuracy, e porque não a usamos

- **Simples:** é a percentagem de acertos. Parece boa, mas engana.
- **A fundo:** só 18,6% das sessões são anormais. Um modelo que diz sempre "normal" acerta 81% e não serve para nada.
- **Técnico:** com classes desequilibradas, a accuracy é dominada pela classe maioritária. Por isso o protocolo usa
  métricas centradas na classe positiva.

#### Precision e recall

- **Simples:** a precision é "dos alertas que dei, quantos eram mesmo falhas?". O recall é "das falhas que houve,
  quantas apanhei?".
- **A fundo:** há um compromisso. Baixar o threshold dá mais alertas: o recall sobe e a precision desce. Subir faz o
  contrário.
- **Técnico:** precision = TP / (TP + FP); recall = TP / (TP + FN). O recall também se chama sensibilidade ou taxa de
  verdadeiros positivos.
- **No projeto:** no teste, precision 0,677 (cerca de 2 em cada 3 alertas são falhas reais) e recall 0,286 (apanhamos
  cerca de 1 em cada 3,5 falhas).

#### F1

- **Simples:** uma nota única que junta precision e recall.
- **A fundo:** é a média harmónica das duas, por isso fica baixa se uma delas for baixa.
- **Técnico:** F1 = 2PR / (P + R). Dá o mesmo peso aos dois erros, e por isso não o usámos para escolher o threshold:
  sem custos reais, não há razão para dizer que um falso alerta e uma falha perdida valem o mesmo. O enunciado pede-o na
  comparação final e por isso aparece na Task 5.
- **No projeto:** F1 0,402 no teste, contra 0,311 da B1.

#### Curva PR e PR-AUC

- **Simples:** em vez de olhar para um só threshold, vemos todos e medimos a área. Quanto maior, melhor o modelo
  ordena as sessões de risco.
- **A fundo:** a curva mostra a precision para cada valor de recall. A área por baixo (PR-AUC) resume-a num número. É a
  nossa métrica principal porque só olha para a classe positiva, a que interessa.
- **Técnico:** calculamos com `average_precision_score`, que é a média das precisions em cada ponto em que o recall sobe
  (soma de (R_n − R_{n−1}) · P_n), sem interpolação. Não depende do threshold, só da ordem dos scores.
- **No projeto:** 0,626 em desenvolvimento, 0,532 no teste.

#### No-skill, baseline e lift

- **Simples:** um modelo às cegas tem uma PR-AUC igual à percentagem de falhas. O nosso tem de ficar bem acima disso, e
  também acima de uma regra simples.
- **A fundo:** a B0 é o acaso: PR-AUC = percentagem de anormais (0,178 no teste). A B1 é a regra que um operador já
  podia usar, a taxa de falha do posto a 7 dias, sem treino nenhum (0,381).
- **Técnico:** o lift é a PR-AUC a dividir pela percentagem de anormais. Como a PR-AUC sobe com essa percentagem, só se
  podem comparar períodos diferentes pelo lift. No fold 4 o lift era 0,660 / 0,211 ≈ 3,1; aplicado à percentagem do
  teste dá 0,550, por isso 87% da queda até 0,532 vem da percentagem.

#### ROC-AUC

- **Simples:** a probabilidade de, entre uma sessão anormal e uma normal escolhidas ao acaso, o modelo dar mais risco à
  anormal.
- **A fundo:** 0,5 é o acaso e 1 é perfeito. Ao contrário da PR-AUC, não muda com a percentagem de anormais, e por isso
  serve para ver se a ordenação piorou mesmo.
- **Técnico:** é a área da curva TPR contra FPR. Com classes desequilibradas pode parecer otimista, porque a FPR tem
  muitos negativos no denominador. Por isso é complementar e não principal.
- **No projeto:** 0,825 a 0,844 por fold e 0,794 no teste: houve uma pequena perda real de ordenação.

#### Balanced accuracy e MCC

- **Simples:** são versões "justas" da accuracy, que não se deixam enganar pela classe grande.
- **A fundo:** a balanced accuracy é a média do recall nas falhas e nas normais. O MCC é uma correlação entre o que
  previmos e o que aconteceu: 0 é o acaso e 1 é perfeito.
- **Técnico:** BA = (recall + especificidade) / 2 = (0,286 + 0,971) / 2 ≈ 0,628. MCC = (TP·TN − FP·FN) /
  √((TP+FP)(TP+FN)(TN+FP)(TN+FN)), que usa as quatro células. O protocolo da Task 2 não as usava para escolher, mas
  o enunciado pede-as na comparação final.
- **No projeto:** BA 0,628 e MCC 0,373 no teste; a B0 dá 0,501 e 0,003, ou seja, acaso.

#### Calibração e Brier score

- **Simples:** um modelo está calibrado quando, das sessões a que dá 70% de risco, cerca de 70% falham mesmo.
- **A fundo:** verificamos dividindo os scores em 10 faixas e comparando o score médio com a percentagem real de falhas
  em cada uma. Se não batesse certo, aplicávamos um calibrador (Platt ou isotónica).
- **Técnico:** o Brier é a média de (score − resultado)², e quanto mais baixo melhor. Uma constante igual à percentagem
  de anormais dá p(1 − p) ≈ 0,150. Um calibrador monótono não muda a ordem dos scores, por isso não mudaria quais são as
  10% de sessões com alerta.
- **No projeto:** Brier 0,103; desvio máximo 0,015; faixa de cima 0,738 previsto contra 0,740 real. Não calibrámos.

### 8.4 Os modelos

#### Árvore de decisão

- **Simples:** uma sequência de perguntas de sim ou não: "o posto falhou nas últimas 24 h?", "são mais de 20 h?"… Cada
  caminho acaba numa folha com uma percentagem de falhas.
- **A fundo:** em cada nó, a árvore escolhe a pergunta que melhor separa normais de anormais. Se crescer sem limite,
  decora o treino; por isso limitamos a profundidade e o mínimo de sessões por folha.
- **Técnico:** a separação escolhe-se pela maior redução de impureza (Gini ou entropia). É fácil de ler, mas instável:
  uma pequena mudança nos dados pode mudar a árvore toda (variância alta).
- **No projeto:** a melhor árvore ficou a 0,028 do boosting, mais de 5 vezes a tolerância.

#### Ensembles

- **Simples:** em vez de perguntar a um especialista, perguntas a muitos e juntas as respostas.
- **A fundo:** muitas árvores juntas erram menos do que uma só. Há duas formas principais: em paralelo (bagging) e em
  sequência (boosting).
- **Técnico:** o bagging reduz sobretudo a variância; o boosting reduz sobretudo o viés. Os ensembles não foram dados
  nas aulas; o bagging liga-se ao bootstrap do MINDD-04.

#### Bagging e random forest

- **Simples:** treinas 200 árvores, cada uma com uma amostra um pouco diferente dos dados, e fazes a média do que dizem.
- **A fundo:** cada árvore vê uma amostra com reposição (bootstrap) e, em cada nó, só um subconjunto aleatório das
  features. Isso torna as árvores diferentes entre si, e a média delas é mais estável.
- **Técnico:** a variância da média de árvores pouco correlacionadas é menor do que a de uma árvore. O `max_features`
  controla essa correlação. Hiperparâmetros procurados: `min_samples_leaf` e `max_features`.
- **No projeto:** 0,622, a 0,003 do boosting, e 4 vezes mais lenta a treinar (12,4 s contra 3,3 s por fold).

#### Boosting e gradient boosting

- **Simples:** treinas uma árvore, vês onde errou, e a árvore seguinte concentra-se em corrigir esses erros. E assim
  200 vezes.
- **A fundo:** cada árvore nova é pequena e corrige um pouco o que as anteriores somadas ainda erram. A learning rate
  diz quanto cada árvore pode corrigir: mais baixa é mais lenta mas mais cuidadosa.
- **Técnico:** é descida de gradiente no espaço das funções. Cada árvore ajusta-se ao gradiente negativo da log-loss
  (os "resíduos" das previsões atuais) e é somada com peso igual à learning rate: F_m(x) = F_{m−1}(x) + η · h_m(x).
  O score final é a sigmoide da soma.
- **No projeto:** o modelo final.

#### HistGradientBoosting e os hiperparâmetros do modelo final

- **Simples:** é uma versão rápida do gradient boosting, que agrupa os valores de cada variável em "caixas" antes de
  procurar as perguntas.
- **A fundo:** como agrupa os valores (até 255 caixas por variável), é muito mais rápido com 350 mil linhas. Também
  aceita valores em falta: aprende para que lado da pergunta devem ir as sessões sem histórico.
- **Técnico:** os nossos valores: `max_depth=6` (cada árvore faz até 6 perguntas seguidas), `learning_rate=0.1`,
  `max_iter=200` (200 árvores, cada uma com no máximo 31 folhas, o valor por defeito), `min_samples_leaf=100` (cada folha tem pelo menos 100 sessões, para não decorar casos
  raros), `early_stopping=False` (o early stopping usaria uma validação aleatória e mudava o número de árvores de fold
  para fold) e `random_state=42`.

### 8.5 A otimização

#### Grid search

- **Simples:** experimentas todas as combinações de botões numa lista e ficas com a melhor.
- **A fundo:** definimos para cada modelo uma grelha de valores e treinámos cada combinação nos 4 folds. É a forma mais
  transparente de cumprir o "espaço de procura explícito" do enunciado.
- **Técnico:** com poucos hiperparâmetros, a procura exaustiva é viável (93 configurações, 37 minutos). Uma random
  search ou uma otimização bayesiana só compensam com espaços maiores. A grid search não foi dada nas aulas; o
  relatório diz isso.

#### Tolerância, regra da mais simples e planalto

- **Simples:** se duas opções estão praticamente empatadas, escolhes a mais simples.
- **A fundo:** diferenças abaixo de 0,005 de PR-AUC são do tamanho do ruído entre folds. Para mudar de configuração,
  exigimos mais de 0,005 de ganho e ganhar em pelo menos 3 dos 4 folds.
- **Técnico:** com só 4 folds não há potência para um teste estatístico, por isso usámos uma regra fixa antes da
  procura. "Planalto" quer dizer que muitas configurações dão quase o mesmo: 31 das 39 do boosting ficam a 0,005 da
  melhor, por isso afinar não podia ganhar muito.

### 8.6 O threshold

#### O que é e porque não fica em 0,5

- **Simples:** é a linha a partir da qual o score vira alerta. O 0,5 é só o valor por defeito; não tem nada de
  especial.
- **A fundo:** o threshold certo depende do que custa cada erro e de quantos alertas o operador consegue tratar. Mudar o
  threshold não muda o modelo, só o compromisso entre precision e recall.
- **Técnico:** com probabilidades calibradas e custo c de uma falha perdida contra 1 de um falso alerta, o threshold
  que minimiza o custo esperado é 1 / (1 + c). O nosso 0,490 corresponde a c ≈ 1,04.

#### Orçamento de alertas

- **Simples:** o operador diz "consigo verificar 10% das sessões", e o modelo marca as 10% mais arriscadas.
- **A fundo:** é o critério "operational alert-rate constraint" do enunciado. Escolhemo-lo porque não temos os custos,
  e a capacidade é algo que o operador consegue fixar diretamente.
- **Técnico:** o threshold é o percentil 90 dos scores out-of-fold. No teste dá 7,4% e não 10%, porque o threshold é
  fixo e a distribuição dos scores mudou. O enunciado proíbe reajustá-lo.

#### Análise de custos

- **Simples:** verificamos para que custos o modelo compensa mais do que "nunca avisar" ou "avisar sempre".
- **A fundo:** com um falso alerta a custar 1 e uma falha perdida a custar c, o modelo é a opção mais barata para c
  entre 0,48 e 6,37. Para custos de falha maiores, compensa mais avisar quase tudo.
- **No projeto:** com c = 10, o valor do laboratório, alertar tudo sai mais barato. Por isso a primeira recomendação é
  pedir os custos reais ao operador.

### 8.7 A interpretação

#### Permutation importance

- **Simples:** baralhas uma coluna, para o modelo passar a ver lixo nela, e medes quanto piora. Se piorar muito, o
  modelo usava essa coluna.
- **A fundo:** baralhámos grupos inteiros de colunas (todo o histórico do posto, por exemplo), porque as janelas de 1, 7
  e 30 dias dizem quase o mesmo. Baralhando só uma, o modelo usava as outras e ela parecia pouco importante.
- **Técnico:** importância = PR-AUC original − PR-AUC com o grupo permutado, com várias repetições. Funciona com
  qualquer modelo (model-agnostic). Mede o uso, não a causa, e com features correlacionadas a importância divide-se
  entre elas.
- **No projeto:** baralhar o histórico do posto tira 0,366 de PR-AUC na validação e 0,271 no teste.

#### Permutação contra ablação

- **Simples:** a ablação treina o modelo de novo sem o grupo; a permutação estraga o grupo num modelo já treinado.
- **A fundo:** respondem a perguntas diferentes. A ablação diz quanto se perde se nunca tivermos aquela informação. A
  permutação diz quanto este modelo depende dela. Por isso os tamanhos são diferentes, mas a ordem é a mesma.

#### Partial dependence

- **Simples:** mostra como o risco previsto muda quando mexemos numa só variável e deixamos o resto igual.
- **A fundo:** pomos a taxa de falha do posto a 1 dia com o mesmo valor em todas as sessões, calculamos o score médio, e
  repetimos para vários valores. A curva mostra a forma do efeito.
- **Técnico:** PD(v) = média de f(x com x_j = v). Assume que a variável pode mudar sem mudar as outras, o que é falso
  para janelas correlacionadas, e mostra só o efeito médio. Não foi dada nas aulas.
- **No projeto:** o score sobe muito quando a taxa de 1 dia do posto passa de 0,3.

### 8.8 A comparação com a baseline

#### Intervalo bootstrap

- **Simples:** repetimos o teste muitas vezes com amostras ligeiramente diferentes para ver quanto o ganho podia variar.
- **A fundo:** tiramos amostras com reposição das sessões do teste, calculamos o ganho em cada uma e ficamos com os 95%
  do meio.
- **Técnico:** percentis 2,5 e 97,5 da distribuição bootstrap da diferença de PR-AUC. Assume sessões independentes,
  o que não é verdade (o mesmo posto no mesmo dia), por isso o intervalo real é mais largo.
- **No projeto:** ganho de 0,152, entre 0,145 e 0,158.

#### Teste de McNemar

- **Simples:** contamos as sessões em que só o modelo acerta e aquelas em que só a B1 acerta.
- **A fundo:** as sessões em que os dois acertam ou os dois erram não dizem nada sobre quem é melhor. Só contam as
  discordâncias.
- **Técnico:** usámos a versão exata: um teste binomial às discordâncias b e c, com p = 0,5 (`binomtest` no código). A
  versão clássica é o qui-quadrado (b − c)² / (b + c). Mesmo sendo exato, o teste assume sessões independentes, e
  sessões do mesmo posto e do mesmo dia não o são. Por isso lemos o tamanho da diferença e não confiamos no p-valor.
- **No projeto:** 4.283 sessões em que só o modelo acerta, contra 2.223 em que só a B1 acerta.

### 8.9 O que muda no tempo e nos grupos

#### Mudança de distribuição

- **Simples:** o mundo muda. O que o modelo aprendeu em 2020 pode valer menos no fim de 2021.
- **A fundo:** no teste há menos falhas (17,6% contra 21,1% no fold 4) e a ordenação piorou um pouco (ROC-AUC 0,794).
  A maior parte da queda da PR-AUC é só por haver menos falhas.
- **Técnico:** distinguimos a mudança da percentagem da classe (prior shift), que mexe na PR-AUC mas não na ROC-AUC, de
  uma mudança na relação entre as features e o resultado (concept drift), que mexe nas duas. Vimos sobretudo a primeira
  e um pouco da segunda. A resposta é treinar de novo com regularidade e vigiar a ordenação.

#### Cold start

- **Simples:** o modelo conhece mal quem chega pela primeira vez, porque não tem histórico dessa pessoa.
- **A fundo:** para os utilizadores novos, as colunas de histórico do utilizador estão vazias e o modelo só tem o posto,
  o tempo e o local. Dá-lhes menos alertas e apanha menos falhas.
- **No projeto:** utilizadores novos (12,9% do teste): recall 0,146 contra 0,307 dos que voltam.

## 9. Conceitos do resto do trabalho (Tasks 1 a 3)

O professor pode puxar qualquer coisa do trabalho, porque as Tasks 4 e 5 assentam em tudo o que veio antes. Os
conceitos da Secção 8 (leakage, folds, purga, métricas, árvores e ensembles) não se repetem aqui. O formato é o mesmo:
**Simples**, **A fundo**, **Técnico** e **No projeto**.

### 9.1 Perceber e preparar os dados (Task 1)

#### Auditoria da qualidade dos dados

- **Simples:** antes de usar os dados, verificar se estão bem: linhas repetidas, valores impossíveis, datas trocadas.
- **A fundo:** o enunciado exige investigar antes de corrigir. Um valor estranho pode ser um erro ou um caso real, e
  apagar casos reais tira informação ao modelo.
- **Técnico:** para cada problema seguimos três passos: detetar, perceber a causa e decidir com base no significado da
  variável. Cada decisão ficou registada no decision log.
- **No projeto:** tabs a mais em datas e em 18.370 locais (corrigidos ao ler); nenhum duplicado verdadeiro; 17 pares da
  mesma conta em dois postos no mesmo segundo, que são frotas e ficaram. Nenhuma linha foi apagada.

#### Construir o target

- **Simples:** o ficheiro não dizia que sessões correram mal, por isso tivemos de definir a regra.
- **A fundo:** das 15 causas de fim, "Charging ends normally" e "User stops charging" são normais, e as outras 13 são
  avarias. O utilizador parar conta como normal, porque foi escolha dele.
- **Técnico:** validámos a regra contra as colunas de histórico do próprio dataset, recontando as falhas anteriores com
  ela. Bateu em 100,00% (posto) e 99,98% (utilizador); com a alternativa, só em 0,26% e 35,85%.
- **No projeto:** 18,58% de anormais, ou seja, 1 para cada 4,4 normais.

#### Desequilíbrio de classes, e porque não reamostrámos

- **Simples:** há muito menos sessões anormais do que normais, e o modelo podia ignorá-las.
- **A fundo:** há três formas de lidar com isso: mudar os dados (oversampling, undersampling, SMOTE), dar mais peso à
  classe rara no treino, ou deixar os dados como estão e tratar o desequilíbrio na métrica e no threshold. Escolhemos a
  terceira.
- **Técnico:** reamostrar ou dar pesos desloca as probabilidades, que deixam de corresponder à percentagem real, e
  depois era preciso recalibrar. O SMOTE interpola entre sessões e criaria casos impossíveis, como meia flag ou um posto
  entre dois postos. A PR-AUC e o threshold por orçamento já tratam o desequilíbrio sem mexer nos dados.
- **No projeto:** o modelo final ficou calibrado sem correção (Brier 0,103), o que confirma a escolha.

#### Valores em falta

- **Simples:** células vazias. Antes de as encher, é preciso perceber porque estão vazias.
- **A fundo:** aqui o vazio quer dizer "isto nunca aconteceu", como as horas desde a última falha de um posto que nunca
  falhou. Não é falta de informação, é informação.
- **Técnico:** é um caso de falta estrutural, não aleatória (missing not at random). Pôr a média seria errado, porque
  diria que o posto falhou há um tempo médio. Nas árvores deixámos o NaN, que o HistGradientBoosting trata de forma
  nativa. Na regressão logística pusemos o máximo do treino ("há muito tempo") e mantivemos a flag de "sem histórico".
- **No projeto:** só 4 colunas têm vazios, e cada vazio coincide com a sua flag.

#### Outliers

- **Simples:** valores muito afastados dos outros. Podem ser erros ou casos reais raros.
- **A fundo:** usámos três olhares: a regra do IQR em cada coluna, a inspeção dos casos extremos um a um e um Isolation
  Forest, que procura sessões raras olhando para várias colunas ao mesmo tempo.
- **Técnico:** a regra de Tukey marca valores fora de [Q1 − 1,5·IQR, Q3 + 1,5·IQR]. O Isolation Forest isola cada ponto
  com cortes aleatórios, e os pontos que se isolam com poucos cortes são anómalos. Como os extremos eram reais, não os
  tirámos. Para os modelos lineares aplicámos `log1p`, que encolhe as caudas sem apagar nada. As árvores não precisam,
  porque só usam a ordem dos valores.
- **No projeto:** as sessões marcadas pelo Isolation Forest eram 60% anormais, ou seja, os "outliers" eram exatamente o
  sinal que queríamos.

#### Variáveis categóricas: encoding

- **Simples:** os modelos só trabalham com números, por isso "distrito A, B, C" tem de virar números.
- **A fundo:** há duas formas. Códigos ordinais (A = 0, B = 1, C = 2) funcionam bem em árvores. One-hot (uma coluna 0/1
  por categoria) é preciso nos modelos lineares, que senão leriam os códigos como uma escala.
- **Técnico:** a lista de categorias aprende-se no treino. Uma categoria nova na validação fica com −1 nas árvores e com
  zeros em todas as colunas no one-hot (`handle_unknown="ignore"`). Com muitas categorias, o one-hot cria muitas colunas
  (a versão linear tinha 126).
- **No projeto:** `location` e `district` com códigos ordinais nas árvores; one-hot no posto e na tarifa na versão linear.

#### Variáveis cíclicas

- **Simples:** a hora 23 está ao lado da hora 0, mas os números 23 e 0 parecem longe um do outro.
- **A fundo:** para um modelo linear, transformamos a hora num ponto de um círculo, com seno e cosseno. Assim as 23 h e
  as 0 h ficam próximas.
- **Técnico:** hora → (sin(2π·h/24), cos(2π·h/24)); o dia da semana o mesmo, com 7. As árvores não precisam disto,
  porque podem cortar em qualquer ponto.

#### Scaling

- **Simples:** pôr todas as colunas numa escala parecida, para nenhuma pesar mais só porque tem números maiores.
- **A fundo:** a regressão logística com penalização precisa disto, porque a penalização castiga coeficientes grandes e
  a escala da variável muda o tamanho do coeficiente. As árvores não precisam.
- **Técnico:** `StandardScaler`: (x − média) / desvio padrão, com a média e o desvio aprendidos só no treino de cada
  fold.

#### Taxas suavizadas

- **Simples:** um posto com 1 falha em 1 sessão não tem 100% de risco; é só pouca informação. A suavização puxa a taxa
  para um valor razoável quando há poucas sessões.
- **A fundo:** as taxas do dataset são (falhas + 1) / (sessões + 5), como se cada posto já tivesse 5 sessões
  imaginárias com 1 falha. Sem histórico, a taxa é 0,2; com 1 falha em 1 sessão, é 0,33.
- **Técnico:** é a média a posteriori com um prior Beta(1, 4): (k + α) / (n + α + β), com α = 1 e β = 4, e a média a
  priori é 0,2. Confirmámo-la nas 6 janelas, com diferença máxima de 1,1 × 10⁻¹⁶.

#### Correlação, multicolinearidade e VIF

- **Simples:** duas variáveis que dizem quase o mesmo. Para alguns modelos isso confunde.
- **A fundo:** usámos a correlação de Spearman (que olha para a ordem e não exige relações lineares) e o VIF, que mede
  quanto uma variável é explicada pelas outras. As árvores e os modelos com penalização lidam bem com isso; uma
  regressão linear sem penalização não.
- **Técnico:** VIF_j = 1 / (1 − R²_j), com R²_j a regressão da variável j em todas as outras. Acima de 10 há
  redundância forte. Na regressão logística, a multicolinearidade torna os coeficientes instáveis, mas não estraga as
  previsões.
- **No projeto:** as janelas de 180 e 730 dias do utilizador chegam a VIF 65,4. Fizemos um conjunto reduzido, com VIF
  máximo de 8,6, para modelos lineares simples.

#### PCA

- **Simples:** junta muitas variáveis parecidas em poucas variáveis novas que resumem a informação.
- **A fundo:** testámos e não usámos: comprimia pouco e misturava o posto com o utilizador, o que tirava a leitura das
  variáveis.
- **Técnico:** a PCA encontra as direções de maior variância (vetores próprios da matriz de covariância dos dados
  normalizados). É não supervisionada: a variância que guarda não tem de ser a que separa as classes.
- **No projeto:** precisava de 11 de 23 componentes para 90% da variância, e a primeira tinha AUC 0,51 (acaso).

#### AUC univariada

- **Simples:** quão bem uma variável sozinha separa as sessões normais das anormais.
- **A fundo:** usámo-la para comparar variáveis entre si e para encontrar o leakage: as variáveis do fim da sessão
  separavam bem demais.
- **Técnico:** é a ROC-AUC com a própria variável como score. Uma AUC abaixo de 0,5 quer dizer que a relação é inversa;
  por isso olha-se para max(AUC, 1 − AUC).
- **No projeto:** variáveis do fim da sessão 0,82 a 0,85; a melhor do início 0,77 (histórico do posto); utilizador 0,69
  a 0,70.

#### Drift ao longo do tempo

- **Simples:** os dados de 2020 não são iguais aos de 2021.
- **A fundo:** mudaram o volume de sessões, a percentagem de anormais e os tipos de avaria. Isto obrigou a dividir por
  tempo e a ler a PR-AUC sempre com a percentagem de anormais.
- **No projeto:** a percentagem mensal de anormais foi de 26,3% a 13,7% e voltou a 22,9%. O que se manteve foi a
  percentagem de falhas de cada posto (Spearman 0,81 entre 2020 e 2021), e é por isso que o histórico do posto
  funciona.

#### Identificadores (key fields)

- **Simples:** colunas como o `UserID` só dizem "quem é", e o modelo podia decorá-las em vez de aprender padrões.
- **A fundo:** o `UserID` saiu porque muitas sessões futuras são de contas que o modelo nunca viu, e porque identifica
  pessoas. O histórico do utilizador é o substituto legítimo. O `post_id` ficou na Task 1 e saiu na Task 3.
- **No projeto:** 61,3% das sessões de teste são de contas que não aparecem no treino.

### 9.2 Definir o problema e a avaliação (Task 2)

#### Formulação do problema

- **Simples:** dizer exatamente o que se prevê, quando e para quê.
- **A fundo:** uma previsão por sessão, no momento em que começa, para ordenar as sessões e os postos por risco e dizer
  aos técnicos onde olhar primeiro. Não é um diagnóstico da avaria.
- **Técnico:** fixar a unidade de observação, o momento de previsão e o uso decide que variáveis são legítimas, que
  métrica faz sentido e como se divide o tempo.

#### Holdout, K-fold e avaliação temporal

- **Simples:** o holdout é separar um bocado dos dados para testar. O K-fold faz isso K vezes, com bocados diferentes.
- **A fundo:** o K-fold aleatório pressupõe que as sessões são independentes e que o futuro se parece com o passado.
  Aqui nenhuma das duas coisas é verdade, por isso usámos folds por tempo (Secção 8.2).
- **Técnico:** o K-fold estratificado mantém a percentagem de anormais em cada fold, mas não resolve a dependência no
  tempo: sessões do mesmo posto na mesma semana caíam no treino e na validação.

#### Agregar os folds

- **Simples:** juntar os resultados dos 4 folds num número só.
- **A fundo:** usámos a média simples, para cada trimestre contar uma vez. Mostrámos também a média ponderada pelo
  número de sessões e o valor pooled (todas as previsões juntas), que serve para o threshold.
- **Técnico:** como a percentagem de anormais muda entre folds, não se comparam folds entre si. Comparam-se dois modelos
  no mesmo fold, com diferenças emparelhadas e folds ganhos.

#### Significância com 4 folds (Wilcoxon)

- **Simples:** com só 4 comparações, não dá para provar estatisticamente que um modelo é melhor.
- **A fundo:** por isso usámos uma tolerância prática (0,005) e a regra de ganhar em pelo menos 3 de 4 folds, em vez de
  p-valores.
- **Técnico:** no teste exato de Wilcoxon com n = 4, há 2⁴ = 16 combinações de sinais. Mesmo que um modelo ganhe os 4
  folds, o p-valor bilateral mínimo é 2/16 = 0,125, acima de 0,05. A escala da tolerância vem do bootstrap: o erro
  padrão de uma PR-AUC é de 0,004 a 0,006.

#### Log-loss

- **Simples:** uma nota que castiga o modelo quando está muito confiante e errado.
- **Técnico:** −média[y·log(p) + (1 − y)·log(1 − p)]. É a função que a regressão logística e o boosting minimizam no
  treino. Aparece como métrica complementar, ao lado do Brier.
- **No projeto:** Naive Bayes 0,839 contra 0,472 da constante: ordena bem, mas as probabilidades são más.

### 9.3 Ablação e modelos (Task 3)

#### Ablação de grupos de features

- **Simples:** juntar os grupos de variáveis um a um e ver quanto cada um ajuda.
- **A fundo:** usámos sempre o mesmo modelo de referência, um gradient boosting sem afinação, para que as diferenças
  venham da informação e não do modelo. Os quatro conjuntos são os do enunciado (S1 a S4).
- **Técnico:** a ablação mede o valor marginal de um grupo dado os que já lá estão, por isso a ordem conta. Treina-se de
  novo em cada passo, ao contrário da permutação (Secção 8.7).
- **No projeto:** S1 0,290; + tarifa +0,0006; + histórico do posto +0,294; + histórico do utilizador +0,031. Sem
  `post_id` e sem tarifa: 0,626 com 27 features.

#### Viés indutivo, ou "princípios diferentes"

- **Simples:** cada tipo de modelo tem uma ideia própria de como o mundo funciona.
- **A fundo:** o enunciado pede pelo menos três princípios. A regressão logística acha que o risco sobe de forma suave
  com as variáveis. O Naive Bayes junta pedaços de evidência como se fossem independentes. A árvore corta em limiares.
- **Técnico:** o viés indutivo é o conjunto de pressupostos que o algoritmo usa para generalizar. Modelos com vieses
  diferentes fazem erros diferentes, e é isso que o stacking aproveita.

#### Regressão logística

- **Simples:** soma as variáveis, cada uma com um peso, e passa o resultado por uma curva em S que dá um número entre 0
  e 1.
- **A fundo:** cada peso diz quanto essa variável sobe ou desce o risco. Precisa de dados normalizados, de `log1p` nas
  caudas e de one-hot nas categorias. A penalização impede pesos exagerados.
- **Técnico:** p = σ(β₀ + Σ βⱼxⱼ), com σ(z) = 1 / (1 + e⁻ᶻ). Os βs minimizam a log-loss mais λ‖β‖² (penalização L2).
  No scikit-learn, C = 1/λ: C menor quer dizer penalização mais forte.
- **No projeto:** C = 0,01 e C = 1 deram o mesmo (0,593), e ficou a penalização mais forte, que é o modelo mais simples.
  Com mais de 100 mil sessões e menos de 50 variáveis, os dados dominam a penalização.

#### Naive Bayes

- **Simples:** calcula o risco multiplicando quanto cada variável, sozinha, faz pensar em "falha", como se não tivessem
  nada a ver umas com as outras.
- **A fundo:** usa o teorema de Bayes e o pressuposto "naive" de que as variáveis são independentes, dada a classe. Aqui
  isso é falso: as janelas de 1, 7 e 30 dias dizem quase o mesmo, e o modelo conta a mesma evidência várias vezes. Por
  isso as probabilidades saem exageradas.
- **Técnico:** P(y | x) ∝ P(y) · Π P(xⱼ | y). Usámos o `CategoricalNB`, com as variáveis numéricas em 10 faixas de igual
  frequência e alpha = 1 (suavização de Laplace, para nenhuma probabilidade ser zero).
- **No projeto:** ordena razoavelmente (ROC-AUC 0,814), mas o Brier é 0,172, pior do que uma constante (0,148).

#### Porque não kNN nem SVM

- **Simples:** os dois eram lentos demais com este volume de dados e obrigavam a deitar fora informação.
- **A fundo:** o kNN compara cada sessão nova com todas as do treino (até 271 mil) e precisa de uma distância que faça
  sentido entre contagens, taxas e categorias. O SVM com kernel demora entre o quadrado e o cubo do número de sessões e
  não dá probabilidades.
- **Técnico:** os dois obrigariam a treinar numa amostra, e a amostra perderia exatamente o histórico onde está o sinal.

#### Stacking

- **Simples:** um modelo "chefe" aprende a combinar as opiniões de outros modelos.
- **A fundo:** juntámos a regressão logística, o Naive Bayes e a árvore, com uma regressão logística por cima a aprender
  quanto confiar em cada um. Não usámos voting (todos com o mesmo peso), porque o Naive Bayes é bem mais fraco.
- **Técnico:** o meta-modelo tem de treinar com previsões de modelos que não viram essas sessões. Uma validação cruzada
  interna aleatória deixaria sessões do futuro influenciar previsões do passado. Por isso, dentro do treino de cada fold,
  cada trimestre é previsto por modelos treinados só com sessões que acabaram antes dele. O meta-modelo recebe o logit
  das três previsões.
- **No projeto:** 0,610: acima dos três componentes, mas 0,015 abaixo do boosting.

#### Privacidade e ética do histórico do utilizador

- **Simples:** guardar o comportamento de cada condutor é sensível, e um condutor pode ficar "marcado" por uma avaria que
  não foi culpa dele.
- **A fundo:** mantivemos o histórico do utilizador porque melhora a ordenação (+0,031), mas só para ordenar sessões
  internamente, nunca para decidir nada sobre um condutor. Há uma alternativa sem esse histórico (0,599).
- **Técnico:** é um perfil de comportamento ligado a uma conta, por isso é um dado pessoal. Isso pede minimização de
  dados, um prazo de retenção e uma finalidade declarada.

#### Reprodutibilidade

- **Simples:** qualquer pessoa que corra o notebook tem de obter os mesmos números.
- **A fundo:** fixámos a seed (42), as versões das bibliotecas (`requirements.txt`) e o SHA-256 do CSV. Cada notebook
  corre sozinho, do início ao fim, a partir dos ficheiros em `prepared/`.
- **Técnico:** todos os passos que aprendem algo estão num `Pipeline` ajustado só no treino. Todas as decisões ficam no
  decision log, e as escolhas finais no ficheiro congelado. Uma corrida nova num ambiente limpo deu 0 diferenças nos
  ficheiros de `prepared/`.
