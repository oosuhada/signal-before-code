# Flash Recognition Mode

Read the signal, say **two candidates**, then say what additional fact would decide. The point is
candidate recall speed, not reflexively blurting one algorithm name.

| Signal | Candidate recall | Deciding question |
| --- | --- | --- |
| “minimum feasible capacity” | binary search on answer | is feasibility monotonic? |
| “dependency order” | topological sort / DFS cycle reasoning | directed prerequisites? need an order? |
| “repeated smallest element” | heap / sorting | does the candidate set change? |
| “longest contiguous substring under a condition” | sliding window / prefix-based method | does boundary movement preserve monotonic validity? |
| “next greater element” | monotonic stack | nearest one-sided greater/smaller relation? |
| “maximum in every window of size K” | monotonic queue / heap | can stale/out-of-window entries be removed efficiently? |
| “many static range sums” | prefix sum | are updates absent? |
| “merge overlapping bookings” | interval sort/sweep | can sorting by start expose all overlaps? |
| “all subsets, N=18” | bitmask / backtracking | need direct enumeration or pruning? |
| “same subproblem appears in many recursion branches” | memoization / DP | can future behavior be captured by a compact state? |
| “dynamic connectivity after unions” | Union-Find / traversal | need path details or only component identity? |
| “non-negative weighted shortest path” | Dijkstra | are there negative edges? |
| “prefix lookup for many words” | trie / hash set | query by full key or by prefix? |
| “top K frequent” | hash + heap / bucket/sort | size of K and value/count range? |
| “sorted pair sum” | two pointers / hash | can ordered elimination save memory and stay linear? |

## Drill rule

If you answer in under five seconds but cannot state the deciding assumption, count it as recognition
without defense—not mastery.
