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
- Testing an in-place function: keep the list in your own variable, call, then assert on that variable. `assert s == ...` checks the Solution object (LC 88 re-solve).
- `m` counts the real values, not the zero slots; `len(nums1) == m + n`, and the expected output has no zeros (LC 88 re-solve).
- Spread the tests: make sure one case leaves leftovers in EACH input, or one leftover loop never runs (LC 88 re-solve).
