# Checklist da entrega do Projeto 1

Versão em inglês: `docs/SUBMISSION_CHECKLIST.md`. As duas têm os mesmos itens e o mesmo estado; quem marca um item
marca-o nas duas.

A professora Fátima Rodrigues pediu: "O 1º Projeto (notebook e relatório) 1 fx. zip por grupo, deve ser submetido no
moodle, até às 20:00h, do próximo dia 31 de outubro." Esta lista serve para a reunião de hoje (30/10) e para os
últimos passos de amanhã. Em cada linha, quem a fecha marca `[x]`. Uma linha aberta tem de sair da reunião com dono e
hora. O zip já montado está em `../entrega/MINDD-GPA-1200720-1221579-1231205.zip` (fora do repositório). Na coluna "Todos?", "sim" quer dizer que precisa do acordo dos três.

Uma regra vale para tudo o que se segue: o teste já foi visto a 27/10, por isso a partir daqui só mudamos texto,
figuras e apresentação. Nenhum modelo, feature, hiperparâmetro ou threshold muda.

## Calendário

| Quando | O quê |
| --- | --- |
| Hoje, reunião | Percorrer esta lista, dar dono e hora a cada linha aberta, confirmar nomes e número do grupo |
| Hoje, já feito antes da reunião | Correções da revisão do relatório (spec 007), cada notebook de task corrido sozinho a partir do conteúdo do zip, PDF recompilado, zip refeito com os cinco notebooks |
| Amanhã até às 16:00 | Últimas verificações e teammate check. Se algo obrigar a recompilar, ainda há tempo |
| Amanhã até às 18:00 | Upload no Moodle e captura de ecrã da submissão |
| Amanhã, logo a seguir | Outra pessoa descarrega o zip do Moodle e confirma que abre |

## 0. Cumprimento do enunciado

Fonte: `TP1-MINDD2026_27-Tasks_1+2+3+4+5.pdf`, a versão final do enunciado. Cada linha diz onde o relatório
(`docs/FINAL_REPORT.pdf`) e os notebooks das tasks (`Task1.ipynb` a `Task5.ipynb`) respondem ao pedido. Para verificar, abrimos a
secção indicada e confirmamos que o pedido está lá.

