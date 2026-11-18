# Project 2 — Day-Ahead Forecasting of EV Charging Demand

Forecast the number of charging sessions starting in each of the next 24 hours, for the whole network and for each
of the three districts. The statement is [TP2-MINDD2026_27-Task1.pdf](TP2-MINDD2026_27-Task1.pdf); the latest version
of the statement is the source of requirements.

## Layout

| Path | Purpose |
| --- | --- |
| `TaskN.ipynb` | One notebook per task, run from this folder with Restart and Run All |
| `prepared/` | Small files the notebooks save for one another (protocol, decision logs, figures). Never edited by hand |
| `docs/` | Plan, memory and the LaTeX report (`docs/report/`) |
| `requirements.txt` | Pinned dependencies for this project (Python 3.12) |
| `Charging_Data.csv` | Dataset from the course channel, placed here and never committed |

## Dataset

`Charging_Data.csv` is the original transaction file, without the precomputed history features of Project 1
(24 columns, one row per charging transaction).

The copy that was in the repository on 2026-11-18 came from an unfinished browser download: it is 48.5 MB and its
last row is cut off. Download the file again from the course channel, check that the last line is complete, and record
its SHA-256 in the root README and in `docs/PLAN.md`:

```sh
sha256sum Charging_Data.csv
```
