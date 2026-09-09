# 05 — Binary Search

## 1. What problem shape does this solve?

Binary search finds a target or boundary in an ordered/monotonic search space by proving that half of
the remaining candidates cannot contain the answer.

## 2. Signals to notice

```text
sorted
first / last position
minimum feasible
maximum possible
monotonic predicate
huge numeric answer range
```

## 3. Naive idea

Scan candidates one by one, or test every possible answer value.

## 4. Why the naive idea breaks

It fails to exploit one-sided evidence. If a comparison proves every value below/above the midpoint
has the same fate, checking them individually repeats the same conclusion.

## 5. Core intuition

Do not think “look at the middle.” Think “**which half can I delete with proof?**” Binary search is a
safe-elimination algorithm.

## 6. Invariant

Choose a boundary convention and state it. For lower-bound style search:

```text
[0, left)      definitely too small / false
[right, n)     candidate-or-true region depending on convention
```

For answer search, the predicate should look like `False ... False | True ... True` (or reverse).

## 7. Step-by-step walkthrough

Find first value `>= 7` in `[1, 4, 7, 7, 9]`:

```text
lo=0 hi=5 mid=2 value=7 → answer could be 2 or earlier, hi=2
lo=0 hi=2 mid=1 value=4 → too small, lo=2
lo=2 hi=2 → boundary is 2
```

## 8. Implementation

```python
def lower_bound(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

## 9. Complexity

Each comparison cuts the remaining interval roughly in half, so after `k` decisions only
`N / 2^k` candidates remain. Reaching one candidate takes `O(log N)` decisions and `O(1)` extra
space for iterative search.

## 10. Common mistakes

- binary-searching a predicate that is not monotonic;
- mixing closed and half-open interval conventions;
- infinite loops from `lo = mid` without progress;
- returning any match when the task asks first/last boundary;
- choosing wrong feasible bounds for answer search.

## 11. When NOT to use it

- Arbitrary unordered search has no safe half to discard.
- Sorted pair relationships may be simpler with two pointers.
- Tiny ranges may not justify boundary complexity.

## 12. Neighboring patterns

- **Binary search vs two pointers:** one monotonic boundary vs coordinated endpoints.
- **Binary search vs greedy:** answer search may call a greedy feasibility check internally.
- **Binary search vs BST:** static indexed array search vs dynamic ordered structure.

## 13. Mutation ladder

```text
exact target in sorted array      → binary search
first >= target                   → lower bound
minimum feasible capacity         → binary search on answer
predicate loses monotonicity       → binary search invalid
pair sum in sorted array           → two pointers often simpler
```

## 14. Practice ladder

- **Understand:** exact search and lower bound.
- **Recognize:** first/last occurrence, rotated ordering.
- **Apply:** binary search on answer with a feasibility function.
- **Mixed:** prove monotonicity before choosing it.

See [`../../wrong-turns/binary-search-without-monotonicity.md`](../../wrong-turns/binary-search-without-monotonicity.md).
