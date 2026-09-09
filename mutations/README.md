# Mutation Lab — learn the boundary, not the label

A pattern becomes useful knowledge when one changed assumption makes you reconsider it. The
canonical machine-readable map is [`chains.json`](chains.json). Every transition answers:

```text
What changed?
→ Which proof/invariant stopped working?
→ Which candidate set should replace it?
```

These are **candidate transitions**, not a cookbook. A real problem may contain several signals at
once, and constraints still decide whether a theoretically valid approach is practical.

## High-value chains

```text
unweighted shortest path
→ BFS
  edge weights become 0/1
→ 0-1 BFS candidate
  arbitrary nonnegative weights
→ Dijkstra candidate
  negative edge appears
→ Dijkstra finalization proof breaks
```

```text
sorted pair sum
→ Two Pointers
  ordering removed, exact complement lookup remains
→ Hash candidate
  requirement becomes contiguous range sum
→ Sliding Window if boundary movement is monotonic
  negative values appear
→ Prefix Sum / Hash / Monotonic Queue candidates
```

```text
one minimum from static data
→ Linear scan
  need full sorted output
→ Sort
  repeated min with insertions
→ Heap
```

Study [`../docs/decision-boundaries.md`](../docs/decision-boundaries.md) beside the chains, then use
[`../scripts/challenge.py`](../scripts/challenge.py) to attack claims with small counterexamples.
