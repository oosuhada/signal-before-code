# Wrong Turn — Monotonic Stack without matching direction

## Tempting idea
Use a decreasing stack for any “greater element” question.

## Why it looks reasonable
Next-greater examples often use the same familiar stack shape.

## Smallest counterexample
Ask for the **previous** greater element while scanning as if resolving future next-greater answers.

## Step-by-step failure
The stored unresolved state answers a different temporal question. Popping on the current value may
destroy the candidate that should answer “previous greater” for the current index.

## Correct signal
State precisely whether the answer lies left/right and whether current input resolves old items or
old items answer the current one.

## Better candidates
Choose increasing/decreasing stack and scan direction from the relation being answered.

## General lesson
Monotonicity direction is part of the invariant, not a template detail.
