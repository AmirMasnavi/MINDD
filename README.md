# MINDD: EV charging project

Predict, at the start of an EV charging session, whether it will end abnormally (Project 1, MINDD 2026/27, MEI at ISEP).

Task 1 (data understanding, audit and preparation) is complete. The team still has to review it, and the instructor
still has to confirm the target mapping.

| Read this | For |
| --- | --- |
| [TP1_Task1_Merged.ipynb](TP1_Task1_Merged.ipynb) | **Main Task 1 notebook.** §2 to §4 load, describe and clean the data, §5 builds the target (a team assumption), §6 covers missing values, §7 changes over time, §8 leakage, §9 the start-time predictors, §10 outliers, §11 the time split and sampling, §12 feature engineering and reduction, §13 the learned operations, their ledger and class imbalance, §14 the saved files and integrity checks, and §15 the synthesis and decision log |
| [TP1_Task1_Data_Understanding_and_Preparation.ipynb](TP1_Task1_Data_Understanding_and_Preparation.ipynb) | Extended reference notebook (§0 to §17). Holds the model-based diagnostics that move to Task 2: class weights (§14) and the preliminary feature-group ablation and cold-start scores (§15). The report cites it as C-§x.y |
| [Task1_Minimal_EDA.ipynb](Task1_Minimal_EDA.ipynb) | Earlier minimal EDA, kept for reference |
| [docs/TASK1_REPORT.md](docs/TASK1_REPORT.md) | The short report section to submit |
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

Place `Charging_Data_educational.csv` next to the notebook. The file is about 179 MB, comes from the course channel,
and is never committed. Restart the kernel and run all cells from top to bottom. The merged notebook fits no models
and runs in about a minute. The extended notebook takes a few minutes because its §14 and §15 fit about 40 small
gradient-boosting models on training-window folds.

## Files

| Path | Purpose |
| --- | --- |
| `TP1-MINDD2026_27-Task1.pdf` | Assignment statement |
| `TP1_Task1_Merged.ipynb` | Main Task 1 notebook |
| `TP1_Task1_Data_Understanding_and_Preparation.ipynb` | Extended Task 1 notebook with the model-based diagnostics |
| `requirements.txt` | Direct dependencies |
| `prepared/figures_merged/` | Figures saved by the merged notebook. Each run re-creates them |
| `prepared/figures/` | Figures saved by the extended notebook (the report uses some of them). Each run re-creates them |
| `prepared/decision_log.csv`, `prepared/learned_operations_ledger.csv`, `prepared/feature_groups.json` | Decision log, ledger of learned operations, feature groups for Task 2. Both notebooks write these files, so the last notebook you run wins; the merged notebook is the reference |
| `prepared/task1_prepared.csv.gz` | Prepared dataset with split labels for Task 2. The notebook generates it, and it is not committed |
| `docs/` | Report, dataset guide, plan, memory |
| `docs/report/` | LaTeX source of the report (ISEP template style). Upload the folder to Overleaf or run `pdflatex main.tex` twice, then copy `main.pdf` to `docs/TASK1_REPORT.pdf` |

## Team workflow

Only one person edits the notebook at a time. Work on a branch and merge through a pull request that another member
reviews. After meaningful work, update `docs/PLAN.md` and add a short dated entry to `docs/MEMORY.md`.
The repository must stay private because it contains course material, so check the GitHub visibility setting.
