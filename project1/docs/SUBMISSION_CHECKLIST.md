# Project 1 submission checklist

English version of `docs/CHECKLIST_ENTREGA.md` (Portuguese). Both list the same items with the same status; whoever
ticks an item ticks it in both files.

The instructor, Fátima Rodrigues, wrote: "The 1st Project (notebook and report), 1 zip file per group, must be
submitted on Moodle by 20:00 on 31 October." This list is for today's meeting (30/10) and for the last steps
tomorrow. Whoever closes a line marks it `[x]`. Every open line must leave the meeting with an owner and a time. The
finished zip is at `../entrega/MINDD-GPA-1200720-1221579-1231205.zip`, outside the repository. In the "All?" column,
"yes" means the item needs the agreement of all three of us.

One rule covers everything below: the test period was seen on 27/10, so from now on we only change wording, figures
and layout. No model, feature, hyperparameter or threshold changes.

## Timeline

| When | What |
| --- | --- |
| Today, meeting | Go through this list, give every open line an owner and a time, confirm names and group number |
| Today, done before the meeting | Report review fixes (spec 007), each task notebook run on its own from the zip contents, PDF rebuilt, zip rebuilt with the five task notebooks |
| Tomorrow by 16:00 | Last checks and the teammate check. If anything forces a rebuild, there is still time |
| Tomorrow by 18:00 | Upload to Moodle and screenshot of the submission |
| Tomorrow, right after | Someone else downloads the zip from Moodle and confirms it opens |

## 0. Coverage of the assignment statement

Source: `TP1-MINDD2026_27-Tasks_1+2+3+4+5.pdf`, the final statement. Each line says where the report
(`docs/FINAL_REPORT.pdf`) and the task notebooks (`Task1.ipynb` to `Task5.ipynb`) answer the request. To check, open the
section given and confirm the request is answered there.

