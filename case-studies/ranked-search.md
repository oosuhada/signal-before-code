# Case Study — Ranked Search: Full Sort vs Top-K

## Verified artifact

`source-archive/search-worker.js`, remote-main blob
`9a48df9dd43da65430a3c9657c0bdcc2a2343a7a`.

The worker loads prebuilt search metadata, scores every document against query tokens, filters zero
scores, and sorts all matches by descending score plus an ID tie-break before returning the ordered
IDs.

## Why sorting is reasonable here

The current requirement returns the complete ranked match list. Once every matching document has a
score, sorting directly expresses that output contract.

```text
all matches ranked
→ full ordering has value
→ sort is a natural candidate
```

## Requirement mutation: return only top 10

If the corpus became very large and only ten results were required, full sorting would establish
order among many results the caller never sees. A size-10 min-heap could become a candidate while
scanning scores:

```text
all ranked results → sort all matches
top K only          → bounded heap becomes plausible
```

## Why not a hash table?

Exact key lookup is not the query. Every document can receive a graded relevance score based on
multiple tokens, so ranking work remains even if metadata itself is indexed by ID.

## Online/offline bridge

The repository also prebuilds `data/search-index.json` outside the worker. This illustrates another
boundary: expensive metadata preparation can happen offline while latency-sensitive scoring happens
at query time.
