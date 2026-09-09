# 01 — Array & Hash

**v0.1 state:** seed chapter, ready to study — **not a mastery claim**.

The point of this chapter is not “hash maps are O(1).” The point is to notice when repeated scanning
is throwing away knowledge that could have been stored once.

## 1. The Situation

Imagine an event stream represented as a list of IDs:

```text
["A17", "B04", "C11", "B04", "D20"]
```

We need the **first value whose appearance proves that we have seen it before**.

Nothing is sorted. We do not need the values in sorted order. We only need to answer this question
over and over as we move left to right:

```text
Have I seen this key already?
```

That repeated membership question is the real shape of the problem.

## 2. First Naive Idea

For every new value, scan everything before it.

```text
A17  → nothing before it
B04  → compare with A17
C11  → compare with A17, B04
B04  → compare with A17, B04 → duplicate
```

This is easy to invent and correct.

## 3. Why It Breaks

It becomes **too slow** as the list grows.

If there is no duplicate until the end, the comparisons look roughly like:

```text
0 + 1 + 2 + ... + (n - 1)
```

That sum grows quadratically: `O(n²)` comparisons.

The deeper problem is not merely “nested loops are bad.” It is that every new element asks a
question we have effectively answered before, but the naive version stores none of that knowledge.

## 4. Signal to Notice

> **Repeated membership, frequency, or key → value lookup with no need for sorted traversal**
> should make a set or hash map a candidate.

Problem-language signals include:

```text
"have we seen this before?"
"how many times did this appear?"
"find the item with the same key"
"group by this identifier"
"lookup the matching record repeatedly"
```

Also inspect the key domain. If keys are tiny bounded integers, an array may be even simpler than a
hash structure.

## 5. Candidate Approaches

| Candidate | Time | Extra space | Why keep/reject it |
| --- | --- | --- | --- |
| scan previous values | `O(n²)` worst case | `O(1)` | simplest, but repeats membership work |
| sort then compare neighbors | `O(n log n)` | depends on sort | useful if ordering is also valuable; may destroy original order/index meaning |
| set of seen values | expected `O(n)` | `O(n)` | directly stores the answer to “seen before?” |
| counting array | `O(n + K)` or `O(n)` with fixed allocation | `O(K)` | excellent when key range `0..K` is small and known |

The point is not that hashing always wins. It wins here because original scan order matters and the
query is repeated exact membership.

## 6. Why This Pattern

Maintain this invariant:

> Before processing position `i`, `seen` contains exactly the values from positions `0..i-1`.

Then the current membership check answers the duplicate question directly.

```text
value not in seen
→ this is its first appearance
→ store it

value already in seen
→ earlier occurrence exists
→ duplicate proven
```

We traded memory for remembered work.

## 7. Walkthrough

Input:

```text
["A17", "B04", "C11", "B04", "D20"]
```

| Step | Current | `seen` before | Decision | `seen` after |
| ---: | --- | --- | --- | --- |
| 0 | `A17` | `{}` | new | `{A17}` |
| 1 | `B04` | `{A17}` | new | `{A17, B04}` |
| 2 | `C11` | `{A17, B04}` | new | `{A17, B04, C11}` |
| 3 | `B04` | `{A17, B04, C11}` | already present → stop | unchanged |

The visualization is small because the important state change is small: the set represents what the
prefix has already taught us.

For frequency counting, the state is slightly richer:

```text
value
↓
hash lookup
↓
previous count + 1
```

## 8. Implementation

Only now do we write code:

```python
def first_duplicate(values):
    seen = set()
    for value in values:
        if value in seen:
            return value
        seen.add(value)
    return None
```

The reusable tested version is in
[`../../signal_before_code/array_hash.py`](../../signal_before_code/array_hash.py). It also includes a
small frequency-counter example.

The implementation is intentionally ordinary. The learning value is in deriving why the set belongs
here.

## 9. Complexity

For `n` input values:

- the loop visits each value once;
- each set membership/add operation is expected `O(1)` for Python's hash table under normal
  conditions;
- therefore expected total time is `O(n)`;
- in the all-unique case, `seen` stores `n` values, so extra space is `O(n)`.

This is an **expected/amortized hash-table argument**, not a universal promise that every possible
hash implementation has deterministic constant-time operations.

For a bounded counting array with domain size `K`, direct indexing can avoid hashing entirely and may
have better constants, at the cost of `O(K)` storage.

## 10. When NOT to Use It

Do not reach for a hash map merely because keys exist.

```text
Need one minimum from a list once?
→ scan; a map stores irrelevant state.

Need sorted iteration or range queries?
→ hashing does not preserve numeric/key order; sorting or an ordered structure may fit better.

Keys are integers 0..25?
→ a 26-slot array can be simpler and cheaper.

Need only adjacent duplicate detection in already sorted data?
→ compare neighbors; no O(n) set is required.
```

Production bridge:
[`AskOosu/src/lib/rag/search-cache.ts`](https://github.com/oosuhada/AskOosu/blob/main/src/lib/rag/search-cache.ts)
builds a stable query-derived key for its RAG search cache and looks it up in PostgreSQL. That is a
real key-based lookup use case, but it is **not** evidence that a Python dictionary is the right
implementation for a database cache.

## 11. Mutation

Start from “find the first duplicate.” Now change one condition:

### Mutation A — keys are guaranteed to be integers `0..100`

Candidate shift:

```text
hash set
→ fixed boolean/counting array becomes attractive
```

The bounded domain is new information that hashing does not exploit.

### Mutation B — return duplicates in sorted order

The set still detects membership, but it no longer solves the ordering requirement by itself. A
sort step or ordered approach enters the design.

### Mutation C — only duplicates inside the last `k` positions count

The “seen forever” invariant is now wrong. State must expire:

```text
global seen set
→ bounded moving membership state
→ sliding-window family becomes a candidate
```

### Mutation D — group all words that are anagrams

Membership is no longer enough. We need a **derived key → group** mapping, which is still hash-shaped
but with a richer key design.

## 12. Practice

Do not open solutions first. For every problem, write the repeated query and candidate structures
before coding.

### Understand

- [LeetCode 217 — Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) — What work
  is repeated if every item scans the prefix?
- [LeetCode 242 — Valid Anagram](https://leetcode.com/problems/valid-anagram/) — Is the key domain
  bounded enough that an array can compete with a hash map?

### Recognize

- [Programmers 42576 — 완주하지 못한 선수](https://school.programmers.co.kr/learn/courses/30/lessons/42576)
  — What should the lookup key represent when duplicates are possible?
- [LeetCode 49 — Group Anagrams](https://leetcode.com/problems/group-anagrams/) — What canonical key
  turns a grouping problem into repeated lookup?

### Apply

- [LeetCode 347 — Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) —
  Hashing can count, but what additional selection problem remains after the counts exist?

See the machine-readable entries in [`../../curriculum/problems.json`](../../curriculum/problems.json).
