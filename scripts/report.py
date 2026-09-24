"""Summarise an experiment's finished runs, per condition, both scoring policies.

    python scripts/report.py <exp>
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

exp = sys.argv[1]
root = Path(__file__).resolve().parents[1] / "results" / exp
queue = json.loads((root / "queue.json").read_text())["runs"]
done = [json.loads(p.read_text()) for p in sorted(root.glob("runs/*/DONE"))]
print(f"{exp}: {len(done)}/{len(queue)} runs done\n")
if not done:
    sys.exit(0)

print(f"{'instance':32}{'cond':9}{'exit':28}{'res':>5}{'res*':>5}{'F2P':>7}{'broke':>6}{'turns':>6}{'tok':>8}{'max':>6}{'trunc':>6}{'min':>6}")
for r in done:
    print(f"{r['instance_id']:32}{r['condition']:9}{str(r['exit_status']):28}"
          f"{'yes' if r['resolved'] else 'no':>5}{'yes' if r['resolved_final'] else 'no':>5}"
          f"{r['f2p_passed']:>3}/{r['f2p_total']:<3}{r['p2p_broken']:>6}{r['turns']:>6}"
          f"{r['gen_tokens']:>8,}{r['max_turn_tokens']:>6}{r['truncated_turns']:>6}{r['agent_s']/60:>6.1f}")
print("res = submitted patch (primary) | res* = final repository state (secondary)\n")

by = defaultdict(list)
for r in done:
    by[r["condition"]].append(r)
for cond, rs in by.items():
    n = len(rs)
    print(f"[{cond}] n={n} | resolved {sum(r['resolved'] for r in rs)}/{n}"
          f" (final-state {sum(r['resolved_final'] for r in rs)}/{n})"
          f" | mean F2P fraction {sum(r['f2p_fraction'] for r in rs)/n:.2f}"
          f" (final {sum(r['f2p_fraction_final'] for r in rs)/n:.2f})"
          f" | tests broken {sum(r['p2p_broken'] for r in rs)}"
          f" | context overflows {sum(r['exit_status'] == 'ContextWindowExceededError' for r in rs)}"
          f" | truncated turns {sum(r['truncated_turns'] for r in rs)}"
          f" | mean {sum(r['agent_s'] for r in rs)/n/60:.1f} min/run")
