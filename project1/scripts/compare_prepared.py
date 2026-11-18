"""Check that a staging run of a task notebook saved the same results as the committed files.

Usage: python scripts/compare_prepared.py N

Every JSON and CSV file in ../entrega/staging/taskN/prepared/ is compared with the repository prepared/ file of the
same name. Numbers must agree to 1e-6. Fit and run times, timestamps (the freeze time included) and file paths are
ignored, because they change from run to run without changing a result. For Tasks 4 and 5 the test PR-AUC of the
final model, B1 and B0 is printed. The exit status is 1 if anything else differs.
"""
import json
import math
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent  # project1/
REPO = ROOT.parent
TOL = 1e-6
VOLATILE_KEY = re.compile(r"time|seconds|minutes|frozen_at|duration|path", re.I)
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2})?")
DURATION = re.compile(r"\b\d[\d,.]*\s*(s|sec|seconds|min|minutes)\b")


def clean(text):
    return DURATION.sub("<dur>", TIMESTAMP.sub("<ts>", text))


def compare_json(a, b, where, out):
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            out.append(f"{where}: keys {sorted(set(a) ^ set(b))}")
        for k in a.keys() & b.keys():
            if not VOLATILE_KEY.search(str(k)):
                compare_json(a[k], b[k], f"{where}/{k}", out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"{where}: length {len(a)} vs {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            compare_json(x, y, f"{where}[{i}]", out)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        if not (math.isclose(a, b, rel_tol=0, abs_tol=TOL) or (math.isnan(a) and math.isnan(b))):
            out.append(f"{where}: {a} vs {b}")
    elif isinstance(a, str) and isinstance(b, str):
        if clean(a) != clean(b):
            out.append(f"{where}: text differs")
    elif a != b:
        out.append(f"{where}: {a!r} vs {b!r}")


def compare_csv(new, old, name, out):
    a, b = pd.read_csv(new), pd.read_csv(old)
    if list(a.columns) != list(b.columns) or len(a) != len(b):
        out.append(f"{name}: shape {a.shape} vs {b.shape}")
        return
    for col in a.columns:
        if VOLATILE_KEY.search(col):
            continue
        x, y = a[col], b[col]
        numeric = [pd.api.types.is_numeric_dtype(v) and not pd.api.types.is_bool_dtype(v) for v in (x, y)]
        if all(numeric):
            gap = (x - y).abs().max()
            if gap > TOL:
                out.append(f"{name}/{col}: max difference {gap:.2e}")
        else:
            rows = sum(clean(str(u)) != clean(str(v)) for u, v in zip(x, y))
            if rows:
                out.append(f"{name}/{col}: {rows} rows differ")


def test_pr_auc(n, folder):
    if n == 4:
        models = json.loads((folder / "task4_results.json").read_text())["test"]["models"]
    else:
        models = json.loads((folder / "task5_results.json").read_text())["test"]["comparison"]
    return {m.get("model", m.get("row")): round(m["PR-AUC"], 4) for m in models}


def main():
    n = int(sys.argv[1])
    folder = REPO.parent / "entrega" / "staging" / f"task{n}" / "prepared"
    out = []
    for new in sorted(folder.iterdir()):
        old = ROOT / "prepared" / new.name
        if not new.is_file() or new.name.endswith(".csv.gz"):
            continue
        if not old.exists():
            out.append(f"{new.name}: not in the repository")
        elif new.read_bytes() == old.read_bytes():
            continue
        elif new.suffix == ".json":
            compare_json(json.loads(new.read_text()), json.loads(old.read_text()), new.name, out)
        elif new.suffix == ".csv":
            compare_csv(new, old, new.name, out)
    print(f"Task {n}: {len(out)} differences" + "".join(f"\n  {d}" for d in out))
    if n in (4, 5):
        print(f"Task {n} test PR-AUC: {test_pr_auc(n, folder)}")
    sys.exit(1 if out else 0)


if __name__ == "__main__":
    main()
