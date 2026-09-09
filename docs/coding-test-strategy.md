# Coding-Test Strategy — Signal Before Code

The goal is not to spend five minutes naming patterns. It is to make the first few minutes produce
evidence that prevents the wrong implementation.

## First 2 minutes

### 1. Restate input and output

Write what one input unit means and exactly what must be returned. Separate “find one,” “count,”
“return all,” “minimum,” and “online query” because those requirements can change the data structure.

### 2. Read constraints as a budget

Estimate the obvious brute force. `N=200,000` does not magically mean O(n log n), but it should make
an O(n²) pair scan defend itself before you code it.

### 3. Write the correctness baseline

State the simplest approach that obviously works, even if too slow. This gives you something to
optimize rather than pattern-matching from a blank page.

## Next: candidate selection

Ask:

- Is the data contiguous, sorted, hierarchical, or a graph?
- Is the same membership/min/range/subproblem work repeated?
- What property is monotonic?
- Is the input static or updated online?
- Do I need one extremum, top K, or complete order?
- Are edge weights equal, nonnegative, or possibly negative?

Keep two plausible candidates alive until one has a stronger correctness argument.

## Before code

Write one sentence for the invariant. Then choose:

- state representation;
- boundary convention (`[l,r]` vs `[l,r)`);
- visited timing;
- numeric width (`int` vs `long` in Java);
- duplicate policy;
- base cases and empty input behavior.

If you cannot state why a pointer may move, why a node may finalize, or what `dp[i]` means, do not
hide that uncertainty by coding faster.

## After code

Run tiny tests chosen to attack the invariant:

1. minimum-size valid input;
2. no-solution case;
3. duplicate/equal values;
4. first/last boundary;
5. maximal sum/product/weight for overflow;
6. disconnected/cyclic graph when relevant.

Then derive complexity from operations. A nested loop is not automatically O(n²), and a heap does
not make an entire algorithm O(log n).

## If stuck

Return to the mutation question:

> Which single assumption would make my current approach obviously valid?

The gap between the actual problem and that assumption often reveals the missing pattern.
