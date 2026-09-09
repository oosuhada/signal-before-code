# Canonical Java Transfer Set

This directory contains a compact transfer set, not Java copies of the 168-problem roadmap.

- 29 canonical implementations cover all 28 textbook chapters.
- [`catalog.json`](catalog.json) is the machine-readable chapter → symbol map.
- `src/` contains six deliberately small source files grouped by reasoning domain.
- CI compiles every source file with Java 21.

Use these only after you can explain the corresponding Python chapter invariant. A successful
translation means the reasoning survives different library APIs, integer behavior, and type syntax.