| Done | Requirement | Report | Notebook |
| --- | --- | --- | --- |
| [x] | Task 1: variable types and meaning, missing values, duplicates and inconsistencies | 2.1, 2.2 | Task 1 notebook, Sections 2–4 and 6 |
| [x] | Task 1: target distribution, distributions, outliers investigated before acting | 1.1, 2.2, 2.3 | Task 1 notebook, Sections 5, 9 and 10 |
| [x] | Task 1: changes over time (volume, prevalence, predictors, post and user activity) and what they imply | 2.4 | Task 1 notebook, Section 7 |
| [x] | Task 1: figures interpreted, not only shown | 2.1–2.4 | Task 1 notebook |
| [x] | Task 1: every operation that learns from the data documented separately | 3.3 (learned-operations table) | Task 1 notebook, Section 13 |
| [x] | Task 1: synthesis at the end of the task (problems, evidence, retained variables, limitations, implications) | 9 (Synthesis) | Task 1 notebook, Section 15 |
| [x] | Task 2: unit of observation, classes, target from `end_cause`, moment and purpose of the prediction | 4.1 | Task 2 notebook, Section 3 |
| [x] | Task 2: variables in the four categories, every exclusion justified | 4.2 | Task 2 notebook, Section 4 |
| [x] | Task 2: consequences of a false positive and a false negative | 4.3 | Task 2 notebook, Section 5 |
| [x] | Task 2: primary, complementary, operational and stability metrics, justified | 4.4 | Task 2 notebook, Section 6 |
| [x] | Task 2: temporal strategy (boundaries, number of folds, fold sizes, preprocessing inside the fold, test protection) | 4.5 | Task 2 notebook, Section 7 |
| [x] | Task 2: aggregation across folds (mean, variability, weighted or pooled, trend) | 4.6 | Task 2 notebook, Section 8 |
| [x] | Task 2: no-skill and simple baselines, interpreted | 4.7 | Task 2 notebook, Section 9 |
| [x] | Task 2: evaluation protocol summarised before optimisation | 4.8 | Task 2 notebook, Section 10 |
| [x] | Task 3: ablation of the four sets and the five questions (tariff, post history, user history, consistency over time, operational and ethical concerns) | 5.1 | Task 3 notebook, Section 3 |
| [x] | Task 3: at least three classification principles, justified (data types, imbalance, assumptions, interpretability, cost, relationships) | 5.2 | Task 3 notebook, Section 4 |
| [x] | Task 3: at least three ensembles of different principles, leak-free stacking, why they can improve | 5.3 | Task 3 notebook, Section 5 |
| [x] | Task 4: two or three models optimised, explicit search space, time order, positive-class metric | 6.1 | Task 4 notebook, Sections 3–4 |
| [x] | Task 4: optimised against initial configuration (meaningful and stable gain?) | 6.2 | Task 4 notebook, Section 5 |
| [x] | Task 4: one threshold criterion, chosen on validation data and applied unchanged to the test | 6.3 | Task 4 notebook, Section 6 |
| [x] | Task 4: default against selected threshold (precision, recall, F1, alert rate, per-1,000 counts) | 6.3 (default vs selected table) | Task 4 notebook, Section 6 |
| [x] | Task 4: calibration considered | 6.4 | Task 4 notebook, Section 7 |
| [x] | Task 4: interpretation of the final model, with limitations | 6.6 | Task 4 notebook, Section 10 |
| [x] | Task 5: final model chosen from development results only (performance, stability, cost, interpretability, operational implications) and baseline | 7.1 | Task 5 notebook, Section 2 |
| [x] | Task 5: refit on all development data, decisions fixed, test evaluated once | 6.5, 7, 8.3 | Task 4 notebook, Sections 8–9; Task 5 notebook, Sections 3–4 |
| [x] | Task 5: comparison with the baseline on PR-AUC, precision, recall, F1, balanced accuracy, MCC, alert rate and per-1,000 counts | 7.2 (final vs baseline table) | Task 5 notebook, Section 5 |
| [x] | Task 5: performance across time periods and groups (districts, posts) | 7.3 | Task 5 notebook, Sections 6–7 |
| [x] | Task 5: error analysis (false positives and false negatives) | 7.4 | Task 5 notebook, Section 8 |
| [x] | Task 5: interpretation suited to the model, with limitations | 7.5 | Task 5 notebook, Section 9 |
| [x] | Task 5: practical consequences of the threshold and usefulness for the operator | 7.6 | Task 5 notebook, Section 10 |
| [x] | Task 5: conclusion with findings, limitations and recommendations | 9 | Task 5 notebook, Section 11 |
| [x] | Submission: complete and reproducible notebook | 8.3 | whole notebook |
| [x] | Submission: final report | `docs/FINAL_REPORT.pdf` | |
| [x] | Submission: table of candidate, baseline and final models | 8.1 | Task 4 notebook, Section 13 |
| [x] | Submission: description of final preprocessing, features, hyperparameters and threshold | 8.2 | Task 4 notebook, Section 13 |
| [x] | Submission: reproducibility statement | 8.3 | |
| [x] | Submission: test used once, nothing changed after seeing it | 6.5, 8.3 | Task 4 notebook, Sections 8–9 |

The comparison with the statement found three wording gaps, fixed before the PDF was rebuilt:

| Done | Gap | How to check | Who | All? |
| --- | --- | --- | --- | --- |
| [x] | The bibliography still said "(Tasks 1 to 4)" | In the PDF, the statement's entry says "Tasks 1 to 5" | Manuela | no |
| [x] | Section 7.1 did not mention the operational implications of the choice | 7.1 has a sentence on what the choice means for the operator's work | Manuela | no |
| [x] | The recommendations were mixed with the limitations in the Synthesis | The last paragraph of chapter 9 states our recommendations in prose | Manuela | no |

## 1. Zip contents

