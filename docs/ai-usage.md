# AI usage: textbook authoring vs personal evidence

This repository deliberately allows different AI policies for its two layers.

## Textbook layer

AI assistance is allowed for:

- chapter explanations and examples;
- algorithm comparisons;
- counterexamples and wrong-turn analysis;
- mutation ladders;
- practice curation metadata;
- Python reference examples;
- structural review and validation tooling.

The textbook is **AI-assisted and source-referenced educational content**. External sources are
recorded in [`references.md`](references.md); their code/prose is not copied into the repository.

## Personal learning layer

The policy is stricter because this layer is evidence of my own performance.

### Before first attempt

AI may:

- clarify ambiguous wording;
- restate input/output format;
- ask what constraints I notice.

AI must not:

- reveal the expected pattern;
- provide solution code;
- provide the key invariant;
- rank candidate algorithms for me.

### After I have committed to an approach

AI may act as an interviewer:

- “Why does that pointer move never need to reverse?”
- “What input breaks your complexity?”
- “What assumption makes first discovery optimal?”
- “Can you construct a counterexample to your greedy rule?”

It should challenge before correcting.

### After submission

AI may:

- review correctness and complexity;
- separate recognition failure from implementation failure;
- generate counterexamples;
- compare alternatives;
- propose mutations;
- quiz the invariant during revisits.

## Evidence rule

AI may help **analyze** an attempt, but it may not fabricate one. Fields such as `solved`,
`hint_free`, `revisit_success`, and `mastered` are written only from actual sessions.

The default interviewer prompt remains in [`../prompts/interviewer.md`](../prompts/interviewer.md).
