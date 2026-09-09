# 20 — 1D DP

## 1. What problem shape does this solve?

1D DP fits problems where one primary coordinate—usually an index, amount, or step—captures the
subproblem and the answer at `i` depends on a small set of earlier states.

## 2. Signals to notice

```text
best/count up to index i
choose or skip along one sequence
reach position/amount i
transition from a few previous positions
```

## 3. Naive idea

At each position, recursively explore every take/skip or previous-step choice.

## 4. Why the naive idea breaks

Many paths reach the same index/amount with the same future question. Re-solving that suffix or
remaining amount is repeated work.

## 5. Core intuition

Choose a direction and define what is already solved. A common form is:

> `dp[i]` = best answer for the prefix ending at / up to position `i`.

Then list every legal way the final decision could arrive at that state.

## 6. Invariant

When computing `dp[i]` bottom-up, every state referenced by its transition is already correct under
the same definition.

## 7. Step-by-step walkthrough

House robber values `[2, 7, 9, 3]` where adjacent choices conflict:

```text
dp[0] = 2
dp[1] = max(2, 7) = 7
dp[2] = max(dp[1], dp[0] + 9) = 11
dp[3] = max(dp[2], dp[1] + 3) = 11
```

The two candidates are “skip current” and “take current, therefore combine with i-2.”

## 8. Implementation

```python
def max_non_adjacent_sum(nums: list[int]) -> int:
    prev2 = 0
    prev1 = 0
    for value in nums:
        current = max(prev1, prev2 + value)
        prev2, prev1 = prev1, current
    return prev1
```

## 9. Complexity

One transition per item with constant work gives `O(N)` time. Because only the previous two states
matter here, the full `O(N)` table can be compressed to `O(1)` space.

## 10. Common mistakes

- defining `dp[i]` as “ending at i” but using transitions for “up to i”;
- wrong initialization for empty/single-element input;
- space-optimizing before the recurrence is correct;
- updating rolling variables in the wrong order;
- assuming values are positive when the problem permits negatives.

## 11. When NOT to use it

- If state needs two independent coordinates, 2D DP may be the honest model.
- If one local greedy decision is provably safe, DP is unnecessary.
- If the task asks for all combinations, backtracking may be more direct.

## 12. Neighboring patterns

- **1D DP vs greedy:** compare “take/skip” histories unless one dominates by proof.
- **1D DP vs LIS:** LIS is a specialized sequence-state family with richer transitions.
- **1D DP vs prefix sum:** optimal state vs deterministic cumulative aggregate.

## 13. Mutation ladder

```text
linear houses                    → 1D DP
first and last become adjacent   → solve two linear cases
need reconstruct chosen indices  → store decisions/parents
transition depends on all j < i  → may become O(N²) or need stronger structure
```

## 14. Practice ladder

- **Understand:** climbing stairs, max non-adjacent sum.
- **Recognize:** decode/count/coin-style single-coordinate states.
- **Apply:** circular constraints and reconstruction.
- **Mixed:** state the exact meaning of `dp[i]` before touching code.
