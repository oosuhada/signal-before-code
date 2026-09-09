# 17 — Prefix Sum

## 1. What problem shape does this solve?

Prefix sums precompute cumulative information so repeated static range-sum/count queries can be
answered by subtracting two boundaries instead of rescanning the range.

## 2. Signals to notice

```text
many range sum/count queries
subarray sum equals K
cumulative totals
static array, many queries
```

## 3. Naive idea

For every query `[l, r]`, loop from `l` to `r` and add again.

## 4. Why the naive idea breaks

Overlapping queries repeatedly add the same prefix. With `Q` queries each spanning `O(N)`, runtime
can become `O(NQ)`.

## 5. Core intuition

Store “sum before position i.” Then any range becomes the difference between two already-computed
cumulative states.

## 6. Invariant

Define `prefix[i]` precisely. A convenient convention is:

> `prefix[i]` = sum of `nums[0:i]`, excluding index `i`.

Then `sum(l..r) = prefix[r+1] - prefix[l]`.

## 7. Step-by-step walkthrough

For `[2, 5, 1, 4]`:

```text
prefix = [0, 2, 7, 8, 12]
sum indices 1..3 = prefix[4] - prefix[1] = 12 - 2 = 10
```

The leading zero removes special handling for `l=0`.

## 8. Implementation

```python
def prefix_sums(nums: list[int]) -> list[int]:
    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] + value)
    return prefix


def range_sum(prefix: list[int], left: int, right: int) -> int:
    return prefix[right + 1] - prefix[left]
```

## 9. Complexity

Preprocessing is `O(N)` once. Each range query is `O(1)`. Space is `O(N)`. This is valuable when the
same static data serves many queries.

## 10. Common mistakes

- inconsistent inclusive/exclusive definitions;
- forgetting the leading zero;
- off-by-one at `right + 1`;
- using static prefix sums when frequent updates change values;
- assuming prefix sums only work with positive values—they work with negatives for range queries.

## 11. When NOT to use it

- Frequent point/range updates need a dynamic range structure.
- Longest valid contiguous interval may require sliding window or another search pattern.
- One total sum does not need an entire prefix array.

## 12. Neighboring patterns

- **Prefix sum vs sliding window:** known-range query vs discovering a valid range.
- **Prefix sum + hash:** count subarrays with target sums by remembering earlier prefix values.
- **Prefix sum vs Fenwick/segment tree:** static queries vs dynamic updates.

## 13. Mutation ladder

```text
one range sum             → direct loop may be fine
many static range sums    → prefix sum
subarray sum = K          → prefix sum + hash map
point updates             → Fenwick/segment tree territory
2D rectangle queries     → 2D prefix sum
```

## 14. Practice ladder

- **Understand:** static range sums, running totals.
- **Recognize:** subarray-sum counts using prefix differences.
- **Apply:** 2D prefix sums and prefix+hash combinations.
- **Mixed:** distinguish static query structure from moving-window search.
