# AI usage rule

AI is allowed in this repository only when it preserves the part of the task I am trying to train.

The target skill is **algorithm selection under uncertainty**. If AI reveals the pattern before I
have formed candidates, it has removed the training stimulus.

## Before the first attempt

AI may:

- clarify ambiguous wording;
- restate input/output in neutral terms;
- ask me what constraints seem important.

AI must not:

- name the intended algorithm or pattern;
- provide solution code or pseudocode;
- rank candidate algorithms for me;
- reveal a key invariant or hidden trick;
- point to a solved version of the same problem.

Default instruction:

```text
Do not give me the solution or name the pattern.
Only clarify wording if I ask.
Make me identify the constraints and candidates myself.
```

## After I have written a first approach

AI becomes an **interviewer and adversary**.

It may ask:

1. Which constraint makes the naive approach risky?
2. What invariant does your approach rely on?
3. Can you construct an input that breaks it?
4. Which alternative did you reject, and why?
5. What happens if one assumption changes?

It should challenge the approach before offering a replacement.

## After submission

AI becomes a **reviewer and problem mutator**.

It may:

- review time and space complexity;
- generate counterexamples;
- compare valid alternatives;
- identify implementation-only bugs;
- mutate constraints and ask whether the algorithm still applies;
- evaluate whether my explanation actually defends the choice.

If the submission failed because of pattern recognition, the review should reconstruct the missed
signal rather than merely present final code.

## After a successful solve

AI may generate a mutation, but the mutation should change an applicability boundary rather than
only rename variables.

Useful mutations include:

- sorted → unsorted;
- static → streaming;
- one query → repeated queries;
- unweighted → weighted;
- positive weights → negative edge;
- exact answer → top-K;
- fixed window → variable window.

## What AI should never become here

AI is not the answer key I consult before thinking. It is not a generator that fills all future
chapters and marks them complete. Unstudied chapters remain scaffolds until real attempts create the
need for more content.

Use [`../prompts/interviewer.md`](../prompts/interviewer.md) as the default review prompt.