| Feito | Pedido do enunciado | Relatório | Notebook |
| --- | --- | --- | --- |
| [x] | Task 1: tipos e significado das variáveis, valores em falta, duplicados e inconsistências | 2.1, 2.2 | Notebook Task 1, secções 2–4 e 6 |
| [x] | Task 1: distribuição do target, distribuições, outliers investigados antes de agir | 1.1, 2.2, 2.3 | Notebook Task 1, secções 5, 9 e 10 |
| [x] | Task 1: mudanças ao longo do tempo (volume, prevalência, preditores, atividade de postos e utilizadores) e o que implicam | 2.4 | Notebook Task 1, secção 7 |
| [x] | Task 1: figuras interpretadas, não só mostradas | 2.1–2.4 | Notebook Task 1 |
| [x] | Task 1: operações que aprendem com os dados documentadas uma a uma | 3.3 (Tabela de learned operations) | Notebook Task 1, secção 13 |
| [x] | Task 1: síntese no fim da task (problemas, evidência, variáveis mantidas, limitações, implicações) | 9 (Synthesis) | Notebook Task 1, secção 15 |
| [x] | Task 2: unidade de observação, classes, target a partir de `end_cause`, momento e finalidade da previsão | 4.1 | Notebook Task 2, secção 3 |
| [x] | Task 2: classificação das variáveis nas quatro categorias, com cada exclusão justificada | 4.2 | Notebook Task 2, secção 4 |
| [x] | Task 2: consequências do falso positivo e do falso negativo | 4.3 | Notebook Task 2, secção 5 |
| [x] | Task 2: métrica principal, complementares, operacionais e de estabilidade, justificadas | 4.4 | Notebook Task 2, secção 6 |
| [x] | Task 2: estratégia temporal (fronteiras, n.º de folds, tamanhos diferentes, preprocessing dentro do fold, proteção do teste) | 4.5 | Notebook Task 2, secção 7 |
| [x] | Task 2: agregação entre folds (média, variabilidade, ponderado ou pooled, tendência) | 4.6 | Notebook Task 2, secção 8 |
| [x] | Task 2: baseline no-skill e baseline simples, interpretadas | 4.7 | Notebook Task 2, secção 9 |
| [x] | Task 2: protocolo de avaliação resumido antes da otimização | 4.8 | Notebook Task 2, secção 10 |
| [x] | Task 3: ablação dos quatro conjuntos e as cinco perguntas (tarifa, histórico do posto, histórico do utilizador, consistência no tempo, questões operacionais e éticas) | 5.1 | Notebook Task 3, secção 3 |
| [x] | Task 3: pelo menos três princípios de classificação, justificados (tipos de dados, desequilíbrio, pressupostos, interpretabilidade, custo, relações) | 5.2 | Notebook Task 3, secção 4 |
| [x] | Task 3: pelo menos três ensembles de princípios diferentes, stacking sem leakage, porque podem melhorar | 5.3 | Notebook Task 3, secção 5 |
| [x] | Task 4: dois ou três modelos otimizados, espaço de procura explícito, ordem temporal, métrica da classe positiva | 6.1 | Notebook Task 4, secções 3–4 |
| [x] | Task 4: otimizado contra configuração inicial (ganho relevante e estável?) | 6.2 | Notebook Task 4, secção 5 |
| [x] | Task 4: um critério de threshold, escolhido em validação e aplicado sem mudanças ao teste | 6.3 | Notebook Task 4, secção 6 |
| [x] | Task 4: threshold por defeito contra o escolhido (precision, recall, F1, alert rate, valores por 1.000) | 6.3 (Tabela default vs selected) | Notebook Task 4, secção 6 |
| [x] | Task 4: calibração considerada | 6.4 | Notebook Task 4, secção 7 |
| [x] | Task 4: interpretação do modelo final, com limitações | 6.6 | Notebook Task 4, secção 10 |
| [x] | Task 5: escolha do modelo final só com dados de desenvolvimento (desempenho, estabilidade, custo, interpretabilidade, implicações operacionais) e baseline | 7.1 | Notebook Task 5, secção 2 |
| [x] | Task 5: refit em todo o desenvolvimento, decisões fixas, teste avaliado uma vez | 6.5, 7, 8.3 | Notebook Task 4, secções 8–9; Notebook Task 5, secções 3–4 |
| [x] | Task 5: comparação com a baseline em PR-AUC, precision, recall, F1, balanced accuracy, MCC, alert rate e valores por 1.000 | 7.2 (Tabela final vs baseline) | Notebook Task 5, secção 5 |
| [x] | Task 5: desempenho por períodos e por grupos (distritos, postos) | 7.3 | Notebook Task 5, secções 6–7 |
| [x] | Task 5: análise de erros (falsos positivos e falsos negativos) | 7.4 | Notebook Task 5, secção 8 |
| [x] | Task 5: interpretação adequada ao modelo, com limitações | 7.5 | Notebook Task 5, secção 9 |
| [x] | Task 5: consequências práticas do threshold e utilidade para o operador | 7.6 | Notebook Task 5, secção 10 |
| [x] | Task 5: conclusão com resultados, limitações e recomendações | 9 | Notebook Task 5, secção 11 |
| [x] | Entrega: notebook completo e reprodutível | 8.3 | todo o notebook |
| [x] | Entrega: relatório final | `docs/FINAL_REPORT.pdf` | |
| [x] | Entrega: tabela de candidatos, baselines e modelo final | 8.1 | Notebook Task 4, secção 13 |
| [x] | Entrega: descrição do preprocessing, features, hiperparâmetros e threshold finais | 8.2 | Notebook Task 4, secção 13 |
| [x] | Entrega: reproducibility statement | 8.3 | |
| [x] | Entrega: teste usado uma vez e nada mudado depois de o ver | 6.5, 8.3 | Notebook Task 4, secções 8–9 |

Na comparação com o enunciado encontrámos três falhas de texto. Corrigem-se antes de recompilar o PDF:

| Feito | Falha | Como verificar | Quem | Todos? |
| --- | --- | --- | --- | --- |
| [x] | A bibliografia ainda diz "(Tasks 1 to 4)" | No PDF, a entrada do enunciado diz "Tasks 1 to 5" | Manuela | não |
| [x] | A secção 7.1 não falava das implicações operacionais da escolha | A 7.1 tem uma frase sobre o efeito da escolha no trabalho do operador | Manuela | não |
| [x] | As recomendações estavam misturadas com as limitações na Synthesis | O último parágrafo do capítulo 9 diz em texto corrido o que recomendamos | Manuela | não |

## 1. Conteúdo do zip

