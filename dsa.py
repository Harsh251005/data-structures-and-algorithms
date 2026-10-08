#!/usr/bin/env python3
"""
DSA Forge: your daily DSA progress tracker.

    python dsa.py                                   dashboard
    python dsa.py log 121 E --mins 14 --hints 0     log a solved problem
    python dsa.py log 121 E --hints 3 --viewed      solution viewed: re-solve tomorrow, then +3/+7/+21d
    python dsa.py resolve 121                       log a spaced re-solve (resolve/ file needs 3 tests)
    python dsa.py event mock | promotion            log a mock / passed promotion review
    python dsa.py next                              set up the next problem of the current unit
    python dsa.py new 121 "Best Time to Buy and Sell Stock" E
                                                    create a solution file (in the unit that lists it)
    python dsa.py add 1752 "Check if Array Is Sorted and Rotated" E
                                                    add a reinforcement problem to the current unit
    python dsa.py journal "forgot the empty-array case"
    python dsa.py unit [next]                       show the current unit (it advances by itself)
    python dsa.py target [n]                        show / set the daily target (default 2 new + due re-solves;
                                                    1 new on days that start with 4+ re-solves due)
    python dsa.py check 121                         count your own tests (log and resolve need 3;
                                                    checks resolve/ first when a re-solve is open)
    python dsa.py undo                              remove the last log entry

Standard library only. Data lives in progress/ (log.csv, state.json, journal.md).
Set NO_COLOR=1 to disable colours.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(os.environ.get("DSA_HOME", Path(__file__).resolve().parent))
PROGRESS = ROOT / "progress"
LOG_FILE = PROGRESS / "log.csv"
STATE_FILE = PROGRESS / "state.json"
JOURNAL_FILE = PROGRESS / "journal.md"
TRACKER_FILE = PROGRESS / "tracker.csv"  # feeds the Google Sheet via IMPORTDATA
REPO_URL = "https://github.com/Harsh251005/data-structures-and-algorithms"
FIELDS = ["date", "kind", "pid", "name", "diff", "hints", "mins", "xp", "note"]

# ── Rules (mirrors ROADMAP.md §2) ─────────────────────────────────────────────
XP_SOLVE = {"E": 10, "M": 25, "H": 60}
XP_NO_HINTS = 5
XP_RESOLVE = 5
XP_EVENT = {"mock": 40, "promotion": 100}
RESOLVE_AFTER_DAYS = (3, 7, 21)
VIEWED_RESOLVE_AFTER_DAYS = (1, 3, 7, 21)  # solution was viewed: re-solve cold the next day first
VIEWED_TAG = "[viewed]"
DEFAULT_DAILY_TARGET = 2  # new problems per day, plus every re-solve that's due
MIN_OWN_TESTS = 3  # `log` refuses until the solution file has this many tests not marked "added in review"

# Levels are earned ONLY by passing promotion reviews (3 unseen problems, 90 min, pass 2 of 3), never by XP:
# grinding easy problems must not be able to fake a hiring-level claim. XP is the score, not the rank.
# The hiring calibration is judgement from common interview formats, not data; it varies by company.
LEVELS = [  # (promotion reviews passed, icon, title, what it means in hiring terms, gate to the next level)
    (0, "🌱", "Beginner", "learning the basics; not interview-ready anywhere yet",
     "Phase 1 review: arrays, hashing, two pointers, sliding window"),
    (1, "🧱", "Foundations", "easy rounds and simple online assessments (array/string questions) on a good day",
     "Phase 2 review: recursion, binary search, linked lists, stacks"),
    (2, "⚙️", "Core", "easier online assessments and service-company coding rounds within reach; product companies not yet",
     "Phase 3 + 4 reviews: trees, heaps, backtracking, graphs"),
    (4, "🌲", "OA-ready", "most online assessments passable more often than not; no DP yet",
     "Phase 5 review (DP) + final readiness review (2 back-to-back unseen mediums)"),
    (6, "🎯", "Interview-ready", "THE GOAL: unseen mediums in 25-35 min, the DSA round at most companies",
     "optional: Phase 7 review + a hard-problem mock"),
    (8, "🏆", "Top-tier ready", "optional stretch: hards in core patterns ~40-50%, the toughest DSA loops", ""),
]

STREAK_MILESTONES = {3, 7, 14, 21, 30, 50, 75, 100, 150, 200, 365}

GOAL_LAST_UNIT = 25  # DP ends here; Interview Mode follows, Units 26+ are the optional stretch

RESOLVE_CAP = 4  # this many re-solves due at the start of a day drops that day's new target to 1
QUALITY_HINTS = 3.0  # a unit averaging this many hints needs reinforcement problems before it counts as done
REINFORCE_COUNT = 2  # how many reinforcement problems (`dsa.py add`) clear the quality flag
UNLISTED_UNIT_SIZE = 7  # ETA guess for a unit without a fixed list


def _p(spec: str) -> list[tuple[str, str, str]]:
    """'1 E Two Sum; 217 E Contains Duplicate' -> [(pid, diff, name), ...]"""
    return [tuple(item.strip().split(" ", 2)) for item in spec.split(";") if item.strip()]


# Units replace calendar weeks: a unit is done when its problems are, however many days that takes.
# A pid belongs to the first unit that lists it; later mentions in ROADMAP.md are re-solves.
UNITS = {  # unit: (folder, topic, problems)
    1: ("phase0_setup/week01_toolkit", "Setup · Python toolkit · Big-O",
        _p("1 E Two Sum; 217 E Contains Duplicate; 344 E Reverse String")),
    2: ("phase1_foundations/week02_arrays_strings", "Arrays & Strings",
        _p("26 E Remove Duplicates from Sorted Array; 27 E Remove Element; 88 E Merge Sorted Array;"
           "121 E Best Time to Buy and Sell Stock; 169 E Majority Element; 14 E Longest Common Prefix;"
           "125 E Valid Palindrome; 387 E First Unique Character in a String; 189 M Rotate Array;"
           "238 M Product of Array Except Self")),
    3: ("phase1_foundations/week03_hashing", "Hashing",
        _p("242 E Valid Anagram; 383 E Ransom Note; 205 E Isomorphic Strings; 290 E Word Pattern;"
           "49 M Group Anagrams; 347 M Top K Frequent Elements; 128 M Longest Consecutive Sequence;"
           "36 M Valid Sudoku; 560 M Subarray Sum Equals K")),
    4: ("phase1_foundations/week04_two_pointers", "Two Pointers",
        _p("283 E Move Zeroes; 977 E Squares of a Sorted Array; 167 M Two Sum II - Input Array Is Sorted;"
           "15 M 3Sum; 11 M Container With Most Water; 75 M Sort Colors; 42 H Trapping Rain Water")),
    5: ("phase1_foundations/week05_sliding_window_prefix", "Sliding Window + Prefix Sum",
        _p("643 E Maximum Average Subarray I; 724 E Find Pivot Index; 303 E Range Sum Query - Immutable;"
           "3 M Longest Substring Without Repeating Characters; 209 M Minimum Size Subarray Sum;"
           "1004 M Max Consecutive Ones III; 424 M Longest Repeating Character Replacement;"
           "567 M Permutation in String; 525 M Contiguous Array; 974 M Subarray Sums Divisible by K;"
           "76 H Minimum Window Substring")),
    6: ("phase2_core/week06_recursion", "Recursion",
        _p("509 E Fibonacci Number; 231 E Power of Two; 50 M Pow(x, n); 206 E Reverse Linked List;"
           "21 E Merge Two Sorted Lists")),
    7: ("phase2_core/week07_sorting_binary_search", "Sorting + Binary Search",
        _p("912 M Sort an Array; 704 E Binary Search; 35 E Search Insert Position; 278 E First Bad Version;"
           "69 E Sqrt(x); 74 M Search a 2D Matrix; 34 M Find First and Last Position of Element in Sorted Array;"
           "33 M Search in Rotated Sorted Array; 153 M Find Minimum in Rotated Sorted Array; 162 M Find Peak Element")),
    8: ("phase2_core/week08_bs_answer_linked_lists", "Binary Search on Answer + Linked Lists",
        _p("875 M Koko Eating Bananas; 1011 M Capacity To Ship Packages Within D Days; 410 H Split Array Largest Sum;"
           "206 E Reverse Linked List; 876 E Middle of the Linked List; 141 E Linked List Cycle;"
           "160 E Intersection of Two Linked Lists; 234 E Palindrome Linked List; 19 M Remove Nth Node From End of List;"
           "142 M Linked List Cycle II; 143 M Reorder List; 2 M Add Two Numbers")),
    9: ("phase2_core/week09_stacks_queues", "Stacks, Queues, Monotonic Stack",
        _p("20 E Valid Parentheses; 232 E Implement Queue using Stacks; 496 E Next Greater Element I; 155 M Min Stack;"
           "150 M Evaluate Reverse Polish Notation; 394 M Decode String; 739 M Daily Temperatures;"
           "503 M Next Greater Element II; 901 M Online Stock Span; 853 M Car Fleet; 84 H Largest Rectangle in Histogram")),
    10: ("phase2_core/week10_consolidation", "Consolidation",
         _p("138 M Copy List with Random Pointer; 146 M LRU Cache; 215 M Kth Largest Element in an Array;"
            "56 M Merge Intervals; 179 M Largest Number; 23 H Merge k Sorted Lists; 25 H Reverse Nodes in k-Group")),
    11: ("phase3_trees/week11_binary_trees_1", "Binary Trees I",
         _p("94 E Binary Tree Inorder Traversal; 144 E Binary Tree Preorder Traversal; 145 E Binary Tree Postorder Traversal;"
            "104 E Maximum Depth of Binary Tree; 226 E Invert Binary Tree; 100 E Same Tree; 101 E Symmetric Tree;"
            "112 E Path Sum; 102 M Binary Tree Level Order Traversal; 103 M Binary Tree Zigzag Level Order Traversal;"
            "199 M Binary Tree Right Side View")),
    12: ("phase3_trees/week12_binary_trees_2", "Binary Trees II",
         _p("543 E Diameter of Binary Tree; 110 E Balanced Binary Tree; 572 E Subtree of Another Tree; 113 M Path Sum II;"
            "1448 M Count Good Nodes in Binary Tree; 236 M Lowest Common Ancestor of a Binary Tree;"
            "105 M Construct Binary Tree from Preorder and Inorder Traversal; 124 H Binary Tree Maximum Path Sum;"
            "297 H Serialize and Deserialize Binary Tree")),
    13: ("phase3_trees/week13_bst_heaps", "BST + Heaps",
         _p("700 E Search in a Binary Search Tree; 701 M Insert into a Binary Search Tree;"
            "235 M Lowest Common Ancestor of a Binary Search Tree; 98 M Validate Binary Search Tree;"
            "230 M Kth Smallest Element in a BST; 450 M Delete Node in a BST; 703 E Kth Largest Element in a Stream;"
            "1046 E Last Stone Weight; 973 M K Closest Points to Origin; 621 M Task Scheduler; 355 M Design Twitter;"
            "295 H Find Median from Data Stream")),
    14: ("phase3_trees/week14_backtracking", "Backtracking",
         _p("78 M Subsets; 90 M Subsets II; 46 M Permutations; 47 M Permutations II; 77 M Combinations;"
            "39 M Combination Sum; 40 M Combination Sum II; 17 M Letter Combinations of a Phone Number;"
            "79 M Word Search; 131 M Palindrome Partitioning; 51 H N-Queens")),
    15: ("phase3_trees/week15_greedy_intervals", "Greedy + Intervals",
         _p("455 E Assign Cookies; 55 M Jump Game; 45 M Jump Game II; 134 M Gas Station; 763 M Partition Labels;"
            "846 M Hand of Straights; 678 M Valid Parenthesis String; 57 M Insert Interval; 435 M Non-overlapping Intervals;"
            "452 M Minimum Number of Arrows to Burst Balloons; 135 H Candy")),
    16: ("phase4_graphs/week16_graph_basics", "Graph Basics",
         _p("1971 E Find if Path Exists in Graph; 733 E Flood Fill; 200 M Number of Islands; 695 M Max Area of Island;"
            "841 M Keys and Rooms; 133 M Clone Graph; 547 M Number of Provinces; 130 M Surrounded Regions")),
    17: ("phase4_graphs/week17_bfs_toposort", "Multi-source BFS + Topological Sort",
         _p("994 M Rotting Oranges; 1091 M Shortest Path in Binary Matrix; 417 M Pacific Atlantic Water Flow;"
            "785 M Is Graph Bipartite?; 207 M Course Schedule; 210 M Course Schedule II; 127 H Word Ladder")),
    18: ("phase4_graphs/week18_union_find", "Union-Find",
         _p("684 M Redundant Connection; 721 M Accounts Merge; 990 M Satisfiability of Equality Equations")),
    19: ("phase4_graphs/week19_shortest_paths_mst", "Shortest Paths + MST",
         _p("743 M Network Delay Time; 787 M Cheapest Flights Within K Stops; 1584 M Min Cost to Connect All Points;"
            "778 H Swim in Rising Water; 332 H Reconstruct Itinerary")),
    20: ("phase5_dp/week20_dp_1d", "1D DP",
         _p("70 E Climbing Stairs; 746 E Min Cost Climbing Stairs; 198 M House Robber; 213 M House Robber II;"
            "91 M Decode Ways; 343 M Integer Break")),
    21: ("phase5_dp/week21_dp_1d_2", "1D DP II",
         _p("322 M Coin Change; 139 M Word Break; 300 M Longest Increasing Subsequence; 152 M Maximum Product Subarray;"
            "5 M Longest Palindromic Substring; 647 M Palindromic Substrings")),
    22: ("phase5_dp/week22_dp_grid", "2D / Grid DP",
         _p("62 M Unique Paths; 63 M Unique Paths II; 64 M Minimum Path Sum; 120 M Triangle; 221 M Maximal Square;"
            "329 H Longest Increasing Path in a Matrix")),
    23: ("phase5_dp/week23_knapsack", "Knapsack Family",
         _p("416 M Partition Equal Subset Sum; 494 M Target Sum; 518 M Coin Change II")),
    24: ("phase5_dp/week24_string_dp", "String DP",
         _p("1143 M Longest Common Subsequence; 72 M Edit Distance; 97 M Interleaving String; 115 H Distinct Subsequences;"
            "10 H Regular Expression Matching")),
    25: ("phase5_dp/week25_advanced_dp", "State-machine / Tree / Interval DP",
         _p("309 M Best Time to Buy and Sell Stock with Cooldown; 337 M House Robber III;"
            "1235 H Maximum Profit in Job Scheduling; 312 H Burst Balloons")),
    26: ("phase6_advanced/week26_tries_bits", "Tries + Bit Manipulation",
         _p("208 M Implement Trie (Prefix Tree); 211 M Design Add and Search Words Data Structure; 212 H Word Search II;"
            "136 E Single Number; 191 E Number of 1 Bits; 338 E Counting Bits; 268 E Missing Number; 190 E Reverse Bits;"
            "371 M Sum of Two Integers")),
    27: ("phase6_advanced/week27_deque_windows", "Monotonic Deque + Advanced Windows",
         _p("239 H Sliding Window Maximum; 4 H Median of Two Sorted Arrays")),
    28: ("phase6_advanced/week28_segtree_strings", "Segment / Fenwick Tree + KMP",
         _p("307 M Range Sum Query - Mutable; 315 H Count of Smaller Numbers After Self;"
            "28 E Find the Index of the First Occurrence in a String")),
    29: ("phase6_advanced/week29_hard_week", "Hard-problem Week", []),  # mixed hards, picked when we get there
}
_seen: set[str] = set()
for _u, (_f, _t, _probs) in UNITS.items():  # keep each pid in its first unit only
    UNITS[_u] = (_f, _t, [p for p in _probs if p[0] not in _seen])
    _seen.update(p[0] for p in _probs)
INTERVIEW_MODE = ("phase7_interview", "Interview Mode")

TIPS = [
    "Brute force first, out loud. Interviewers grade the path, not just the destination.",
    "If you need fast lookup, reach for a hash map before anything clever.",
    "Sorted input is a hint: think two pointers or binary search.",
    "'Contiguous subarray' usually means sliding window or prefix sums.",
    "The timebox calls it: Easy hint at 15 min, solution at 30. Struggling past that isn't learning.",
    "Every recursive function is a promise: trust it for n-1, handle n.",
    "Write the edge cases before the code: empty, one element, all same, negatives.",
    "Name variables for what they mean: `left`, `window_sum`, not `i2`, `tmp`.",
    "State complexity before the interviewer asks. It signals seniority.",
    "A problem you re-solve cold in a week is worth five you skimmed once.",
    "'Top k' or 'k-th' should make you think heap.",
    "Shortest path in an unweighted graph is BFS. Weighted means Dijkstra.",
    "DP is recursion plus a cache. Find the recurrence first, the table second.",
    "Consistency beats intensity. Twenty minutes today beats three hours someday.",
    "Dry-run your code on a tiny input before you hit submit. Every time.",
    "Every hard problem is a medium problem with one extra insight.",
    "When a solution feels messy, the pattern is usually wrong, not the code.",
]

# ── Terminal styling ──────────────────────────────────────────────────────────
USE_COLOR = "NO_COLOR" not in os.environ
if os.name == "nt":
    os.system("")  # enable ANSI escape handling on Windows terminals


def c(text: str, *codes: str) -> str:
    if not USE_COLOR or not codes:
        return str(text)
    return "".join(f"\033[{code}m" for code in codes) + str(text) + "\033[0m"


BOLD, DIM = "1", "2"
SAFFRON, GOLD, CREAM = "38;5;208", "38;5;220", "38;5;223"
GREEN, RED, CYAN, GREY = "38;5;114", "38;5;203", "38;5;117", "38;5;244"
DIFF_STYLE = {"E": GREEN, "M": GOLD, "H": RED}
HEAT = ["38;5;238", "38;5;94", "38;5;130", "38;5;172", "38;5;214"]  # embers → flame

WIDTH = 66


def rule(title: str = "") -> str:
    if not title:
        return c("─" * WIDTH, GREY)
    return c("── ", GREY) + c(title.upper(), BOLD, CREAM) + " " + c("─" * (WIDTH - len(title) - 4), GREY)


def bar(fraction: float, width: int = 34) -> str:
    fraction = max(0.0, min(1.0, fraction))
    filled = round(fraction * width)
    shades = ["38;5;130", "38;5;166", "38;5;202", "38;5;208", "38;5;214", "38;5;220"]
    out = "".join(c("█", shades[min(len(shades) - 1, i * len(shades) // width)]) for i in range(filled))
    return out + c("░" * (width - filled), "38;5;238")


# ── Storage ───────────────────────────────────────────────────────────────────
def load_state() -> dict:
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text())
        state.pop("week", None)  # pre-units: the current unit is now derived from the log
        return state
    state = {"start": date.today().isoformat()}
    save_state(state)
    return state


def save_state(state: dict) -> None:
    PROGRESS.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


def load_log() -> list[dict]:
    if not LOG_FILE.exists():
        return []
    with LOG_FILE.open(newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["xp"] = int(row["xp"] or 0)
        row["day"] = date.fromisoformat(row["date"])
    return rows


def append_log(entry: dict) -> None:
    PROGRESS.mkdir(parents=True, exist_ok=True)
    is_new = not LOG_FILE.exists()
    with LOG_FILE.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow({k: entry.get(k, "") for k in FIELDS})


def rewrite_log(rows: list[dict]) -> None:
    with LOG_FILE.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDS})


# ── Derived stats ─────────────────────────────────────────────────────────────
def total_xp(rows: list[dict]) -> int:
    return sum(r["xp"] for r in rows)


def reviews_passed(rows: list[dict]) -> int:
    return sum(1 for r in rows if r["kind"] == "promotion")


def level_for(rows: list[dict]) -> tuple[int, tuple]:
    passed = reviews_passed(rows)
    idx = max(i for i, lvl in enumerate(LEVELS) if passed >= lvl[0])
    return idx, LEVELS[idx]


def streaks(rows: list[dict], today: date) -> tuple[int, int, bool]:
    """(current, best, at_risk). 'Never miss twice': one missed day is forgiven, two in a row reset."""
    active = {r["day"] for r in rows}
    if not active:
        return 0, 0, False
    current = best = misses = 0
    day = min(active)
    while day < today:
        if day in active:
            current, misses = current + 1, 0
        else:
            misses += 1
            if misses >= 2:
                current = 0
        best = max(best, current)
        day += timedelta(days=1)
    if today in active:
        current += 1
        misses = 0
    best = max(best, current)
    at_risk = today not in active and misses == 1 and current > 0
    return current, best, at_risk


def schedule_for(solve: dict) -> tuple[int, ...]:
    """Re-solve offsets for a solve row: tighter when the solution was viewed (logged with --viewed)."""
    return VIEWED_RESOLVE_AFTER_DAYS if (solve.get("note") or "").startswith(VIEWED_TAG) else RESOLVE_AFTER_DAYS


def resolve_queue(rows: list[dict], today: date) -> tuple[list, list]:
    """Each solve schedules re-solves at +3/+7/+21 days. Returns (due, upcoming) as (date, pid, name, stage)."""
    first_solve: dict[str, dict] = {}
    resolves: dict[str, int] = {}
    for r in rows:
        if r["kind"] == "solve":
            first_solve.setdefault(r["pid"], r)
        elif r["kind"] == "resolve":
            resolves[r["pid"]] = resolves.get(r["pid"], 0) + 1
    due, upcoming = [], []
    for pid, r in first_solve.items():
        stage = resolves.get(pid, 0)
        offsets = schedule_for(r)
        if stage >= len(offsets):
            continue
        when = r["day"] + timedelta(days=offsets[stage])
        item = (when, pid, r["name"], stage + 1)
        (due if when <= today else upcoming).append(item)
    return sorted(due), sorted(upcoming)


def target_for(rows: list[dict], today: date, state: dict) -> int:
    """The base target, dropped to 1 when this morning's re-solve queue was RESOLVE_CAP or more."""
    base = state.get("daily_target", DEFAULT_DAILY_TARGET)
    due_at_start, _ = resolve_queue([r for r in rows if r["day"] < today], today)
    return 1 if len(due_at_start) >= RESOLVE_CAP else base


