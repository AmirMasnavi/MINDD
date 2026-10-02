# MINDD: EV charging project

Predict, at the start of an EV charging session, whether it will end abnormally (Project 1, MINDD 2026/27, MEI at ISEP).

Task 1 (data understanding, audit and preparation) is complete. The team still has to review it, and the instructor
still has to confirm the target mapping.

| Read this | For |
| --- | --- |
| [TP1_Task1_Data_Understanding_and_Preparation.ipynb](TP1_Task1_Data_Understanding_and_Preparation.ipynb) | All the evidence. §1 to §12 audit and explore the data, §13 holds the learned transformations and their ledger, §14 covers class imbalance, §15 the preliminary ablation and checks, §16 the saved artefacts and integrity checks, and §17 the synthesis and decision log |
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
and is never committed. Restart the kernel and run all cells from top to bottom. A full run takes a few minutes because
§14 and §15 fit about 40 small gradient-boosting models on training-window folds.

## Files

| Path | Purpose |
| --- | --- |
| `TP1-MINDD2026_27-Task1.pdf` | Assignment statement |
| `TP1_Task1_Data_Understanding_and_Preparation.ipynb` | Task 1 notebook, the single source of evidence |
| `requirements.txt` | Direct dependencies |
| `prepared/figures/` | Figures the notebook saves and the report uses. Each run re-creates them |
| `prepared/decision_log.csv`, `prepared/learned_operations_ledger.csv`, `prepared/feature_groups.json` | Decision log, ledger of learned operations, feature groups for Task 2 |
| `prepared/task1_prepared.csv.gz` | Prepared dataset with split labels for Task 2. The notebook generates it, and it is not committed |
| `docs/` | Report, dataset guide, plan, memory |

## Team workflow

Only one person edits the notebook at a time. Work on a branch and merge through a pull request that another member
reviews. After meaningful work, update `docs/PLAN.md` and add a short dated entry to `docs/MEMORY.md`.
The repository must stay private because it contains course material, so check the GitHub visibility setting.
