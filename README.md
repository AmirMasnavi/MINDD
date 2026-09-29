# MINDD — EV charging project

Start with [project.md](project.md) for the objective and scope, then read
[REQUIREMENTS.md](REQUIREMENTS.md) for the assignment and [PLAN.md](PLAN.md) for the work order.
[MEMORY.md](MEMORY.md) records current progress, decisions, and open questions.
[AGENTS.md](AGENTS.md) contains the shared working rules for people and AI assistants.

**Current stage: planning and environment setup only.** No analysis or model has been implemented.

## Local setup

The local `.venv` is ready. To use it, activate it and launch JupyterLab with the
commands below, skipping environment creation and installation on this machine.

For a teammate's first setup, use Python 3.12 and a separate `.venv` inside `Project/`:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

On Windows, activate with `.venv\Scripts\activate` instead. Each teammate creates
their own environment; do not copy or share `.venv`.

Open `main.ipynb` and select the Python interpreter in `Project/.venv`.
In an IDE, choose `.venv/bin/python` (Windows: `.venv\Scripts\python.exe`).
The existing notebook metadata reports Python 2.7.6 despite its Python 3 kernel label;
it will need to be refreshed when the team first saves it using the correct kernel.

## Files and data

| Path | Purpose |
| --- | --- |
| `TP1-MINDD2026_27-Task1.pdf` | Authoritative assignment; page references are in REQUIREMENTS.md |
| `Charging_Data_educational.csv` | Original supplied data; keep unchanged |
| `main.ipynb` | Existing empty notebook; future analysis goes here |
| `requirements.txt` | Six tested direct dependencies with exact versions; indirect dependencies are resolved by pip |
| `data/` | Existing folder reserved for justified derived data, if needed |
| `models/` | Existing folder reserved for later modelling; unused in Task 1 |

The CSV is about 179 MB. Obtain the original through the team's agreed private
course channel and place it beside the notebook; the sharing location is still to
be agreed. Do not assume the original research dataset has the same schema or rows.
Run the notebook from `Project/` and use relative paths.

## Team handoff

Before work, read MEMORY.md and claim one PLAN.md step with an owner and reviewer.
Use one notebook editor at a time to avoid conflicting notebook changes; others can
review evidence and draft report text. After work, update the step status and leave
a short dated memory entry with the outcome, evidence location, and next action.

Private repository: [AmirMasnavi/MINDD](https://github.com/AmirMasnavi/MINDD).
The repository root corresponds to this local `Project/` folder. Teammates with
access can clone it, then follow the local setup instructions from the cloned root.
The dataset, local environment, IDE settings, and generated data/models are excluded.
Empty `data/` and `models/` folders are not tracked; create them only when needed.
Agree notebook ownership before editing and use focused branches and pull requests
for team changes. Repository access for teammates still needs to be arranged.
