# Requirement Mutation Drill

Small output changes often change the best data structure even when the input is identical.

```text
find one matching value
→ early scan/hash lookup may be enough

find all matches in sorted order
→ ordering becomes part of the requirement

find top K while data streams in
→ maintained size-K heap becomes a candidate

count only
→ do not retain full reconstruction state unless needed

answer static range queries
→ preprocessing can pay off

answer queries between updates
→ maintained dynamic state becomes important
```

Before choosing an algorithm, rewrite the output contract in one sentence: **one/all/count/order,
online/offline, static/dynamic**. Those words often decide more than the problem's theme.
