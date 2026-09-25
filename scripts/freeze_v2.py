"""Freeze the v2 task set from the pre-flight.

    python scripts/freeze_v2.py [--cap N] [--seed S]

Writes tasks/frozen_v2.json — every pre-flight admit, at most `cap` per
repository (seeded choice within a repo) — and prints the rung-collapse report.
Impossible-task selection lives in scripts/make_impossible.py.
"""
import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("--cap", type=int, default=8)
ap.add_argument("--seed", type=int, default=0)
a = ap.parse_args()

cands = {t["instance_id"]: t for t in json.loads((ROOT / "tasks/candidates_v2.json").read_text())["tasks"]}
pf = [json.loads(l) for l in (ROOT / "results/preflight_v2.jsonl").read_text().splitlines()]
admitted = [r for r in pf if r["admitted"]]
rejected = [r for r in pf if not r["admitted"]]
if any(r["reason"].startswith("HARNESS") for r in rejected):
    raise SystemExit("pre-flight has HARNESS rejections: investigate before freezing")

rng = random.Random(a.seed)
by_repo = defaultdict(list)
for r in sorted(admitted, key=lambda r: r["instance_id"]):
    by_repo[r["repo"]].append(r)
frozen = []
for repo in sorted(by_repo):
    rs = by_repo[repo][:]
    rng.shuffle(rs)
    frozen += rs[:a.cap]
frozen.sort(key=lambda r: r["instance_id"])

tasks = [{**cands[r["instance_id"]], "check_seconds": r.get("check_seconds"), "test_files": r.get("test_files"),
          "rung_chars": r.get("rung_chars")} for r in frozen]
(ROOT / "tasks/frozen_v2.json").write_text(json.dumps({
    "source": "SWE-bench/SWE-bench_Verified", "preflight": "results/preflight_v2.jsonl",
    "rule": f"every pre-flight admit, at most {a.cap} per repository (seed {a.seed})",
    "n": len(tasks), "tasks": tasks}, indent=2))

print(f"pre-flight: {len(admitted)} admitted, {len(rejected)} rejected")
for why, n in Counter(r["reason"].split(";")[0] for r in rejected).most_common():
    print(f"   {n:3}  {why}")
print(f"\nfrozen_v2: {len(tasks)} tasks (cap {a.cap}/repo)")
for repo, n in Counter(t["repo"] for t in tasks).most_common():
    print(f"   {n:3}  {repo}")

adj = [("location", "outcome"), ("diff", "location"), ("trace", "diff")]
print("\nrung collapse (tasks where the higher rung shows nothing more):")
for hi, lo in adj:
    same = [t["instance_id"] for t in tasks if t["rung_chars"] and t["rung_chars"][hi] == t["rung_chars"][lo]]
    print(f"   {hi:>8} == {lo:<8} {len(same):3} task(s) {same[:4]}")
