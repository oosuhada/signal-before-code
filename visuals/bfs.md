# Visual Trace — BFS

```text
A
├─ B
│  ├─ D
│  └─ E
└─ C
   └─ F

queue=[A]
visit A → queue=[B,C]
visit B → queue=[C,D,E]
visit C → queue=[D,E,F]
```

The FIFO queue preserves discovery layers. In an unweighted graph, every node currently in a later
layer requires at least as many edges as nodes already ahead of it.

```bash
python3 scripts/trace.py bfs --predict
python3 scripts/trace.py --wrong bfs-visited-too-late
```