def daily_progress(rows: list[dict], today: date, target: int) -> tuple[int, int, bool]:
    """(new problems solved today, re-solves still due, target met). Met = target new solves + empty re-solve queue."""
    new_today = sum(1 for r in rows if r["kind"] == "solve" and r["day"] == today)
    due, _ = resolve_queue(rows, today)
    return new_today, len(due), new_today >= target and not due


def target_line(rows: list[dict], today: date, target: int) -> str:
    new_today, due_left, met = daily_progress(rows, today, target)
    if met:
        return c("🎯 Daily target hit. ", BOLD, GREEN) + c("Anything more is bonus. Stopping here is a win too.", GREEN)
    parts = [f"{min(new_today, target)}/{target} new"]
    if due_left:
        parts.append(f"{due_left} re-solve{'s' if due_left != 1 else ''} due")
    return c("🎯 Today's target: ", BOLD, GOLD) + c("  ·  ".join(parts), CREAM)


def gauntlet_line(rows: list[dict], today: date) -> str:
    """Friday Gauntlet: 2 cold re-solves of this week's problems, no hints, logged as `event mock`.
    Shown Friday to Sunday until it's done that week."""
    monday = today - timedelta(days=today.weekday())
    done = any(r["kind"] == "mock" and r["day"] >= monday for r in rows)
    if done:
        return c("⚔  Friday Gauntlet cleared this week ✔", GREEN) if today.weekday() >= 4 else ""
    if today.weekday() < 4:
        return ""
    return c("⚔  Friday Gauntlet due: 2 cold re-solves from this week, no hints → python dsa.py event mock", BOLD, GOLD)


