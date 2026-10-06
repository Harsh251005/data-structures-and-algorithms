# Two pointers, converging

**Spot it when:** you work on pairs from both ends (reverse, palindrome, pair-sum on sorted input).
**Core move:** `i` at the start, `j` at the end; act, then move them inward until they meet.

```python
i, j = 0, len(a) - 1
while i < j:
    a[i], a[j] = a[j], a[i]    # or compare / check
    i += 1
    j -= 1
```

| Problem | Twist |
|---|---|
| 344 Reverse String | in-place swap |

## My traps
- `s = s[::-1]` rebinds the local name; the caller's list never changes. In-place means mutate (LC 344).
