# Wrong Turn — Two Pointers on an unsorted pair-sum array

## Tempting idea
Put one pointer at each end and move based on whether the sum is too small or too large.

## Why it looks reasonable
The code shape is simple and resembles the correct sorted-array solution.

## Smallest counterexample
`[8, 1, 4, 2]`, target `6`.

## Step-by-step failure
Endpoints sum to 10. Moving the right pointer left because 10 is “too large” assumes smaller values
live to the left. In unsorted input, that assumption is false and can discard the valid pair `4+2`.

## Correct signal
Boundary elimination requires ordering or another monotonic relation.

## Better candidates
Hash complement lookup; sort a copy then use two pointers if original indices are not required.

## General lesson
Two indices do not make a two-pointer proof; safe elimination does.
