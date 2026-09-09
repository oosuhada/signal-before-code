# Naming review

The existing GitHub naming style tends to describe a mechanism, investigation surface, or point of
view rather than sound like a course: `beneath-the-stack`, `evidence-scenario-engine`,
`search-observatory`, `elevator-queue-lab`, `decision-module-runtime`, and similar names.

The new repository should therefore avoid names that sound like a generic coding-test curriculum or
solution site.

| Candidate | Strength | Concern |
| --- | --- | --- |
| **signal-before-code** | Names the exact behavior to train; phrase-like and memorable | Needs the README description to make “signal” concrete |
| reason-before-code | Strong emphasis on explanation | Slightly broader than algorithm selection |
| pattern-before-code | Clear interview context | Can sound like pattern memorization, which is not the goal |
| algorithm-intuition-lab | Accurate and searchable | More course/lab-like and less distinctive |
| pattern-recognition-lab | Explicit training target | Sounds more academic than the surrounding portfolio |
| problem-signal-lab | Keeps “signal” central | A little mechanical |
| constraint-to-choice | Captures the reasoning pipeline | Meaning is less obvious at first glance |
| choice-defense-lab | Emphasizes defending trade-offs | Does not immediately imply algorithms |
| signal-to-strategy | Compact and flexible | Could refer to many non-algorithm domains |
| algorithm-selection-lab | Extremely clear | Generic and instructional-site sounding |

## Selected: `signal-before-code`

Why it wins:

1. The repository exists to notice constraints and hidden clues **before** implementation.
2. “Signal” is wider than a memorized pattern keyword: sortedness, repeated extrema, equal edge
   weight, bounded key domains, and monotonic predicates are all signals.
3. The phrase fits next to `beneath-the-stack`: one name says where to look, the other says when in
   the reasoning process to look.
4. It leaves room for Python first and Java later without putting a language or judge in the name.
5. It does not imply a giant algorithm catalog or a teaching platform.

Availability was checked before repository creation with the authenticated GitHub CLI.
