"""Join Task1.ipynb to Task5.ipynb into MINDD_Project1.ipynb, the single notebook of the final submission.

Only headings and namespace resets are added. Every cell of the task notebooks is kept as it is, without its
outputs, so the merged notebook must be run once with Restart and Run All before it is submitted.
"""
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parent.parent  # project1/
TASKS = [ROOT / f"Task{n}.ipynb" for n in range(1, 6)]
OUT = ROOT / "MINDD_Project1.ipynb"
RUN_TIMES = ["about 1 minute", "about 12 seconds", "about 6 minutes", "about 40 minutes", "about 1.5 minutes"]
# The comment sits on its own line: after the magic, its words would be read as arguments and skip the reset
RESET = "# each part starts from an empty namespace, as when the task notebooks ran on their own\n%reset -f"


def task_title(nb):
    """Title of a task notebook, read from the level-1 heading of its first cell ("TP1 · " removed)."""
    first_line = nb.cells[0].source.splitlines()[0]
    return first_line.lstrip("# ").replace("TP1 · ", "")


def title_cell(titles):
    rows = "\n".join(f"| {n} | {t} | {time} |" for n, (t, time) in enumerate(zip(titles, RUN_TIMES), start=1))
    return nbformat.v4.new_markdown_cell(
        "# Project 1: Classification of abnormal electric-vehicle charging sessions\n\n"
        "**Course:** Mineração de Dados (MINDD), 2026/2027, 1st semester, ISEP / DEI\n\n"
        "**Group:** Amir Masnavi (1221579), Inês Oliveira (1231205), Manuela Leite (1200720)\n\n"
        "This notebook holds the whole project in five parts, one per task. Each part was developed as a separate task "
        "notebook and is kept here unchanged, with its own section numbers, so \"Part 4, Section 9\" is Section 9 of "
        "Task 4. The parts run in order with Restart and Run All, because each one reads the files the previous ones "
        "saved in `prepared/`. Each part starts from an empty namespace. The data file `Charging_Data_educational.csv` "
        "goes next to this notebook.\n\n"
        "| Part | Task | Run time |\n| --- | --- | --- |\n" + rows + "\n"
    )


def main():
    notebooks = [nbformat.read(path, as_version=4) for path in TASKS]
    titles = [task_title(nb) for nb in notebooks]
    cells = [title_cell(titles)]
    for n, (nb, title) in enumerate(zip(notebooks, titles), start=1):
        cells.append(nbformat.v4.new_markdown_cell(f"# Part {n} · {title}"))
        if n > 1:
            cells.append(nbformat.v4.new_code_cell(RESET))
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == "code":
                cell.outputs, cell.execution_count = [], None
            if i == 0:                                       # the task title becomes a level-2 heading
                cell.source = "#" + cell.source
            cell.pop("id", None)                             # new ids are given below, so no two cells share one
            cells.append(cell)

    merged = nbformat.v4.new_notebook(cells=cells, metadata=notebooks[0].metadata)
    merged.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    for cell in merged.cells:
        cell["id"] = nbformat.corpus.words.generate_corpus_id()
    nbformat.validate(merged)
    nbformat.write(merged, OUT)
    print(f"Wrote {OUT.name}: {len(merged.cells)} cells, {sum(c.cell_type == 'code' for c in merged.cells)} code")


if __name__ == "__main__":
    main()
