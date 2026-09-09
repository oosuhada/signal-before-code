# Case Study — Hash Intuition vs Database Storage

## Verified artifact

`AskOosu/src/lib/rag/search-cache.ts`, remote-main blob
`0f5f71059d6ab16f810d853551e5909eb77369fd`.

The source serializes retrieval parameters into a stable hash-derived `cache_key`, selects cached
results by that key while checking expiry, and upserts payloads into PostgreSQL.

## Textbook bridge

The algorithmic signal is repeated exact lookup:

> The same logical query configuration should map to the same cached result slot.

That resembles the key → value intuition behind a hash map.

## Why not replace PostgreSQL with a Python/Java hash map?

Because the production requirements include persistence, process boundaries, TTL queries, indexes,
and database concurrency. The **keying idea** transfers; the implementation substrate does not.

## Why not use only the raw query string as key?

Retrieval mode, weights, entity, language, privacy/content flags, and limit all change the semantic
request. Omitting them would create collisions at the application-meaning level even if the hash
function itself had no collision.

## Interview defense

Distinguish “hashing is the selection idea” from “HashMap is the production storage choice.”
