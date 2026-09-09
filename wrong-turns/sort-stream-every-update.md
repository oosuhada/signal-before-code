# Wrong Turn — Sorting the whole stream after every update

## Tempting idea
Keep data sorted so every top-K/min/max query is easy.

## Why it looks reasonable
Sorting solves ordering perfectly in an offline batch and produces simple query code.

## Smallest counterexample
Insert `5, 1, 4, 2` one at a time and ask for the minimum after every insertion.

## Step-by-step failure
Re-sorting prefixes of sizes 1,2,3,4 repeats ordering work that earlier sorts already performed. The
answer only needs one extremum, not total order.

## Correct signal
Online updates + repeated extremum query suggest maintaining only the order the query needs.

## Better candidates
Heap for repeated min/max; balanced ordered structures if richer predecessor/range operations matter.

## General lesson
Full order is expensive state when the output contract only asks for partial order.
