# Data Structures & Algorithms

My DSA journey from zero to interview-ready (any unseen medium in 25–35 minutes), in Python, one day at a time.

- **[ROADMAP.md](ROADMAP.md)**: the plan, from Big-O through graphs and DP to mock interviews
- **`phase*/week*/`**: my solutions, one file per problem, each with its approach, complexity and test cases
- **`progress/`**: the daily log, plus a journal of what tricked me and what clicked
- **[`patterns/`](patterns/README.md)**: one card per pattern: how to spot it, the core move, and the traps I actually fell into
- **[CHANGELOG.md](CHANGELOG.md)**: every change to the system, newest first

## DSA Forge

`dsa.py` is the tracker that keeps me showing up. It has XP, levels that mean something in hiring terms (Beginner → Interview-ready, the goal: any medium in 25–35 minutes. Earned only by passing promotion reviews, never by XP), a streak with a "never miss twice" rule, an activity heatmap, and a spaced re-solve queue. The roadmap moves in **units** at my own pace: a unit ends when its problem list is done, and the dashboard estimates the dates from my last 7 days. `log` refuses a problem until its file has at least 3 tests I wrote myself (cases marked `added in review` don't count). Friday to Sunday the dashboard shows the **Friday Gauntlet**: 2 cold re-solves from the week, no hints.

```bash
python dsa.py                                   # dashboard
python dsa.py next                              # set up the next problem of the current unit
python dsa.py new 1 "Two Sum" E                 # create a solution file (in the unit that lists it)
python dsa.py add 1752 "Check if Array Is Sorted and Rotated" E   # reinforcement problem for this unit
python dsa.py log 1 E --mins 18 --hints 0       # log a solve
python dsa.py log 1 E --hints 3 --viewed       # solution viewed: re-solve tomorrow, then days 3, 7, 21
python dsa.py resolve 1                         # spaced re-solve (days 3, 7, 21)
python dsa.py event mock                        # Friday Gauntlet cleared
python dsa.py check 1                           # count my own tests (log needs 3)
python dsa.py journal "forgot the empty input"  # one-line journal
python dsa.py unit                              # current unit (advances by itself when its list is done)
python dsa.py target 3                          # change the daily target (default: 2 new + due re-solves)
```

Standard library only, so there's nothing to install.
