"""Summarise a pilot run and project the full experiment's cost.

The plan's week-1 exit criterion is "tokens per run measured", and its scale-up
rule is: hours = runs x tokens per run / measured tokens per second. If that
exceeds a few days, rent H100 time for the bulk.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo.trajectory import load  # noqa: E402

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "results/pilot")
FULL_RUNS = 48 * 5 * 3          # plan: ~48 tasks x 5 conditions x 3 attempts
TASKS = 48

timing = {r["instance_id"]: r for r in csv.DictReader(open(OUT / "timing.tsv"), delimiter="\t")}
reports = {p.parent.name: next(iter(json.load(open(p)).values()))
           for p in OUT.glob("logs/run_evaluation/*/*/*/report.json")}

rows = []
for iid, tm in timing.items():
    traj = OUT / iid / f"{iid}.traj.json"
    if not traj.exists():
        continue
    t = load(traj)
    info = json.loads(traj.read_text()).get("info", {})
    rep = reports.get(iid, {})
    ts = rep.get("tests_status", {})
    f2p, p2p = ts.get("FAIL_TO_PASS", {}), ts.get("PASS_TO_PASS", {})
    nf = len(f2p.get("success", [])) + len(f2p.get("failure", []))
    rows.append({
        "id": iid, "exit": info.get("exit_status"), "resolved": bool(rep.get("resolved")),
        "f2p": f"{len(f2p.get('success', []))}/{nf}" if nf else "-",
        "p2p_broken": len(p2p.get("failure", [])),
        "turns": len(t.turns), "gen_tok": t.total_completion_tokens,
        "max_turn_tok": max((x.completion_tokens for x in t.turns), default=0),
        "truncated": t.n_truncated,
        "agent_s": int(tm["agent_s"]), "eval_s": int(tm["eval_s"]), "pull_s": int(tm["pull_s"]),
    })

print(f"{'task':34}{'exit':28}{'res':>5}{'F2P':>7}{'broke':>6}{'turns':>6}{'gen tok':>9}{'max/turn':>9}{'trunc':>6}{'min':>6}")
for r in rows:
    print(f"{r['id']:34}{str(r['exit']):28}{'yes' if r['resolved'] else 'no':>5}{r['f2p']:>7}{r['p2p_broken']:>6}"
          f"{r['turns']:>6}{r['gen_tok']:>9,}{r['max_turn_tok']:>9}{r['truncated']:>6}{r['agent_s']/60:>6.1f}")

n = len(rows) or 1
mean_agent = sum(r["agent_s"] for r in rows) / n
mean_eval = sum(r["eval_s"] for r in rows) / n
mean_pull = sum(r["pull_s"] for r in rows) / n
per_run = mean_agent + mean_eval
total_h = (FULL_RUNS * per_run + TASKS * mean_pull) / 3600
print(f"\nresolved {sum(r['resolved'] for r in rows)}/{len(rows)} | "
      f"context overflows {sum(r['exit'] == 'ContextWindowExceededError' for r in rows)} | "
      f"truncated turns {sum(r['truncated'] for r in rows)} | "
      f"max tokens in any turn {max((r['max_turn_tok'] for r in rows), default=0)}")
print(f"mean per run: agent {mean_agent/60:.1f} min + eval {mean_eval:.0f} s; "
      f"mean {sum(r['turns'] for r in rows)/n:.0f} turns, {sum(r['gen_tok'] for r in rows)/n:,.0f} generated tokens")
print(f"projection: {FULL_RUNS} runs -> {total_h:.0f} GPU-hours = {total_h/24:.1f} days on this card (serial)")
