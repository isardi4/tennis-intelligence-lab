# Tennis Intelligence Lab
## Project Master Plan

**Working title:** Tennis Intelligence Lab  
**Primary use case:** Predict ATP tennis matches and tournaments using only information that would have been available before the prediction date.  
**Initial historical cutoff:** **2025-12-31**  
**Primary backtest period:** **2026 season**  
**Status:** Planning / Phase 0  
**Document role:** Long-term source of truth for the project. Codex and contributors should read this file before significant work.

---

# 1. Vision

Tennis Intelligence Lab is an end-to-end data, analytics, machine-learning, and simulation platform for professional tennis.

The project should answer questions such as:

- Who is more likely to win a specific match?
- How does the playing surface affect that probability?
- How much does recent form matter?
- Are certain player styles systematically favorable or unfavorable against others?
- How difficult is each player's path through a tournament draw?
- What is each player's probability of reaching every round?
- How much did the actual draw improve or reduce a player's title probability?
- Which players are systematically over- or underrated by rankings?
- Which statistics actually improve predictive accuracy?
- Can playing styles or matchup archetypes be discovered from data?
- Can the system explain *why* it prefers one player over another?

The long-term goal is to combine:

1. Data engineering
2. Tennis analytics
3. Statistical modeling
4. Machine learning
5. Monte Carlo simulation
6. Backtesting and model evaluation
7. Interactive visualization
8. Explainable predictions
9. Eventually, an AI analysis layer

The project should be useful as a portfolio project, a research playground, and a reusable tennis analytics platform.

---

# 2. North Star

The ultimate product experience should support a user selecting a tournament, for example:

> Australian Open 2026

and seeing:

- the full draw,
- player ratings,
- match win probabilities,
- probability of reaching each round,
- title probability,
- draw difficulty,
- upset candidates,
- dangerous unseeded players,
- likely paths,
- and explanations of important matchup dynamics.

Example output:

| Player | R16 | QF | SF | Final | Champion |
|---|---:|---:|---:|---:|---:|
| Player A | 95.1% | 83.2% | 66.5% | 48.8% | 29.4% |
| Player B | 96.8% | 88.7% | 71.9% | 51.3% | 31.2% |
| Player C | 84.3% | 63.9% | 38.4% | 19.7% | 8.4% |

The user should also be able to inspect:

> Why does the model give Player A 61% against Player B?

The explanation must be grounded in actual model features, for example:

- stronger surface-adjusted Elo,
- better recent return performance,
- more rest,
- favorable style matchup,
- best-of-five advantage,
- or other measured factors.

The system must never invent explanations unrelated to the actual model.

---

# 3. Core Research Principle: Simulate the Past Honestly

The project is built around **temporal correctness**.

The first major experiment will use:

> **All information available up to and including 2025-12-31**

in order to predict:

> **the 2026 tennis season**

This means the system must behave as if the future were unknown.

## Forbidden leakage

When predicting a match on date `D`, the feature pipeline must never use:

- matches occurring after `D`,
- rankings published after `D`,
- Elo updates resulting from the target match,
- later rounds of the same tournament,
- future 2026 season aggregates,
- future injuries or withdrawals,
- future draw changes,
- future rankings,
- future surface results,
- manually entered knowledge of what later happened.

This principle takes precedence over model performance.

A weaker model with honest historical evaluation is preferable to a stronger model with leakage.

---

# 4. Backtest Strategy

Initial historical timeline:

```text
Historical data:
1968 ─────────────────────────────── 2025-12-31
                                      │
                                      │ hard model-training cutoff
                                      ▼
Prediction period:
2026-01-01 ────────────────────────── 2026-12-31
```

Priority evaluation targets:

1. Australian Open 2026
2. Roland Garros 2026
3. Wimbledon 2026
4. US Open 2026
5. Masters 1000
6. ATP 500
7. ATP 250
8. Full ATP season
9. Challenger Tour, later

No cherry-picking successful tournaments.

---

# 5. Crucial Distinction: Frozen Model vs Frozen Information

Two experiments must be clearly separated.

## Frozen model

Model parameters are trained only using information through **2025-12-31**.

## Historical online features

When predicting a July 2026 match, it is legitimate to use matches from January-June 2026 because those results were already known at prediction time.

Therefore the preferred realistic backtest is:

```text
model parameters frozen at 2025-12-31
+
features updated chronologically during 2026
```

This allows Elo and recent form to evolve naturally without retraining the ML model.

A stricter secondary experiment may also use:

```text
all information frozen at 2025-12-31
```

Both modes must be labeled clearly and never mixed.

---

# 6. V1 Scope

V1 should support:

- ATP men's singles
- historical match data
- rankings
- player metadata
- court surface
- tournament level
- tournament round
- Elo ratings
- surface Elo
- recent form
- basic serve statistics
- basic return statistics
- head-to-head features
- fatigue / workload features
- probabilistic match prediction
- tournament draw ingestion
- Monte Carlo tournament simulation
- round-by-round advancement probabilities
- title probabilities
- historical backtesting
- model calibration evaluation
- basic web interface

