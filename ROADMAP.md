# DSA Roadmap: Zero → Interview Ready

**Learner:** Harsh · **Language:** Python 3.14 · **Editor:** PyCharm · **Started:** 2026-10-04
**Pace:** ~2 h/day, 6 days/week · **Length:** set by your pace. The dashboard's ROADMAP section shows live estimates (next unit, phase end, the 🎯 goal units) from your last 7 days

**Scope:** DSA only. The target is applied engineering roles, where the DSA round is the gate; ML theory, system
design and behavioural prep are outside this folder.

**The goal (🎯 Interview-ready).** On unseen problems, you can:
- Solve any **medium** in 25–35 minutes while talking through your approach, the way you would with an interviewer.
- State the time and space complexity of any solution without hesitating.
- That is the DSA bar at most companies (the aim is ~90%). It's proved by the final readiness review, not by a count.

**Optional stretch (🏆 Top-tier ready):** hards in the core patterns (sliding window, DP, graphs, heaps) roughly
40–50% of the time, for the small set of companies whose loops go beyond mediums.

> Honest calibration: the timeline is an estimate, not a promise. This plan lists 191 problems to the goal; with reinforcement problems, re-solves and Interview Mode's mixed sets, expect roughly 250 well-reviewed problems in total. Solving 600 problems carelessly gets you there slower than solving 250 carefully. The plan adjusts to your actual pace.

### Units, not calendar weeks (2026-10-06)
The curriculum below is split into **units** (numbered like the old weeks). A unit ends when its problem list is done, whether that takes 3 days or 9. `python dsa.py next` sets up the next problem in the list, and the next unit starts by itself when the current one is finished.
- **Daily target:** at least 2 new problems plus all due re-solves. Doing more pulls the estimated dates forward. It does **not** bank days off, because the streak is about showing up.
- **Re-solve cap:** if 4 or more re-solves are due at the start of a day, that day's target drops to 1 new problem, so the backlog can't snowball.
- **Quality gate:** if a unit averages 3 or more hints per problem, it isn't done until 2 extra reinforcement problems (same pattern) are solved.
- A problem belongs to the first unit that lists it. Later mentions (206 in Unit 8, 509 in Unit 20, 547 in Unit 18) are re-solves.

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
| 6. **Re-solve** | The same problems come back on Day 3, 7 and 21 (spaced repetition). If you saw the solution, it also comes back the next day | You |

### The hint ladder
Hints come in this order:
1. **Nudge**: "What do you need to look up quickly here?"
2. **Pattern**: "This is a sliding window problem. What makes the window invalid?"
3. **Skeleton**: the outline of the approach in plain English, without code.
4. **Walkthrough**: only after a real attempt. Afterwards you re-code it yourself the next day.

**Timebox (agreed 2026-10-06):** the clock counts work minutes from "start" (pomodoro breaks excluded). You never decide when to give up; the timer calls it, with a desktop alert, and I act on it straight away without asking:

| Difficulty | Hint arrives at | Full solution arrives at |
|---|---|---|
| Easy | 15 min | 30 min |
| Medium | 25 min | 45 min |
| Hard | 40 min | 60 min |

After a viewed solution you type it from memory, it is logged with `--viewed`, and it comes back for a cold re-solve the next day.

### The 6-step problem framework (practise it from day 1, because interviews grade it)
1. **Understand.** Restate the problem, ask about input size, edge cases, duplicates and negatives.
2. **Examples.** Work through 2–3 by hand, including an edge case.
3. **Brute force.** State it and its complexity, even if it's slow.
4. **Optimise.** Find what is repeated or wasted, then pick a pattern.
5. **Code.** Write clean code with meaningful names.
6. **Test.** Dry-run your own examples and edge cases, then give the final complexity.

---

## 2. Consistency system (fun, but professional)

### Levels (earned by promotion reviews, not XP)
Each level is a claim about what you could pass in a real hiring process, so it can only be earned by passing a
**promotion review** (3 unseen problems, 90 minutes, me as the interviewer, pass 2 of 3). XP is the score that
rewards showing up. It never changes your level, because grinding easy problems can't prove an interview skill.

