# Decision Boundaries — signals narrow candidates; they do not dictate answers

Use this table to ask the **next discriminating question**. Never stop at the candidate column.

| Signal / requirement | Candidate set | Next boundary question |
| --- | --- | --- |
| unweighted shortest hops | BFS | are all edge costs truly equal? |
| nonnegative weighted shortest path | Dijkstra | can negative edges appear? |
| reachability only | BFS / DFS | is shortest distance or memory shape important? |
| prerequisite-respecting order | Topological Sort | can cycles exist, and what should they mean? |
| repeated connectivity merges | Union-Find | do you need an actual path or only same-component? |
| repeated current min/max | Heap | online updates, top K, or full sorted output? |
| one minimum | Linear scan | is this query repeated? |
| full ordered output | Sort | must updates occur between queries? |
| sorted pair relation | Two Pointers | does one comparison eliminate a boundary monotonically? |
| contiguous + monotonic validity | Sliding Window | do negatives or non-monotonic effects break boundary repair? |
| many static range sums | Prefix Sum | are there online updates? |
| monotonic feasible/infeasible answer | Binary Search | prove the predicate changes in one direction only |
| local choice seems best | Greedy candidate | can you exchange an optimal solution toward the local choice? |
| repeated subproblem state | DP / memoization | what exactly does one state mean? |
| all combinations, small N | Backtracking / Bitmask | what is the exponential budget? |
| next greater/smaller | Monotonic Stack | is the question one-sided or does a window expire old items? |
| window max/min | Monotonic Queue | which candidates are dominated and which expire by age? |

The same word can map to different candidates. “Shortest” may mean BFS, Dijkstra, DP on a DAG, or
something else depending on edge cost and state structure. The table is therefore a question
generator, not an answer sheet.
