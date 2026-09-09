# Personal learner progress

This directory is an **evidence ledger**, not a textbook completion tracker.

The 28 textbook chapters can all be complete while every learner metric here remains zero.

## Files

- [`learner-status.json`](learner-status.json) — aggregate personal evidence; initially all zero.
- [`schema.json`](schema.json) — schema for one actual attempt record.
- [`revisits.csv`](revisits.csv) — scheduled revisit ledger; header only until a real solve occurs.

Attempt records may be appended to `attempts.jsonl` later. The repository intentionally does not
ship a fake starter record.

## Metrics

```text
Attempted
Solved
Solved without hint
Correct pattern identified
Pattern-recognition failure
Implementation failure
Revisit success
Timed mocks completed
```

Rates are undefined (`n/a`) before the denominator exists. Zero attempts is not a 0% recognition
rate; there has been no evidence yet.

## Evidence rule

Do not update a success field because:

- the textbook contains a solution;
- the same problem exists in `codetest-study`;
- AI explained the algorithm;
- a judge solution was read without a fresh attempt.

Update it only after an actual session described by [`../attempts/TEMPLATE.md`](../attempts/TEMPLATE.md)
or [`../revisits/TEMPLATE.md`](../revisits/TEMPLATE.md).