| Level | Earned by passing | What you can do | What it means for hiring | Not there yet |
|---|---|---|---|---|
| 🌱 Beginner | (start) | Learning arrays, strings and Big-O | Not interview-ready anywhere yet. Normal at this stage | Everything below |
| 🧱 Foundations | Phase 1 review | Easys reliably; mediums on arrays, hashing, two pointers and sliding window, slowly | Easy coding rounds and simple online assessments (array/string questions) on a good day | Recursion, binary search, linked lists, stacks, trees, graphs, DP |
| ⚙️ Core | Phase 2 review | Recursion, binary search, linked lists, stacks; standard mediums on familiar patterns, slowly | Easier online assessments and service-company coding rounds within reach | Trees, graphs and DP, which product companies ask constantly |
| 🌲 OA-ready | Phase 3 + 4 reviews | Trees, heaps, backtracking, graphs | Product-company online assessments (2-3 problems, 60-90 min) passable more often than not | DP, and speed on unseen mediums |
| 🎯 **Interview-ready (the goal)** | Phase 5 review + final readiness review | Unseen mediums in 25-35 min across all core patterns including DP, explained out loud | **The DSA round at most companies (aim: ~90%).** Apply with confidence | Hards, which only the toughest loops need |
| 🏆 Top-tier ready (optional) | Phase 7 review + a hard-problem mock | Everything above, plus hards in the core patterns ~40-50% of the time | The DSA rounds at the toughest top-tier companies | Nothing left in DSA |

**Final readiness review (the gate to the goal):** two back-to-back mock interviews on unseen mediums from mixed
patterns, each solved in 35 minutes or less while explaining out loud, with correct complexity. Logged as a
promotion review only if both are passed.

> Honest calibration: the hiring column is my judgement from common interview formats and public interview reports,
> not measured data. "~90% of companies" is the aim, not a statistic, and bars vary between companies.

**XP:** Easy 10 · Medium 25 · Hard 60 · Solved with no hints +5 · Spaced re-solve 5 · Friday Gauntlet / weekly mock 40 · Promotion review passed 100

### Promotion reviews (boss fights)
At the end of each phase you get a **timed assessment**: 3 unseen problems in 90 minutes, with me as the interviewer. You don't see the problems in advance. Pass 2 of 3 to get promoted. Fail, and you get a targeted 3-day revision sprint, then a retry.

### Streak rules
- **Minimum viable day:** on a bad day, **one re-solve or one easy problem (about 20 minutes)** keeps the streak alive. Showing up counts for more than the score.
- **Never miss twice.** Missing one day is life. Missing two days in a row is the start of quitting.
- **Friday Gauntlet:** 2 cold re-solves of the week's problems, no hints, solution mark only. Clearing it is logged with `dsa.py event mock` (+40 XP). The dashboard shows it Friday to Sunday until it's done.
- **Sunday** is pattern-card review, or rest if you need it.
- **Tests gate:** `dsa.py log` refuses a problem until the file has at least 3 tests you wrote yourself. Writing test cases is graded in interviews.

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

### Phase 0: Setup & Toolkit (Unit 1)
**Goal:** a working environment, plus the Python and Big-O you need before anything else.
- PyCharm project, venv, pytest, git, folder structure (see §4)
- Python for DSA: lists, slicing, `dict`, `set`, `collections` (`Counter`, `defaultdict`, `deque`), `heapq`, `sorted` with `key=`, list comprehensions, classes for nodes
- **Big-O**: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ). How to read code and state its complexity. Space complexity. Why `x in list` is O(n) and `x in set` is O(1)
- Practice: 15 short "what's the complexity?" snippets I'll give you, plus 1 ★Two Sum (E), 217 Contains Duplicate (E), 344 Reverse String (E)

### Phase 1: Foundations (Units 2–5) · 🌱 Beginner
| Unit | Topic | Problems |
|---|---|---|
| 2 | **Arrays & Strings** | 26 (E), 27 (E), 88 (E), 121★ (E), 169 (E), 14 (E), 125 (E), 387 (E), 189 (M), 238★ (M) |
| 3 | **Hashing** | 242★ (E), 383 (E), 205 (E), 290 (E), 49★ (M), 347★ (M), 128★ (M), 36 (M), 560★ (M) |
| 4 | **Two Pointers** | 283 (E), 977 (E), 167★ (M), 15★ (M), 11★ (M), 75 (M), 42★ (H) |
| 5 | **Sliding Window + Prefix Sum** | 643 (E), 724 (E), 303 (E), 3★ (M), 209 (M), 1004 (M), 424★ (M), 567★ (M), 525 (M), 974 (M), 76★ (H) |

