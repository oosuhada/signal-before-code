# Online vs Offline

## Same-looking requirement

“Keep the smallest / largest / top K values.”

### Offline

All values are available before any answer is required. Sorting can spend `O(N log N)` once and then
serve ordered output cheaply. If only one minimum is needed, even sorting is excessive; scan once.

### Online

Values arrive one by one and an answer may be requested between arrivals. “Sort everything first” is
not an available move because the future input does not exist yet. A heap can preserve only the
extremum information needed across updates.

## Decision signal

Ask **when must an answer be available relative to when data arrives?** Online/offline is often more
important than the noun in the problem statement.

## Engineering bridge

The same distinction appears in queues, schedulers, stream processing, caches, and incremental
indexes: repeated online updates reward maintained state; one offline batch often rewards simpler
sorting/scanning.
