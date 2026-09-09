# Wrong-Turn / Counterexample Library

Correct solutions teach what works. Small counterexamples teach the **boundary of applicability**.
Every entry follows the same attack pattern: tempting idea → why plausible → smallest counterexample
→ step-by-step failure → correct signal → better candidates → general lesson.

## Search and traversal

- [BFS on a weighted graph](bfs-on-weighted-graph.md)
- [DFS first path treated as shortest](dfs-first-path-shortest.md)
- [Marking BFS visited too late](bfs-visited-too-late.md)
- [Binary search without monotonicity](binary-search-without-monotonicity.md)
- [Topological sort on a cycle](topological-sort-on-cycle.md)
- [Union-Find for shortest path](union-find-for-shortest-path.md)

## Sequence / ordering / maintained state

- [Sliding window with negative values](sliding-window-with-negative-values.md)
- [Two pointers on unsorted pair sum](two-pointers-unsorted-pair.md)
- [Heap for one-time minimum](heap-for-one-time-min.md)
- [Sorting a stream after every update](sort-stream-every-update.md)
- [Trusting stale heap priorities](stale-heap-priority.md)
- [Static prefix sums with updates](prefix-sum-with-updates.md)
- [Monotonic stack with wrong direction](monotonic-stack-wrong-direction.md)
- [Trie for one exact lookup](trie-for-one-exact-lookup.md)

## Search / optimization state

- [Greedy without a proof](greedy-counterexample.md)
- [Greedy on arbitrary coin systems](greedy-arbitrary-coins.md)
- [DP overengineering](dp-overengineering.md)
- [DP with ambiguous state meaning](dp-wrong-state-definition.md)
- [Backtracking after N outgrows the tree](backtracking-large-n.md)
- [Recursion without progress](recursion-without-progress.md)

Use `python3 scripts/challenge.py --list` to see the corresponding active-recall claims.
