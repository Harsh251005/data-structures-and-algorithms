# Data Structures & Algorithms

My DSA journey from zero to MNC-interview level, in Python, one day at a time.

- **[ROADMAP.md](ROADMAP.md)**: the ~30-week plan, from Big-O through graphs and DP to mock interviews
- **`phase*/week*/`**: my solutions, one file per problem, each with its approach, complexity and test cases
- **`progress/`**: the daily log, plus a journal of what tricked me and what clicked

## DSA Forge

`dsa.py` is the tracker that keeps me showing up. It has XP, career ranks (Intern → Principal), a streak with a "never miss twice" rule, an activity heatmap, and a spaced re-solve queue.

```bash
python dsa.py                                   # dashboard
python dsa.py new 1 "Two Sum" E                 # create a solution file in this week's folder
python dsa.py log 1 E --mins 18 --hints 0       # log a solve
python dsa.py resolve 1                         # spaced re-solve (days 3, 7, 21)
python dsa.py journal "forgot the empty input"  # one-line journal
python dsa.py week next                         # move to the next roadmap week
python dsa.py target 3                          # change the daily target (default: 2 new + due re-solves)
```

Standard library only, so there's nothing to install.