| Done | Item | How to check | Who | All? |
| --- | --- | --- | --- | --- |
| [x] | The zip holds `Task1.ipynb` to `Task5.ipynb`, `MINDD_TP1_Relatorio.pdf` (English report), the zip's `README.md`, `requirements.txt` and `prepared/` with the 17 small files the notebooks read | `unzip -l` lists exactly these (tree in `specs/007-review-fixes-separate-notebooks/contracts/zip-layout.md`) | | no |
| [x] | Left out: the merged notebook `MINDD_Project1.ipynb`, the Portuguese report, the 179 MB CSV, `prepared/*.csv.gz` and the figure folders, `.venv/`, the reference notebooks, the statement PDFs, the earlier reports, `docs/report/`, this file, the study guides, `specs/`, `openspec/`, `.claude/`, `.specify/` and `.git/` | The `unzip -l` listing shows none of them | | no |
| [x] | The zip is named `MINDD-GPA-1200720-1221579-1231205.zip` (format `MINDD-GPA-NumberX-NumberY-NumberZ.zip`, student numbers in ascending order) | `ls ../entrega` | | yes |
| [ ] | The size fits the Moodle limit | The zip is 4.4 MB; compare with the limit on the submission page | | no |
| [x] | the zip's `README.md` mentions only files in the zip, maps each notebook to its task and chapter, says how to run one notebook alone and how to rebuild everything, and gives the setup and the CSV's SHA-256 (it is written in English) | Read it top to bottom | | no |

## 2. Notebook

| Done | Item | How to check | Who | All? |
| --- | --- | --- | --- | --- |
| [x] | Each task notebook runs on its own from the zip contents plus the CSV | `scripts/stage_run.py N` for N = 1..5: exit 0, 0 error cells (run log in `specs/007-.../runlog.md`) | | no |
| [x] | Each run saved the same results as the committed files | `scripts/compare_prepared.py N`: 0 differences (times, timestamps and paths ignored) | | no |
| [x] | The full run finished without errors | No cell shows an error; run time recorded (49 min) | | no |
| [x] | Test numbers equal those of 27/10 | Task 4 notebook, Section 9: PR-AUC 0.532 (model), 0.381 (B1), 0.178 (B0) | | no |
| [ ] | The title cell has the three names and student numbers right | Amir Masnavi 1221579, Inês Oliveira 1231205, Manuela Leite 1200720 | | yes |
| [x] | Outputs are saved in the file | Open the notebook without running anything and see tables and figures | | no |
| [ ] | The notebook opens on another computer | Another member opens the file from the zip in their Jupyter | | no |

## 3. Report

| Done | Item | How to check | Who | All? |
| --- | --- | --- | --- | --- |
| [ ] | The cover has the three names and student numbers | First page of the PDF. Numbers are right (1221579, 1231205, 1200720). Decide "Ines" (cover) or "Inês" (notebook and guides) | | yes |
| [x] | Abstract, chapters 1 to 9 and bibliography are present | PDF table of contents | | no |
| [x] | The Synthesis is updated with Task 5 | Chapter 9 covers the test, groups, errors and recommendations | | no |
| [x] | No "TODO", "??" or broken references | `pdftotext docs/FINAL_REPORT.pdf - \| grep -n -E 'TODO\|\?\?'` returns nothing; the LaTeX log has no "undefined" warnings | | no |
| [ ] | Figures are readable | View each figure at 100% zoom | | no |
| [x] | The PDF was built from the latest `main.tex` | `docs/FINAL_REPORT.pdf` is newer than the last edit of `main.tex` | | no |
| [x] | Notebook references name the task notebook ("Task N notebook, Section M"), with no "Part N", merged notebook or repository | `pdftotext docs/FINAL_REPORT.pdf - \| grep -c -E 'Part [0-9]\|MINDD_Project1\|repositor'` returns 0 | | no |
| [x] | The report reproduces no code | Leaf through the PDF: only column and function names, no code blocks | | no |

## 4. Consistency between notebook and report

