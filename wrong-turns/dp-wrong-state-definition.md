# Wrong Turn — DP with an ambiguous state definition

## Tempting idea
Start writing transitions like `dp[i] = max(dp[i-1], ...)` before saying what `dp[i]` means.

## Why it looks reasonable
Familiar recurrence syntax can look plausible even when two incompatible meanings are mixed.

## Smallest counterexample
One line treats `dp[i]` as “best answer using first i items”; another treats it as “best answer
ending exactly at i.” Those states have different transitions and base cases.

## Step-by-step failure
A transition imports a value whose semantic promise does not match what the next line assumes. The
table may fill without exceptions while representing no coherent subproblem.

## Correct signal
Write one sentence: `dp[...] = ...` and test that every dependency refers to a smaller state with the
same contract.

## Better candidates
Redefine the state before coding; sometimes a simpler greedy/scan eliminates DP entirely.

## General lesson
DP bugs often begin as definition bugs, not loop bugs.
