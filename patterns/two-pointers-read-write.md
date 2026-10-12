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
- **Flipped the keep condition** (`==` instead of `!=`) on the 27 cold re-solve (2026-10-11), and the asserts carried the same
  misread, so everything passed. Then fixed only the return (`len - count`) and left `nums` wrong. `i` already IS `k`.
- **No assert on `nums[:k]`**: the asserts checked only `k`, so a correct `k` with garbage in `nums` passed. Always assert
  `sorted(nums[:k]) == expected` too.
- **Deduping with a `set`, then writing it back** (`nums[:len(seen)] = seen`, LC 26 cold re-solve 2026-10-12). It's not just
  O(n) extra space, it's WRONG: a set has no order. `[-1, 0, 0, 1]` came back as `[0, 1, -1]`. The tests missed it because
  they asserted only on `k`, and two of the inputs weren't even sorted.
- **A redundant counter beside `i`** (27 on 2026-10-11, then 26 on 2026-10-12): `i + 1` already IS `k` on 26 (`i` on 27).
