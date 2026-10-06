# Two pointers, read/write (same direction)

**Spot it when:** filter or deduplicate an array **in place** and return the new length `k`.
**Core move:** `j` reads every element; `i` is the next slot to write. Copy keepers to `i`, ignore the rest.

```python
i = 0
for j in range(len(nums)):
    if keep(nums[j]):
        nums[i] = nums[j]
        i += 1
return i                       # k
```

| Problem | Twist |
|---|---|
| 26 Remove Duplicates from Sorted Array | keep when `nums[j] != nums[i]`; `j` starts at 1 and the answer is `i + 1` |
| 27 Remove Element | keep when `nums[j] != val`; `j` starts at 0 |

## My traps
- **Moving the unwanted values to the end.** Proposed it on BOTH 26 and 27; it's O(n²) and unnecessary.
  Only the first `k` slots are judged, so copy keepers forward instead.
- `i = j` instead of `i += 1` (LC 26).
- Moving `j` by hand inside a `for` loop that already moves it gives an IndexError (LC 26).
- A counter set only inside the loop stays wrong when the body never runs (`[7]`, `[1, 1, 1]`, LC 26).
