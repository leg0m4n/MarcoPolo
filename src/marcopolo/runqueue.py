"""The run queue: every run of an experiment, listed up front, resumable.

results/<exp>/queue.json     ordered run specs
results/<exp>/runs/<run_id>/ one directory per run; DONE marks it complete

A run without DONE is pending, including one killed mid-way at the window's
close. run_one.sh wipes a pending run's directory before starting, so a
re-queued run never inherits a half-finished predecessor.

Runs are ordered by task, so each task's Docker image is pulled once and
deleted after its last run.

CLI:
    python -m marcopolo.runqueue build <exp> <tasks.json> <cond,cond,..> <attempts>
    python -m marcopolo.runqueue next <exp>            # "run_id instance cond n_f2p dataset", exit 1 if done
    python -m marcopolo.runqueue pending-for <exp> <instance_id>
    python -m marcopolo.runqueue stats <exp>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "results"
DEFAULT_DATASET = "SWE-bench/SWE-bench_Verified"


def build(exp: str, tasks_file: str, conditions: list[str], attempts: int) -> list[dict]:
    tasks = json.loads(Path(tasks_file).read_text())["tasks"]
    specs = [{"run_id": f"{t['instance_id']}__{c}__a{a}", "instance_id": t["instance_id"],
              "condition": c, "attempt": a, "n_fail_to_pass": t["n_fail_to_pass"],
              "dataset": t.get("dataset", DEFAULT_DATASET)}
             for t in tasks for c in conditions for a in range(1, attempts + 1)]
    d = ROOT / exp
    if (d / "queue.json").exists():
        raise SystemExit(f"{d/'queue.json'} exists; refusing to overwrite a pre-registered queue")
    d.mkdir(parents=True, exist_ok=True)
    (d / "queue.json").write_text(json.dumps({"tasks_file": tasks_file, "conditions": conditions,
                                              "attempts": attempts, "runs": specs}, indent=2))
    return specs


def runs(exp: str) -> list[dict]:
    return json.loads((ROOT / exp / "queue.json").read_text())["runs"]


def is_done(exp: str, run_id: str) -> bool:
    return (ROOT / exp / "runs" / run_id / "DONE").exists()


def pending(exp: str) -> list[dict]:
    return [r for r in runs(exp) if not is_done(exp, r["run_id"])]


def _main(argv: list[str]) -> int:
    cmd, exp = argv[1], argv[2]
    if cmd == "build":
        specs = build(exp, argv[3], argv[4].split(","), int(argv[5]))
        print(f"{len(specs)} runs queued in results/{exp}/queue.json")
    elif cmd == "next":
        p = pending(exp)
        if not p:
            return 1
        r = p[0]
        print(r["run_id"], r["instance_id"], r["condition"], r["n_fail_to_pass"],
              r.get("dataset", DEFAULT_DATASET))
    elif cmd == "pending-for":
        print(sum(r["instance_id"] == argv[3] for r in pending(exp)))
    elif cmd == "stats":
        total, left = len(runs(exp)), len(pending(exp))
        print(f"{exp}: {total - left}/{total} done, {left} pending")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
