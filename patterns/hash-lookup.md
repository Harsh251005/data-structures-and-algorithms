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
| 169 Majority Element | dict value → count with `seen.get(x, 0) + 1`; return once a count passes n // 2 |

## My traps
- Adding before checking lets a number pair with itself (LC 1, `[3, 2, 4]`, 6).
- Brute force inner loop starting at `1` instead of `i + 1`: same self-pairing bug, `[9, 10, 2, 3, 2]`, 4 returned `[2, 2]` (LC 1 re-solve).
- `in` on a list looks innocent but makes the loop O(n²) (LC 217).