def unit_info(unit: int) -> tuple[str, str]:
    folder, topic, _ = UNITS.get(unit, (*INTERVIEW_MODE, []))
    return folder, topic


def solved_hints(rows: list[dict]) -> dict[str, int]:
    """pid -> hints on its first solve."""
    out: dict[str, int] = {}
    for r in rows:
        if r["kind"] == "solve" and r["pid"] not in out:
            out[r["pid"]] = int(r["hints"] or 0)
    return out


def unit_problems(unit: int, state: dict) -> list[tuple[str, str, str]]:
    """The unit's list plus any reinforcement problems added with `dsa.py add`."""
    listed = UNITS[unit][2] if unit in UNITS else []
    return listed + [tuple(p) for p in state.get("extras", {}).get(str(unit), [])]


def unit_status(unit: int, rows: list[dict], state: dict) -> dict:
    """done/total, average hints over the listed problems, and whether the unit needs reinforcement."""
    hints = solved_hints(rows)
    listed = UNITS[unit][2] if unit in UNITS else []
    problems = unit_problems(unit, state)
    done = [p for p in problems if p[0] in hints]
    listed_done = [hints[p[0]] for p in listed if p[0] in hints]
    avg = sum(listed_done) / len(listed_done) if listed_done else 0.0
    extras = state.get("extras", {}).get(str(unit), [])
    weak = avg >= QUALITY_HINTS and len(extras) < REINFORCE_COUNT
    complete = bool(listed) and len(done) == len(problems) and not weak
    return {"done": len(done), "total": len(problems), "avg_hints": avg, "weak": weak, "complete": complete}


