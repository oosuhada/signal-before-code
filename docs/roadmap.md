# Roadmap after v0.2

v0.2 changes the repository contract: the textbook is intentionally complete before personal study.
Future work should improve evidence and explanations rather than inflate topic count by default.

## v0.2 — textbook complete, learner evidence empty

- 28 intuition-first chapters complete;
- constraint/complexity guides;
- algorithm selection map;
- neighboring-pattern comparisons;
- wrong-turn library;
- mutation atlas;
- 168-problem curated roadmap with review-only answer metadata;
- recognition quiz and flash drill;
- personal attempt/revisit/mixed/mock templates;
- CI that validates textbook and learner-layer separation.

## v0.3 — personal evidence begins

Only actual sessions can create these artifacts:

- first-attempt logs;
- hint-free results;
- pattern-recognition failures;
- implementation failures;
- Day 3 / Day 14 / Day 30+ revisit results;
- mixed-set classification scores;
- timed mock reports.

No migration should mark historical catalog problems as solved merely because solution code exists in
another repository. If old submission history is linked, it remains historical context until a
`signal-before-code` evidence session explicitly records what was reconstructed.

## Possible textbook extensions

Add only when the current 28 chapters expose a real gap:

- 0-1 BFS;
- Bellman-Ford / negative-edge shortest path;
- minimum spanning tree / Kruskal;
- Fenwick tree / segment tree;
- strongly connected components;
- advanced DAG DP;
- meet-in-the-middle;
- string matching.

These should enter as mutation-derived needs, not as a race toward a larger catalog.
