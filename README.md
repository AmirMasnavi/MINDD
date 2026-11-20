# MINDD 2026/27 — EV Charging Projects

Data mining projects (MEI, ISEP) on the China EV Charging Dataset (Zhang et al., 2025).

| Folder | Project | Status |
| --- | --- | --- |
| [project1/](project1/README.md) | Project 1: classification of abnormal charging sessions at session start (Tasks 1 to 5) | Complete; notebooks, `prepared/` files and report kept as delivered |
| [project2/](project2/README.md) | Project 2: day-ahead forecasting of hourly charging demand, network and district level | Tasks 1 and 2 complete (protocol and baselines; statistical models, report with both tasks); Task 3 next |

Each project folder is self-contained: its notebooks run from that folder, read the dataset placed next to them and
write only to that folder's `prepared/`. Each has its own `requirements.txt`, `docs/` and report.

## Setup

Use Python 3.12. Create one `.venv` at the repository root and install the requirements of the project you work on:

```sh
python3.12 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
python -m pip install -r project1/requirements.txt
python -m jupyterlab
```

Datasets come from the course channel and are never committed. Place each one in its project folder:

| Project | File | SHA-256 |
| --- | --- | --- |
| 1 | `project1/Charging_Data_educational.csv` | `f6109dc066162bc770417c39294cdecc7519646c3cfa8c1d95671ea30f0e0a9b` |
| 2 | `project2/Charging_Data.csv` | `6f3643db401327ec4f4a074109987706e421896869acac26a8ee1a5c6e3b45ee` |

## Team workflow

Only one person edits a notebook at a time. Work on a branch and merge through a pull request that another member
reviews. After meaningful work, update the project's `docs/PLAN.md` and add a short dated entry to its
`docs/MEMORY.md`. The repository must stay private because it contains course material.
