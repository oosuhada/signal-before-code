# Wrong Turn: “Take the Best-Looking Choice”

## Temptation

Greedy code is short, so a locally best move is easy to trust.

## Counterexample

With coins `[1, 3, 4]` and target `6`, largest-first gives `4 + 1 + 1`, while `3 + 3` uses fewer
coins.

## The missing proof

A greedy rule needs a reason that committing now cannot destroy a better global solution. Typical
proof shapes include exchange arguments, cut properties, or dominance ordering.

If the only defense is “it seems best,” keep DP or exhaustive search alive as candidates.