## Out of scope for V1

Do not block V1 on:

- WTA
- doubles
- betting products
- live betting
- live point-by-point prediction
- video analysis
- computer vision
- biomechanical analysis
- proprietary commercial feeds
- complicated deep learning architectures
- mobile apps
- social features
- user accounts
- monetization

---

# 7. Data Sources

The architecture must treat data sources as replaceable adapters.

No core model should depend directly on one external schema.

## 7.1 Jeff Sackmann tennis datasets

Primary candidate for the historical foundation.

Expected data includes:

- ATP matches
- tournaments
- players
- rankings
- winner / loser
- surface
- round
- ranking at match time
- scores
- serve statistics for many matches
- Challenger data

Likely initial canonical historical source.

The raw source should not automatically be committed to Git.

## 7.2 Match Charting Project

Optional advanced source.

Potential uses:

- point sequences
- shot-level information
- serve directions
- rally structure
- winners and errors
- tactical tendencies
- player style modeling

Coverage is incomplete.

Therefore the base prediction model must **not** require this source.

## 7.3 Rankings

Historical rankings must always be joined as they existed at prediction time.

Never use current ranking to reproduce a historical match.

## 7.4 Tournament draws

The simulator will require actual historical draws.

Eventually support:

- seeds
- qualifiers
- lucky losers
- withdrawals
- byes
- updated draws
- draw state as known at a given timestamp

Historical reproducibility matters.

---

# 8. Data Licensing

Licensing is a first-class engineering constraint.

Maintain:

```text
docs/data_sources.md
```

For every source:

```yaml
source_name:
source_url:
license:
commercial_use_allowed:
redistribution_allowed:
attribution_required:
raw_data_committed_to_repo:
notes:
```

Do not redistribute data publicly without verifying the license.

If the data source is non-commercial only, keep the architecture replaceable for future commercial use.

---

# 9. Repository Philosophy

This should not become a notebook graveyard.

Notebooks are allowed for:

- exploration,
- charts,
- hypothesis testing,
- model diagnostics.

Production logic belongs in normal Python modules.

Guiding principle:

```text
reproducible pipeline > impressive notebook
```

---

# 10. Proposed Repository Structure

```text
tennis-intelligence-lab/
│
├── README.md
├── PROJECT_PLAN.md
├── AGENTS.md
├── CHANGELOG.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── configs/
│   ├── base.yaml
│   ├── features.yaml
│   ├── models.yaml
│   └── tournaments.yaml
│
├── data/
│   ├── raw/
│   ├── staging/
│   ├── processed/
│   └── external/
│
├── src/
│   └── tennis_lab/
│       ├── ingestion/
│       │   ├── sackmann.py
│       │   ├── rankings.py
│       │   ├── draws.py
│       │   └── match_charting.py
│       ├── cleaning/
│       │   ├── matches.py
│       │   ├── players.py
│       │   └── tournaments.py
│       ├── features/
│       │   ├── elo.py
│       │   ├── surface.py
│       │   ├── form.py
│       │   ├── serve.py
│       │   ├── return_stats.py
│       │   ├── head_to_head.py
│       │   ├── fatigue.py
│       │   ├── opponent_adjustment.py
│       │   └── matchup.py
│       ├── models/
│       │   ├── baseline.py
│       │   ├── logistic.py
│       │   ├── gradient_boosting.py
│       │   ├── calibration.py
│       │   └── registry.py
│       ├── simulation/
│       │   ├── match.py
│       │   ├── bracket.py
│       │   └── monte_carlo.py
│       ├── evaluation/
│       │   ├── metrics.py
│       │   ├── backtest.py
│       │   ├── calibration.py
│       │   └── reports.py
│       ├── api/
│       └── utils/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_elo_experiments.ipynb
│   ├── 03_feature_research.ipynb
│   └── 04_model_diagnostics.ipynb
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── regression/
│
├── scripts/
│   ├── download_data.py
│   ├── build_dataset.py
│   ├── train_model.py
│   ├── backtest.py
│   └── simulate_tournament.py
│
├── docs/
│   ├── architecture.md
│   ├── data_sources.md
│   ├── data_dictionary.md
│   ├── modeling.md
│   ├── evaluation.md
│   └── decisions/
│
└── frontend/
```

This is a target structure, not something to create empty on day one.

Avoid abstractions that are not yet needed.

---

# 11. Canonical Data Model

The project should own its own canonical tennis schema.

External source column names should not leak across the entire codebase.

## Player

```text
player_id
source_player_id
first_name
last_name
full_name
hand
birth_date
country_code
height_cm
```

## Tournament

```text
tournament_id
name
season
start_date
surface
level
location
country
draw_size
best_of
```

Potential levels:

```text
GS
M1000
ATP500
ATP250
CH
ITF
```

