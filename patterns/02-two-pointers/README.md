# 02 — Two Pointers

**v0.1 state:** seed chapter, ready to study — **not a mastery claim**.

Two pointers are not “use two indexes.” The useful signal is that moving a boundary can eliminate a
whole set of possibilities without revisiting them.

## 1. The Situation

Given a **sorted** array, find whether two values sum to `10`.

```text
[1, 2, 3, 4, 6, 8, 9]
```

The word `sorted` is not decoration. It is information the algorithm should exploit.

## 2. First Naive Idea

Check every pair:

```text
(1,2), (1,3), (1,4), ...
(2,3), (2,4), ...
```

This is correct and easy to explain.

## 3. Why It Breaks

There are roughly `n(n-1)/2` pairs, so the approach takes `O(n²)` comparisons in the worst case.

More importantly, it ignores the strongest clue in the input: **order**.

If `1 + 9` is too small, pairing `1` with anything to the left of `9` cannot help because those
values are even smaller. If a sum is too large, moving toward an even larger value cannot help.

Order lets one comparison eliminate possibilities.

## 4. Signal to Notice

> **Ordered data + a relationship that changes monotonically when a boundary moves** should make
> two pointers a candidate.

Typical signals:

```text
sorted array
pair from opposite ends
palindrome / symmetric comparison
partition around a condition
merge-like scan across ordered sequences
```

Do not reduce this to the keyword “sorted.” Binary search also likes sorted data. Ask what the
operation is: one value lookup, or a relationship between moving positions?

## 5. Candidate Approaches

| Candidate | Time | Extra space | Trade-off |
| --- | --- | --- | --- |
| every pair | `O(n²)` | `O(1)` | simplest, ignores order |
| hash complement lookup | expected `O(n)` | `O(n)` | great on unsorted data / original-index needs, but spends memory |
| binary search complement for each value | `O(n log n)` | `O(1)` | uses ordering, but repeats logarithmic searches |
| left/right pointers | `O(n)` | `O(1)` | uses monotonic effect of moving sorted boundaries |

Hashing is not “wrong.” If the array were unsorted and original indices mattered, it might become the
better choice. The sorted invariant is what lets two pointers win this version without extra memory.

## 6. Why This Pattern

Initialize:

```text
left  = smallest remaining value
right = largest remaining value
```

Then compare `values[left] + values[right]` with the target.

```text
sum < target
→ current left value is too small even with the largest remaining partner
→ left++ is safe

sum > target
→ current right value is too large even with the smallest remaining partner
→ right-- is safe

sum == target
→ found
```

Invariant:

> After each movement, every discarded index has been proven unable to participate in a valid pair
> with any still-relevant partner.

That proof is the pattern. Two integer variables are merely its implementation.

## 7. Walkthrough

Target: `10`

```text
[1, 2, 3, 4, 6, 8, 9]
 L                 R
```

| Step | Left | Right | Sum | Reason | Move |
| ---: | ---: | ---: | ---: | --- | --- |
| 1 | 1 | 9 | 10 | target reached | stop |

That input is almost too easy, so try target `11`:

| Step | Left | Right | Sum | Reason | Move |
| ---: | ---: | ---: | ---: | --- | --- |
| 1 | 1 | 9 | 10 | too small | `left → 2` |
| 2 | 2 | 9 | 11 | target reached | stop |

Why was discarding `1` safe? With `9` already the largest remaining value, `1` cannot reach `11`
with any other partner.

A longer miss case shows the same one-way behavior:

```text
too small → left only moves right
too large → right only moves left
neither pointer ever moves backward
```

## 8. Implementation

```python
def find_pair_with_sum(values, target):
    left = 0
    right = len(values) - 1

    while left < right:
        current = values[left] + values[right]
        if current == target:
            return values[left], values[right]
        if current < target:
            left += 1
        else:
            right -= 1

    return None
```

The tested version in
[`../../signal_before_code/two_pointers.py`](../../signal_before_code/two_pointers.py) checks the
sorted-input precondition so misuse is visible during practice.

## 9. Complexity

`left` starts at index `0` and only increases. `right` starts at `n-1` and only decreases.

Across the entire algorithm:

- `left` can move at most `n-1` times;
- `right` can move at most `n-1` times;
- no movement is undone.

Therefore total pointer movement is `O(n)`, not `O(n²)`, and the algorithm stores only a constant
amount of state: `O(1)` extra space.

If sorting is required first, the end-to-end cost becomes `O(n log n)` and the choice must account
for whether reordering is allowed.

## 10. When NOT to Use It

Two pointers need a defensible monotonic elimination rule.

```text
Unsorted pair-sum + must preserve original indices
→ hash complement lookup is usually more direct.

Search for one value in sorted data
→ binary search may discard half the range faster.

Subarray sum with arbitrary positive and negative values
→ expanding/shrinking a window is not monotonic; prefix-sum + hash may fit.

No ordering or boundary relation at all
→ two indexes do not magically create useful information.
```

Also distinguish **two pointers** from **sliding window**. Both may move indexes forward, but sliding
window maintains state for a contiguous interval, while the opposite-end pair example eliminates
candidate pairs by order.

## 11. Mutation

### Mutation A — the array is unsorted

If original indices do not matter:

```text
sort O(n log n)
→ two pointers O(n)
```

If original indices do matter, sorting needs index decoration or a different approach. A hash map may
give expected `O(n)` directly.

### Mutation B — find three values that sum to a target

One common decomposition is:

```text
fix one position
↓
solve a two-sum problem on the remaining sorted suffix
↓
two pointers inside the outer loop
```

The time becomes `O(n²)`, but that is still a major reduction from enumerating all triples `O(n³)`.

### Mutation C — find a contiguous positive-number subarray with a target sum

Now the important state is an interval sum. Positive values make expansion increase the sum and
shrinking decrease it:

```text
pair-elimination two pointers
→ variable sliding window
```

The implementation may still use `left` and `right`, but the invariant has changed.

### Mutation D — allow arbitrary negative values in that subarray problem

The monotonic window behavior disappears. Shrinking can increase or decrease the sum unpredictably,
so prefix sums plus hash lookup become candidates.

## 12. Practice

### Understand

- [LeetCode 125 — Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) — What symmetric
  fact lets the two boundaries move inward?
- [LeetCode 167 — Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) —
  State exactly why each pointer move eliminates a set of pairs.

### Recognize

- [LeetCode 15 — 3Sum](https://leetcode.com/problems/3sum/) — Which dimension can be fixed so the
  remaining search becomes monotonic?
- [Programmers 42885 — 구명보트](https://school.programmers.co.kr/learn/courses/30/lessons/42885)
  — After sorting, which pairing decision can be made permanently from the extremes?

### Apply

- [LeetCode 11 — Container With Most Water](https://leetcode.com/problems/container-with-most-water/)
  — Why is moving the taller boundary not the useful move?

See [`../../curriculum/problems.json`](../../curriculum/problems.json).
