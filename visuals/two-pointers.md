# Visual Trace — Two Pointers

Question: in a sorted array, which boundary becomes impossible after one comparison?

```text
[1, 2, 4, 6, 8]
 L           R

1 + 8 = 9 < 10
even the largest partner is too small for value 1
→ discard index 0

[1, 2, 4, 6, 8]
    L        R
2 + 8 = 10
```

Invariant: every index outside `[L, R]` has already been ruled out using sorted order. The discarded
side never needs reconsideration.

Try predicting each boundary move:

```bash
python3 scripts/trace.py two-pointers --predict
```