## Match

Represent participants neutrally, even if the raw source stores winner/loser.

```text
match_id
tournament_id
match_date
round
surface
best_of
player_1_id
player_2_id
winner_id
score
minutes
```

Modeling feature tables must never expose `winner_id` as a predictive feature.

## Match player statistics

Prefer long format:

```text
match_id
player_id
aces
double_faults
serve_points
first_serves_in
first_serve_points_won
second_serve_points_won
service_games
break_points_saved
break_points_faced
```

Derived statistics:

```text
ace_rate
double_fault_rate
first_serve_in_pct
first_serve_win_pct
second_serve_win_pct
service_points_won_pct
break_points_saved_pct
```

## Rankings

```text
ranking_date
player_id
rank
ranking_points
```

Historical joins must use the latest ranking available at or before prediction time.

---

# 12. Feature Store Philosophy

Every feature must answer:

> Could this value have been known at the moment this prediction would have been made?

Features should either include an explicit `as_of_date` or be generated chronologically.

Avoid unconstrained aggregations over the complete dataset.

---

# 13. Baselines

Before ML, establish strong transparent baselines.

## Baseline 0 — ATP ranking

Purpose:

- sanity check
- minimum benchmark

## Baseline 1 — Overall Elo

Implement Elo internally.

Generic expectation formula:

```text
expected_A = 1 / (1 + 10 ^ ((elo_B - elo_A) / scale))
```

Research parameters:

- initial Elo
- K factor
- tournament weighting
- inactivity handling
- retirements
- best-of-five effects

## Baseline 2 — Surface Elo

Maintain ratings for:

- hard
- clay
- grass

Potential blend:

```text
effective_rating = alpha * surface_elo + (1 - alpha) * overall_elo
```

Tune `alpha` only on pre-2026 validation data.

---

# 14. Elo Research Roadmap

Potential variants:

- classic Elo
- dynamic-K Elo
- surface Elo
- recency-decayed Elo
- tournament-weighted Elo
- margin-aware Elo
- set-based Elo
- game-based Elo
- inactivity regression
- Glicko
- Bayesian rating systems

Do not implement them all at once.

Each new version must justify itself against the existing baseline.

---

# 15. Recent Form Features

Candidate windows:

```text
last_5_matches
last_10_matches
last_20_matches
last_52_weeks
last_90_days
last_180_days
```

Potential features:

```text
win_rate
opponent_adjusted_win_rate
average_opponent_elo
elo_change
sets_won_pct
games_won_pct
tiebreak_win_pct
```

Surface equivalents:

```text
hard_recent_form
clay_recent_form
grass_recent_form
```

Control for small samples.

---

# 16. Serve Features

Rolling candidates:

```text
ace_rate
double_fault_rate
first_serve_in_pct
first_serve_win_pct
second_serve_win_pct
service_points_won_pct
hold_rate
break_points_saved_pct
```

Possible later normalization:

- opponent-adjusted
- surface-adjusted
- recency-weighted

---

# 17. Return Features

Potential features:

```text
return_points_won_pct
first_serve_return_points_won_pct
second_serve_return_points_won_pct
break_rate
break_points_converted_pct
```

Return quality should receive equal analytical attention to serving.

---

# 18. Opponent Adjustment

Raw stats are context-dependent.

Potential methods:

- residualization against opponent quality
- Elo-based adjustment
- iterative offense/defense ratings
- expected-vs-actual performance
- hierarchical models later

This is a research area, not a Phase 0 requirement.

---

# 19. Head-to-Head

Candidate features:

```text
h2h_matches
h2h_wins
h2h_win_pct
h2h_surface_matches
h2h_surface_win_pct
h2h_last_24_months
```

H2H has small samples.

The model should be allowed to conclude that H2H adds little predictive value.

---

# 20. Fatigue and Workload

Possible features:

```text
days_since_last_match
matches_last_7_days
matches_last_14_days
matches_last_30_days
sets_last_7_days
sets_last_14_days
games_last_7_days
games_last_14_days
minutes_last_7_days
minutes_last_14_days
previous_match_duration
previous_match_sets
```

Travel/timezone features are later-stage ideas.

---

# 21. Age and Career Stage

Possible features:

```text
age
age_squared
career_matches
career_surface_matches
```

Avoid hard-coded assumptions about peak age.

Let out-of-time data determine whether the effect is useful.

---

# 22. Best-of-Five

Grand Slam men's matches differ structurally.

Potential features:

```text
best_of_5
career_bo5_record
bo5_elo
fifth_set_record
```

A basic `best_of_5` indicator should precede specialized metrics.

---

# 23. Tournament Context

Potential variables:

```text
tournament_level
round
surface
best_of
seeded_status
home_country
```

Possible later variables:

- altitude
- indoor/outdoor
- court speed
- weather
- ball type

Not V1 requirements.

---

# 24. Matchup Modeling

Long-term differentiator.

The project should eventually move beyond:

