# MINDD: EV charging project

Predict, at the start of an EV charging session, whether it will end abnormally (Project 1, MINDD 2026/27, MEI at ISEP).

Task 1 (data understanding, audit and preparation) and Task 2 (prediction and evaluation setting) are complete.
Model fitting and the feature-group ablation belong to the next task.

| Read this | For |
| --- | --- |
| [Task1.ipynb](Task1.ipynb) | **Task 1 notebook.** Sections 2 to 4 load, describe and clean the data, Section 5 builds the target, Section 6 covers missing values, 7 changes over time, 8 leakage, 9 the start-time predictors, 10 outliers, 11 the time split and sampling, 12 feature engineering and reduction, 13 the learned operations and class imbalance, 14 the saved files and integrity checks, and 15 the synthesis and decision log |
| [Task2.ipynb](Task2.ipynb) | **Task 2 notebook.** It fits no model. Section 3 defines the prediction problem, 4 classifies the 47 columns, 5 discusses the two errors, 6 chooses the metrics, 7 builds the four temporal folds, 8 defines the aggregation across folds, 9 evaluates the two baselines, and 10 gives the evaluation protocol |
| [docs/TASK2_REPORT.pdf](docs/TASK2_REPORT.pdf) | The report for Tasks 1 and 2. Chapters 1 to 3 are Task 1, chapter 4 is Task 2, and chapter 5 is the Synthesis of both, which is rewritten at each deliverable |
| [docs/TASK1_REPORT.pdf](docs/TASK1_REPORT.pdf) / [docs/TASK1_REPORT.md](docs/TASK1_REPORT.md) | The report as submitted for Task 1 |
| [TP1_Task1_Data_Understanding_and_Preparation.ipynb](TP1_Task1_Data_Understanding_and_Preparation.ipynb) | Extended Task 1 reference notebook (Sections 0 to 17). It holds model-based diagnostics that belong to the modelling task: class weights (Section 14) and a preliminary feature-group ablation with cold-start scores (Section 15) |
| [Task1_Minimal_EDA.ipynb](Task1_Minimal_EDA.ipynb) | Earlier minimal EDA, kept for reference |
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
and is never committed. Restart the kernel and run all cells from top to bottom.

`Task2.ipynb` reads `prepared/feature_groups.json`, which `Task1.ipynb` writes and which is committed, so it can be run
without running Task 1 first. It takes a few seconds. The extended notebook takes a few minutes because its Sections 14
and 15 fit about 40 small gradient-boosting models on training-window folds.

## Files

| Path | Purpose |
| --- | --- |
| `TP1-MINDD2026_27-Task1+Task2.pdf` | Assignment statement for Tasks 1 and 2 (`TP1-MINDD2026_27-Task1.pdf` is the earlier version) |
| `Task1.ipynb` | Task 1 notebook |
| `Task2.ipynb` | Task 2 notebook |
| `TP1_Task1_Data_Understanding_and_Preparation.ipynb` | Extended Task 1 notebook with the model-based diagnostics |
| `requirements.txt` | Direct dependencies |
| `prepared/figures_merged/` | Figures saved by `Task1.ipynb`. Each run re-creates them |
| `prepared/figures/` | Figures saved by the extended notebook (the report uses some of them). Each run re-creates them |
| `prepared/figures_task2/` | Figures saved by `Task2.ipynb` (the temporal folds and the baselines). Each run re-creates them |
| `prepared/decision_log.csv`, `prepared/learned_operations_ledger.csv`, `prepared/feature_groups.json` | Task 1 decision log, ledger of learned operations and feature groups. Both Task 1 notebooks write these files, so the last one you run wins; `Task1.ipynb` is the reference |
| `prepared/task2_protocol.json`, `prepared/task2_decision_log.csv` | Evaluation protocol (predictors, exclusions, metrics, folds, aggregation, baselines) and Task 2 decision log, written by `Task2.ipynb`. The modelling task reads the protocol |
| `prepared/task1_prepared.csv.gz` | Prepared dataset with split labels. `Task1.ipynb` generates it, and it is not committed |
| `docs/` | Reports, dataset guide, plan, memory |
| `docs/report/` | LaTeX source of the report (ISEP template style). Upload the folder to Overleaf or run `latexmk -pdf main.tex`, then copy `main.pdf` to `docs/TASK2_REPORT.pdf`. The Task 2 figures in `docs/report/figures/` are copies of `prepared/figures_task2/` |

## Team workflow

Only one person edits a notebook at a time. Work on a branch and merge through a pull request that another member
reviews. After meaningful work, update `docs/PLAN.md` and add a short dated entry to `docs/MEMORY.md`.
The repository must stay private because it contains course material, so check the GitHub visibility setting.
