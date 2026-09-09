# 26 — Trie

## 1. What problem shape does this solve?

A trie stores strings by shared prefixes. It becomes useful when queries repeatedly ask about
prefixes, autocomplete-like branching, dictionary traversal by characters, or many words sharing
common beginnings.

## 2. Signals to notice

```text
prefix / starts with
autocomplete
dictionary of many strings
character-by-character search
word search with shared prefixes
```

## 3. Naive idea

For every prefix query, scan every stored word and call `startswith`.

## 4. Why the naive idea breaks

Repeated queries recompare the same leading characters across many words. A trie stores those shared
prefix transitions once.

## 5. Core intuition

Each path from the root spells a prefix. A node answers “this prefix exists,” while a terminal flag
answers “a full word ends here.” Shared prefixes become shared path nodes.

## 6. Invariant

After inserting a word, traversing its characters from the root follows existing child edges and the
final node is marked terminal. Prefix existence does not imply full-word existence.

## 7. Step-by-step walkthrough

Insert `car` then `cat`:

```text
root
 └─ c
    └─ a
       ├─ r*   (* full word)
       └─ t*
```

`ca` is a valid prefix but not a full stored word unless its node is also terminal.

## 8. Implementation

```python
class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.terminal = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.terminal = True

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

## 9. Complexity

Insert/search costs `O(L)` for word length `L`, independent of number of stored words except through
memory/cache effects. Space is proportional to the number of distinct prefix nodes, up to total
characters inserted.

## 10. Common mistakes

- forgetting terminal markers;
- confusing prefix existence with exact-word existence;
- allocating fixed large child arrays for sparse alphabets unnecessarily;
- ignoring memory overhead in Python object/dict tries;
- using trie for one-off exact membership where a set is simpler.

## 11. When NOT to use it

- Exact whole-string membership → hash set/map is simpler.
- Very memory-sensitive workloads may prefer sorted strings + binary search/compressed structures.
- Tiny dictionaries do not justify structural complexity.

## 12. Neighboring patterns

- **Trie vs hash:** prefix traversal vs full-key lookup.
- **Trie + DFS/backtracking:** board word search can prune when no dictionary prefix exists.
- **Trie vs binary search:** sorted word list can answer prefix ranges without explicit nodes.

## 13. Mutation ladder

```text
exact membership only       → hash set
many prefix queries         → trie
sorted static dictionary    → binary-search prefix range candidate
board search + dictionary   → backtracking + trie pruning
huge alphabet/memory limit  → compressed representation considerations
```

## 14. Practice ladder

- **Understand:** implement insert/search/prefix.
- **Recognize:** replace repeated prefix scans.
- **Apply:** wildcard/prefix DFS and board search.
- **Mixed:** compare trie memory cost with hash/sorted-list alternatives.
