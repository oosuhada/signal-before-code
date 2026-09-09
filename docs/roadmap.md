# Roadmap — Feature Complete at v0.6

The repository has reached the intended training-system boundary. New algorithm chapters or product
features are no longer the default source of value; actual learner evidence is.

## v0.2 — Complete Textbook

- 28 intuition-first chapters;
- constraint and complexity guides;
- selection map, comparisons, wrong turns, mutation ladders;
- 168 curated practice problems;
- textbook status separated from learner mastery.

## v0.3 — See the Algorithm

- machine-readable trace schema;
- 12 core visual algorithms plus 2D DP trace;
- ASCII/Markdown state views;
- `--step` and predict-before-reveal CLI modes;
- wrong-state traces.

## v0.4 — Understand Its Boundaries

- 24 mutation chains;
- 20 smallest-counterexample documents;
- constraint and requirement mutation drills;
- online/offline and static/dynamic comparisons;
- 56 adversarial recognition prompts;
- Break-My-Algorithm CLI.

## v0.5 — Train and Measure Weaknesses

- actual-attempt recorder and expanded failure taxonomy;
- confidence tracking and calibration;
- explainable spaced-repetition scheduler;
- due/weakest/unseen/recognition/implementation practice modes;
- timed mock generation/review;
- synthetic fixtures isolated from real progress.

## v0.6 — Transfer to Interviews and Real Engineering

- 29 canonical Java implementations covering all 28 chapters;
- Python→Java implementation-friction guide;
- 28 oral defenses with 30-second, 2-minute, and deep follow-up modes;
- random interview CLI;
- code-less reasoning and whiteboard drills;
- coding-test and debugging strategies;
- verified applied case studies with “Why not another algorithm?” defenses.

## After v0.6 — practice, do not manufacture mastery

The valuable directories now are:

```text
attempts/
revisits/
mixed/
mocks/
progress/
```

Only real sessions may create claims such as:

```text
solved
hint-free
mastered
interview passed
```

Do not mark catalog problems as mastered because a solution exists elsewhere or because the textbook
contains the algorithm. When a genuine gap appears during practice, improve the smallest relevant
explanation, trace, counterexample, or test rather than restarting a feature-expansion cycle.

## Deferred topics

Topics such as 0-1 BFS, Bellman-Ford, MST/Kruskal, Fenwick/segment trees, SCC, advanced DAG DP,
meet-in-the-middle, or string matching remain mutation-derived extensions. Add one only when actual
practice evidence shows the existing 28-chapter model cannot explain a recurring decision boundary.
