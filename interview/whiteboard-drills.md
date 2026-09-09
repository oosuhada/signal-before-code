# Whiteboard Implementation Drills

Use no IDE, autocomplete, previous solution, or AI. State the invariant first, then write pseudocode
or compilable code from memory.

## Core set

| Drill | Must say before writing | Boundary test |
| --- | --- | --- |
| Hash frequency | processed prefix is summarized exactly | duplicate keys |
| Two pointers pair sum | discarded boundary cannot form target | no solution |
| Variable sliding window | window summary matches `[left,right]` | smallest valid window |
| Binary search | answer remains inside chosen interval | first/last element |
| Heap top-K | heap stores only useful current candidates | K=1 / K=N |
| Reverse linked list | reversed prefix + reachable suffix | one node |
| Tree DFS | each call returns a defined subtree fact | null root |
| BFS | queue preserves discovery layers | disconnected node |
| Iterative DFS | stack stores unfinished branches | cycle |
| Union-Find | each component has one representative root | repeated union |
| Topological sort | ready queue contains zero-indegree nodes | directed cycle |
| Dijkstra | extracted non-stale minimum is final | duplicate heap entry |
| Prefix sum | prefix[i] summarizes values before i | empty range |
| Merge intervals | merged suffix is final before next interval | touching endpoints |
| 1D DP | define dp[i] in one sentence | base sizes 0/1 |
| 2D DP | define both dimensions before recurrence | first row/column |
| 0/1 knapsack | current item used at most once | capacity exactly weight |
| Monotonic stack | stack contains unresolved monotonic candidates | duplicates |
| Monotonic queue | deque front is window extremum | expired maximum |
| Trie | path spells a prefix | word vs prefix only |
| Bitmask subsets | bit i means choose item i | empty/full mask |

## Review rule

Do not grade only syntax. After writing, answer:

- Which line enforces the invariant?
- Which line is most likely to be off by one?
- What input makes recursion/overflow/memory a concern in Java?
- Which mutation would make this implementation the wrong algorithm entirely?
