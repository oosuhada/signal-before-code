# Visual Trace — Union-Find

```text
parent = [0,1,2,3,4,5]

union(0,1)
parent = [0,0,2,3,4,5]

union(2,3)
parent = [0,0,2,2,4,5]

union(1,2)
find(1)=0, find(2)=2
→ merge representatives
```

Invariant: each element reaches one representative root for its component. Path compression may
change internal parent pointers without changing which component an element belongs to.

```bash
python3 scripts/trace.py union-find --predict
```
