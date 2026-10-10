# Running best-so-far (one pass)

**Spot it when:** each position's answer depends on the best thing *behind* it (cheapest so far, max so far).
**Core move:** carry that "best behind me" in one variable, so you never look back.

```python
best_behind = float('inf')
answer = 0
for x in nums:
    best_behind = min(best_behind, x)          # check 1: update what's behind
    answer = max(answer, x - best_behind)      # check 2: use it now
```

| Problem | Twist |
|---|---|
| 121 Best Time to Buy and Sell Stock | cheapest price so far; best profit = price − cheapest |

## My traps
- Carrying the brute force's `i`/`j` into the one-pass version. The variable *replaces* `i` (LC 121).
- Starting the minimum at 0: nothing is ever smaller, so it never updates. Use `inf` (LC 121).
- Joining the two updates with `and`: they never happen on the same step (LC 121).
- Re-solve history (LC 121): 54 min + viewed (10-06) → 10 min cold (10-07) → 6 min cold, 0 hints (10-10). His own tests now include a high-before-low case ([7,1,5,3,6,4]).
- **Needed:** a trace table (day by day) is what made it click. Draw one when stuck.
