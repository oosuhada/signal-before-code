# Progress and mastery records

This directory tracks **selection quality**, not a solved-count leaderboard.

## Two layers of record

1. Rich reasoning lives in a copy of [`../attempts/TEMPLATE.md`](../attempts/TEMPLATE.md).
2. A compact JSON Lines record can be appended to `progress/attempts.jsonl` after the session so
   aggregate metrics can be calculated.

No `attempts.jsonl` file is committed in v0.1 because there are no real attempts yet. Create it with
one JSON object per line when the first session happens.

The allowed record shape is described in [`schema.json`](schema.json).

Example shape **for documentation only — do not paste it as fake progress**:

```text
problem_key: platform-id
date: YYYY-MM-DD
level: Understand | Recognize | Apply | Mixed | Mock
pattern_guess: what I wrote before implementation
pattern_correct: true | false
solved: true | false
used_hint: true | false
failure_mode: null | pattern_recognition | complexity | implementation | edge_case | explanation
revisit_stage: day0 | day3 | day14 | day30plus
```

## Summary command

```bash
python scripts/progress.py
```

It reports:

- attempted records;
- solved without hint;
- correct pattern identified;
- implementation failures;
- pattern-recognition failures;
- pattern-recognition rate;
- hint-free solve rate;
- revisit success rate.

Missing data is shown as `n/a`; the script does not invent zero-denominator percentages.

## Revisit queue

[`revisits.csv`](revisits.csv) is intentionally a plain CSV. Add a row only after a real Day 0
attempt.

Recommended schedule:

```text
Day 0  → first solve
Day 3  → no previous code
Day 14 → mixed set
Day 30+ → explain from scratch, then implement
```
