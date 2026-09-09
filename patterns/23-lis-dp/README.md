# 23 — LIS-style DP

## 1. What problem shape does this solve?

Longest Increasing Subsequence (LIS) is a useful case study in **state definition and algorithm
upgrade**. The straightforward DP asks for the best increasing subsequence ending at each index;
stronger ordering insight can reduce `O(N²)` to `O(N log N)`.

## 2. Signals to notice

```text
subsequence, not necessarily contiguous
increasing / decreasing order
best sequence ending at i
N small enough for O(N²) or large enough to demand optimization
```

## 3. Naive idea

Enumerate all subsequences (`2^N`) and test which are increasing.

## 4. Why the naive idea breaks

Most subsets are irrelevant. The future only needs structured summaries of promising prefixes, not
the identity of every chosen subset.

## 5. Core intuition

First DP formulation:

> `dp[i]` = length of the longest increasing subsequence **ending exactly at i**.

Then every earlier `j < i` with `nums[j] < nums[i]` can extend into `i`.

For large N, keep `tails[length-1]` = smallest possible tail value for an increasing subsequence of
that length. Smaller tails leave more room for future extension.

## 6. Invariant

In patience/binary-search optimization, `tails` is sorted and each position stores the smallest tail
seen for that subsequence length. `tails` itself is not necessarily an actual subsequence.

## 7. Step-by-step walkthrough

Values `[3, 5, 2, 6]`:

```text
3 → tails=[3]
5 → tails=[3,5]
2 → replace first >=2 → [2,5]
6 → append → [2,5,6]
length=3
```

Replacing `3` with `2` does not lose a solution; it improves the future tail boundary.

## 8. Implementation

```python
from bisect import bisect_left


def lis_length(nums: list[int]) -> int:
    tails: list[int] = []
    for value in nums:
        index = bisect_left(tails, value)
        if index == len(tails):
            tails.append(value)
        else:
            tails[index] = value
    return len(tails)
```

## 9. Complexity

The classic DP checks every earlier index for every `i`: `O(N²)`. The tails method performs one
binary search per element: `O(N log N)` time and `O(N)` space.

## 10. Common mistakes

- confusing subsequence with contiguous subarray;
- using `bisect_right` when strict increase requires `bisect_left` semantics;
- treating `tails` as the actual LIS sequence;
- applying the `O(N log N)` trick when reconstruction/variant constraints need extra bookkeeping;
- writing `dp[i]` without “ending at i” in the definition.

## 11. When NOT to use it

If the task is contiguous increasing run, a linear scan/window is enough. If extra constraints alter
the extension relation, vanilla LIS optimization may not apply.

## 12. Neighboring patterns

- **LIS vs 1D DP:** LIS is a sequence-ending-state DP.
- **LIS vs binary search:** binary search optimizes the maintained tail frontier.
- **LIS vs greedy:** the tails replacement behaves greedily but is justified by a precise dominance
  invariant.

## 13. Mutation ladder

```text
strictly increasing       → bisect_left
non-decreasing            → bisect_right candidate
need actual sequence      → store predecessor/reconstruction state
contiguous increasing run → simple linear scan
N <= 1000                 → O(N²) DP may be easier to explain
```

## 14. Practice ladder

- **Understand:** `O(N²)` LIS state definition.
- **Recognize:** increasing-subsequence transformations.
- **Apply:** `O(N log N)` tails and reconstruction.
- **Mixed:** distinguish subsequence from subarray before choosing anything.
