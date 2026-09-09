# 19 — Dynamic Programming Fundamentals

## 1. What problem shape does this solve?

DP is a way to solve a graph of repeated subproblems **once per state**. It often appears after a
natural recursive solution reveals that different decision paths reach the same remaining problem.

The hardest part is not the loop. It is deciding what a state means.

## 2. Signals to notice

```text
minimum / maximum / count ways
choices lead to the same remaining state
naive recursion repeats work
answer for position/state depends on smaller states
```

## 3. Naive idea

Write the recurrence as plain recursion and let every branch compute its own answer independently.

## 4. Why the naive idea breaks

For Fibonacci-like branching, the same state is recomputed many times:

```text
f(5)
├─ f(4)
│  ├─ f(3)
│  └─ f(2)
└─ f(3)   ← repeated whole subtree
```

The recursion tree can be exponential even when the number of **distinct** states is only linear.

## 5. Core intuition

Start with the recursive question, then compress repeated calls into named states:

```text
naive recursion
↓
which arguments repeat?
↓
define state meaning
↓
memoize each state once
↓
optionally reorder into bottom-up evaluation
```

## 6. Invariant

The essential invariant is semantic:

> `dp[state]` always means one precise thing.

For example, `dp[i] = minimum cost to reach index i`. If some transitions treat it as “cost after
processing i” and others as “cost before i,” the table can be syntactically valid but logically wrong.

## 7. Step-by-step walkthrough

Minimum cost to climb to step `i` when you can move 1 or 2 steps:

```text
dp[0] = known base
dp[1] = known base
dp[2] = cost[2] + min(dp[1], dp[0])
dp[3] = cost[3] + min(dp[2], dp[1])
```

Before writing that transition, say aloud: “`dp[i]` means the minimum total cost of reaching i.”

## 8. Implementation

```python
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    return prev1
```

This tiny example is about the transformation from repeated recursive state to one-time state, not
about memorizing Fibonacci.

## 9. Complexity

Analyze **number of states × transitions per state**. If there are `N` states and each checks two
previous states, time is `O(N)`. Space may often be reduced when only a small recent frontier of states
is needed.

## 10. Common mistakes

- creating a DP table before defining state semantics;
- missing base cases or defining them under a different meaning;
- iterating in an order before dependencies are ready;
- memoizing with an incomplete key that ignores future-relevant state;
- assuming every optimization problem is DP.

## 11. When NOT to use it

- No overlapping subproblems → divide-and-conquer/recursion may be enough.
- A provable greedy invariant can eliminate alternatives more simply.
- The state space is larger than the original brute-force work you were trying to avoid.

## 12. Neighboring patterns

- **DP vs recursion:** same recurrence, but DP stores repeated states.
- **DP vs greedy:** preserve alternatives vs prove one can be discarded.
- **DP vs backtracking:** optimize/count states vs enumerate/prune paths.

## 13. Mutation ladder

```text
plain recursion, no repeated states → recursion
repeated arguments                 → memoization
dependency order obvious           → bottom-up DP
only previous two states needed    → rolling-space optimization
local choice proven safe           → greedy may replace DP
```

## 14. Practice ladder

- **Understand:** climb stairs / house-style one-dimensional recurrence.
- **Recognize:** identify repeated recursion state before coding a table.
- **Apply:** define multidimensional state and transition direction.
- **Mixed:** explain why DP is necessary instead of merely possible.

See [`../../wrong-turns/dp-overengineering.md`](../../wrong-turns/dp-overengineering.md).
