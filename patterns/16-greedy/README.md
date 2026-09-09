# 16 — Greedy

## 1. What problem shape does this solve?

Greedy algorithms commit to a locally preferred choice and never revisit it. They are appropriate
only when a proof shows that this commitment cannot exclude a globally optimal solution.

## 2. Signals to notice

```text
maximize count / minimize resources
sort then choose
earliest finish / smallest cost / largest gain
local choice seems to dominate alternatives
```

These signals produce a **candidate**, not a proof.

## 3. Naive idea

Enumerate every subset/order of choices and calculate the best total result.

## 4. Why the naive idea breaks

The choice space is exponential or factorial. If one local rule can safely discard alternatives,
greedy can collapse that search dramatically.

## 5. Core intuition

Ask an exchange question:

> If an optimal solution does not make my greedy choice first, can I swap my choice in without
> making the solution worse?

If yes, the greedy choice is compatible with at least one optimum.

## 6. Invariant

After each greedy choice, there still exists an optimal complete solution extending the chosen
prefix/set. This is the hidden claim that a correctness proof must defend.

## 7. Step-by-step walkthrough

Maximum number of non-overlapping intervals. Sort by finish time:

```text
[1,3], [2,5], [4,6], [6,8]
choose [1,3]
skip [2,5] because overlaps
choose [4,6]
choose [6,8]
```

Finishing earlier leaves at least as much room for future intervals as a later-finishing competing
choice.

## 8. Implementation

```python
def max_non_overlapping(intervals: list[tuple[int, int]]) -> int:
    intervals.sort(key=lambda item: item[1])
    count = 0
    end = float("-inf")
    for start, finish in intervals:
        if start >= end:
            count += 1
            end = finish
    return count
```

## 9. Complexity

Sorting dominates at `O(N log N)`; the selection scan is `O(N)`. Space depends on whether the sort
is in-place and on language runtime implementation.

## 10. Common mistakes

- trusting a local rule without a counterexample search or proof;
- sorting by the wrong field;
- confusing “earliest start” with “earliest finish” in interval scheduling;
- applying canonical coin-system intuition to arbitrary denominations;
- ignoring tie behavior when it affects future feasibility.

## 11. When NOT to use it

If different local choices lead to different future values and no exchange/dominance proof exists,
DP or search may be necessary.

## 12. Neighboring patterns

- **Greedy vs DP:** commit and discard alternatives vs retain state over alternative histories.
- **Greedy + sorting:** ordering often creates the dominance relation.
- **Greedy + heap:** some scheduling problems repeatedly choose the best available candidate.

## 13. Mutation ladder

```text
interval maximum count       → earliest-finish greedy
weighted intervals           → greedy can fail; DP candidate
canonical coin system        → greedy may work
arbitrary coin denominations → counterexample may force DP
online candidate arrivals    → heap may join greedy strategy
```

## 14. Practice ladder

- **Understand:** interval scheduling, simple resource choices with clear proof.
- **Recognize:** sort-and-sweep dominance problems.
- **Apply:** scheduling with heap, exchange-argument reasoning.
- **Mixed:** attempt to break the greedy rule before trusting it.

See [`../../comparisons/greedy-vs-dp.md`](../../comparisons/greedy-vs-dp.md).
