# Project 1 presentation script (MINDD 2026/27)

Slides: `docs/MINDD_TP1_Presentation.pptx` (12 slides, about 13 min plus questions). The text below is the same as the
speaker notes in the file. Portuguese version: `docs/GUIAO_APRESENTACAO.md`. The two have the same slides, times and
numbers.

## Who presents what

| Who | Slides | Time | Content | Commits behind it |
| --- | --- | --- | --- | --- |
| Amir | 1 to 4 | about 4:00 | Introduction and Task 1: target, leakage, post history, time-based split | `724de72` project setup, `4c97b8b` Task 1 EDA, `beb9039` minimal version, `99cc6aa` Task 1 sections 0 to 6 |
| Inês | 5 to 8 | about 4:30 | Task 2: temporal folds, PR-AUC, baselines. Task 3: ablation, six models | `eb92ca6` Task 2 first version, `ede6a52` Task 2 fixes, `cb75870` Task 3 first version |
| Manuela | 9 to 12 | about 4:45 | Task 4: tuning, cut-off 0.490, freeze. Task 5: test 0.532 against 0.381. Conclusion | `14db8b2` Task 4 rework and `task4_frozen.json`, `8c7e7ac` Task 5 integrated into the report, all report commits |

Inês also wrote the first version of the Task 4 (`ede6a52`) and Task 5 (`c093d9f`) notebooks and Task 1 sections 7 to
10 (`defc15a`). Amir also fixed the Task 3 temporal evaluation and preprocessing (`a5be2d8`, `aa17d1b`).

There are two handovers: Amir ends slide 4 with "Over to Inês" and Inês ends slide 8 with "Over to Manuela".

---

## Amir: slides 1 to 4

### Slide 1. Abnormal EV charging sessions (about 45 s)

Introduce the group. The project asks whether the information available when a charging session starts can predict
that it will end abnormally. We follow the five tasks in order: data, evaluation protocol, models, optimisation and the
final test.

Optional line on who did what: "Inês wrote the first version of the notebooks for Tasks 2 to 5, I wrote the first
version of Task 1 and the protocol fix in Task 3, and Manuela integrated the tasks and wrote the report."

### Slide 2. The problem and the data (about 1 min)

We have 441 thousand sessions over two years at 92 posts. The file does not contain is_Abnormal, so we built it from
the end cause. A user stopping the session counts as normal, because it is the user's choice. The evidence that the
definition is right: the counts of earlier failures supplied with the dataset match ours in about 100% of the rows,
against less than 36% with the alternative definition. Only 18.6% of the sessions are abnormal, so a model that always
says "normal" is already 81% accurate, and accuracy is not a useful metric.

### Slide 3. Only what is known at the start (about 1 min 15 s)

The first rule of the project: a variable can only be a predictor if it is known when the session starts. Energy,
costs and duration separate the classes very well, but they describe the result; using them would be leakage. The best
legitimate variable reaches 0.77. We also noticed two details. The supplied failure rates are smoothed: they add one
imaginary failure in five imaginary sessions, so a post with no history always gets 0.2, and one failure in one
session gives 0.33 instead of 1. We confirmed the formula by recomputing it in all six windows. And 9,058 normal
sessions delivered no energy; we kept them, because the energy is only known at the end.

### Slide 4. Post history is the strongest signal (about 1 min)

This chart is the main result of the exploration: when the post's 7-day failure rate is split into deciles, the
abnormal share rises from 4% to 60%. User history helps too, but less. The data are not stable over time, so the
split is chronological. Task 1 ends with 29 candidate features in 7 groups, built from 27 columns; Task 3 will reduce
them to 27 features. Over to Inês.

---

## Inês: slides 5 to 8

### Slide 5. Evaluate as in real use (about 1 min 15 s)

Before training any model we fixed how it would be evaluated. A random K-fold would mix weeks of training and
validation and give optimistic results, so we use four expanding-window folds: training grows and always validates on
the next quarter. The first three months are a burn-in, because the history columns are still incomplete. The last
quarter of 2021 is the test and is used for no choice. The primary metric is PR-AUC, because the positive class is the
minority. We do not know the cost ratio c, so the best cut-off 1/(1+c) cannot be fixed yet; instead we report fixed
alert budgets.

### Slide 6. First, two baselines (about 1 min)

We defined two baselines. B0 is no skill: its PR-AUC equals the abnormal share of each fold, between 0.16 and 0.21,
which shows that no skill is not a fixed number. B1 uses only the post's 7-day failure rate as its score, fits
nothing, and already reaches 0.511 on average. That is the bar the models have to clear.

### Slide 7. Which information helps? (about 1 min)

To see which information is worth having, we added the feature groups one at a time and measured the gain with the
same reference model. Post history makes almost all the difference: PR-AUC goes from 0.29 to 0.58. User history adds
0.03. The tariff adds nothing beyond the hour. Removing the post identifier even helps, because the history already
says what matters and the model stops memorising posts. The final set has 27 features: the 29 candidates without
post_id and the tariff.

### Slide 8. Six models, three principles (about 1 min 15 s)

We trained three classifiers built on different principles, logistic regression, Naive Bayes and a decision tree, and
three ensembles: random forest, gradient boosting, and a stacking model built in time order so that nothing leaks. All
of them beat B1 in every fold except Naive Bayes. Gradient boosting leads with 0.626, but the random forest is only
0.003 behind, inside our 0.005 tolerance, so both go on to optimisation. Over to Manuela.

---

## Manuela: slides 9 to 12

### Slide 9. Tune, then freeze before the test (about 1 min 15 s)

We tuned gradient boosting, the random forest and the tree with a grid search, always on the same four folds and in
time order. No configuration improved by more than the tolerance, so the final model is the Task 3 gradient boosting.
The cut-off was chosen on development data so that 10% of the sessions raise an alert, which gives 0.490, almost the
default 0.5. We checked calibration and nothing needed correcting. All these choices were written to a file before the
test was read.

### Slide 10. Test result: Oct to Dec 2021 (about 1 min 15 s)

Only after freezing everything did we evaluate the test, once. The model reaches a PR-AUC of 0.532, against 0.381 for
B1 and 0.178 for no skill. At the frozen cut-off it alerts on 7.4% of the sessions, and 68% of those alerts are real
failures. Per thousand sessions: 50 correct alerts, 24 false ones and 126 failures without an alert. With the same
number of alerts, B1 gets 38 right and 36 wrong. Performance falls from development, but most of the fall comes from
the lower abnormal share of the quarter.

### Slide 11. Where it works and where it fails (about 1 min)

The margin over B1 holds in every district and station. Permutation importance confirms that the model lives on post
history. The error analysis shows the limit: sessions that start a few hours after a failure at their post get almost
all the alerts, while failures that come after a quiet period are almost never flagged; they are half of the missed
failures. New users, with no history, are also served worse.

### Slide 12. Conclusion (about 1 min 15 s, then questions)

To answer the question: partly, yes. Start-time information gives a useful ranking of the posts that are failing now,
well above the simple rule, but it cannot see failures that give no signal in the recent history. The main
limitations: we do not know the costs or the response capacity, the signal weakens over time, and user history has
privacy implications. We recommend getting the real costs, refitting the model regularly and adding maintenance data.
Everything is reproducible: each notebook runs on its own, with seed 42 and pinned versions. Thank you; we are happy to
take questions.

---

## Questions

Everyone answers questions about their own slides. The likely questions and model answers are in
`docs/STUDY_GUIDE.md` (Amir's part, Inês's part, Manuela's part and the common questions at the end).
