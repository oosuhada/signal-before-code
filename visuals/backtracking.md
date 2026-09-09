# Visual Trace — Backtracking

The reusable state transition is **choose → explore → undo**.

```text
[]
├─ choose 1 → [1]
│  ├─ choose 2 → [1,2]
│  │  └─ ...
│  └─ undo 2 → [1]
└─ undo 1 → []
```

Invariant: mutable path state represents exactly the decisions on the current root-to-node branch.
Undo must restore the parent state before a sibling branch begins.

```bash
python3 scripts/trace.py backtracking --predict
```
