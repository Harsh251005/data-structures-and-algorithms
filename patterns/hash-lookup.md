# Hash lookup (set / dict)

**Spot it when:** "have I seen this before?" or "does its partner exist?", with no ordering needed.
**Core move:** trade O(n) memory for O(1) lookups: one pass, checking the set/dict before adding.

```python
seen = {}                      # or set()
for i, x in enumerate(nums):
    if need(x) in seen:        # check FIRST
        return ...
    seen[x] = i                # then add
```

| Problem | Twist |
|---|---|
| 217 Contains Duplicate | set; `x in set` is O(1), `x in list` is O(n) |
| 1 Two Sum | dict value → index; look for `target - x` |

## My traps
- Adding before checking lets a number pair with itself (LC 1, `[3, 2, 4]`, 6).
- `in` on a list looks innocent but makes the loop O(n²) (LC 217).