🏁 **Promotion review → 🧱 Foundations**

### Phase 2: Core Techniques (Units 6–10) · 🧱 Foundations
| Unit | Topic | Problems |
|---|---|---|
| 6 | **Recursion** (call stack, base case, trust the recursion), trained with the debugger | 509 (E), 231 (E), 50 (M), recursive 206 (E), 21 (E), and I'll give you print-all-subsets |
| 7 | **Sorting + Binary Search** (merge sort and quicksort written from scratch) | 912 (M), 704★ (E), 35 (E), 278 (E), 69 (E), 74 (M), 34★ (M), 33★ (M), 153★ (M), 162 (M) |
| 8 | **Binary Search on Answer + Linked Lists** | 875★ (M), 1011 (M), 410 (H), 206★ (E), 876 (E), 141★ (E), 160 (E), 234 (E), 19★ (M), 142 (M), 143 (M), 2 (M) |
| 9 | **Stacks, Queues, Monotonic Stack** | 20★ (E), 232 (E), 496 (E), 155★ (M), 150 (M), 394 (M), 739★ (M), 503 (M), 901 (M), 853 (M), 84★ (H) |
| 10 | **Consolidation**: 138 (M), 146★ LRU Cache (M), 215 (M), 56★ (M), 179 (M), 23 (H), 25 (H), plus re-solves of weak spots | |

🏁 **Promotion review → ⚙️ Core**

### Phase 3: Trees, Heaps, Backtracking (Units 11–15) · ⚙️ Core
| Unit | Topic | Problems |
|---|---|---|
| 11 | **Binary Trees I**: traversals (recursive and iterative), DFS vs BFS | 94, 144, 145 (E), 104★ (E), 226★ (E), 100 (E), 101 (E), 112 (E), 102★ (M), 103 (M), 199★ (M) |
| 12 | **Binary Trees II**: postorder thinking ("what does my child return?") | 543★ (E), 110 (E), 572 (E), 113 (M), 1448 (M), 236★ (M), 105★ (M), 124★ (H), 297 (H) |
| 13 | **BST + Heaps / Priority Queue** | 700 (E), 701 (M), 235 (M), 98★ (M), 230★ (M), 450 (M), 703 (E), 1046 (E), 973★ (M), 621★ (M), 355 (M), 295★ (H) |
| 14 | **Backtracking** (choose → explore → un-choose) | 78★ (M), 90 (M), 46★ (M), 47 (M), 77 (M), 39★ (M), 40 (M), 17 (M), 79★ (M), 131 (M), 51★ (H) |
| 15 | **Greedy + Intervals** | 455 (E), 55★ (M), 45 (M), 134 (M), 763 (M), 846 (M), 678 (M), 57★ (M), 435★ (M), 452 (M), 135 (H) |

🏁 **Promotion review** (checkpoint, no level change)

### Phase 4: Graphs (Units 16–19) · ⚙️ Core
| Unit | Topic | Problems |
|---|---|---|
| 16 | **Graph basics**: adjacency lists, BFS/DFS, grids as graphs | 1971 (E), 733 (E), 200★ (M), 695 (M), 841 (M), 133★ (M), 547 (M), 130 (M) |
| 17 | **Multi-source BFS + Topological Sort** | 994★ (M), 1091 (M), 417★ (M), 785 (M), 207★ (M), 210★ (M), 127★ (H) |
| 18 | **Union-Find** (path compression + union by rank) | 684★ (M), 721 (M), 990 (M), plus 547 re-solved with DSU |
| 19 | **Shortest Paths + MST**: Dijkstra, Bellman-Ford idea, Prim/Kruskal | 743★ (M), 787★ (M), 1584★ (M), 778 (H), 332 (H) |

🏁 **Promotion review → 🌲 OA-ready** (needs the Phase 3 review too)

### Phase 5: Dynamic Programming (Units 20–25) · 🌲 OA-ready
The big one. Method: **recursion → memoization → tabulation → space-optimised**, done in that order for every problem in the first two units.

