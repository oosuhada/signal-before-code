# Visual Trace — Binary Search

```text
values = [1, 4, 7, 10, 13, 17, 23]
          L         M           R

M = 10 < target 17
→ indices through M cannot contain 17
→ L = M + 1
```

Invariant: if the target exists, it remains in the current closed interval `[L, R]`. Binary search
works because one comparison proves an entire half impossible, not because “middle is fast.”

```bash
python3 scripts/trace.py binary-search --predict
python3 scripts/trace.py --wrong binary-search-no-monotonicity
```
