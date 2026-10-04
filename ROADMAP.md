# DSA Roadmap: Zero → MNC Interview Ready

**Learner:** Harsh · **Language:** Python 3.14 · **Editor:** PyCharm · **Started:** 2026-10-04
**Pace:** ~2 h/day, 6 days/week · **Estimated length:** ~30 weeks (7–8 months), then interview mode

**Exit criteria.** You're done when, on unseen problems, you can do the following:
- Solve a **medium** in 25–35 minutes while talking through your approach, the way you would with an interviewer.
- Solve **hards** in the core patterns (sliding window, DP, graphs, heaps) roughly 40–50% of the time.
- State the time and space complexity of any solution without hesitating.

> Honest calibration: the timeline is an estimate, not a promise. Most people reach "mediums are comfortable" after roughly 250–350 well-reviewed problems. Solving 600 problems carelessly gets you there slower than solving 300 carefully. The plan adjusts to your actual pace.

---

## 1. How I'll teach

You'll write every line of code yourself. My role is the senior engineer sitting next to you.

### The topic loop (repeats for every topic)

| Step | What happens | Who drives |
|---|---|---|
| 1. **Why** | Short lesson: the problem this idea solves, with a real-world scenario (e.g. "a hash map is the coat-check counter at a wedding hall") | Me, short. You ask for depth |
| 2. **See it** | Trace it by hand on a tiny input: pen and paper or the PyCharm debugger. No code yet | Together |
| 3. **Build it** | You write the core template from scratch (binary search, BFS…) and it goes into `templates/` | You |
| 4. **Ladder** | Problems in order of difficulty: Easy → Medium → Medium+ → Hard | You |
| 5. **Review** | I review your code the way I would a PR: correctness, edge cases, complexity, naming, cleaner alternatives | Me |
| 6. **Re-solve** | The same problems come back on Day 3, 7 and 21 (spaced repetition) | You |

### The hint ladder: I never hand you the solution
When you're stuck, ask for hints in order:
1. **Nudge**: "What do you need to look up quickly here?"
2. **Pattern**: "This is a sliding window problem. What makes the window invalid?"
3. **Skeleton**: the outline of the approach in plain English, without code.
4. **Walkthrough**: only after a real attempt. Afterwards you re-code it yourself the next day.

**25-minute rule:** stuck for 25 minutes with no progress means ask for hint 1. Struggling longer than that stops being useful.

### The 6-step problem framework (practise it from day 1, because interviews grade it)
1. **Understand.** Restate the problem, ask about input size, edge cases, duplicates and negatives.
2. **Examples.** Work through 2–3 by hand, including an edge case.
3. **Brute force.** State it and its complexity, even if it's slow.
4. **Optimise.** Find what is repeated or wasted, then pick a pattern.
5. **Code.** Write clean code with meaningful names.
6. **Test.** Dry-run your own examples and edge cases, then give the final complexity.

---

## 2. Consistency system (fun, but professional)

### Career ladder (levels = XP)
| Level | XP | Unlocks |
|---|---|---|
| 🎓 Intern | 0 | Phase 0–1 |
| 💼 SDE-1 | 500 | Phase 2 |
| 🔧 SDE-2 | 1,500 | Phase 3–4 |
| 🧠 Senior SDE | 3,500 | Phase 5 (DP) |
| 🏛️ Staff Engineer | 6,000 | Phase 6 + Interview mode |
| 👑 Principal | 9,000 | You're interview-ready |

**XP:** Easy 10 · Medium 25 · Hard 60 · Solved with no hints +5 · Spaced re-solve 5 · Weekly mock 40 · Promotion review passed 100

### Promotion reviews (boss fights)
At the end of each phase you get a **timed assessment**: 3 unseen problems in 90 minutes, with me as the interviewer. You don't see the problems in advance. Pass 2 of 3 to get promoted. Fail, and you get a targeted 3-day revision sprint, then a retry.

### Streak rules
- **Minimum viable day:** on a bad day, **one re-solve or one easy problem (about 20 minutes)** keeps the streak alive. Showing up counts for more than the score.
- **Never miss twice.** Missing one day is life. Missing two days in a row is the start of quitting.
- **Sunday** is review and mock day, or rest if you need it.

### Daily ritual (2 hours)
| Time | Block |
|---|---|
| 10 min | **Warm-up**: one spaced re-solve from the due queue |
| 30 min | **Learn**: new concept or pattern (lesson + hand trace) |
| 70 min | **Solve**: 2–3 ladder problems |
| 10 min | **Log**: commit to git, update tracker, one line in your journal about what tricked you |

Each session in this folder, I open with: **Day N · streak · XP · today's task.** You don't have to remember where we were.

---

## 3. The curriculum

`E` = Easy, `M` = Medium, `H` = Hard. Numbers are LeetCode problem IDs. ★ = must-do classic.

