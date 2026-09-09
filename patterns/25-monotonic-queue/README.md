# 25 — Monotonic Queue

## 1. What problem shape does this solve?

A monotonic queue maintains the minimum or maximum of a **moving window** while both adding new items
and expiring old ones in amortized constant time.

## 2. Signals to notice

```text
maximum/minimum for every window of size K
moving range extreme
sliding window + repeated min/max
```

## 3. Naive idea

For every window, scan all K values for the max/min, or maintain a heap without carefully deleting
expired entries.

## 4. Why the naive idea breaks

Rescanning costs `O(NK)`. A heap can work in `O(N log K)` but may need lazy expiration. Monotonic
order lets us discard dominated values permanently.

## 5. Core intuition

For window maximum, if a new value is greater than an older value behind it, the older value can
never become maximum again while both remain in future windows. Remove dominated tails now.

## 6. Invariant

The deque stores indices inside the current window, with values decreasing from front to back. The
front is therefore the current maximum.

## 7. Step-by-step walkthrough

Window size 3 over `[1, 3, 2, 5]`:

```text
1 → deque=[1]
3 → remove 1 (dominated), deque=[3]
2 → deque=[3,2] → first window max=3
5 → remove 2, remove 3, deque=[5] → next max=5
```

## 8. Implementation

```python
from collections import deque


def sliding_max(nums: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()
    result: list[int] = []
    for i, value in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= value:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

## 9. Complexity

Every index enters the deque once and leaves at most once from either end. Total work is `O(N)` and
deque space is `O(K)`.

## 10. Common mistakes

- storing values instead of indices and losing expiration information;
- expiring after reading the answer instead of before;
- wrong duplicate comparison (`<` vs `<=`) for desired tie behavior;
- confusing monotonic queue with ordinary BFS queue;
- using it where window validity, not extrema, is the main state.

## 11. When NOT to use it

- Ordinary longest-valid-window counts/sums may need only a hash map/counter.
- One global min/max needs no deque.
- Arbitrary dynamic range queries may need segment/Fenwick trees.

## 12. Neighboring patterns

- **Monotonic queue vs sliding window:** it is a specialized state structure inside a window.
- **Monotonic queue vs heap:** `O(N)` dominated-candidate removal vs `O(N log K)` general priority.
- **Monotonic queue vs monotonic stack:** expiring two-sided window vs one-sided nearest relation.

## 13. Mutation ladder

```text
window max/min            → monotonic deque
window sum/count          → ordinary sliding window
dynamic arbitrary ranges → range tree territory
need top several values   → heap/multiset candidate
nearest greater right     → monotonic stack
```

## 14. Practice ladder

- **Understand:** sliding window maximum.
- **Recognize:** minimum/maximum rolling constraints.
- **Apply:** prefix-sum + monotonic deque shortest-range variants.
- **Mixed:** decide whether a heap's generality is necessary.
