# Data Structures & Algorithms

My DSA journey from zero to MNC-interview level, in Python, one day at a time.

- **[ROADMAP.md](ROADMAP.md)**: the ~30-week plan, from Big-O through graphs and DP to mock interviews
- **`phase*/week*/`**: my solutions, one file per problem, each with its approach, complexity and test cases
- **`progress/`**: the daily log, plus a journal of what tricked me and what clicked
- **[`patterns/`](patterns/README.md)**: one card per pattern: how to spot it, the core move, and the traps I actually fell into

## DSA Forge

`dsa.py` is the tracker that keeps me showing up. It has XP, career ranks (Intern → Principal), a streak with a "never miss twice" rule, an activity heatmap, and a spaced re-solve queue. `log` refuses a problem until its file has at least 3 tests I wrote myself (cases marked `added in review` don't count). Friday to Sunday the dashboard shows the **Friday Gauntlet**: 2 cold re-solves from the week, no hints.

```bash
python dsa.py                                   # dashboard
python dsa.py new 1 "Two Sum" E                 # create a solution file in this week's folder
python dsa.py log 1 E --mins 18 --hints 0       # log a solve
python dsa.py log 1 E --hints 3 --viewed       # solution viewed: re-solve tomorrow, then days 3, 7, 21
python dsa.py resolve 1                         # spaced re-solve (days 3, 7, 21)
python dsa.py event mock                        # Friday Gauntlet cleared
python dsa.py check 1                           # count my own tests (log needs 3)
python dsa.py journal "forgot the empty input"  # one-line journal
python dsa.py week next                         # move to the next roadmap week
python dsa.py target 3                          # change the daily target (default: 2 new + due re-solves)
```

Standard library only, so there's nothing to install.
