# Changelog

Every change to the system (tracker, roadmap, rules) gets a line here, newest first.

## 2026-10-07
- **Cold re-solve files.** Re-solves are typed into a fresh file in `resolve/` (gitignored), so the original solution stays out of sight. The scratch file is deleted after `dsa.py resolve`.

## 2026-10-06
- **Units replace calendar weeks.** Each unit is a problem list. It ends when the list is done, and the next unit starts by itself. `dsa.py next` sets up the next problem, and `dsa.py unit` replaces `week`.
- **Pace-based dates.** The dashboard's ROADMAP section estimates the next unit, the phase end and the full roadmap from the last 7 days' pace.
- **Daily target stays at 2 new problems minimum, with no banking.** Extra problems pull the dates forward but don't buy days off.
- **Re-solve cap.** A day that starts with 4 or more re-solves due has a target of 1 new problem.
- **Quality gate.** A unit averaging 3 or more hints needs 2 reinforcement problems (`dsa.py add`) before it's done.
- `dsa.py new` files a problem under the unit that lists it, not the "current week".
- Fixed: the tracker's "Next re-solve" ignored the tighter schedule for viewed solutions (LC 121 showed 9 Oct, but it is due 7 Oct).
- Moved LC 26, 27, 88 and 121 from the Week 1 folder to `phase1_foundations/week02_arrays_strings/`.
- Earlier today: tests gate (`log` needs 3 of my own tests), pattern cards, Friday Gauntlet, timebox.