| Feito | Item | Como verificar | Quem | Todos? |
| --- | --- | --- | --- | --- |
| [x] | O zip tem `Task1.ipynb` a `Task5.ipynb`, `MINDD_TP1_Relatorio.pdf` (relatório em inglês), o `README.md` do zip, `requirements.txt` e `prepared/` com os 17 ficheiros pequenos que os notebooks leem | `unzip -l` mostra exatamente estes (árvore em `specs/007-review-fixes-separate-notebooks/contracts/zip-layout.md`) | | não |
| [x] | Ficam de fora: o notebook único `MINDD_Project1.ipynb`, o relatório em português, o CSV de 179 MB, `prepared/*.csv.gz` e as pastas de figuras, `.venv/`, os notebooks de referência, os PDFs do enunciado, os relatórios antigos, `docs/report/`, este ficheiro, o guião, `specs/`, `openspec/`, `.claude/`, `.specify/` e `.git/` | A listagem do `unzip -l` não mostra nenhum deles | | não |
| [x] | O nome do zip é `MINDD-GPA-1200720-1221579-1231205.zip` (formato `MINDD-GPA-NumeroX-NumeroY-NumeroZ.zip`, números de aluno por ordem crescente) | `ls ../entrega` | | sim |
| [ ] | O tamanho cabe no limite do Moodle | O zip tem 4,4 MB; comparar com o limite da página de submissão | | não |
| [x] | O `README.md` do zip só fala de ficheiros que estão no zip, liga cada notebook à sua task e capítulo, diz como correr um notebook sozinho e como refazer tudo, e tem a instalação e o SHA-256 do CSV (está em inglês) | Ler o ficheiro de cima a baixo | | não |

## 2. Notebook

| Feito | Item | Como verificar | Quem | Todos? |
| --- | --- | --- | --- | --- |
| [x] | Cada notebook de task corre sozinho a partir do conteúdo do zip mais o CSV | `scripts/stage_run.py N` para N = 1..5: exit 0, 0 células com erro (registo em `specs/007-.../runlog.md`) | | não |
| [x] | Cada corrida guardou os mesmos resultados que os ficheiros do commit | `scripts/compare_prepared.py N`: 0 diferenças (tempos, datas e caminhos ignorados) | | não |
| [x] | A corrida completa terminou sem erros | Nenhuma célula mostra um erro; ficou registado o tempo da corrida | | não |
| [x] | Os números de teste são iguais aos de 27/10 | Notebook Task 4, secção 9: PR-AUC 0.532 (modelo), 0.381 (B1), 0.178 (B0) | | não |
| [ ] | A célula de título tem os três nomes e números certos | Amir Masnavi 1221579, Inês Oliveira 1231205, Manuela Leite 1200720 | | sim |
| [x] | Os outputs ficaram guardados no ficheiro | Abrir o notebook sem correr nada e ver tabelas e figuras | | não |
| [ ] | O notebook abre noutro computador | Outro membro abre o ficheiro do zip no seu Jupyter | | não |

## 3. Relatório

| Feito | Item | Como verificar | Quem | Todos? |
| --- | --- | --- | --- | --- |
| [ ] | A capa tem os três nomes e números de estudante | Primeira página do PDF. Números certos (1221579, 1231205, 1200720). Decidir se fica "Ines" (capa) ou "Inês" (notebook e guião) | | sim |
| [x] | O abstract e os capítulos 1 a 9 estão presentes, com a bibliografia | Índice do PDF | | não |
| [x] | A Synthesis está atualizada com a Task 5 | O capítulo 9 fala do teste, dos grupos, dos erros e das recomendações | | não |
| [x] | Não há "TODO", "??" nem referências partidas | `pdftotext docs/FINAL_REPORT.pdf - \| grep -n -E 'TODO\|\?\?'` não devolve nada; o log do LaTeX não tem "undefined" | | não |
| [ ] | As figuras leem-se bem | Ver cada figura com zoom a 100% | | não |
| [x] | O PDF foi gerado a partir do `main.tex` mais recente | A data do `docs/FINAL_REPORT.pdf` é posterior à última edição do `main.tex` | | não |
| [x] | As referências a notebooks nomeiam o notebook da task ("Task N notebook, Section M"), sem "Part N", notebook único nem repositório | `pdftotext docs/FINAL_REPORT.pdf - \| grep -c -E 'Part [0-9]\|MINDD_Project1\|repositor'` devolve 0 | | não |
| [x] | O relatório não reproduz código | Folhear o PDF: só há nomes de colunas e de funções, nenhum bloco de código | | não |

## 4. Coerência entre notebook e relatório

| Feito | Item | Como verificar | Quem | Todos? |
| --- | --- | --- | --- | --- |
| [x] | Os números do capítulo 8 são iguais aos outputs | Notebook Task 4, secção 13 e Tabela 8.1: médias 0.626 / 0.511 / 0.181; teste 0.532 / 0.381 / 0.178 | | não |
| [x] | O threshold e o alert rate batem certo | Cut-off 0.490, 10% em desenvolvimento, 7.4% no teste (Notebook Task 4, secções 6 e 9) | | não |
| [x] | O conjunto final tem 27 features nos grupos certos | Post history 8, user history 10, weather 4, calendar 2, location 2, concurrency 1 (Tabela 8.2) | | não |
| [x] | O modelo final e os hiperparâmetros estão iguais | Gradient boosting, profundidade 6, learning rate 0.1, 200 iterações, folha mínima 100 | | não |
| [x] | A tabela da Task 5 bate com o notebook | Notebook Task 5, secção 5 contra a Tabela 7.1 (F1 0.402, balanced accuracy 0.628, MCC 0.373) | | não |
| [x] | Os tempos de fit das secções 6.2 e 7.1 eram diferentes (3.1 contra 12.0 s e 3.2 contra 12.6 s, de corridas diferentes). A 7.1 passou a dizer "cerca de quatro vezes mais barato" e remete para a 6.2 | A 7.1 já não tem segundos, só a remissão para a Secção 6.2. Se alguém preferir os números da Task 5, volta-se atrás | | sim |