def current_unit(rows: list[dict], state: dict) -> int:
    """First unit (at or after any manual `unit next` skip) that isn't complete. Never set by hand per problem."""
    unit = state.get("unit_floor", 1)
    while unit in UNITS and unit_status(unit, rows, state)["complete"]:
        unit += 1
    return unit


def unit_of(pid: str, state: dict) -> int | None:
    return next((u for u in UNITS if any(p[0] == pid for p in unit_problems(u, state))), None)


def pace(rows: list[dict], today: date, state: dict) -> float:
    """New problems per day over the last 7 days (fewer if the project is younger)."""
    window = min(7, (today - date.fromisoformat(state["start"])).days + 1)
    recent = sum(1 for r in rows if r["kind"] == "solve" and (today - r["day"]).days < window)
    return recent / window


def eta(remaining: int, per_day: float, today: date) -> date | None:
    """The day the remaining problems run out at this pace, counting from tomorrow."""
    return today + timedelta(days=math.ceil(remaining / per_day)) if per_day else None


# ── Dashboard ─────────────────────────────────────────────────────────────────
def heatmap(rows: list[dict], today: date, weeks: int = 18) -> list[str]:
    xp_by_day: dict[date, int] = {}
    for r in rows:
        xp_by_day[r["day"]] = xp_by_day.get(r["day"], 0) + r["xp"]
    start = today - timedelta(days=today.weekday()) - timedelta(weeks=weeks - 1)

    def cell(d: date) -> str:
        if d > today:
            return "  "
        xp = xp_by_day.get(d, 0)
        shade = 0 if xp == 0 else 1 if xp < 15 else 2 if xp < 40 else 3 if xp < 80 else 4
        glyph = "■" if xp else "·"
        if d == today:
            return c("◆", BOLD, CYAN if not xp else HEAT[shade]) + " "
        return c(glyph, HEAT[shade]) + " "

    lines = []
    for wd, label in enumerate(["Mon", "   ", "Wed", "   ", "Fri", "   ", "Sun"]):
        row = "".join(cell(start + timedelta(weeks=w, days=wd)) for w in range(weeks))
        lines.append("  " + c(label, GREY) + "  " + row)
    legend = "less " + " ".join(c("■", h) for h in HEAT[1:]) + " more   " + c("◆", CYAN) + " today"
    lines.append("       " + c(legend, GREY))
    return lines


