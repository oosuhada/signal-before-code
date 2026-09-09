# Reading Constraints Before Choosing an Algorithm

Constraints are not decoration. They are often the first piece of evidence that tells you which
approaches are still alive.

The useful question is not “what complexity matches this exact number?” It is:

> **Which families of approaches can I eliminate before I write code?**

## A rough feasibility lens

These ranges are interview heuristics, not laws. Language, constants, input shape, memory limit,
runtime environment, and the amount of work inside the loop all matter.

| Rough input size | Approaches worth considering | What should make you suspicious |
| ---: | --- | --- |
| `N <= 20` | `O(2^N)`, subset enumeration, backtracking, bitmask DP | `O(N!)` may still be too large unless pruning is strong |
| `N <= 100` | `O(N^3)` can sometimes fit; `O(N^2)` is usually comfortable | expensive nested work inside cubic loops |
| `N <= 1,000` | `O(N^2)` may be realistic | repeated sorting or cubic state transitions |
| `N ~ 100,000` | usually `O(N log N)` or `O(N)` territory | pair enumeration, repeated scans, per-query `O(N)` work |
| `N ~ 1,000,000` | often linear or near-linear with small constants | heavy object allocation, quadratic anything |

Do not convert this table into a memorized answer key. A `100,000`-element input does not prove that
the solution is `O(N log N)`. It only tells you that an obvious `O(N^2)` approach probably needs a
very strong reason to survive.

## Read all dimensions

Many mistakes come from reading only `N`.

```text
N = number of nodes
M = number of edges
Q = number of queries
K = target/top-K/number of selections
W = capacity or state dimension
alphabet = possible symbols
value range = can values index an array directly?
```

Examples:

- `N = 100,000`, `Q = 100,000`, and every query scans `N` items → `O(NQ)` is the real danger.
- `N = 200`, `W = 100,000` in knapsack → `O(NW)` may be much larger than `N` suggests.
- `V = 100,000`, `E = 120,000` → adjacency list traversal is near-linear; adjacency matrix storage
  is not.

## Constraint phrases that act like signals

### “Return any pair / detect existence”

If the naive approach checks every pair, ask whether you can remember previous values with a hash
table or exploit ordering with two pointers.

### “Many range sum queries”

Repeatedly recomputing the same prefixes is suspicious. Prefix sums may move work from query time to
preprocessing time.

### “At most K distinct / at least K / longest contiguous”

The condition is describing a moving interval. Sliding window becomes a candidate if expanding and
shrinking changes validity in a controllable direction.

### “Minimum feasible X / maximum possible X”

The answer itself may be a sorted search space. Ask whether `feasible(x)` is monotonic.

### “All combinations” with small N

Backtracking or bitmask enumeration may be intended. The small constraint is permission to explore
an exponential state space, not a guarantee that every exponential method fits.

### “Dependencies / prerequisites”

The graph is directed and order matters. That raises topological sort, not merely BFS/DFS.

### “Repeated connectivity after unions”

If edges are added and you repeatedly ask whether two nodes are connected, Union-Find can store the
component information instead of retraversing the graph after every update.

## A five-question constraint pass

Before coding, write answers to these:

1. What is the largest dimension?
2. How many times will my naive inner work repeat?
3. Is the data static or changing between queries?
4. Is there an order, monotonicity, or bounded key range I can exploit?
5. Which candidate complexity is clearly impossible?

That last question is powerful: algorithm selection often starts by proving what **cannot** work.
