# Wrong Turn — Trie for one exact lookup

## Tempting idea
Strings suggest tries, especially when prefixes are mentioned elsewhere in the textbook.

## Why it looks reasonable
A trie can certainly answer exact membership, so it is correct in a broad sense.

## Smallest counterexample
Store three words and perform one exact membership query.

## Step-by-step failure
The trie allocates node/child structure for every prefix even though no prefix operation is used. A
hash set represents the required exact keys directly with much less code.

## Correct signal
Trie value comes from repeated prefix traversal, lexicographic structure, or character-by-character
sharing—not from strings alone.

## Better candidates
Hash Set for exact membership; sorted list + binary search for ordered static data.

## General lesson
Prefer the weakest structure that supports the required operations.
