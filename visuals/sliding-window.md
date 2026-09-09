# Visual Trace — Sliding Window

Demo condition: longest positive-number window with sum `<= 5`.

```text
[2, 1, 3, 2, 1]
 L-----R          sum = 6   invalid

remove 2

[2, 1, 3, 2, 1]
    L--R          sum = 4   valid again
```

The important fact is not “two indices move.” It is that all values are positive, so removing the
leftmost value can only decrease the sum. That gives the boundary motion a useful direction.

```bash
python3 scripts/trace.py sliding-window --predict
python3 scripts/trace.py --wrong sliding-window-negative
```