> Player A is stronger than Player B.

Toward:

> Player A's style is particularly favorable against Player B's style.

## Statistical player profiles

Potential player vector:

```text
serve_strength
return_strength
ace_dependency
first_serve_dependency
second_serve_strength
aggression
break_rate
hold_rate
tiebreak_frequency
surface_bias
rally_profile
```

## Player archetypes

Potential methods:

- K-Means
- Gaussian Mixture Models
- hierarchical clustering
- PCA + clustering
- UMAP for visualization

Possible emergent archetypes:

- big server
- serve + forehand attacker
- aggressive baseliner
- balanced all-court player
- return-oriented baseliner
- defensive counterpuncher

Labels should be assigned after inspecting clusters rather than imposed in advance.

## Similarity engine

Potential methods:

- standardized Euclidean distance
- cosine similarity
- Mahalanobis distance
- PCA-space distance
- learned embeddings later

## Matchup effects

Possible experiment:

```text
Player A baseline expected win rate: 68%

vs Big Servers:       -4.1 pp
vs Counterpunchers:   +3.7 pp
vs Aggressive Base:   +0.9 pp
```

Use shrinkage and significance checks.

Do not report noise as tactical truth.

---

# 25. Model Progression

## Model A — Ranking baseline

No ML.

## Model B — Elo

No ML.

## Model C — Logistic Regression

Candidate feature differences:

```text
elo_diff
surface_elo_diff
ranking_diff
age_diff
recent_form_diff
serve_strength_diff
return_strength_diff
fatigue_diff
```

This should be the first serious model because it is interpretable.

## Model D — Gradient Boosted Trees

Candidates:

- XGBoost
- LightGBM
- CatBoost

Only after the logistic pipeline is trustworthy.

## Model E — Advanced models

Optional later research:

- Bayesian models
- neural networks
- embeddings
- sequence models

---

# 26. Prediction Output

Models must output probabilities.

Not just:

```text
Player A wins
```

but:

```text
P(Player A wins) = 0.643
P(Player B wins) = 0.357
```

Calibration matters.

A model that predicts 70% should be correct approximately 70% of the time in that probability bucket.

---

# 27. Evaluation Metrics

Accuracy alone is not enough.

Primary metrics:

- Log Loss
- Brier Score
- Accuracy
- Calibration Error
- ROC-AUC, secondary

Calibration buckets:

```text
Predicted 50-55% → actual win rate?
Predicted 55-60% → actual win rate?
Predicted 60-65% → actual win rate?
...
```

Tournament-level evaluation:

- round probability calibration
- winner probability quality
- upset identification
- bracket likelihood

---

# 28. Calibration

Potential methods:

- Platt scaling
- isotonic regression
- beta calibration

Calibration must itself be trained only on historical pre-evaluation data.

Never calibrate on the tournament being evaluated.

---

# 29. Temporal Cross-Validation

Random train/test split is forbidden for production evaluation.

Example:

```text
Train:       <= 2022
Validation:  2023
Test:        2024

Train:       <= 2023
Validation:  2024
Test:        2025

Final:
Train/tune:  <= 2025-12-31
Backtest:    2026
```

Exact windows may evolve; chronological integrity may not.

---

# 30. Frozen 2025 Model Artifact

The first flagship model must be frozen using only pre-2026 information.

Once declared frozen:

**Do not retune it using 2026 results.**

Suggested artifact structure:

```text
artifacts/
└── frozen_2025_model/
    ├── model.*
    ├── feature_config.yaml
    ├── training_manifest.json
    ├── metrics_pre_2026.json
    └── README.md
```

Suggested Git tag:

```text
v0.1-frozen-2025
```

---

# 31. Grand Slam Historical Simulation

For each 2026 Slam:

1. reconstruct the draw as known before tournament start,
2. generate player features as of tournament start,
3. calculate required pairwise match probabilities,
4. run Monte Carlo simulations,
5. save pre-tournament probability tables,
6. compare with reality only afterward.

Prediction artifacts should be immutable.

Example:

```text
predictions/
└── 2026/
    ├── australian_open_pre_tournament.parquet
    ├── roland_garros_pre_tournament.parquet
    ├── wimbledon_pre_tournament.parquet
    └── us_open_pre_tournament.parquet
```

---

# 32. Tournament Simulation Engine

Inputs:

```text
draw
players
match_probability_function
number_of_simulations
```

Outputs per player:

```text
R2 probability
R3 probability
R4 probability
QF probability
SF probability
Final probability
Champion probability
```

Requirements:

- deterministic seed support
- reproducible results
- configurable number of simulations
- unit-tested bracket propagation
- vectorized where useful

V1 target:

```text
100,000 tournament simulations
```

Optimize only if needed.

---

# 33. Draw Difficulty

A flagship derived analytic.

Question:

> How favorable or difficult was the actual draw for a player?

Potential methodology:

