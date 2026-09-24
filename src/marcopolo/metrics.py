"""Per-run scoring, as pre-registered.

Two scoring policies, both reported:

  submitted (PRIMARY)  score only the patch the agent explicitly submitted.
                       "Fixed it, and knew it was done." Standard SWE-bench.
  final    (secondary) score the repository as it was when the run ended,
                       submitted or not. Differs only for runs that ended
                       without submitting, mostly by filling the context.

Why both: richer feedback may get agents to a fix sooner, so fewer runs
overflow. The policy choice can then change the size of the rung effect.

Per policy, three numbers:

  resolved      every target test passes and nothing that passed before breaks
  f2p_fraction  share of target (FAIL_TO_PASS) tests the patch makes pass —
                partial progress that `resolved` cannot see (secondary)
  p2p_broken    previously-passing (PASS_TO_PASS) tests the patch breaks —
                damage (secondary)

An empty patch scores f2p 0 and breaks nothing; the evaluator skips it and
writes no report, so those values are filled in here.

Both policies score source files only: test-file changes are stripped first and
kept for the tampering audit (see patches.py).
"""
from __future__ import annotations

import json
from pathlib import Path

from marcopolo.trajectory import load


def find_report(run_dir: Path, eval_id: str, instance_id: str) -> dict | None:
    for p in Path(run_dir).glob(f"logs/run_evaluation/{eval_id}/*/{instance_id}/report.json"):
        return json.loads(p.read_text()).get(instance_id)
    return None


def count_tests(report: dict | None, n_fail_to_pass: int) -> dict:
    """Resolved / f2p / p2p from one evaluator report; empty patch if None."""
    if not report:
        return {"resolved": False, "f2p_passed": 0, "f2p_total": n_fail_to_pass,
                "f2p_fraction": 0.0, "p2p_broken": 0, "patch_applied": False}
    ts = report.get("tests_status", {})
    f2p, p2p = ts.get("FAIL_TO_PASS", {}), ts.get("PASS_TO_PASS", {})
    passed = len(f2p.get("success", []))
    total = passed + len(f2p.get("failure", [])) or n_fail_to_pass
    return {"resolved": bool(report.get("resolved")), "f2p_passed": passed, "f2p_total": total,
            "f2p_fraction": passed / total if total else 0.0,
            "p2p_broken": len(p2p.get("failure", [])),
            "patch_applied": bool(report.get("patch_successfully_applied"))}


def score_run(run_dir: Path, instance_id: str, n_fail_to_pass: int) -> dict:
    """Everything the analysis needs for one run, under both policies."""
    run_dir = Path(run_dir)
    traj_path = run_dir / instance_id / f"{instance_id}.traj.json"
    traj = load(traj_path)
    info = json.loads(traj_path.read_text()).get("info", {})
    submitted = bool(info.get("submission"))

    sub = count_tests(find_report(run_dir, "submitted", instance_id), n_fail_to_pass)
    # The agent chooses which files go into its submitted patch, so the final
    # repository state can differ even when it submits. run_one.sh evaluates the
    # final state separately unless both make the same change.
    policy = run_dir / "final_policy.json"
    same = json.loads(policy.read_text()).get("final_equals_submitted", False) if policy.exists() else False
    final = sub if same else count_tests(find_report(run_dir, "final", instance_id), n_fail_to_pass)

    row = {
        "instance_id": instance_id,
        "final_equals_submitted": same,
        "exit_status": info.get("exit_status"),
        "submitted": submitted,
        "turns": len(traj.turns),
        "gen_tokens": traj.total_completion_tokens,
        "max_turn_tokens": max((t.completion_tokens for t in traj.turns), default=0),
        "truncated_turns": traj.n_truncated,
        "empty_turns": traj.n_empty,
    }
    row.update({k: v for k, v in sub.items()})
    row.update({f"{k}_final": v for k, v in final.items()})
    return row


if __name__ == "__main__":
    import sys
    print(json.dumps(score_run(Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])), indent=2))
