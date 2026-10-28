# MINDD: EV charging project

Predict, at the start of an EV charging session, whether it will end abnormally (Project 1, MINDD 2026/27, MEI at ISEP).

Tasks 1 to 4 are complete: data understanding, audit and preparation (Task 1), the prediction and evaluation setting
(Task 2), the feature-group ablation with individual and ensemble models (Task 3), and the optimisation, decision
threshold and single test evaluation of the final model (Task 4). The final report is
[docs/FINAL_REPORT.pdf](docs/FINAL_REPORT.pdf). Its chapter 7 compares the candidate, baseline and final models,
describes the final model and gives the reproducibility statement.

| Read this | For |
| --- | --- |
| [Task1.ipynb](Task1.ipynb) | **Task 1 notebook.** Sections 2 to 4 load, describe and clean the data, Section 5 builds the target, Section 6 covers missing values, 7 changes over time, 8 leakage, 9 the start-time predictors, 10 outliers, 11 the time split and sampling, 12 feature engineering and reduction, 13 the learned operations and class imbalance, 14 the saved files and integrity checks, and 15 the synthesis and decision log |
| [Task2.ipynb](Task2.ipynb) | **Task 2 notebook.** It fits no model. Section 3 defines the prediction problem, 4 classifies the 47 columns, 5 discusses the two errors, 6 chooses the metrics, 7 builds the four temporal folds, 8 defines the aggregation across folds, 9 evaluates the two baselines, and 10 gives the evaluation protocol |
| [Task3.ipynb](Task3.ipynb) | **Task 3 notebook.** Section 2 loads the data and rebuilds the folds and baselines of Task 2, 3 runs the feature-group ablation (four nested sets, `post_id` and tariff checks, cold start, operational and ethical concerns), 4 fits the individual models (logistic regression, Naive Bayes, decision tree) and checks the outlier caps, 5 fits the ensembles (random forest, gradient boosting, time-ordered stacking), 6 compares all models with the baselines and translates them into alerts, and 7 saves the results and the decision log |
| [Task4.ipynb](Task4.ipynb) | **Task 4 notebook.** Section 2 rebuilds the folds and reproduces Task 3, 3 chooses the models to optimise, 4 runs the hyperparameter searches, 5 compares optimised and initial configurations and picks the final model, 6 chooses the threshold, 7 checks calibration, 8 freezes the choices, 9 scores the test period once, 10 interprets the final model, 11 concludes, 12 saves the files and the decision log, and 13 builds the final comparison table and model description from the saved files |
| [docs/FINAL_REPORT.pdf](docs/FINAL_REPORT.pdf) | **The final report.** Chapters 1 to 3 are Task 1, chapter 4 is Task 2, chapter 5 is Task 3, chapter 6 is Task 4, chapter 7 is the final model (comparison table, final model description, reproducibility statement), and chapter 8 is the Synthesis |
| [docs/TASK4_REPORT.pdf](docs/TASK4_REPORT.pdf) / [docs/TASK3_REPORT.pdf](docs/TASK3_REPORT.pdf) | The report as submitted for Task 4 and for Task 3 |
| [docs/TASK2_REPORT.pdf](docs/TASK2_REPORT.pdf) | The report as submitted for Task 2. Chapters 1 to 3 are Task 1, chapter 4 is Task 2, and chapter 5 is the Synthesis of both, which is rewritten at each deliverable |
| [docs/TASK1_REPORT.pdf](docs/TASK1_REPORT.pdf) / [docs/TASK1_REPORT.md](docs/TASK1_REPORT.md) | The report as submitted for Task 1 |
| [TP1_Task1_Data_Understanding_and_Preparation.ipynb](TP1_Task1_Data_Understanding_and_Preparation.ipynb) | Reference material, not part of the submission. Extended Task 1 notebook (Sections 0 to 17). It holds model-based diagnostics that were later done properly in Task 3: class weights (Section 14) and a preliminary feature-group ablation with cold-start scores (Section 15) |
| [Task1_Minimal_EDA.ipynb](Task1_Minimal_EDA.ipynb) | Reference material, not part of the submission. Earlier minimal EDA |
| [docs/TEAMMATE_CHECK.md](docs/TEAMMATE_CHECK.md) | The 15-minute reproducibility check that a teammate who did not write the statement does before the final submission |
| [docs/DATASET.md](docs/DATASET.md) | Field meanings and the derived target |
| [docs/MEMORY.md](docs/MEMORY.md) / [docs/PLAN.md](docs/PLAN.md) | Progress, decisions, open questions, work order |

## Local setup

Use Python 3.12. Each teammate creates a separate `.venv` and does not share it:

