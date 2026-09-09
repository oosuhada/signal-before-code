# Algorithm Debugging Strategy

Debug the violated invariant before randomly editing lines.

## Fast classification

| Symptom | First question |
| --- | --- |
| wrong only at first/last index | is the interval convention consistent? |
| BFS queue grows with duplicates | when is `visited` marked? |
| Dijkstra revisits old priorities | is a stale heap entry being skipped? |
| duplicate values fail | should the comparison be `<` or `<=`? |
| binary search loops forever | does every branch strictly shrink the interval? |
| DP is correct except smallest inputs | are state meaning and base cases aligned? |
| Java answer becomes negative/strange | did `int` overflow before conversion to `long`? |
| recursion crashes on path-like input | is call depth proportional to N? |

## Off-by-one

Write the interval semantics next to the code. For `[left,right]`, emptiness is `left > right`; for
`[left,right)`, emptiness is `left >= right`. Mixing those conventions is the bug, not “binary search
being tricky.”

## Visited timing

For BFS shortest hops, marking at enqueue time means one node occupies the frontier once. Marking at
dequeue time can let several parents enqueue the same node, increasing memory and potentially
complicating parent/distance tracking.

## Stale heap entries

Java/Python priority queues usually do not support cheap arbitrary decrease-key. Pushing the improved
distance is simple, but old entries remain. Compare the popped priority with the current best value
and discard stale work.

## DP base/state mismatch

Before checking the transition, fill the sentence:

```text
dp[i] means ____________________
dp[i][j] means ____________________
```

Then manually compute the first two or three states from that definition. If the table and sentence
disagree, the recurrence is not the first bug to fix.

## Integer overflow

In Java, promote before arithmetic:

```java
long sum = (long) a + b;
```

not:

```java
long sum = a + b; // may already overflow as int
```

## Debug order

1. Reproduce with the smallest failing input.
2. Identify the first step where the invariant becomes false.
3. Classify: selection, state definition, boundary, implementation, or numeric issue.
4. Fix the earliest violated assumption.
5. Add a mutation/counterexample so the same misunderstanding becomes reusable evidence.
