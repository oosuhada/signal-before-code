# 24 — Monotonic Stack

## 1. What problem shape does this solve?

A monotonic stack solves nearest-greater/smaller and span problems where each new value can prove
that some earlier candidates will never matter again. It is a stack plus an ordering invariant.

## 2. Signals to notice

```text
next greater / next smaller
previous greater / previous smaller
nearest blocking height
days until warmer
largest rectangle / span
```

## 3. Naive idea

For every index, scan left/right until finding the first qualifying value.

## 4. Why the naive idea breaks

Long increasing/decreasing runs cause the same values to be inspected repeatedly, leading to
`O(N²)` work.

## 5. Core intuition

Keep only unresolved candidates in monotonic order. When a new value defeats the stack top, it also
proves that top's answer; pop it permanently.

## 6. Invariant

For a decreasing stack used for “next greater,” indices on the stack have values in decreasing order
from bottom to top and are still waiting for a greater value to their right.

## 7. Step-by-step walkthrough

Temperatures `[73, 71, 75]`:

```text
73 → stack=[73]
71 → stack=[73,71]
75 → pop 71: 75 is its first greater to right
     pop 73: 75 is also its first greater
     push 75
```

Why first? If an earlier greater value existed, the item would already have been popped.

## 8. Implementation

```python
def next_greater_distance(nums: list[int]) -> list[int]:
    answer = [0] * len(nums)
    stack: list[int] = []
    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] < value:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer
```

## 9. Complexity

Each index is pushed once and popped at most once. Even with a nested `while`, total stack operations
are `O(N)`, so runtime is amortized `O(N)` with `O(N)` stack space.

## 10. Common mistakes

- choosing increasing vs decreasing direction backwards;
- using `<` versus `<=` incorrectly with duplicates;
- storing values when indices/distances are needed;
- assuming the stack contains final answers rather than unresolved candidates;
- overlooking left-to-right versus right-to-left scan direction.

## 11. When NOT to use it

- Moving-window maximum/minimum → monotonic queue.
- Arbitrary range maximum queries → other range structures.
- If only global max/min is needed, one linear scan suffices.

## 12. Neighboring patterns

- **Monotonic stack vs ordinary stack:** ordering invariant is the essential extra property.
- **Monotonic stack vs monotonic queue:** nearest one-sided relation vs extrema over a moving window.
- **Monotonic stack vs two pointers:** both eliminate candidates, but stack preserves multiple
  unresolved boundaries.

## 13. Mutation ladder

```text
next greater right       → decreasing stack
next smaller right       → increasing stack
previous relation        → scan direction/answer changes
window max for each K    → monotonic queue
global maximum only      → simple scan
```

## Visual Trace / Try Predicting

See why resolved candidates leave permanently in
[`../../visuals/monotonic-stack.md`](../../visuals/monotonic-stack.md).

## 14. Practice ladder

- **Understand:** next greater element, daily temperatures.
- **Recognize:** stock span, nearest smaller boundary.
- **Apply:** largest rectangle / trapping-boundary variants.
- **Mixed:** state exactly what every stack entry is still waiting for.
