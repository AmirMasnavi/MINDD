# Dataset guide

This guide describes the supplied `Charging_Data_educational.csv`. It draws on the assignment
and on the checks in [TP1_Task1_Data_Understanding_and_Preparation.ipynb](../TP1_Task1_Data_Understanding_and_Preparation.ipynb). The file is an educational adaptation of
the China EV Charging Dataset cited in the assignment. The local copy has 441,077
rows and 47 original columns, and its session starts run from 31 December 2019 to
31 December 2021. Each row appears to be one charging transaction. The checks found no
full-row duplicate and no duplicate `(UserID, Charging Post ID, Start Time)` key.

## Reading the outcome

The original CSV has no `is_Abnormal` column. The notebook creates it in memory
from `end_cause` under this project assumption:

| Label | Termination reasons | Reasoning |
| --- | --- | --- |
| 0 = normal | `Charging ends normally`; `User stops charging` | A user-requested stop counts as an intentional end, not an equipment or vehicle fault. |
| 1 = abnormal | The other 13 recorded causes. Each name contains "fault" or "failure" | These describe equipment, vehicle, connection, communication, or power failures. |

The PDF does not state this definition. The notebook (§4.2) tests it against the dataset's own
abnormal-count history columns, and it reproduces them in at least 99.97% of rows in all six windows. It yields 81,934
abnormal sessions (18.58%) and 359,143 normal sessions (81.42%). If "User stops
charging" counted as abnormal, the abnormal share would be 53.93%.
That alternative matches the history columns in at most 36% of rows. The team should still get
the instructor's confirmation before making final model claims with this label. A new or missing cause value must stop the
mapping for review instead of silently becoming abnormal. `end_cause` and the
derived label are outcomes, so neither can be a predictor at session start.

One `Location Information` category has a trailing tab in 18,370 rows.
Stripping the surrounding whitespace leaves the same 13 categories and is a justified
cleanup before encoding. The original CSV stays unchanged.

## Original field dictionary

Names match the CSV exactly. The suffixes `1D`, `7D`, `30D`, `180D` and `730D` mean
lookback windows of that many days. According to PDF p. 3, a "previous completed" outcome
excludes earlier-started sessions that are still active at prediction time.
The PDF does not give the smoothing formula for the rates. The notebook (§4.3) finds that every
rate equals (abnormal + 1) / (sessions + 5), a prior of 0.2 with weight 5, so an entity with no
history gets 0.2.

| CSV field | Meaning and timing |
| --- | --- |
| `UserID` | Account identifier. Available for lookup, but sensitive and high-cardinality. |
| `Charging Post ID` | Charging-post identifier. Available for lookup. |
| `Location Information` | Station location; known at start. |
| `District Name` | District of the station; known at start. |
| `Order creation time` | Recorded order creation timestamp. It should precede the start, but many rows conflict with that order. |
| `Transaction power/kwh` | Energy for the completed transaction; unavailable at start. CSV spelling uses lowercase `kwh`. |
| `Electricity cost/Yuan` | Final electricity charge; unavailable at start. |
| `Service charge/Yuan` | Final service charge; unavailable at start. |
| `Transaction Amount/Yuan` | Listed final total; equals electricity plus service charges in this CSV. |
| `Actual Payment/Yuan` | Final amount paid; can differ from listed total. |
| `Start Time` | Charging start timestamp and prediction-time anchor. |
| `End Time` | Charging end timestamp; unavailable at start. |
| `Payment time` | Recorded payment timestamp; unavailable at start. |
| `Temperature(℃)` | Weather estimate/forecast at start, as instructed by the PDF. |
| `Relative Humidity(%)` | Weather estimate/forecast at start. |
| `Precipitation(mm)` | Weather estimate/forecast at start. |
| `end_cause` | Termination reason; outcome known after the session. |
| `electricity_price` | Electricity price applicable at session start. |
| `tariff_period` | Start-time tariff interval. |
| `post_previous_sessions_1D` | Completed sessions at this post in prior 1 day. |
| `post_previous_abnormal_1D` | Completed abnormal sessions at this post in prior 1 day. |
| `post_previous_abnormal_rate_1D` | Provided smoothed prior abnormal rate for this post and window. |
| `post_previous_sessions_7D` | Completed sessions at this post in prior 7 days. |
| `post_previous_abnormal_7D` | Completed abnormal sessions at this post in prior 7 days. |
| `post_previous_abnormal_rate_7D` | Provided smoothed prior abnormal rate for this post and window. |
| `post_previous_sessions_30D` | Completed sessions at this post in prior 30 days. |
| `post_previous_abnormal_30D` | Completed abnormal sessions at this post in prior 30 days. |
| `post_previous_abnormal_rate_30D` | Provided smoothed prior abnormal rate for this post and window. |
| `post_hours_since_previous_completed_session` | Hours since the post's last completed session; blank when none exists. |
| `post_no_previous_completed_session` | Flag for no previous completed session at the post. |
| `post_hours_since_previous_completed_abnormal` | Hours since last completed abnormal session at this post; blank when none exists. |
| `post_no_previous_completed_abnormal` | Flag for no previous completed abnormal session at the post. |
| `is_new_user` | 1 for the account's first session in the file (verified in notebook §4.3). It depends on the observation window. |
| `user_previous_sessions_30D` | Completed sessions for this account in prior 30 days. |
| `user_previous_abnormal_30D` | Completed abnormal sessions for this account in prior 30 days. |
| `user_previous_abnormal_rate_30D` | Provided smoothed prior abnormal rate for this account and window. |
| `user_previous_sessions_180D` | Completed sessions for this account in prior 180 days. |
| `user_previous_abnormal_180D` | Completed abnormal sessions for this account in prior 180 days. |
| `user_previous_abnormal_rate_180D` | Provided smoothed prior abnormal rate for this account and window. |
| `user_previous_sessions_730D` | Completed sessions for this account in prior 730 days. |
| `user_previous_abnormal_730D` | Completed abnormal sessions for this account in prior 730 days. |
| `user_previous_abnormal_rate_730D` | Provided smoothed prior abnormal rate for this account and window. |
| `user_days_since_previous_completed_session` | Days since account's last completed session; blank when none exists. |
| `user_no_previous_completed_session` | Flag for no previous completed session for the account. |
| `user_days_since_previous_completed_abnormal` | Days since account's last completed abnormal session; blank when none exists. |
| `user_no_previous_completed_abnormal` | Flag for no previous completed abnormal session for the account. |
| `user_active_sessions_at_start` | Number of other sessions on the same account active at current start time; no unfinished outcome is used. |

## How to use this guide

Use the notebook for measurements and justification, this page for definitions,
and the assignment PDF for what it demands.
A field's presence in the CSV does not make it suitable for prediction.
The notebook holds the prediction-time grouping and the current preparation decisions.
Do not share raw user-level examples in reports or screenshots.
