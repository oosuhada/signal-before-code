# Wrong Turn: Binary Search without Monotonicity

## Temptation

The answer is numeric and the range is huge, so binary search feels attractive.

## The missing assumption

Binary search needs a predicate whose truth values form one boundary:

```text
false false false | true true true
```

or the reverse. If `feasible(x)` can flip back and forth, discarding half the answer space is not
safe.

## Repair

Write down two example values on each side of the supposed boundary. If you cannot prove monotonicity,
do not binary-search the answer.
