# Visual Trace — Topological Sort

Topological sort is easier to see as **prerequisites disappearing**.

```text
A → C → E → F
B → C
B → D → F

indegree 0 initially: A, B
emit A: C still waits for B
emit B: C and D become ready
```

Invariant: a node enters the ready queue only when every incoming prerequisite edge has been
accounted for. If processed count is smaller than node count, a dependency cycle prevented progress.

```bash
python3 scripts/trace.py topological-sort --predict
```