1. simulate actual draw,
2. generate many hypothetical valid draws respecting seeding rules,
3. simulate those draws,
4. compare actual title probability with the neutral/random distribution.

Metrics:

```text
actual_title_probability
median_random_draw_title_probability
draw_luck_delta
draw_difficulty_percentile
```

Example:

```text
Player A
Actual draw title probability:    28.4%
Neutral draw median probability:  33.2%
Draw effect:                      -4.8 pp
Draw difficulty percentile:       89th
```

---

# 34. Path Difficulty

For each player estimate difficulty by round.

Possible metrics:

```text
expected opponent Elo
expected opponent surface Elo
expected match win probability
```

Future opponents are uncertain, so expected values should incorporate branch probabilities.

---

# 35. Upset Detection

Candidate definitions:

```text
lower-ranked player model probability > 40%
```

or

```text
model probability materially higher than ranking-baseline probability
```

Keep the definition configurable and measurable.

---

# 36. Player Pages

Potential sections:

```text
Player Name
Country
Age
Ranking
Overall Elo
Surface Elo
Recent Form
Serve Profile
Return Profile
Surface Performance
Similar Players
Tournament Probabilities
Match History
```

Potential visualizations:

- Elo history
- ranking history
- surface split
- serve/return percentile chart
- rolling form
- model strength over time

---

# 37. Match Pages

Example:

```text
Player A vs Player B
Roland Garros 2026
Quarterfinal
Clay
Best of 5
```

Display:

```text
Model probability
Elo probability
Surface Elo probability
ATP ranking
Recent form
Serve comparison
Return comparison
Fatigue
Head-to-head
```

Explain using actual model factors.

---

# 38. Explainability

For linear models:

- coefficients
- standardized feature impacts

For boosted-tree models:

- SHAP or equivalent

Example structured explanation:

```text
Player A: 64.2%

Positive factors:
+ Surface Elo advantage
+ Better recent return performance
+ More rest

Negative factors:
- Lower recent serve performance
- Slight H2H disadvantage
```

Do not introduce LLM-generated explanations until structured explanations already exist.

---

# 39. AI Analyst — Future Phase

Possible questions:

> Why is Player A favored over Player B?

> Who has the hardest Wimbledon draw?

> Which unseeded player has the highest quarterfinal probability?

> Compare two players' hard-court profiles.

Architecture:

```text
User
 ↓
LLM / agent
 ↓
approved analytical tools
 ↓
model outputs / semantic layer
 ↓
structured answer
```

The LLM should never calculate predictive probabilities independently.

---

# 40. Data Pipeline

```text
External datasets
       │
       ▼
Raw immutable files
       │
       ▼
Validation
       │
       ▼
Canonical tables
       │
       ▼
Feature generation
       │
       ▼
Training dataset
       │
       ▼
Model
       │
       ▼
Predictions
       │
       ▼
Tournament simulator
       │
       ▼
API / UI
```

Raw data remains immutable.

Transforms must be reproducible.

---

# 41. Storage

Recommended V1 stack:

- Parquet
- DuckDB

Reasons:

- fast analytical queries
- SQL support
- minimal infrastructure
- easy Python integration
- ideal for local development and portfolio work

Potential later migration:

- PostgreSQL
- BigQuery

Do not start with cloud infrastructure unless there is a concrete need.

---

# 42. Python Stack

Initial candidate stack:

```text
Python
Polars or Pandas
DuckDB
PyArrow
scikit-learn
XGBoost / LightGBM later
Pydantic
FastAPI later
pytest
```

Avoid Spark unless scale genuinely requires it.

---

# 43. Experiment Tracking

At minimum save:

```text
experiment_id
timestamp
git_commit
data_cutoff
feature_set
model_type
hyperparameters
train_period
validation_period
test_period
metrics
```

Initially JSON/YAML is enough.

Possible later tools:

- MLflow
- Weights & Biases

Only add them when useful.

---

# 44. Reproducibility

Every published result should answer:

```text
Which data version?
Which code commit?
Which cutoff date?
Which feature set?
Which model?
Which parameters?
Which random seed?
```

Predictions must be reproducible.

---

# 45. Testing Strategy

## Unit tests

Critical cases:

- Elo update calculation
- historical cutoff logic
- surface filtering
- rolling features
- ranking as-of joins
- draw propagation
- match simulation
- probability totals

## Leakage tests

Mandatory.

For a target match:

```text
max(source_match_date_used_for_features) < target_match_date
```

Automate this assertion.

## Integration tests

Example:

```text
raw matches
→ clean data
→ features
→ prediction
```

## Regression tests

Freeze selected known outputs so refactors do not silently change them.

---

# 46. Data Quality Checks

Examples:

```text
winner != loser
player IDs exist
surface in allowed set
rank > 0 if present
0 <= percentage <= 1
serve_points >= first_serves_in
first_serve_points_won <= first_serves_in
```

Track missingness by:

- year
- tournament
- level
- player

Never silently convert missing statistics into zero.

---

