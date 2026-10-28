# Reproducibility check for a teammate (about 15 minutes)

Do this before we submit on Friday 2026-10-30. It must be done by a teammate who did not write the reproducibility
statement. Use only `README.md` and Section 7.3 of `docs/FINAL_REPORT.pdf` ("Reproducibility statement"), and don't ask
the author anything while you work; write down every step you found unclear. There is no need to run the notebooks,
because all four were run from a fresh clone on 2026-10-28.

1. Clone the repository into an empty folder and check out the branch we are submitting.
2. Create the environment as `README.md` describes (Python 3.12, a new `.venv`, `pip install -r requirements.txt`).
3. Run `python --version` and check that it reports 3.12.
4. Copy `Charging_Data_educational.csv` next to the notebooks and run `sha256sum Charging_Data_educational.csv`.
   The hash must equal the one printed in the statement and in `README.md`.
5. Start Jupyter (`python -m jupyterlab`), open `Task4.ipynb` and check that Section 13 shows the comparison table and
   the final model description.
6. Reply with one line: "done, 0 questions", or "done, questions:" followed by every point where the statement or the
   README was unclear.
