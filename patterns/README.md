# Pattern cards

One card per pattern: how to spot it, the core move, a skeleton, the problems that used it,
and **my own traps**: mistakes I actually made, with the problem they came from.

How they're used:
- **After every problem**, the card for its pattern gets updated: the new problem, plus any new trap.
- **Session start**: one trap from a card is the warm-up question.
- **Sunday review**: read all the cards for the week's patterns.
- **Never before a new problem.** Knowing the pattern up front is a hint (hint level 2), and
  in interviews nobody tells you which pattern it is.

| Card | Problems |
|---|---|
| [Hash lookup](hash-lookup.md) | 217, 1 |
| [Two pointers, converging](two-pointers-converging.md) | 344 |
| [Two pointers, read/write](two-pointers-read-write.md) | 26, 27 |
| [Running best-so-far](running-best-so-far.md) | 121 |
| [Merge two sorted](merge-two-sorted.md) | 88 |

## Traps that cross patterns
- **Tests that check only the return value.** When a problem mutates its input (344, 26, 27, 88), the
  input list is what gets judged, so assert on it.
- **`if` + `if` vs `if / else`.** Ask: can both happen in the same step? Yes means two `if`s (121: new
  minimum and new best profit are independent). Exactly one means `if / else` (88: you take one number per step).
