# Wrong Turn — Binary Search without monotonicity

## Tempting idea

Use binary search on any large yes/no search space because halving sounds automatically efficient.

## Why it looks reasonable

Binary search's `O(log N)` label is memorable, while the proof obligation—one test must eliminate an
entire side—is easier to forget.

## Smallest counterexample

```text
index:      0 1 2 3 4
predicate:  F T F T F
```

## Step-by-step failure

Testing index 2 returns false. That result tells us nothing about whether index 1 or index 3 is the
desired true position. Removing either half can delete a valid answer.

## Correct signal

Look for sorted order or a monotonic feasibility boundary such as `FFFFTTTT` or `TTTTFFFF`.

## Better candidates

Linear scan, hashing, another search structure, or reformulating the state until a monotonic
predicate can actually be proved.

## General lesson

Binary search is an elimination proof, not a generic speed trick.
