# Wrong Turn: DP Overengineering

## Temptation

The problem asks for a minimum/maximum, so create a `dp` table immediately.

## Failure mode

DP is not synonymous with optimization. If there are no overlapping subproblems or if a stronger
invariant enables a greedy/linear solution, a large state table adds complexity without buying
anything.

## Diagnostic

Before building a table, answer:

1. What does one state mean?
2. Can different decision paths reach the same state?
3. Does the future depend only on that state?
4. How many states and transitions exist?

If those answers are vague, the DP design is premature.
