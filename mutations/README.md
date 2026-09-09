# Mutation Atlas

Mutation practice changes one assumption and asks whether the original algorithm survives.

| Original condition | Mutation | Selection shift |
| --- | --- | --- |
| unweighted shortest path | arbitrary non-negative weights | BFS → Dijkstra |
| weights are 0/1 | only two edge costs 0 and 1 | Dijkstra candidate → 0-1 BFS candidate |
| sorted pair sum | input becomes unsorted | two pointers → sort first or hash |
| positive-number sum window | negative values allowed | ordinary shrinking window may fail → prefix-based reasoning |
| static range sums | point updates added | prefix sum → Fenwick/segment tree territory |
| one minimum query | repeated insert + extract-min | scan → heap |
| static connectivity | many edge additions + queries | traversal → Union-Find |
| DAG prerequisite graph | cycle introduced | topological order becomes impossible |
| non-negative shortest path | negative edge introduced | Dijkstra guarantee disappears |
| coin system has greedy property | arbitrary denominations | greedy may fail → DP |
| enumerate all subsets | only best value per subset-state needed | bitmask enumeration → bitmask DP candidate |
| nearest greater element | maximum over every moving window | monotonic stack → monotonic queue |

## How to use a mutation

For every solved problem, write one sentence in this form:

> “My solution relies on ______. If ______ changed, I would reconsider ______ because ______.”

That sentence tests whether you learned a name or an applicability boundary.
