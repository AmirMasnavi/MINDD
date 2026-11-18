"""Run one task notebook on its own, from the files the submission zip holds, and log the result.

Usage: python scripts/stage_run.py N

The staging folder ../entrega/staging/taskN/ is rebuilt with TaskN.ipynb, requirements.txt, a link to the course CSV
and a copy of the small files of prepared/ (everything directly under it except *.csv.gz). The notebook is executed
there with Restart and Run All, so it can only use what the zip gives it. The executed copy stays in the folder.
"""
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGING = ROOT.parent / "entrega" / "staging"
CSV = ROOT / "Charging_Data_educational.csv"
RUNLOG = ROOT / "specs" / "007-review-fixes-separate-notebooks" / "runlog.md"
# The fresh environment built from requirements.txt; the repository .venv (same pins) is the fallback
PYTHON = next(p for p in [STAGING / ".venv/bin/python", ROOT / ".venv/bin/python"] if p.exists())


def build_folder(n):
    folder = STAGING / f"task{n}"
    if folder.exists():
        shutil.rmtree(folder)
    (folder / "prepared").mkdir(parents=True)
    shutil.copy2(ROOT / f"Task{n}.ipynb", folder)
    shutil.copy2(ROOT / "requirements.txt", folder)
    (folder / CSV.name).symlink_to(CSV)
    for f in sorted((ROOT / "prepared").iterdir()):
        if f.is_file() and not f.name.endswith(".csv.gz"):
            shutil.copy2(f, folder / "prepared")
    return folder


def main():
    n = int(sys.argv[1])
    folder = build_folder(n)
    notebook = f"Task{n}.ipynb"
    started = time.time()
    run = subprocess.run([str(PYTHON), "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute",
                          "--ExecutePreprocessor.timeout=-1", "--output", notebook, notebook],
                         cwd=folder, capture_output=True, text=True)
    seconds = time.time() - started
    errors = 0
    if (folder / notebook).exists():
        cells = json.loads((folder / notebook).read_text())["cells"]
        errors = sum(o.get("output_type") == "error" for c in cells for o in c.get("outputs", []))
    line = (f"| {datetime.now():%Y-%m-%d %H:%M} | Task {n} | {seconds / 60:.1f} min | exit {run.returncode} | "
            f"{errors} error cells | {PYTHON.relative_to(ROOT.parent)} |")
    print(line)
    if run.returncode:
        print(run.stderr[-3000:])
    with RUNLOG.open("a") as log:
        log.write(line + "\n")
    sys.exit(run.returncode or errors)


if __name__ == "__main__":
    main()
