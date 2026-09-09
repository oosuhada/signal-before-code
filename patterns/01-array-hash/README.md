# 01 — Array & Hash

## 1. What problem shape does this solve?

Use arrays when position/order is the natural key. Consider hashing when the question repeatedly
asks “have I seen this value?”, “how many times?”, or “what data belongs to this key?” and scanning
the whole collection each time would repeat work.

Typical shapes: duplicate detection, frequency counting, complement lookup, grouping, deduplication,
and memo-like key → value state.

## 2. Signals to notice

```text
contains / seen before / duplicate
frequency / count / group by
find complement
lookup by identifier
same values in different order
```

Also inspect the key domain. A small bounded integer range may favor a plain array over a hash map.

## 3. Naive idea

For each value, scan all earlier values to see whether it appeared. For two-sum, test every pair.

## 4. Why the naive idea breaks

The same membership question is answered again and again. `N` items × up to `N` comparisons becomes
`O(N²)`. The waste is not arithmetic; it is forgetting what the previous scan already learned.

## 5. Core intuition

Trade memory for remembered facts. When reading value `x`, store the fact that `x` exists or how many
times it has appeared. Future questions become direct lookups instead of rescans.

## 6. Invariant

After processing indices `[0, i)`, the table exactly summarizes that prefix. A lookup at index `i`
must use only information that is allowed to exist at that moment.

For complement search, that distinction prevents accidentally using the same element twice.

## 7. Step-by-step walkthrough

Find two values summing to `10` in `[3, 8, 4, 7]`.

```text
x=3  need=7  seen={}        → store 3
x=8  need=2  seen={3}       → store 8
x=4  need=6  seen={3,8}     → store 4
x=7  need=3  seen={3,8,4}   → found 3
```

The key signal is not “two-sum uses hash.” It is “the current value asks a membership question about
the processed prefix.”

## 8. Implementation

```python
def two_sum_indices(nums: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        need = target - value
        if need in seen:
            return seen[need], index
        seen[value] = index
    return None
```

## 9. Complexity

Each element causes a constant number of average-case hash operations, so expected time is `O(N)`.
The map can store up to `N` distinct values, so space is `O(N)`. Hash lookup is average-case, not a
universal worst-case promise.

## 10. Common mistakes

- inserting before checking when the same element must not be reused;
- forgetting duplicate counts when a set is insufficient;
- using a hash map when a small integer-indexed array is simpler;
- assuming iteration order is an algorithmic guarantee you actually need;
- building keys from mutable/unhashable structures without canonicalization.

## 11. When NOT to use it

- One minimum/maximum over one pass does not need a map.
- Sorted data may allow a two-pointer solution with `O(1)` extra space.
- Range queries may need prefix sums or a tree structure instead of hashing.
- Prefix search over strings is usually better modeled by a trie.

## 12. Neighboring patterns

- **Hash vs two pointers:** memory-based lookup versus order-based elimination.
- **Hash vs prefix sum:** arbitrary key lookup versus cumulative range structure.
- **Hash vs trie:** whole-key equality versus shared-prefix queries.

## 13. Mutation ladder

```text
unsorted pair sum          → hash lookup
sorted pair sum            → two pointers becomes attractive
values in [0, 1000]        → direct count array may beat hashing
group by string signature  → hash map from canonical key → group
prefix lookup              → trie candidate
```

## 14. Practice ladder

- **Understand:** duplicates, frequency counts, basic two-sum.
- **Recognize:** grouping/anagram signatures, longest consecutive set membership.
- **Apply:** combine frequency map with heap or sliding window.
- **Mixed:** decide whether order lets you avoid hashing entirely.

Use [`../../curriculum/problems.json`](../../curriculum/problems.json) for curated problems.