| Done | Item | How to check | Who | All? |
| --- | --- | --- | --- | --- |
| [x] | Chapter 8 numbers equal the outputs | Task 4 notebook, Section 13 and Table 8.1: means 0.626 / 0.511 / 0.181; test 0.532 / 0.381 / 0.178 | | no |
| [x] | Threshold and alert rate match | Cut-off 0.490, 10% on development, 7.4% on the test (Task 4 notebook, Sections 6 and 9) | | no |
| [x] | The final set has 27 features in the right groups | Post history 8, user history 10, weather 4, calendar 2, location 2, concurrency 1 (Table 8.2) | | no |
| [x] | Final model and hyperparameters match | Gradient boosting, depth 6, learning rate 0.1, 200 iterations, minimum leaf 100 | | no |
| [x] | The Task 5 table matches the notebook | Task 5 notebook, Section 5 against Table 7.1 (F1 0.402, balanced accuracy 0.628, MCC 0.373) | | no |
| [x] | Sections 6.2 and 7.1 quoted different fit times (3.1 vs 12.0 s and 3.2 vs 12.6 s, from different runs). 7.1 now says "about four times cheaper" and points to 6.2 | 7.1 has no seconds, only the pointer to Section 6.2. If anyone prefers the Task 5 numbers, we revert | | yes |

## 5. Reproducibility

| Done | Item | How to check | Who | All? |
| --- | --- | --- | --- | --- |
| [x] | The reproducibility statement describes the zip, the environment, the standalone runs and the single test evaluation, without dates or a repository (spec 007; the dated run log is in `docs/MEMORY.md`) | Section 8.3 of the PDF | | no |
| [x] | The CSV's SHA-256 is the same in the report, `README.md` and the zip's `README.md` | `f6109dc066162bc770417c39294cdecc7519646c3cfa8c1d95671ea30f0e0a9b` in all three | | no |
| [ ] | The teammate check in `docs/TEAMMATE_CHECK.md` is done by someone who did not write the statement | That person replies "done, 0 questions" or sends their questions | | no |
| [x] | `prepared/task4_frozen.json` still has the 27/10 date | `git diff prepared/` shows nothing; the file says `2026-10-27T11:40:32` | | no |

## 6. Moodle upload

| Done | Item | How to check | Who | All? |
| --- | --- | --- | --- | --- |
| [ ] | Uploader and backup are chosen | Names written here | | yes |
| [ ] | Upload done by 18:00 on 31/10 | Time on the submission page | | no |
| [ ] | Screenshot of the submission saved | Image shared in the group chat | | no |
| [ ] | Someone else downloaded the zip from Moodle and opened the notebook and the PDF | Confirmation in the group chat | | no |
| [ ] | Pull request from `feature/task-1` to `main` reviewed and approved by someone who did not write it, before the upload | The PR shows as merged on GitHub | | no |
| [ ] | The repository is still private | GitHub, Settings, General, Danger Zone shows "private" | | no |
| [ ] | Everyone agrees this is the final version | Confirmation from all three at the meeting or in the group chat | | yes |

## 7. Report review fixes (spec 007)

| Done | Item | How to check | Who | All? |
| --- | --- | --- | --- | --- |
| [x] | Section 1.1 explains the smoothing (k + 1)/(n + 5) and how we found it, and how the 9,058 zero-energy normal sessions were found | Read Section 1.1 | | no |
| [x] | Section 4.3 derives t* = 1/(1 + c) and the 4.4 limit, with the share of sessions flagged at that cut-off | Read Section 4.3; the share equals the Task 4 notebook, Section 6 printout | | no |
| [x] | Each statistical technique is explained where it first appears (Spearman, Isolation Forest, VIF, Brier, log-loss, Wilcoxon, bootstrap, permutation importance, partial dependence, McNemar, balanced accuracy, MCC) | Read the sentence at each first use | | no |
| [x] | The counts read in order: 29 candidate features (Section 3.2), built from 27 columns (Table 4.1), reduced to 27 features (Section 5.1) | Abstract, Section 3.2, Tables 4.1 and 4.6 | | no |
| [x] | Course slides are cited as references only; techniques outside the course say "not covered in class; our research led us to it" | `pdftotext docs/FINAL_REPORT.pdf - \| grep -n -i slides` shows bibliography lines only | | no |
| [x] | A list of tables follows the list of figures | Front matter of the PDF | | no |
| [x] | Figures 4.1, 4.2, 5.1, 5.3, 6.1 and 7.1 are redrawn in their notebooks and readable at 100% zoom | View each one; smallest text at least 8 pt | | no |
| [x] | The notebook markdown follows the same slide wording and passed unslop and humanizer | Scanner figures in `specs/007-.../runlog.md` | | no |