def dashboard() -> None:
    state = load_state()
    rows = load_log()
    today = date.today()
    xp = total_xp(rows)
    idx, (_, icon, title, means, gate) = level_for(rows)
    current, best, at_risk = streaks(rows, today)
    due, upcoming = resolve_queue(rows, today)
    day_no = (today - date.fromisoformat(state["start"])).days + 1
    done_today = any(r["day"] == today for r in rows)

    header = f"  D S A   F O R G E"
    right = f"Day {day_no} · {today.strftime('%a %d %b %Y')}  "
    print()
    print(c("  ╭" + "─" * (WIDTH - 2) + "╮", SAFFRON))
    print(c("  │", SAFFRON) + c(header, BOLD, SAFFRON) + " " * (WIDTH - 2 - len(header) - len(right)) + c(right, CREAM) + c("│", SAFFRON))
    print(c("  ╰" + "─" * (WIDTH - 2) + "╯", SAFFRON))
    print()

    # Rank
    print("  " + rule("rank"))
    print(f"   {icon}  {c(title, BOLD, GOLD)}   {c(f'{xp:,} XP', BOLD)}")
    print(f"   {c('means:', GREY)} {c(means, CREAM)}")
    if idx + 1 < len(LEVELS):
        _, nxt_icon, nxt_title, _, _ = LEVELS[idx + 1]
        print(f"   {c('next:', GREY)} {nxt_icon} {nxt_title} {c('· pass', GREY)} {c(gate, CREAM)}")
    else:
        print(f"   {c('max rank. go get the offer.', CREAM)}")
    print()

    # Streak
    print("  " + rule("streak"))
    flame = c("🔥", BOLD) if current else c("·", GREY)
    print(f"   {flame} {c(str(current), BOLD, SAFFRON)} day{'s' if current != 1 else ''}"
          f"   {c('best', GREY)} {best}   {c('│', GREY)}   today: "
          + (c("✔ done", BOLD, GREEN) if done_today else c("✘ not yet", BOLD, RED)))
    if at_risk:
        print("   " + c("⚠  You missed yesterday. Miss today and the streak resets. Do one problem.", BOLD, RED))
    elif not done_today:
        print("   " + c("Minimum viable day: one re-solve or one easy problem keeps it alive.", GREY))
    print()

    # Today's target
    target = target_for(rows, today, state)
    new_today, _, met = daily_progress(rows, today, target)
    print("  " + rule("today's target"))
    print(f"   {bar(min(1.0, new_today / target), width=20)}  " + target_line(rows, today, target))
    if target < state.get("daily_target", DEFAULT_DAILY_TARGET):
        print("   " + c(f"Re-solve heavy day ({RESOLVE_CAP}+ due this morning): 1 new problem today.", GREY))
    gauntlet = gauntlet_line(rows, today)
    if gauntlet:
        print("   " + gauntlet)
    print()

    # Roadmap: units move at his pace, dates are estimates from the last 7 days
    unit = current_unit(rows, state)
    _, topic = unit_info(unit)
    print("  " + rule("roadmap"))
    if unit in UNITS:
        st = unit_status(unit, rows, state)
        frac = st["done"] / st["total"] if st["total"] else 0
        print(f"   Unit {c(str(unit), BOLD, GOLD)} · {c(topic, BOLD)}   {bar(frac, width=12)}  {st['done']}/{st['total'] or '?'}")
        if st["weak"]:
            print("   " + c(f"⚠  Averaging {st['avg_hints']:.1f} hints here: {REINFORCE_COUNT} reinforcement problems "
                            "before the next unit.", GOLD))
        per_day = pace(rows, today, state)
        if per_day:
            left_unit = st["total"] - st["done"] + (REINFORCE_COUNT if st["weak"] else 0)
            phase = UNITS[unit][0].split("/")[0]
            later = [u for u in UNITS if u > unit]
            left_phase = left_unit + sum(len(unit_problems(u, state)) or UNLISTED_UNIT_SIZE
                                         for u in later if UNITS[u][0].startswith(phase))
            left_goal = left_unit + sum(len(unit_problems(u, state)) or UNLISTED_UNIT_SIZE
                                        for u in later if u <= GOAL_LAST_UNIT)
            nxt = unit_info(unit + 1)[1]
            phase_name = phase.split("_")[0].replace("phase", "Phase ")
            print(f"   {c('pace', GREY)} {per_day:.1f} new/day   {c('│', GREY)}   "
                  f"{c('next:', GREY)} {c(nxt, CREAM)} ~{eta(left_unit, per_day, today):%a %d %b}")
            print(f"   {c(phase_name + ' done', GREY)} ~{eta(left_phase, per_day, today):%d %b}   {c('│', GREY)}   "
                  f"{c('🎯 goal units', GREY)} ~{eta(left_goal, per_day, today):%b %Y}"
                  + c("  (+ Interview Mode)", GREY))
    else:
        print(f"   {c(topic, BOLD, GOLD)}: mocks, contests, company-tagged sets")
    week_rows = [r for r in rows if (today - r["day"]).days < 7]
    solves = [r for r in rows if r["kind"] == "solve"]
    counts = {d: sum(1 for r in solves if r["diff"] == d) for d in "EMH"}
    clean = sum(1 for r in solves if r["hints"] in ("0", 0))
    clean_pct = f"{round(100 * clean / len(solves))}%" if solves else "-"
    print(f"   {c('last 7 days', GREY)} {total_xp(week_rows)} XP   {c('│', GREY)}   "
          f"{c('solved', GREY)} {c(str(counts['E']) + ' E', GREEN)}  {c(str(counts['M']) + ' M', GOLD)}  "
          f"{c(str(counts['H']) + ' H', RED)}   {c('│', GREY)}   {c('no-hint', GREY)} {clean_pct}")
    print()

    # Activity
    print("  " + rule("activity"))
    for line in heatmap(rows, today):
        print(line)
    print()

    # Re-solve queue
    print("  " + rule("re-solve queue"))
    if due:
        totals = {r["pid"]: len(schedule_for(r)) for r in rows if r["kind"] == "solve"}
        for when, pid, name, stage in due[:6]:
            late = (today - when).days
            tag = c("due today", GOLD) if late == 0 else c(f"{late}d overdue", RED)
            print(f"   {c('↻', SAFFRON)} LC {pid:<5} {name[:34]:<34} {c(f'round {stage}/{totals.get(pid, 3)}', GREY)}  {tag}")
        if len(due) > 6:
            print(c(f"   … and {len(due) - 6} more", GREY))
    else:
        print("   " + c("Nothing due. ", GREEN) + c(
            f"Next: LC {upcoming[0][1]} on {upcoming[0][0].strftime('%a %d %b')}" if upcoming else "Solve something to fill the queue.",
            GREY))
    print()

    # Tip
    tip = TIPS[today.toordinal() % len(TIPS)]
    print("  " + rule("senior's note"))
    print("   " + c("“" + tip + "”", CREAM))
    print()


