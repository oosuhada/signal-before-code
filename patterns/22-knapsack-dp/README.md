# 22 — Knapsack-style DP

## 1. What problem shape does this solve?

Knapsack-style DP appears when items have costs/weights and values, and you must choose a subset under
a bounded capacity/resource. The second state dimension is often capacity, amount, or budget.

## 2. Signals to notice

```text
capacity / budget / target amount
choose each item at most once or repeatedly
maximize value / count ways / reach target
N × capacity state range is plausible
```

## 3. Naive idea

For each item, recursively choose or skip it, exploring up to `2^N` subsets.

## 4. Why the naive idea breaks

Many different subsets reach the same `(item index, remaining capacity)` question. The future does
not care exactly how you arrived there if that state captures all relevant information.

## 5. Core intuition

Define whether items are reusable, then let capacity summarize resource use. For 0/1 knapsack:

> `dp[c]` = best value achievable with capacity at most `c` using processed items.

Iteration direction encodes whether the current item may be reused.

## 6. Invariant

In 0/1 knapsack with 1D compression, processing capacities **descending** ensures each item contributes
at most once. Ascending order would let the same iteration reuse the item.

## 7. Step-by-step walkthrough

One item `(weight=3, value=5)`, capacity 6:

```text
descending c=6..3:
dp[6] reads old dp[3] → item used once

ascending c=3..6:
dp[3] becomes 5, then dp[6] can read new dp[3] → same item reused
```

That loop direction is part of the correctness proof.

## 8. Implementation

```python
def knapsack_01(items: list[tuple[int, int]], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for weight, value in items:
        for c in range(capacity, weight - 1, -1):
            dp[c] = max(dp[c], dp[c - weight] + value)
    return dp[capacity]
```

## 9. Complexity

There are `N × capacity` transitions, so time is `O(NW)` where `W` is capacity—not input bit-length.
Compressed space is `O(W)`. This is pseudo-polynomial and can be impossible when capacity is huge.

## 10. Common mistakes

- iterating capacity in the wrong direction;
- confusing 0/1 and unbounded item reuse;
- ignoring pseudo-polynomial complexity when W is enormous;
- unclear meaning of “exactly capacity” versus “at most capacity”;
- using zero initialization where unreachable states need `-∞`/sentinel semantics.

## 11. When NOT to use it

- Capacity dimension too large → `O(NW)` may be impossible.
- Greedy ratio works for **fractional** knapsack, but not ordinary 0/1 knapsack.
- Small N with huge weights may favor meet-in-the-middle/subset techniques.

## 12. Neighboring patterns

- **Knapsack vs greedy:** indivisible choices create global trade-offs.
- **Knapsack vs bitmask:** capacity-based pseudo-polynomial state vs enumerate subsets when N is small.
- **Knapsack vs 1D DP:** knapsack is a specialized 1D resource-state transition family.

## 13. Mutation ladder

```text
0/1 item use            → descending capacity
unbounded reuse         → ascending capacity candidate
fractional items        → greedy by value density
N <= 20, huge capacity  → subset/meet-in-middle candidate
need exact reachability → boolean/sentinel state semantics
```

## 14. Practice ladder

- **Understand:** subset sum, basic 0/1 knapsack.
- **Recognize:** partition/target resource states.
- **Apply:** unbounded variants and count/minimum forms.
- **Mixed:** identify whether capacity or N should be the compressed dimension.