| Unit | Topic | Problems |
|---|---|---|
| 20 | **1D DP** | 509 (E), 70★ (E), 746 (E), 198★ (M), 213 (M), 91 (M), 343 (M) |
| 21 | **1D DP II** | 322★ (M), 139★ (M), 300★ LIS (M), 152 (M), 5 (M), 647 (M) |
| 22 | **2D / Grid DP** | 62★ (M), 63 (M), 64 (M), 120 (M), 221 (M), 329 (H) |
| 23 | **Knapsack family** | 416★ (M), 494 (M), 518★ (M), plus re-solving 322 framed as unbounded knapsack |
| 24 | **String DP** | 1143★ LCS (M), 72★ Edit Distance (M), 97 (M), 115 (H), 10 (H) |
| 25 | **State-machine / Tree / Interval DP** | 309 (M), 337 (M), 1235 (H), 312 (H) |

🏁 **Promotion review** (counts towards 🎯 Interview-ready, with the final readiness review)

### Phase 6: Interview Mode (after Unit 25) · 🌲 OA-ready
Runs until the final readiness review is passed. Units 26+ wait until then.
- **Final readiness review → 🎯 Interview-ready (the goal)**: two back-to-back unseen mediums, mixed patterns, 35 minutes each, explained out loud. Retake after a revision sprint if either is failed.
- **Mock interviews** twice a week, with me as the interviewer: clarifying questions, think aloud, follow-ups like "now handle a stream" or "now reduce the memory".
- **LeetCode weekly contests** (start around Unit 12 just to participate, then take them seriously from here).
- **Company-tagged practice** for whichever companies you're interviewing at.
- **Mixed random sets**, where the topic isn't revealed, because in a real interview nobody tells you it's a sliding window problem.

### Phase 7: Advanced Topics, optional stretch (Units 26–29) · 🎯 Interview-ready
Only after the goal is reached. These topics rarely come up outside the toughest loops.
| Unit | Topic | Problems |
|---|---|---|
| 26 | **Tries + Bit Manipulation** | 208★ (M), 211 (M), 212 (H), 136★ (E), 191 (E), 338 (E), 268 (E), 190 (E), 371 (M) |
| 27 | **Monotonic Deque + Advanced Windows** | 239★ (H), 4 (H), re-solve 76 and 84 cold |
| 28 | **Segment Tree / Fenwick Tree + String Matching (KMP idea)** | 307 (M), 315 (H), 28 (E, solved with KMP) |
| 29 | **Hard-problem week**: mixed hards across all patterns, timed | |

🏁 **Promotion review + a hard-problem mock → 🏆 Top-tier ready**

**Rough total:** 191 listed problems to the goal (Phases 0–5: 54 E · 118 M · 19 H), plus reinforcement problems and the mixed sets and mocks of Interview Mode. The optional stretch adds 14 (6 E · 4 M · 4 H) and a hard-problem week.

---

## 4. PyCharm setup

### Structure
```
Data Structures And Algorithms/
├── ROADMAP.md                 ← this file
├── dsa.py                     ← tracker CLI: XP, streak, re-solve queue
├── patterns/                  ← pattern cards: spot it, core move, MY traps (updated after every problem)
├── progress/
│   ├── log.csv                ← every problem: date, id, difficulty, hints used, time
│   └── journal.md             ← one line a day: what tricked you
├── templates/                 ← patterns YOU wrote: binary_search.py, bfs.py, dsu.py…
├── notes/                     ← short concept notes, one per topic
└── phase1_foundations/
    ├── week02_arrays_strings/
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
3. **The debugger is your best teacher.** Breakpoints plus *Step Into* to watch recursion and pointers move. We'll use it heavily in Units 6 and 11.
4. **Turn AI and full-line code completion OFF for this project.** Interviews have no autocomplete, so neither does practice. Basic syntax completion is fine.
5. **Git:** commit every day. Your GitHub contribution graph becomes a visible streak and a portfolio signal.

---

## 5. Supplementary resources (optional)
My lessons are the primary track. If you want a second explanation:
- **NeetCode** (YouTube / neetcode.io): clean pattern-based explanations. Use it *after* attempting a problem, never before.
- **Abdul Bari** (YouTube): classic algorithms (sorting, graphs, DP) explained from first principles.
- **Striver's A2Z DSA sheet** (takeuforward): extra practice if you want more problems on a topic.
