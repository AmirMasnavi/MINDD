# Project 2 — Day-Ahead Forecasting of EV Charging Demand

Forecast the number of charging sessions starting in each of the next 24 hours, for the whole network and for each
of the three districts. The statement is [TP2-MINDD2026_27-Task1.pdf](TP2-MINDD2026_27-Task1.pdf); the latest version
of the statement is the source of requirements.

## Layout

| Path | Purpose |
| --- | --- |
| `Task1.ipynb` | Task 1: checked read, test drop, audit, hourly series, exploration, forecasting formulation, evaluation protocol and baseline scores |
| `prepared/` | Small files the notebooks save for one another. Never edited by hand |
| `docs/` | Plan, memory, the LaTeX report (`docs/report/`) and the built report `docs/TASK1_REPORT.pdf` |
| `requirements.txt` | Pinned dependencies for this project (Python 3.12) |
| `Charging_Data.csv` | Dataset from Moodle, placed here and never committed |

## Running

```sh
cd project2
../.venv/bin/jupyter nbconvert --to notebook --execute --inplace Task1.ipynb
```

A full run needs less than ten seconds of computation. Run the notebooks in task order: later tasks read the files
Task 1 saves. Two runs give byte-identical files, except `task1_run_info.json`.

## Files saved by Task 1

| File | Purpose |
| --- | --- |
| `task1_protocol.json` | The frozen protocol: problem, data fingerprint, periods, folds, predictors and leakage rule, metrics, breakdowns, baselines. Later tasks read it unchanged |
| `task1_hourly_series.csv` | Sessions starting per hour for the network and the three districts, 2020-01-01 to 2021-09-30, with the gap flag |
| `task1_calendar.csv` | Public holidays and adjusted working days, 2020 and 2021 |
| `task1_audit.csv` | Data-quality checks and how each was handled |
| `task1_predictor_catalogue.csv` | Every candidate input with its kind, anchor, availability, smallest lag and decision |
| `task1_folds.csv` | The four folds with issuance and session counts |
| `task1_baseline_scores.csv` | MAE, RMSE and MASE of the three baselines by level, fold and horizon (1,152 rows) |
| `task1_baseline_scores_by_period.csv` | The same errors by month and by day type |
| `task1_learned_operations_ledger.csv` | The MASE scales, fitted on each fold's training hours |
| `task1_results.json` | The numbers quoted in the notebook and the report |
| `task1_decision_log.csv` | Decisions D01 to D14 with their evidence |
| `task1_run_info.json` | Run date, run times and package versions |
| `figures_task1/` | Notebook figures, copied into `docs/report/figures/` |

## Dataset

`Charging_Data.csv` is the original transaction file, without the precomputed history features of Project 1
(24 columns, one row per charging transaction, GBK text). The notebook checks its SHA-256 against the value in the
root README and in `docs/PLAN.md` and stops if the file is incomplete. An earlier browser download had stopped halfway
(254,171 rows, no Xiuzhou); if the check fails, download the file again from Moodle and wait until the download has
finished.