# 47. Missing Data Strategy

Potential approaches:

- explicit missing indicators
- medians by era/surface
- model-native missing handling
- feature exclusion for early historical periods

Document every decision.

Do not invent data.

---

# 48. Retirements and Walkovers

Need explicit classification:

```text
completed
retirement
walkover
default
```

Potential starting policy:

- walkovers excluded from match-outcome training
- retirements excluded from normal completed-match training or analyzed separately
- completed matches used normally

Later, injury/retirement risk may become a separate modeling problem.

---

# 49. Player Identity

Use stable source IDs whenever possible.

Names are presentation attributes, not keys.

Potential issues:

- accents
- spelling changes
- duplicate names
- nationality changes

Build a canonical mapping layer.

---

# 50. Temporal Semantics

Analytical data should clearly distinguish:

```text
event_date
available_at
as_of_date
```

These concepts may differ.

A Monday ranking should not be usable for a Sunday prediction.

---

# 51. Phase 0 — Data Source Spike

## Goal

Prove that the historical source data is sufficient.

Tasks:

- obtain ATP dataset
- inspect files
- inspect seasons through 2025
- identify player tables
- identify rankings
- identify match statistics
- measure missingness
- inspect surface coverage
- inspect tournament levels
- inspect Grand Slam matches
- document licensing
- create initial data dictionary

Deliverable:

```text
docs/data_source_spike.md
```

Success condition:

We can reconstruct a clean ATP match table through **2025-12-31** and clearly exclude 2026.

---

# 52. Phase 1 — Canonical Historical Dataset

Build:

```text
matches.parquet
players.parquet
rankings.parquet
```

Tasks:

- normalize dates
- normalize surfaces
- normalize player IDs
- normalize tournament levels
- handle missing values
- classify match status
- validate uniqueness
- add tests

Deliverable:

```text
scripts/build_dataset.py
```

---

# 53. Phase 2 — Elo Engine

Implement:

- overall Elo
- surface Elo
- pre-match ratings
- post-match updates
- historical Elo table

Feature rows must use **pre-match Elo**.

Deliverables:

```text
src/tennis_lab/features/elo.py
tests/unit/test_elo.py
```

Benchmark Elo against ATP ranking.

---

# 54. Phase 3 — Historical Feature Pipeline

Initial feature set:

```text
overall_elo_diff
surface_elo_diff
ranking_diff
age_diff
recent_win_rate_diff
recent_elo_change_diff
serve_strength_diff
return_strength_diff
rest_days_diff
```

Every feature must be chronologically valid.

Deliverable:

```text
training_matches.parquet
```

---

# 55. Phase 4 — Baseline Modeling

Train and compare:

1. ranking baseline
2. Elo baseline
3. surface Elo
4. logistic regression

Evaluate with temporal validation.

Document in:

```text
docs/model_baselines.md
```

Do not move to boosted trees before this phase is trusted.

---

# 56. Phase 5 — Advanced Feature Engineering

Experiment with:

- serve features
- return features
- opponent adjustment
- fatigue
- tournament level
- round
- best-of-five
- H2H
- age curves
- surface form

Every feature addition should be tested through ablation.

Core question:

> Does this feature improve out-of-time log loss?

If not, remove it or keep it only as exploratory analytics.

---

# 57. Phase 6 — Freeze Pre-2026 Model

Requirements:

- hyperparameter tuning complete
- feature definitions frozen
- model artifact saved
- validation metrics documented
- Git commit tagged

No 2026 result may influence this frozen model.

---

# 58. Phase 7 — Australian Open 2026

First flagship historical demonstration.

Steps:

1. load actual pre-tournament draw,
2. reconstruct player features as of tournament start,
3. generate match probabilities,
4. run Monte Carlo simulation,
5. save predictions,
6. compare against actual result afterward.

Outputs:

- title probabilities
- round probabilities
- draw difficulty
- upset candidates
- explanation of favorites
- post-event evaluation

---

# 59. Phase 8 — All 2026 Grand Slams

Repeat identical methodology for:

- Roland Garros
- Wimbledon
- US Open

Do not tournament-specifically retune based on earlier 2026 Slam results if the experiment is meant to represent the frozen 2025 model.

At the end compare performance across:

- surfaces
- rounds
- ranking bands
- favorites vs underdogs

---

# 60. Phase 9 — Full 2026 Backtest

Predict every eligible ATP match sequentially.

Maintain separate evaluation modes:

## Frozen information mode

Everything fixed as of 2025-12-31.

## Historical online mode

Model parameters frozen, but Elo/recent form/statistics updated with already completed 2026 matches.

Historical online mode is the main realistic benchmark.

---

# 61. Phase 10 — Product UI

Only after the model pipeline is stable.

Candidate stack:

```text
FastAPI
React / Next.js
```

Potential routes:

```text
/
/players
/players/{id}
/matches/{id}
/tournaments
/tournaments/{id}
/model
```

---

