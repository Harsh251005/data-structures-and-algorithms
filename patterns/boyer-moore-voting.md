# Boyer-Moore voting

**Spot it when:** one value is guaranteed to appear **more than n/2 times**, and you want O(1) space.
**Core move:** keep a `candidate` and a `count`. Same vote: +1. Different vote: −1 (both votes cancel).
When `count` hits 0 the stage is empty, so the next vote becomes the candidate.

```python
candidate, count = None, 0
for x in nums:
    if count == 0:             # stage empty
        candidate = x
    count += 1 if x == candidate else -1
return candidate               # only safe because a majority is guaranteed
```

| Problem | Twist |
|---|---|
| 169 Majority Element | the guarantee makes the survivor the answer; hash-map counting is the O(n)-space step before it |

## My traps
- Checking `candidate == 0` instead of `count == 0`: a value of 0 isn't "nobody" (LC 169).
- Forgetting the `return` at the end, so the function returns `None` (LC 169).
- Thinking the vote that empties the stage takes it over. It's used up in the cancel; the **next** vote takes the stage (LC 169).
- Brute force: an inner loop from `i + 1` counts every value one short, so `[5]` fails (LC 169).
