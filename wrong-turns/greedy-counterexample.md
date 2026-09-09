# Wrong Turn — Greedy without a proof

## Tempting idea

Take the locally largest reward at every step because each choice improves the answer immediately.

## Why it looks reasonable

Local improvement feels aligned with global optimization, especially when examples are too small to
expose delayed consequences.

## Smallest counterexample

Coin change with denominations `{1, 3, 4}` and target `6`.

## Step-by-step failure

Largest-first chooses `4`, then `1`, then `1`: three coins. Choosing `3 + 3` uses two coins. The
first greedy choice cannot be exchanged into an optimal solution without changing the result.

## Correct signal

Look for an exchange argument, cut property, monotonic ordering proof, or another reason a local
choice can appear in some global optimum.

## Better candidates

DP for arbitrary coin systems; exhaustive search at tiny scale; a proven greedy rule only when the
problem structure supports it.

## General lesson

“Looks best now” is a hypothesis. Greedy becomes an algorithm only after the hypothesis is proved.
