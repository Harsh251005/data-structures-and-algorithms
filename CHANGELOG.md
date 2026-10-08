# Changelog

Every change to the system (tracker, roadmap, rules) gets a line here, newest first.

## 2026-10-08
- **LeetCode submit gate.** After each new problem I ask him to submit on LeetCode, and the next problem waits until he confirms.
- **Diff check before commits.** I check `git status`/`git diff` before every commit, stage only my own changes, and ask about any file he has edited.
- **Re-solves pass the tests gate too.** `dsa.py resolve` refuses until the `resolve/` file has 3 tests of your own, and `dsa.py check` reads the `resolve/` file first when one is open. Before, `check` counted the original solution file, so a re-solve with zero asserts passed.

## 2026-10-07
- Google Sheet: Summary's Total XP now includes re-solve XP (it showed 85 while the dashboard showed 100). README and the ROADMAP's calibration note now match the 191-problem goal.
- **Re-aimed at the real goal: DSA only, any medium in 25–35 minutes.** 🎯 Interview-ready is the goal level, gated by the Phase 5 review plus a final readiness review (2 back-to-back unseen mediums). Interview Mode moves up to Phase 6, right after DP. Advanced topics (tries, segment trees, hard week) become an optional Phase 7 stretch towards 🏆 Top-tier ready. SDE-specific wording and non-DSA prep are removed.
- **Honest levels.** Intern → Principal is replaced by Beginner → Foundations → Core → OA-ready → SDE-1 Interview-ready → Top-tier ready. Each level states what it means for hiring and what's still missing, and it is earned only by passing promotion reviews (`dsa.py event promotion`), never by XP. The dashboard shows what the current level means and the gate to the next one.
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