### Phase 0: Setup & Toolkit (Week 1)
**Goal:** a working environment, plus the Python and Big-O you need before anything else.
- PyCharm project, venv, pytest, git, folder structure (see §4)
- Python for DSA: lists, slicing, `dict`, `set`, `collections` (`Counter`, `defaultdict`, `deque`), `heapq`, `sorted` with `key=`, list comprehensions, classes for nodes
- **Big-O**: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ). How to read code and state its complexity. Space complexity. Why `x in list` is O(n) and `x in set` is O(1)
- Practice: 15 short "what's the complexity?" snippets I'll give you, plus 1 ★Two Sum (E), 217 Contains Duplicate (E), 344 Reverse String (E)

### Phase 1: Foundations (Weeks 2–5) · 🎓 Intern
| Week | Topic | Problems |
|---|---|---|
| 2 | **Arrays & Strings** | 26 (E), 27 (E), 88 (E), 121★ (E), 169 (E), 14 (E), 125 (E), 387 (E), 189 (M), 238★ (M) |
| 3 | **Hashing** | 242★ (E), 383 (E), 205 (E), 290 (E), 49★ (M), 347★ (M), 128★ (M), 36 (M), 560★ (M) |
| 4 | **Two Pointers** | 283 (E), 977 (E), 167★ (M), 15★ (M), 11★ (M), 75 (M), 42★ (H) |
| 5 | **Sliding Window + Prefix Sum** | 643 (E), 724 (E), 303 (E), 3★ (M), 209 (M), 1004 (M), 424★ (M), 567★ (M), 525 (M), 974 (M), 76★ (H) |

🏁 **Promotion review → SDE-1**

### Phase 2: Core Techniques (Weeks 6–10) · 💼 SDE-1
| Week | Topic | Problems |
|---|---|---|
| 6 | **Recursion** (call stack, base case, trust the recursion), trained with the debugger | 509 (E), 231 (E), 50 (M), recursive 206 (E), 21 (E), and I'll give you print-all-subsets |
| 7 | **Sorting + Binary Search** (merge sort and quicksort written from scratch) | 912 (M), 704★ (E), 35 (E), 278 (E), 69 (E), 74 (M), 34★ (M), 33★ (M), 153★ (M), 162 (M) |
| 8 | **Binary Search on Answer + Linked Lists** | 875★ (M), 1011 (M), 410 (H), 206★ (E), 876 (E), 141★ (E), 160 (E), 234 (E), 19★ (M), 142 (M), 143 (M), 2 (M) |
| 9 | **Stacks, Queues, Monotonic Stack** | 20★ (E), 232 (E), 496 (E), 155★ (M), 150 (M), 394 (M), 739★ (M), 503 (M), 901 (M), 853 (M), 84★ (H) |
| 10 | **Consolidation**: 138 (M), 146★ LRU Cache (M), 215 (M), 56★ (M), 179 (M), 23 (H), 25 (H), plus re-solves of weak spots | |

🏁 **Promotion review → SDE-2**

### Phase 3: Trees, Heaps, Backtracking (Weeks 11–15) · 🔧 SDE-2
| Week | Topic | Problems |
|---|---|---|
| 11 | **Binary Trees I**: traversals (recursive and iterative), DFS vs BFS | 94, 144, 145 (E), 104★ (E), 226★ (E), 100 (E), 101 (E), 112 (E), 102★ (M), 103 (M), 199★ (M) |
| 12 | **Binary Trees II**: postorder thinking ("what does my child return?") | 543★ (E), 110 (E), 572 (E), 113 (M), 1448 (M), 236★ (M), 105★ (M), 124★ (H), 297 (H) |
| 13 | **BST + Heaps / Priority Queue** | 700 (E), 701 (M), 235 (M), 98★ (M), 230★ (M), 450 (M), 703 (E), 1046 (E), 973★ (M), 621★ (M), 355 (M), 295★ (H) |
| 14 | **Backtracking** (choose → explore → un-choose) | 78★ (M), 90 (M), 46★ (M), 47 (M), 77 (M), 39★ (M), 40 (M), 17 (M), 79★ (M), 131 (M), 51★ (H) |
| 15 | **Greedy + Intervals** | 455 (E), 55★ (M), 45 (M), 134 (M), 763 (M), 846 (M), 678 (M), 57★ (M), 435★ (M), 452 (M), 135 (H) |

🏁 **Promotion review** (checkpoint, no level change)

### Phase 4: Graphs (Weeks 16–19) · 🔧 SDE-2
| Week | Topic | Problems |
|---|---|---|
| 16 | **Graph basics**: adjacency lists, BFS/DFS, grids as graphs | 1971 (E), 733 (E), 200★ (M), 695 (M), 841 (M), 133★ (M), 547 (M), 130 (M) |
| 17 | **Multi-source BFS + Topological Sort** | 994★ (M), 1091 (M), 417★ (M), 785 (M), 207★ (M), 210★ (M), 127★ (H) |
| 18 | **Union-Find** (path compression + union by rank) | 684★ (M), 721 (M), 990 (M), plus 547 re-solved with DSU |
| 19 | **Shortest Paths + MST**: Dijkstra, Bellman-Ford idea, Prim/Kruskal | 743★ (M), 787★ (M), 1584★ (M), 778 (H), 332 (H) |