# ── Commands ──────────────────────────────────────────────────────────────────
def celebrate(rows_before: list[dict], gained: int, today: date) -> None:
    rows_after = load_log()
    write_tracker(rows_after)
    before_idx, _ = level_for(rows_before)
    after_idx, (_, icon, title, means, _) = level_for(rows_after)
    print(c(f"   +{gained} XP", BOLD, GOLD) + c(f"   ·   total {total_xp(rows_after):,} XP", GREY))
    if after_idx > before_idx:
        print()
        print(c("   ★ ★ ★  PROMOTED  ★ ★ ★", BOLD, SAFFRON))
        print(f"   {icon}  You are now {c(title, BOLD, GOLD)}. Earned, not given.")
        print(c(f"   That means: {means}.", CREAM))
    was_active = any(r["day"] == today for r in rows_before)
    if not was_active:
        current, _, _ = streaks(rows_after, today)
        msg = f"🔥 streak {current}"
        if current in STREAK_MILESTONES:
            msg += c(f"  ·  {current}-day milestone. This is what consistency looks like.", BOLD, SAFFRON)
        print("   " + msg)
    target = target_for(rows_after, today, load_state())
    print("   " + target_line(rows_after, today, target))
    print()


def normalize_diff(diff: str) -> str:
    d = diff.strip().upper()[:1]
    if d not in XP_SOLVE:
        sys.exit(c("difficulty must be E, M or H", RED))
    return d


def cmd_log(args) -> None:
    rows = load_log()
    pid = str(args.pid)
    if any(r["kind"] == "solve" and r["pid"] == pid for r in rows):
        sys.exit(c(f"LC {pid} is already logged as solved. Use: python dsa.py resolve {pid}", GOLD))
    diff = normalize_diff(args.diff)
    path = solution_file(pid)
    own = own_test_count(path) if path else 0
    if own < MIN_OWN_TESTS:
        where = path.name if path else "no solution file found"
        sys.exit(c(f"LC {pid} ({where}) has {own} test(s) of your own, need {MIN_OWN_TESTS}. "
                   "Write the missing ones yourself; cases marked 'added in review' don't count.", GOLD))
    xp = XP_SOLVE[diff] + (XP_NO_HINTS if args.hints == 0 else 0)
    name = args.name or find_problem_name(pid) or ""
    note = args.note or ""
    if args.viewed:
        note = f"{VIEWED_TAG} {note}".strip()
    entry = {"date": date.today().isoformat(), "kind": "solve", "pid": pid, "name": name, "diff": diff,
             "hints": args.hints, "mins": args.mins or "", "xp": xp, "note": note}
    append_log(entry)
    print()
    print(f"   {c('✔', BOLD, GREEN)} LC {pid} {name} {c('[' + diff + ']', DIFF_STYLE[diff])}"
          + (c("  clean solve, no hints", GREEN) if args.hints == 0 else c(f"  {args.hints} hint(s)", GREY)))
    offsets = schedule_for(entry)
    first = date.today() + timedelta(days=offsets[0])
    rest = " → ".join(f"+{d}d" for d in offsets[1:])
    print(c(f"   ↻ re-solve scheduled: {first.strftime('%a %d %b')} → {rest}", GREY))
    celebrate(rows, xp, date.today())


def cmd_resolve(args) -> None:
    rows = load_log()
    pid = str(args.pid)
    solve = next((r for r in rows if r["kind"] == "solve" and r["pid"] == pid), None)
    if not solve:
        sys.exit(c(f"LC {pid} was never logged as solved. Use: python dsa.py log {pid} <E|M|H>", GOLD))
    path = resolve_file(pid)
    own = own_test_count(path) if path else 0
    if own < MIN_OWN_TESTS:
        where = f"resolve/{path.name}" if path else "no file in resolve/"
        sys.exit(c(f"LC {pid} re-solve ({where}) has {own} test(s) of your own, need {MIN_OWN_TESTS}. "
                   "Write the missing ones yourself; cases marked 'added in review' don't count.", GOLD))
    done = sum(1 for r in rows if r["kind"] == "resolve" and r["pid"] == pid)
    append_log({"date": date.today().isoformat(), "kind": "resolve", "pid": pid, "name": solve["name"],
                "diff": solve["diff"], "xp": XP_RESOLVE, "mins": args.mins or "", "note": args.note or ""})
    print()
    total = len(schedule_for(solve))
    stage = min(done + 1, total)
    print(f"   {c('↻', BOLD, SAFFRON)} LC {pid} {solve['name']} re-solved  {c(f'round {stage}/{total}', GREY)}"
          + (c("  · locked in for good", GREEN) if done + 1 == total else ""))
    celebrate(rows, XP_RESOLVE, date.today())


def cmd_event(args) -> None:
    rows = load_log()
    xp = XP_EVENT[args.kind]
    append_log({"date": date.today().isoformat(), "kind": args.kind, "xp": xp, "note": args.note or ""})
    print()
    label = "Mock interview done" if args.kind == "mock" else "Promotion review PASSED"
    print(f"   {c('◆', BOLD, CYAN)} {c(label, BOLD)}")
    celebrate(rows, xp, date.today())