## 5. Reprodutibilidade

| Feito | Item | Como verificar | Quem | Todos? |
| --- | --- | --- | --- | --- |
| [x] | O reproducibility statement descreve o zip, o ambiente, as corridas isoladas e a avaliação única do teste, sem datas nem repositório (spec 007; o registo datado está em `docs/MEMORY.md`) | Secção 8.3 do PDF | | não |
| [x] | O SHA-256 do CSV é igual no relatório, no `README.md` e no o `README.md` do zip | `f6109dc066162bc770417c39294cdecc7519646c3cfa8c1d95671ea30f0e0a9b` nos três | | não |
| [ ] | O teammate check de `docs/TEAMMATE_CHECK.md` está feito por quem não escreveu o statement | Essa pessoa responde "done, 0 questions" ou manda as dúvidas | | não |
| [x] | `prepared/task4_frozen.json` continua com a data de 27/10 | `git diff prepared/` não mostra nada; o ficheiro diz `2026-10-27T11:40:32` | | não |

## 6. Entrega no Moodle

| Feito | Item | Como verificar | Quem | Todos? |
| --- | --- | --- | --- | --- |
| [ ] | Está decidido quem faz o upload e quem é o suplente | Nomes escritos aqui | | sim |
| [ ] | Upload feito até às 18:00 de 31/10 | Hora na página de submissão | | não |
| [ ] | Captura de ecrã da submissão guardada | Imagem partilhada no grupo | | não |
| [ ] | Outra pessoa descarregou o zip do Moodle e abriu o notebook e o PDF | Confirmação no grupo | | não |
| [ ] | Pull request de `feature/task-1` para `main` revisto e aprovado por quem não o escreveu, antes do upload | O PR aparece como merged no GitHub | | não |
| [ ] | O repositório continua privado | GitHub, Settings, General, Danger Zone mostra "private" | | não |
| [ ] | Toda a gente concorda que esta é a versão final | Confirmação dos três na reunião ou no grupo | | sim |

## 7. Correções da revisão do relatório (spec 007)

| Feito | Item | Como verificar | Quem | Todos? |
| --- | --- | --- | --- | --- |
| [x] | A secção 1.1 explica a suavização (k + 1)/(n + 5) e como a encontrámos, e como encontrámos as 9 058 sessões normais sem energia | Ler a secção 1.1 | | não |
| [x] | A secção 4.3 deduz t* = 1/(1 + c) e o limite de 4.4, com a proporção de sessões assinaladas nesse limiar | Ler a secção 4.3; a proporção é igual à que o notebook Task 4, secção 6, imprime | | não |
| [x] | Cada técnica estatística é explicada onde aparece pela primeira vez (Spearman, Isolation Forest, VIF, Brier, log-loss, Wilcoxon, bootstrap, permutation importance, partial dependence, McNemar, balanced accuracy, MCC) | Ler a frase no primeiro uso de cada uma | | não |
| [x] | As contagens leem-se por ordem: 29 variáveis candidatas (secção 3.2), construídas a partir de 27 colunas (Tabela 4.1), reduzidas a 27 variáveis (secção 5.1) | Abstract, secção 3.2, Tabelas 4.1 e 4.6 | | não |
| [x] | Os slides das aulas são citados só como referência; as técnicas fora da matéria dizem "not covered in class; our research led us to it" | `pdftotext docs/FINAL_REPORT.pdf - \| grep -n -i slides` só mostra linhas da bibliografia | | não |
| [x] | Há uma lista de tabelas a seguir à lista de figuras | Páginas iniciais do PDF | | não |
| [x] | As figuras 4.1, 4.2, 5.1, 5.3, 6.1 e 7.1 foram redesenhadas nos notebooks e leem-se a 100% de zoom | Ver cada uma; o texto mais pequeno tem pelo menos 8 pt | | não |
| [x] | O markdown dos notebooks segue a mesma regra dos slides e passou pelo unslop e pelo humanizer | Valores do scanner em `specs/007-.../runlog.md` | | não |