🏁 **Promotion review → Senior SDE**

### Phase 5: Dynamic Programming (Weeks 20–25) · 🧠 Senior SDE
The big one. Method: **recursion → memoization → tabulation → space-optimised**, done in that order for every problem in the first two weeks.

| Week | Topic | Problems |
|---|---|---|
| 20 | **1D DP** | 509 (E), 70★ (E), 746 (E), 198★ (M), 213 (M), 91 (M), 343 (M) |
| 21 | **1D DP II** | 322★ (M), 139★ (M), 300★ LIS (M), 152 (M), 5 (M), 647 (M) |
| 22 | **2D / Grid DP** | 62★ (M), 63 (M), 64 (M), 120 (M), 221 (M), 329 (H) |
| 23 | **Knapsack family** | 416★ (M), 494 (M), 518★ (M), plus re-solving 322 framed as unbounded knapsack |
| 24 | **String DP** | 1143★ LCS (M), 72★ Edit Distance (M), 97 (M), 115 (H), 10 (H) |
| 25 | **State-machine / Tree / Interval DP** | 309 (M), 337 (M), 1235 (H), 312 (H) |

🏁 **Promotion review → Staff Engineer**

### Phase 6: Advanced Topics (Weeks 26–29) · 🏛️ Staff
| Week | Topic | Problems |
|---|---|---|
| 26 | **Tries + Bit Manipulation** | 208★ (M), 211 (M), 212 (H), 136★ (E), 191 (E), 338 (E), 268 (E), 190 (E), 371 (M) |
| 27 | **Monotonic Deque + Advanced Windows** | 239★ (H), 4 (H), re-solve 76 and 84 cold |
| 28 | **Segment Tree / Fenwick Tree + String Matching (KMP idea)** | 307 (M), 315 (H), 28 (E, solved with KMP) |
| 29 | **Hard-problem week**: mixed hards across all patterns, timed | |

### Phase 7: Interview Mode (Week 30 onward)
- **Mock interviews** twice a week, with me as the interviewer (Google/Amazon style): clarifying questions, think aloud, follow-ups like "now handle a stream" or "now reduce the memory".
- **LeetCode weekly contests** (start around Week 12 just to participate, then take them seriously from here).
- **Company-tagged practice** for whichever companies you're interviewing at.
- **Mixed random sets**, where the topic isn't revealed, because in a real interview nobody tells you it's a sliding window problem.
- Behavioural and "explain your project" prep can be added alongside.

**Rough total:** ~300 problems, about 60% medium, 15% hard.

---

## 4. PyCharm setup

### Structure
```
Data Structures And Algorithms/
├── ROADMAP.md                 ← this file
├── dsa.py                     ← tracker CLI: XP, streak, re-solve queue
├── progress/
│   ├── log.csv                ← every problem: date, id, difficulty, hints used, time
│   └── journal.md             ← one line a day: what tricked you
├── templates/                 ← patterns YOU wrote: binary_search.py, bfs.py, dsu.py…
├── notes/                     ← short concept notes, one per topic
└── phase1_foundations/
    ├── week02_arrays/
    │   ├── lc0121_best_time_to_buy_sell_stock.py
    │   └── ...
```

### Every solution file looks like this
```python
"""
LC 121 · Best Time to Buy and Sell Stock · Easy
Pattern: one-pass, track running minimum
Approach: ...
Time: O(n)   Space: O(1)
Hints used: 0   Time taken: 14 min
"""


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        ...


if __name__ == "__main__":
    s = Solution()
    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0
    assert s.maxProfit([1]) == 0            # edge: single day
    print("all tests passed ✅")
```
Write and test locally first, then paste into LeetCode to submit. Writing your own test cases is itself an interview skill.

### PyCharm settings that matter
1. **Interpreter:** project venv on Python 3.14.
2. **File template:** *Settings → Editor → File and Code Templates* → a "LeetCode Problem" template with the skeleton above, so each new problem takes one click.
3. **The debugger is your best teacher.** Breakpoints plus *Step Into* to watch recursion and pointers move. We'll use it heavily in Weeks 6 and 11.
4. **Turn AI and full-line code completion OFF for this project.** Interviews have no autocomplete, so neither does practice. Basic syntax completion is fine.
5. **Git:** commit every day. Your GitHub contribution graph becomes a visible streak and a portfolio signal.

---

## 5. Supplementary resources (optional)
My lessons are the primary track. If you want a second explanation:
- **NeetCode** (YouTube / neetcode.io): clean pattern-based explanations. Use it *after* attempting a problem, never before.
- **Abdul Bari** (YouTube): classic algorithms (sorting, graphs, DP) explained from first principles.
- **Striver's A2Z DSA sheet** (takeuforward): extra practice if you want more problems on a topic.
