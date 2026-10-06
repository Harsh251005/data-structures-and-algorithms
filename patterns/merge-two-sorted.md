# Merge two sorted

**Spot it when:** two already-sorted sequences need to become one sorted sequence.
**Core move:** one pointer per input; each step take the smaller, then flush the leftovers.

```python
i = j = 0
out = []
while i < len(a) and j < len(b):
    if a[i] <= b[j]:
        out.append(a[i]); i += 1
    else:
        out.append(b[j]); j += 1
out += a[i:] + b[j:]           # leftovers, after the loop
```

| Problem | Twist |
|---|---|
| 88 Merge Sorted Array | write the result back with `nums1[:] = out`; follow-up: fill from the BACK for O(1) space |

## My traps
- Two `if`s instead of `if / else`: the second compare saw the already-moved pointer (LC 88).
- Leftovers handled inside the loop with `if nums1:` (always true for a non-empty list) (LC 88).
- Forgetting to write back to `nums1`, the only thing LeetCode checks (LC 88).