def cmd_check(args) -> None:
    """Checks the re-solve file in resolve/ when one exists, otherwise the solution file."""
    path = resolve_file(str(args.pid)) or solution_file(str(args.pid))
    if not path:
        sys.exit(c(f"No solution file for LC {args.pid}.", GOLD))
    own = own_test_count(path)
    ok = own >= MIN_OWN_TESTS
    label = f"LC {args.pid} re-solve" if path.parent.name == "resolve" else f"LC {args.pid}"
    print(c(f"   {'✔' if ok else '✘'} {label}: {own} test(s) of your own (need {MIN_OWN_TESTS})", BOLD, GREEN if ok else RED))
    if not ok:
        sys.exit(1)


def cmd_undo(_args) -> None:
    rows = load_log()
    if not rows:
        sys.exit(c("Nothing to undo.", GREY))
    last = rows.pop()
    rewrite_log(rows)
    write_tracker()
    print(c(f"   removed: {last['date']} {last['kind']} {last['pid']} {last['name']} ({last['xp']} XP)", GREY))


def cmd_journal(args) -> None:
    PROGRESS.mkdir(parents=True, exist_ok=True)
    if not JOURNAL_FILE.exists():
        JOURNAL_FILE.write_text("# DSA Journal\n\nOne line a day: what tricked you, what clicked.\n\n")
    with JOURNAL_FILE.open("a") as f:
        f.write(f"- **{date.today().isoformat()}**: {args.text}\n")
    print(c("   ✎ noted.", GREEN))


def cmd_unit(args) -> None:
    state = load_state()
    if args.value == "next":  # only for a unit without a fixed list (e.g. the hard week)
        state["unit_floor"] = current_unit(load_log(), state) + 1
        save_state(state)
    unit = current_unit(load_log(), state)
    folder, topic = unit_info(unit)
    print(f"   Unit {c(str(unit), BOLD, GOLD)} · {c(topic, BOLD)}  {c(folder + '/', GREY)}")


def cmd_add(args) -> None:
    """Add a reinforcement problem to a unit (default: the current one)."""
    state = load_state()
    unit = args.unit or current_unit(load_log(), state)
    diff = normalize_diff(args.diff)
    extras = state.setdefault("extras", {}).setdefault(str(unit), [])
    if unit_of(str(args.pid), state):
        sys.exit(c(f"LC {args.pid} is already in unit {unit_of(str(args.pid), state)}", GOLD))
    extras.append([str(args.pid), diff, args.name])
    save_state(state)
    print(f"   {c('+', BOLD, GREEN)} LC {args.pid} {args.name} added to unit {unit} ({unit_info(unit)[1]})")


def cmd_target(args) -> None:
    state = load_state()
    if args.n:
        state["daily_target"] = max(1, args.n)
        save_state(state)
    print(f"   🎯 Daily target: {c(str(state.get('daily_target', DEFAULT_DAILY_TARGET)), BOLD, GOLD)} new problems + all due re-solves")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def find_problem_name(pid: str) -> str | None:
    pattern = f"lc{int(pid):04d}_*.py" if pid.isdigit() else f"lc{pid}_*.py"
    for path in ROOT.glob(f"phase*/**/{pattern}"):
        match = re.search(r"^LC \S+ · (.+?) · ", path.read_text(), re.MULTILINE)
        if match:
            return match.group(1)
    return None


def _file_pattern(pid: str) -> str:
    return f"lc{int(pid):04d}_*.py" if pid.isdigit() else f"lc{slugify(pid)}_*.py"


def solution_file(pid: str) -> Path | None:
    return next(iter(sorted(ROOT.glob(f"phase*/**/{_file_pattern(pid)}"))), None)


def resolve_file(pid: str) -> Path | None:
    """The cold re-solve scratch file in resolve/, if one is in progress."""
    return next(iter(sorted((ROOT / "resolve").glob(_file_pattern(pid)))), None)


def own_test_count(path: Path) -> int:
    """Tests Harsh wrote himself: case rows like `([1, 2], 3),` or asserts against a literal
    (`assert s.f(x) == 5`), in the __main__ block, excluding lines marked "added in review"."""
    text = path.read_text()
    main = text.split('if __name__ == "__main__":', 1)[1] if 'if __name__ == "__main__":' in text else ""
    count = 0
    for line in main.splitlines():
        if "added in review" in line:
            continue
        code = line.split("#", 1)[0].strip()
        if re.match(r"[\(\[].*[\)\]],?$", code):
            count += 1
        elif code.startswith("assert "):
            expr = re.sub(r",\s*f?[\"'].*$", "", code[len("assert "):])  # drop the failure message
            # a literal input or expected value, not just names (`assert got == expected` is a loop check)
            if re.search(r"(?<![\w\]\)])\[|\b\d|[\"']|\b(True|False|None)\b", expr):
                count += 1
    return count


def docstring_fields(path: Path) -> dict[str, str]:
    """Parse 'Key: value' lines (with indented continuation lines) from a solution's docstring."""
    text = path.read_text()
    match = re.match(r'\s*"""(.*?)"""', text, re.S)
    fields: dict[str, str] = {}
    key = None
    for line in (match.group(1) if match else "").splitlines():
        head = re.match(r"^([A-Z][A-Za-z ]+?):\s*(.*)$", line)
        if head and not line.startswith(" "):
            key = head.group(1)
            fields[key] = head.group(2).strip()
        elif key and line.strip():
            fields[key] += " " + line.strip()
    return fields


def topic_for(path: Path) -> str:
    rel = str(path.relative_to(ROOT).parent)
    return next((topic for folder, topic, _ in UNITS.values() if folder == rel), rel)


TRACKER_COLUMNS = ["#", "Date", "LC #", "Problem", "Difficulty", "Topic", "Pattern", "Minutes", "Hints",
                   "Clean solve", "XP", "Re-solves done", "Next re-solve", "Mastered", "Key insight",
                   "LeetCode", "Solution"]


def write_tracker(rows: list[dict] | None = None) -> None:
    """One row per problem, rebuilt from log.csv and the solution docstrings. Never edit the CSV by hand."""
    rows = load_log() if rows is None else rows
    resolves: dict[str, list[dict]] = {}
    for r in rows:
        if r["kind"] == "resolve":
            resolves.setdefault(r["pid"], []).append(r)
    out = []
    solves = [r for r in rows if r["kind"] == "solve"]
    for n, r in enumerate(solves, 1):
        path = solution_file(r["pid"])
        f = docstring_fields(path) if path else {}
        done = len(resolves.get(r["pid"], []))
        offsets = schedule_for(r)  # viewed solutions run +1/+3/+7/+21
        nxt = (r["day"] + timedelta(days=offsets[done])).isoformat() if done < len(offsets) else ""
        out.append({
            "#": n, "Date": r["date"], "LC #": r["pid"], "Problem": r["name"],
            "Difficulty": {"E": "Easy", "M": "Medium", "H": "Hard"}.get(r["diff"], r["diff"]),
            "Topic": topic_for(path) if path else "", "Pattern": f.get("Pattern", ""),
            "Minutes": r["mins"], "Hints": r["hints"], "Clean solve": "Yes" if r["hints"] in ("0", 0) else "No",
            "XP": r["xp"], "Re-solves done": f"{done} of {len(offsets)}", "Next re-solve": nxt,
            "Mastered": "Yes" if done >= len(offsets) else "No",
            "Key insight": f.get("Key insight", ""), "LeetCode": f.get("Link", ""),
            "Solution": f"{REPO_URL}/blob/main/{path.relative_to(ROOT).as_posix()}" if path else "",
        })
    PROGRESS.mkdir(parents=True, exist_ok=True)
    with TRACKER_FILE.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=TRACKER_COLUMNS)
        writer.writeheader()
        writer.writerows(out)


