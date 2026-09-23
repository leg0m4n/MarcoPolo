"""Frozen task-set selection for the rung experiment.

Three constraints drive the selection, beyond the plan's "~40 solvable":

1. **Multi-test tasks.** 345 of 500 SWE-bench Verified instances have exactly
   one FAIL_TO_PASS test. On those, rung 1 ("1 test failed") and rung 2
   ("test_foo failed") differ only by a name — there is no "which of several"
   for rung 2 to disambiguate. Single-test tasks therefore compress the bottom
   of the rung curve. We prefer instances with >= 2 failing tests so rung 2
   carries real information.

2. **Repo spread.** django is 231 of 500. An unstratified sample is a django
   benchmark, and per-repo idiosyncrasies (test runner, error formatting)
   would confound the feedback-shape manipulation we care about.

3. **Difficulty spread.** Ceiling and floor effects both hide rung effects: a
   task the agent solves at rung 1 and a task it fails at rung 4 each
   contribute nothing to the curve.

Contamination: every SWE-bench Verified instance was created between 2013 and
2023-08-07, all well before North Mini Code's June 2026 release. Cohere
deduplicated its RL environments against SWE-bench repositories, but public
issues may still sit in pretraining data. This selection cannot rule that out;
the post-June-2026 task slice the plan calls for is what addresses it.
"""
from __future__ import annotations

import json
import random
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path

DATASET = "princeton-nlp/SWE-bench_Verified"
# Ceiling/floor risk lives at the extremes; keep the middle.
USABLE_DIFFICULTY = ("<15 min fix", "15 min - 1 hour", "1-4 hours")


@dataclass(frozen=True)
class Task:
    instance_id: str
    repo: str
    difficulty: str
    n_fail_to_pass: int
    created_at: str

    
def _n_tests(value) -> int:
    if isinstance(value, str):
        try:
            return len(json.loads(value))
        except Exception:
            return 0
    return len(value or [])


def select(n: int = 40, seed: int = 0, min_failing: int = 2,
           max_per_repo: int = 6) -> list[Task]:
    """Pick a frozen, reproducible task set.

    `min_failing` is the lever for constraint 1: raising it to 2 keeps only
    instances where rung 2 can actually disambiguate.
    """
    from datasets import load_dataset

    ds = load_dataset(DATASET, split="test")
    pool: list[Task] = []
    for row in ds:
        if row["difficulty"] not in USABLE_DIFFICULTY:
            continue
        k = _n_tests(row["FAIL_TO_PASS"])
        if k < min_failing:
            continue
        pool.append(Task(
            instance_id=row["instance_id"],
            repo=row["repo"],
            difficulty=row["difficulty"],
            n_fail_to_pass=k,
            created_at=str(row["created_at"])[:10],
        ))

    rng = random.Random(seed)
    rng.shuffle(pool)

    by_repo: dict[str, int] = defaultdict(int)
    chosen: list[Task] = []
    # Two passes: fill under the per-repo cap first, then relax if short.
    for cap in (max_per_repo, len(pool)):
        for t in pool:
            if len(chosen) >= n:
                break
            if t in chosen or by_repo[t.repo] >= cap:
                continue
            chosen.append(t)
            by_repo[t.repo] += 1
        if len(chosen) >= n:
            break

    return sorted(chosen, key=lambda t: t.instance_id)


def freeze(tasks: list[Task], path: Path) -> None:
    """Write the task set to disk. Commit this file before the first run."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(
        {"dataset": DATASET, "n": len(tasks),
         "tasks": [asdict(t) for t in tasks]}, indent=2), encoding="utf-8")
