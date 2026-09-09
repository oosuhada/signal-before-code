# Visual Trace — DFS

DFS uses unfinished branches as explicit state.

```text
stack=[A]
visit A → stack=[C,B]
visit B → stack=[C,E,D]
visit D → stack=[C,E]
```

The top of the stack is the next branch to deepen. Siblings stay behind as return points. Recursive
DFS hides the same stack in call frames; iterative DFS makes it visible.

```bash
python3 scripts/trace.py dfs --predict
```
