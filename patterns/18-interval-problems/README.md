# 18 — Interval Problems

## 1. What problem shape does this solve?

Interval problems reason about ranges with starts and ends: merging overlaps, inserting one range,
counting rooms/resources, or choosing a compatible subset.

## 2. Signals to notice

```text
start/end times
overlap / merge / schedule
meeting rooms
insert interval
minimum number of simultaneous resources
```

## 3. Naive idea

Compare every interval with every other interval to discover overlaps.

## 4. Why the naive idea breaks

Without ordering, overlap relationships are scattered. Sorting by start (or sometimes finish) makes
relevant conflicts local and avoids `O(N²)` pair checks.

## 5. Core intuition

Sort to expose geometry. Once intervals are ordered by start, a new interval can only overlap the
current merged tail until it starts after that tail ends.

## 6. Invariant

During merge, `merged` contains non-overlapping intervals covering exactly the processed input. Its
last interval is the only one the next start-sorted interval can overlap.

## 7. Step-by-step walkthrough

```text
[1,3], [2,6], [8,10]
start merged=[1,3]
[2,6] overlaps last → extend to [1,6]
[8,10] starts after 6 → append
result: [1,6], [8,10]
```

## 8. Implementation

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals.sort(key=lambda item: item[0])
    merged = [intervals[0][:]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

## 9. Complexity

Sorting is `O(N log N)` and the sweep is `O(N)`. The output can itself contain `O(N)` intervals.

## 10. Common mistakes

- using `<` versus `<=` incorrectly for touching endpoints;
- sorting by the wrong key for the task;
- mutating caller-owned intervals unintentionally;
- applying merge logic to interval scheduling, which needs a different greedy rule;
- forgetting tie semantics for simultaneous start/end events.

## 11. When NOT to use it

Not every scheduling problem is “merge intervals.” Weighted scheduling can require DP; dynamic
arrival/resource scheduling may require heaps.

## 12. Neighboring patterns

- **Intervals + greedy:** earliest finish for maximum compatible count.
- **Intervals + heap:** room allocation by earliest finishing active meeting.
- **Intervals + sweep line:** event counts and simultaneous overlap.

## 13. Mutation ladder

```text
merge overlaps                 → sort by start + sweep
max number non-overlap         → greedy by finish
minimum meeting rooms          → sort + heap / two sorted endpoints
weighted interval scheduling   → DP candidate
online intervals               → data structure requirements change
```

## 14. Practice ladder

- **Understand:** merge and insert interval.
- **Recognize:** meeting rooms, erase overlap count.
- **Apply:** interval + heap/greedy/DP variants.
- **Mixed:** identify which interval objective changes the algorithm.
