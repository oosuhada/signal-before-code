# Greedy vs DP

## Same-looking problem

Both often optimize cost, profit, count, or length.

## What changes?

Greedy throws away alternatives after making a local choice. DP preserves enough state to compare
different histories that lead to future decisions.

Coin example:

```text
coins = [1, 3, 4], target = 6
greedy largest-first: 4 + 1 + 1 = 3 coins
optimal:              3 + 3     = 2 coins
```

## Deciding signal

- can you prove an exchange: replacing an optimal solution's first choice with the greedy choice
  never makes it worse? Greedy may be valid.
- do different earlier choices lead to overlapping states with different values? DP is safer.

“Looks locally best” is not a greedy proof.
