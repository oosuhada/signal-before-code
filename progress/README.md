# Personal learning evidence

This directory is **not textbook content**. It is the state layer produced only by real learner
actions. The repository may ship engines and schemas here, but it must not manufacture successes.

Current baseline remains zero attempts; `progress/attempts.jsonl` is intentionally absent until
`scripts/attempt.py` records a real session.

## Record one attempt

```bash
python3 scripts/attempt.py start
python3 scripts/attempt.py start --problem leetcode-217
```

The pattern answer stays hidden until the learner enters a guess and confidence `1..5`. A record can
distinguish constraint misread, recognition failure, wrong algorithm, complexity error,
implementation bug, edge case, off-by-one, DP state-definition failure, invariant failure, timeout,
and memory limit. Canonical names live in [`failure-taxonomy.json`](failure-taxonomy.json).

## Review scheduling

The scheduler is intentionally explainable rather than Anki-like:

```text
successful Day 0  → Day 3
successful Day 3  → Day 14
successful Day 14 → Day 30+

failure at early stage → retry tomorrow
failure at later stage → retry in three days
```

The next due date is written to each real attempt record. There is no separate opaque scheduling
database to drift out of sync.

## Select practice from evidence

```bash
python3 scripts/practice.py --mixed 5
python3 scripts/practice.py --unseen 5
python3 scripts/practice.py --recognition-only 5
python3 scripts/practice.py --due 5
python3 scripts/practice.py --weakest 5
python3 scripts/practice.py --implementation 5
```

`--due`, `--weakest`, and `--implementation` refuse to invent a queue when no real attempts exist.

## Analytics

```bash
python3 scripts/progress.py
```

With no learner data it must print `No real learner attempts recorded yet.`. With data, it reports
hint-free solve rate, pattern-recognition rate, implementation rate, revisit results, failure modes,
pattern-by-pattern metrics, and confidence calibration.

High-confidence wrong classifications are intentionally weighted more heavily in weakness scoring:
they are stronger evidence of a misconception than a low-confidence miss.

The example in [`../fixtures/demo-user.json`](../fixtures/demo-user.json) is explicitly synthetic and
exists only for tests/documentation. It is never loaded by the default progress commands.