# 62. Research Questions Backlog

These are questions, not promises.

- How much better is surface Elo than overall Elo?
- What is the best blend between surface and overall Elo?
- How quickly should older results decay?
- Does H2H improve out-of-time predictions?
- Does recent form add value beyond Elo?
- Is ATP ranking still useful once Elo is included?
- Do serve and return metrics materially improve predictions?
- How should Challenger results be weighted?
- How much does best-of-five reduce upset probability?
- Can player archetypes improve matchup predictions?
- Can we identify style-specific matchup edges?
- Is fatigue measurable from match history alone?
- How predictive are tiebreak results?
- Are break-point metrics mostly noise after serve/return quality is included?
- Can draw difficulty be summarized with one intuitive metric?

---

# 63. Challenger Expansion

Potential later use cases:

- emerging players
- early detection
- ranking inefficiencies
- transition from Challenger to ATP

Possible future feature:

> Breakout Player Detector

This should come after the core ATP pipeline works.

---

# 64. WTA Expansion

Architecture should avoid ATP-specific assumptions when unnecessary.

WTA is not V1.

When ATP is stable:

- add WTA ingestion
- train independently
- compare feature behavior

Do not assume ATP model coefficients transfer to WTA.

---

# 65. Betting-Market Benchmark — Optional

Not a core product goal.

If historical bookmaker probabilities are legally available, they can be used as a benchmark:

```text
our model log loss
vs
market implied probability log loss
```

The project is not intended as a gambling system.

---

# 66. Product Design Principle

The UI should answer:

> What does the model believe, and why?

Prefer:

- clear probabilities
- percentiles
- comparisons
- concise explanations
- progressive detail

Avoid overwhelming users with raw tables by default.

---

# 67. Definition of Success

## Technical success

- reproducible pipelines
- temporal correctness
- automated tests
- deterministic simulations
- clear lineage

## Modeling success

The model materially improves on ATP ranking and ideally standard Elo on out-of-time probability metrics.

## Product success

A user can inspect a tournament and understand:

- favorites
- paths
- dangerous opponents
- probabilities
- reasons

## Portfolio success

A technical reviewer can see competence in:

- data engineering
- analytics engineering
- statistics
- machine learning
- software engineering
- product thinking
- communication

---

# 68. What We Must Not Do

Avoid:

- data leakage
- random train/test splits for final evaluation
- tuning on 2026
- using future rankings
- using final tournament results when building pre-tournament features
- overcomplicated cloud architecture early
- deep learning for prestige
- LLMs before the analytical system works
- improper redistribution of licensed data
- claiming causality from prediction features
- hiding bad predictions
- cherry-picking successful tournaments

---

# 69. Engineering Principles

1. **Correctness before sophistication**
2. **Historical reproducibility before model score**
3. **Simple baseline before complex model**
4. **Calibration before headline accuracy**
5. **Modular data sources**
6. **Automated leakage tests**
7. **Configuration over hard-coded values**
8. **Notebooks for research, modules for reproducibility**
9. **Every model improvement must beat a benchmark**
10. **Never hide failures**

---

# 70. Working With Codex

Codex must treat this document as the project's strategic source of truth.

Before significant work:

1. Read `PROJECT_PLAN.md`.
2. Read `AGENTS.md`.
3. Inspect existing architecture.
4. Identify the current phase.
5. Make the smallest coherent implementation toward that phase.

Codex should not independently redefine product goals.

If a proposed implementation conflicts with this document, surface the conflict before proceeding.

---

# 71. Codex Working Rules

## Do

- write tests
- prefer readable code
- document assumptions
- preserve temporal correctness
- use typed interfaces where useful
- isolate source adapters
- keep feature generation deterministic
- log experiment metadata
- update docs when architecture changes

## Do not

- silently change schemas
- create unnecessary abstractions
- introduce infrastructure without a concrete need
- commit huge raw datasets
- use 2026 outcomes to tune the frozen pre-2026 model
- rewrite large working areas without a reason

---

# 72. Architecture Decision Records

Important decisions go in:

```text
docs/decisions/
```

Example files:

```text
ADR-001-use-duckdb.md
ADR-002-canonical-player-schema.md
ADR-003-elo-update-method.md
```

Each ADR contains:

```text
Context
Decision
Alternatives
Consequences
```

---

# 73. Research Log

Optionally maintain:

```text
docs/research_log.md
```

Each entry:

```text
date
question
experiment
result
interpretation
next_step
```

Negative experiments are valuable and should be recorded.

---

# 74. First Concrete Milestone

Initial target:

> Given any completed ATP match before 2026, reconstruct what was knowable immediately before it and calculate a valid Elo-based win probability.

Pipeline:

```text
raw historical matches
       ↓
chronological ordering
       ↓
pre-match Elo A
pre-match Elo B
       ↓
probability
       ↓
actual result
       ↓
evaluation
```

If this is not correct, do not build more sophisticated models.

---

# 75. First Codex Mission