def cmd_export(_args) -> None:
    write_tracker()
    print(c(f"   ⇪ {TRACKER_FILE.relative_to(ROOT)} rebuilt", GREEN))


SOLUTION_TEMPLATE = '''"""
LC {pid} · {name} · {difficulty}
Link: https://leetcode.com/problems/{slug}/
Pattern:
Approach:
Time: O(?)   Space: O(?)
Hints used: 0   Time taken: ? min
"""


class Solution:
    # Paste the LeetCode method signature here.
    pass


if __name__ == "__main__":
    s = Solution()
    # assert s.method(input) == expected
    # assert s.method(edge_case) == expected   # edge: ...
    print("all tests passed ✅")
'''


def create_solution(pid: str, name: str, diff: str) -> None:
    """Solution file in the folder of the unit that lists the pid (else the current unit)."""
    state = load_state()
    folder, _ = unit_info(unit_of(pid, state) or current_unit(load_log(), state))
    create_file(folder, pid, name, normalize_diff(diff))


def cmd_new(args) -> None:
    create_solution(str(args.pid), args.name, args.diff)


def cmd_next(_args) -> None:
    """Set up the next unsolved problem of the current unit, or point at the one already in progress."""
    rows, state = load_log(), load_state()
    unit = current_unit(rows, state)
    if unit not in UNITS:
        sys.exit(c("No fixed list here: pick a problem and use `dsa.py new`.", GOLD))
    solved = solved_hints(rows)
    todo = [p for p in unit_problems(unit, state) if p[0] not in solved]
    if not todo:
        sys.exit(c(f"Unit {unit} needs {REINFORCE_COUNT} reinforcement problems: dsa.py add <pid> \"<Name>\" <E|M|H>", GOLD))
    pid, diff, name = todo[0]
    existing = solution_file(pid)
    if existing:
        print(f"   {c('→', BOLD, CYAN)} in progress: {c(str(existing.relative_to(ROOT)), BOLD)}")
        return
    create_solution(pid, name, diff)


def create_file(folder: str, pid: str, name: str, diff: str) -> None:
    prefix = f"lc{int(pid):04d}" if pid.isdigit() else f"lc{slugify(pid)}"
    target = ROOT / folder / f"{prefix}_{slugify(name)}.py"
    if target.exists():
        sys.exit(c(f"already exists: {target.relative_to(ROOT)}", GOLD))
    target.parent.mkdir(parents=True, exist_ok=True)
    full = {"E": "Easy", "M": "Medium", "H": "Hard"}[diff]
    slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9 -]", "", name.lower()).strip().replace(" ", "-"))
    target.write_text(SOLUTION_TEMPLATE.format(pid=pid, name=name, difficulty=full, slug=slug))
    print(f"   {c('✚', BOLD, GREEN)} created {c(str(target.relative_to(ROOT)), BOLD)}")
    print(f"   {c('LC ' + pid + ' · ' + name, BOLD)}  https://leetcode.com/problems/{slug}/")
    print(c(f"   when solved: python dsa.py log {pid} {diff} --mins <n> --hints <n>", GREY))


def main() -> None:
    parser = argparse.ArgumentParser(prog="dsa", description="DSA Forge: daily DSA progress tracker.")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("log", help="log a solved problem")
    p.add_argument("pid", help="LeetCode number (or any id)")
    p.add_argument("diff", help="E | M | H")
    p.add_argument("--hints", type=int, default=0, help="hints used (0 = clean solve, +5 XP)")
    p.add_argument("--mins", type=int, help="minutes taken")
    p.add_argument("--name", help="problem name (auto-read from your solution file if omitted)")
    p.add_argument("--note", help="short note")
    p.add_argument("--viewed", action="store_true", help="solution was viewed: first re-solve tomorrow (+1/+3/+7/+21d)")
    p.set_defaults(fn=cmd_log)

    p = sub.add_parser("resolve", help="log a spaced re-solve")
    p.add_argument("pid")
    p.add_argument("--mins", type=int)
    p.add_argument("--note")
    p.set_defaults(fn=cmd_resolve)

    p = sub.add_parser("event", help="log a mock interview or passed promotion review")
    p.add_argument("kind", choices=list(XP_EVENT))
    p.add_argument("--note")
    p.set_defaults(fn=cmd_event)

    p = sub.add_parser("next", help="set up the next problem of the current unit")
    p.set_defaults(fn=cmd_next)

    p = sub.add_parser("add", help="add a reinforcement problem to a unit")
    p.add_argument("pid")
    p.add_argument("name")
    p.add_argument("diff", help="E | M | H")
    p.add_argument("--unit", type=int, help="unit number (default: current)")
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("new", help="create a solution file (in the unit that lists it)")
    p.add_argument("pid")
    p.add_argument("name")
    p.add_argument("diff", help="E | M | H")
    p.set_defaults(fn=cmd_new)

    p = sub.add_parser("journal", help="add a one-line journal entry")
    p.add_argument("text")
    p.set_defaults(fn=cmd_journal)

    p = sub.add_parser("unit", help="show the current unit ('next' skips a unit without a fixed list)")
    p.add_argument("value", nargs="?", choices=["next"])
    p.set_defaults(fn=cmd_unit)

    p = sub.add_parser("target", help="show or set the daily new-problem target")
    p.add_argument("n", nargs="?", type=int)
    p.set_defaults(fn=cmd_target)

    p = sub.add_parser("export", help="rebuild progress/tracker.csv (the Google Sheet's source)")
    p.set_defaults(fn=cmd_export)

    p = sub.add_parser("check", help="count your own tests in a solution file (the log gate)")
    p.add_argument("pid")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("undo", help="remove the last log entry")
    p.set_defaults(fn=cmd_undo)

    args = parser.parse_args()
    if not args.cmd:
        dashboard()
    else:
        args.fn(args)


if __name__ == "__main__":
    main()
