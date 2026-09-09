# Visual Trace — Dijkstra

```text
A --4--> B --1--> D
 \1      ↑2
  v      |
  C --5->D

tentative: A=0 B=∞ C=∞ D=∞
finalize A → B=4 C=1
finalize C → B=3 D=6
finalize B → D=4
```

Invariant: with nonnegative edges, the smallest tentative distance cannot later be improved through
an unfinalized node. “Finalize” is a proof step, not merely a heap pop.

```bash
python3 scripts/trace.py dijkstra --predict
python3 scripts/trace.py --wrong dijkstra-negative-edge
```