```sh
python3.12 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

Place `Charging_Data_educational.csv` next to the notebooks. The file is about 179 MB, comes from the course channel,
and is never committed. Check that it is the same file:

```sh
sha256sum Charging_Data_educational.csv
# f6109dc066162bc770417c39294cdecc7519646c3cfa8c1d95671ea30f0e0a9b
```

Run the four submission notebooks in this order, each with Restart and Run All, because each one reads the files the
previous ones saved in `prepared/`. Times measured on 2026-10-28 on a laptop with an Intel Core Ultra 7 165H
(22 logical cores):

| Order | Notebook | Time | Main files written |
| --- | --- | --- | --- |
| 1 | `Task1.ipynb` | about 1 minute | `prepared/feature_groups.json`, `prepared/decision_log.csv`, `prepared/learned_operations_ledger.csv`, `prepared/task1_prepared.csv.gz` |
| 2 | `Task2.ipynb` | about 12 seconds | `prepared/task2_protocol.json`, `prepared/task2_decision_log.csv` |
| 3 | `Task3.ipynb` | about 6 minutes | `prepared/task3_results.json`, `prepared/task3_fold_metrics.csv`, `prepared/task3_decision_log.csv` |
| 4 | `Task4.ipynb` | about 40 minutes | `prepared/task4_*`, `prepared/final_comparison.csv`, `prepared/final_model.json` |

`Task4.ipynb` scores the test period in Section 9, with the choices frozen in Section 8. The test was first scored on
2026-10-27. A re-run repeats that evaluation with the same frozen choices and reproduces the same numbers; nothing may be
changed after seeing them. A re-run writes a new freeze time into `prepared/task4_frozen.json` and `prepared/task4_decision_log.csv`, so restore the
committed files afterwards (`git checkout -- prepared/task4_frozen.json prepared/task4_decision_log.csv`). They keep the original
freeze time, 2026-10-27T11:40:32.

The extended reference notebook is not needed for the submission. It overwrites the Task 1 decision log and ledger,
so do not run it before the four notebooks above.

## Files

| Path | Purpose |
| --- | --- |
| `TP1-MINDD2026_27-Tasks_1+2+3+4.pdf` | Assignment statement for Tasks 1 to 4 (`TP1-MINDD2026_27-Task1+Task2+Task3.pdf`, `TP1-MINDD2026_27-Task1+Task2.pdf` and `TP1-MINDD2026_27-Task1.pdf` are the earlier versions) |
| `Task1.ipynb` | Task 1 notebook |
| `Task2.ipynb` | Task 2 notebook |
| `Task3.ipynb` | Task 3 notebook |
| `Task4.ipynb` | Task 4 notebook |
| `TP1_Task1_Data_Understanding_and_Preparation.ipynb` | Extended Task 1 notebook with the model-based diagnostics |
| `requirements.txt` | Direct dependencies |
| `prepared/figures_merged/` | Figures saved by `Task1.ipynb`. Each run re-creates them |
| `prepared/figures/` | Figures saved by the extended notebook (the report uses some of them). Each run re-creates them |
| `prepared/figures_task2/` | Figures saved by `Task2.ipynb` (the temporal folds and the baselines). Each run re-creates them |
| `prepared/figures_task3/` | Figures saved by `Task3.ipynb` (ablation, stacking design, model comparison). Each run re-creates them |
| `prepared/decision_log.csv`, `prepared/learned_operations_ledger.csv`, `prepared/feature_groups.json` | Task 1 decision log, ledger of learned operations and feature groups. Both Task 1 notebooks write these files, so the last one you run wins; `Task1.ipynb` is the reference |
| `prepared/task2_protocol.json`, `prepared/task2_decision_log.csv` | Evaluation protocol (predictors, exclusions, metrics, folds, aggregation, baselines) and Task 2 decision log, written by `Task2.ipynb`. `Task3.ipynb` reads the protocol unchanged |
| `prepared/task3_results.json`, `prepared/task3_fold_metrics.csv`, `prepared/task3_decision_log.csv` | Task 3 results (selected features and configurations, comparison table), metrics of every experiment by fold, and Task 3 decision log, written by `Task3.ipynb`. `Task4.ipynb` reads them instead of repeating the experiments |
| `prepared/task4_frozen.json`, `prepared/task4_results.json`, `prepared/task4_search.csv`, `prepared/task4_fold_metrics.csv`, `prepared/task4_decision_log.csv` | Task 4 frozen choices (written before the test), results (search, verdicts, operating points, calibration, test, importance), every searched configuration, metrics by fold, and decision log, written by `Task4.ipynb` |
| `prepared/final_comparison.csv`, `prepared/final_model.json` | Comparison of the candidate, baseline and final models, and the final model description, written by `Task4.ipynb` Section 13 from the saved files. Report chapter 7 uses them |
| `prepared/figures_task4/` | Figures saved by `Task4.ipynb` (search, threshold, calibration, importance). Each run re-creates them |
| `prepared/task1_prepared.csv.gz` | Prepared dataset with split labels. `Task1.ipynb` generates it, and it is not committed |
| `docs/` | Reports, dataset guide, plan, memory |
| `docs/report/` | LaTeX source of the report (ISEP template style). Upload the folder to Overleaf or run `latexmk -pdf main.tex`, then copy `main.pdf` to `docs/FINAL_REPORT.pdf`. The Task 2 to Task 4 figures in `docs/report/figures/` are copies of `prepared/figures_task2/` to `prepared/figures_task4/` |

## Team workflow

Only one person edits a notebook at a time. Work on a branch and merge through a pull request that another member
reviews. After meaningful work, update `docs/PLAN.md` and add a short dated entry to `docs/MEMORY.md`.
The repository must stay private because it contains course material, so check the GitHub visibility setting.