Suggested prompt:

> Read `PROJECT_PLAN.md` completely before changing code.
>
> We are beginning Phase 0 of Tennis Intelligence Lab.
>
> The project's first model-training cutoff is 2025-12-31. The 2026 season must be treated as unseen evaluation data.
>
> Create the minimal project structure required to perform a data-source spike on the Jeff Sackmann ATP datasets.
>
> Do not build the frontend, boosted models, AI agents, or cloud infrastructure.
>
> Goals:
> 1. Create a reproducible data download/import process.
> 2. Inspect available ATP match, player, and ranking datasets through 2025.
> 3. Produce a report with schemas, row counts, year coverage, missingness, match-stat coverage, surfaces, and tournament levels.
> 4. Verify that 2026 can be cleanly excluded through an explicit date cutoff.
> 5. Add basic automated tests.
> 6. Document data licensing and attribution requirements.
>
> Prefer a simple local stack using Python, Parquet, and DuckDB unless the existing repository gives a strong reason not to.
>
> Before implementation, summarize the approach and list the files you intend to create or modify.

---

# 76. Phase 0 Definition of Done

Phase 0 is complete when:

- project installs locally
- raw data can be obtained reproducibly
- matches through 2025 are queryable
- players are identifiable
- rankings are queryable
- match-stat coverage is documented
- 2026 is excluded by an automated cutoff
- licenses are documented
- basic ingestion tests pass

---

# 77. MVP Definition

The first usable MVP is:

> Select two ATP players and a historical match date and obtain a historically valid pre-match win probability.

It should include:

```text
overall Elo
surface Elo
ATP ranking
recent form
basic serve/return features
probability
model explanation
```

A tournament UI is not required for this MVP.

---

# 78. Flagship V1 Definition

Flagship V1 is complete when the system can:

1. ingest a Grand Slam draw,
2. create historically valid player features,
3. predict every required matchup,
4. simulate the tournament,
5. calculate round/title probabilities,
6. measure draw difficulty,
7. display results in a usable interface,
8. reproduce predictions from a saved model/data snapshot.

Primary showcase:

> **2026 Grand Slam Forecasts generated using a model trained only through 2025.**

---

# 79. Long-Term Differentiators

## Draw Intelligence

Not just title probability, but how the actual draw changes it.

## Matchup Intelligence

Not just who is stronger, but whose game fits the opponent.

## Explainability

Clear reasons behind model probabilities.

## Historical Replay

Travel to any historical date and reproduce what the model would have believed then.

## Model Laboratory

Compare:

```text
ATP ranking
Elo
surface Elo
logistic model
boosted model
```

under identical temporal evaluation rules.

## Player Archetypes

Discover data-driven playing styles.

---

# 80. Open Questions

Do not block Phase 0 on these:

- Exact starting year for training?
- Include Challenger matches in Elo?
- How should Challenger Elo interact with ATP Elo?
- How should retirements be handled?
- Separate indoor/outdoor hard?
- How should inactivity affect ratings?
- What is the best surface Elo blend?
- Which rolling windows are stable for serve/return metrics?
- How complete is historical match-stat coverage?
- Which source should provide historical draws?
- Should the simulator model matches directly or simulate sets?
- How should qualifiers be treated?
- How do we model players with little ATP history?
- How should injuries be incorporated?
- Can Match Charting Project add useful style information despite sparse coverage?

Record resolved questions as ADRs.

---

# 81. Roadmap Summary

```text
PHASE 0
Data source spike
      ↓
PHASE 1
Canonical historical dataset
      ↓
PHASE 2
Elo engine
      ↓
PHASE 3
Historical feature pipeline
      ↓
PHASE 4
Ranking / Elo / Logistic baselines
      ↓
PHASE 5
Advanced features
      ↓
PHASE 6
Freeze model using data through 2025-12-31
      ↓
PHASE 7
Australian Open 2026 backtest
      ↓
PHASE 8
All 2026 Grand Slams
      ↓
PHASE 9
Full 2026 season backtest
      ↓
PHASE 10
Product UI
      ↓
PHASE 11+
Style / matchup / AI analysis
```

---

# 82. The Rule to Remember

Whenever the project becomes complicated, return to this question:

> **Can we use only information available at that point in time to estimate who will win, explain why, and propagate those probabilities through a tournament draw?**

If a feature, architecture decision, visualization, or AI component does not help answer that question, it is probably not a priority.

---

# 83. Immediate Next Step

Do **not** begin with React.

Do **not** begin with XGBoost.

Do **not** begin with an AI agent.

Do **not** begin by predicting Roland Garros.

Begin by proving:

```text
Can we build a trustworthy historical tennis dataset through 2025
and reproduce pre-match state without seeing the future?
```

Once that works, everything else becomes possible.

---

# 84. Project North Star

**Build an honest, reproducible, explainable tennis forecasting engine capable of simulating tournaments and evaluating itself against the unseen 2026 season.**
