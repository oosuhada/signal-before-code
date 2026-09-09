# Visual Trace — Monotonic Stack

For next-greater-element style questions, the stack stores only unresolved candidates.

```text
values = [2,1,4,3,5]

read 2 → stack [2]
read 1 → stack [2,1]
read 4 → 1 and 2 are resolved by 4
         stack [4]
```

Invariant: stack values remain monotonic. Once a current value resolves a smaller top, keeping that
top would add no future information.

```bash
python3 scripts/trace.py monotonic-stack --predict
```
