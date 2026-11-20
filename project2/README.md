# Project 2 — Day-Ahead Forecasting of EV Charging Demand

Forecast the number of charging sessions starting in each of the next 24 hours, for the whole network and for each
of the three districts. The statement is [TP2-MINDD2026_27-Task1.pdf](TP2-MINDD2026_27-Task1.pdf); the latest version
of the statement is the source of requirements.

## Layout

| Path | Purpose |
| --- | --- |
| `Task1.ipynb` | Task 1: checked read, test drop, audit, hourly series, exploration, forecasting formulation, evaluation protocol and baseline scores |
| `Task2.ipynb` | Task 2: statistical models (ETS, SARIMA, SARIMAX with calendar inputs and with temperature, MSTL + ARIMA) scored under the Task 1 protocol |
| `prepared/` | Small files the notebooks save for one another. Never edited by hand |
| `docs/` | Plan, memory, the LaTeX report (`docs/report/`) and the built reports `docs/TASK1_REPORT.pdf` and `docs/TASK2_REPORT.pdf` |
| `requirements.txt` | Pinned dependencies for this project (Python 3.12) |
| `Charging_Data.csv` | Dataset from Moodle, placed here and never committed |

## Running

```sh
uv pip install --python .venv/bin/python -r project2/requirements.txt   # from the repository root
cd project2
../.venv/bin/jupyter nbconvert --to notebook --execute --inplace Task1.ipynb
../.venv/bin/jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 Task2.ipynb
```

Run the notebooks in task order: later tasks read the files Task 1 saves. Task 1 needs less than ten seconds of
computation; Task 2 needs about 25 minutes with 16 parallel workers, almost all of it in the 80 model fits of Section 6. Two runs give
byte-identical files, except `task1_run_info.json` and `task2_run_info.json`.

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

## Task 2 notebook and files

`Task2.ipynb` has 12 sections: setup; Task 1 inputs and the scoring check; daily weather as a day-D forecast;
modelling choices shared by all models; structure selection on fold 1; fitting and forecasting in the four folds;
residual diagnostics; comparison with the baselines; stability over folds, horizons, levels, months and day types;
weather effect and computational cost; saved files and integrity checks; synthesis and decision log. It reads the
Task 1 files unchanged and checks their SHA-256 at the start and the end of the run.

| File | Purpose |
| --- | --- |
| `task2_structures.csv` | Every candidate structure tried on fold 1, with its AIC and the chosen one |
| `task2_fits.csv` | Coefficients, convergence and run time of the 80 (model, level, fold) fits |
| `task2_scores.csv` | MAE, RMSE and MASE of the five models by level, fold and horizon, in the Task 1 layout |
| `task2_scores_by_period.csv` | The same errors by month and by day type |
| `task2_comparison.csv` | One row per model and baseline: primary MASE, per fold, per level, cells beating the reference |
| `task2_diagnostics.csv` | Ljung-Box tests, residual autocorrelation and mean residual by group |
| `task2_weather_daily.csv` | Daily temperature per district and network, used as the day-D forecast |
| `task2_results.json` | The numbers quoted in the notebook and the report |
| `task2_decision_log.csv` | Decisions D15 to D25 with their evidence |
| `task2_learned_operations_ledger.csv` | AIC selections, coefficient estimations and MSTL decompositions with their windows |
| `task2_task1_checksums.json` | SHA-256 of every Task 1 file at the start and the end of the run |
| `task2_run_info.json` | Run date, section times, core count and package versions |
| `task2_forecasts.csv.gz` | Every validation forecast; rebuilt by the run and not committed |
| `figures_task2/` | Notebook figures, partly copied into `docs/report/figures/` |

## Dataset

`Charging_Data.csv` is the original transaction file, without the precomputed history features of Project 1
(24 columns, one row per charging transaction, GBK text). The notebook checks its SHA-256 against the value in the
root README and in `docs/PLAN.md` and stops if the file is incomplete. An earlier browser download had stopped halfway
(254,171 rows, no Xiuzhou); if the check fails, download the file again from Moodle and wait until the download has
finished.
