"""Run the memorisation probe (src/marcopolo/memorisation.py) on a task set.

One call per task: repository + issue in, patch out. No code, no tools.

The answer is PRE-FILLED with the start of a diff, and the model continues it.
Without that, North Mini Code will not answer: shown an issue, it only tries to
explore (on Cohere's API, every variant — no tools, a system message, a
submit tool, a stub bash tool — ended in a rejected tool call or in
`pwd`, `ls`, `find / -name separable.py`; FINDINGS.md). Cohere's API cannot
pre-fill, so the probe runs on the local model (vLLM `continue_final_message`),
inside the GPU window.

    set -a; . ~/.config/marcopolo/cohere.env; set +a
    python scripts/memorisation_probe.py vllm [tasks/frozen_v3.json] [results/memorisation_v1_vllm]

Resumable: tasks already in responses.jsonl are skipped. Writes report.json.
"""
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

from datasets import load_dataset
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from marcopolo import memorisation as mem  # noqa: E402

BACKENDS = {
    "cohere": ("https://api.cohere.ai/compatibility/v1", "north-mini-code-1-0", "COHERE_API_KEY"),
    "vllm": ("http://127.0.0.1:8100/v1", "CohereLabs/North-Mini-Code-1.0-w4a16", None),
}
# reasoning comes first and counts against max_tokens; the local server's
# 64K context leaves room, the hosted one has 256K
MAX_TOKENS = 16000
TEMPERATURE = 0.0          # the model's most likely answer: what memory would produce
PREFILL = "Here is the maintainers' fix, as I remember it:\n\n```diff\n--- a/"

backend = sys.argv[1]
tasks_file = ROOT / (sys.argv[2] if len(sys.argv) > 2 else "tasks/frozen_v3.json")
out_dir = ROOT / (sys.argv[3] if len(sys.argv) > 3 else f"results/memorisation_v1_{backend}")
base, model, key_var = BACKENDS[backend]
if backend != "vllm":
    raise SystemExit("only the vllm backend can pre-fill the answer; see the docstring")
client = OpenAI(base_url=base, api_key=os.environ[key_var] if key_var else "sk-noop", timeout=600)

rows = {r["instance_id"]: r for r in load_dataset("SWE-bench/SWE-bench_Verified", split="test")}
tasks = [t["instance_id"] for t in json.loads(tasks_file.read_text())["tasks"]]
out_dir.mkdir(parents=True, exist_ok=True)
resp_file = out_dir / "responses.jsonl"
done = {json.loads(l)["instance_id"]: json.loads(l) for l in resp_file.read_text().splitlines()} \
    if resp_file.exists() else {}

for i, iid in enumerate(tasks, 1):
    if iid in done:
        continue
    row = rows[iid]
    prompt = mem.PROMPT.format(repo=row["repo"], issue=row["problem_statement"])
    for attempt in range(4):
        try:
            t0 = time.time()
            r = client.chat.completions.create(
                model=model, temperature=TEMPERATURE, max_tokens=MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}, {"role": "assistant", "content": PREFILL}],
                extra_body={"continue_final_message": True, "add_generation_prompt": False})
            break
        except Exception as e:            # rate limit / transient: back off, then give up on this task
            print(f"  {iid}: {type(e).__name__}, retry {attempt + 1}", flush=True)
            time.sleep(30 * (attempt + 1))
    else:
        continue
    msg = r.choices[0].message
    rec = {"instance_id": iid, "repo": row["repo"], "backend": backend, "model": model,
           "answer": PREFILL + (msg.content or ""), "finish_reason": r.choices[0].finish_reason,
           "reasoning": getattr(msg, "reasoning_content", None) or getattr(msg, "reasoning", None),
           "completion_tokens": r.usage.completion_tokens if r.usage else None,
           "seconds": round(time.time() - t0, 1)}
    with resp_file.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    done[iid] = rec
    print(f"[{i}/{len(tasks)}] {iid} {rec['finish_reason']} {rec['completion_tokens']} tok", flush=True)

# score
by_repo = defaultdict(list)
for iid in tasks:
    if iid in done:
        by_repo[rows[iid]["repo"]].append(iid)
report = []
for iid in tasks:
    if iid not in done:
        continue
    row, ans = rows[iid], done[iid]["answer"]
    gold = mem.gold_lines(row["patch"], row["problem_statement"])
    r = mem.recall(gold, ans)
    others = [mem.recall(gold, done[o]["answer"]) for o in by_repo[row["repo"]] if o != iid]
    others = [x for x in others if x is not None]
    report.append({"instance_id": iid, "gold_lines": len(gold), "recall": r,
                   "chance": round(sum(others) / len(others), 3) if others else None,
                   "files_named": mem.files_named(row["patch"], ans),
                   "finish_reason": done[iid]["finish_reason"], "verdict": mem.verdict(gold, r)})
summary = {v: sum(x["verdict"] == v for x in report) for v in ("flagged", "clear", "unassessable")}
(out_dir / "report.json").write_text(json.dumps({"backend": backend, "model": model, "rule": {
    "min_line": mem.MIN_LINE, "min_gold": mem.MIN_GOLD, "flag_recall": mem.FLAG_RECALL},
    "summary": summary, "tasks": report}, indent=2))
print(summary)
for x in sorted(report, key=lambda x: -(x["recall"] or 0)):
    print(f"  {x['verdict']:12} recall {x['recall'] if x['recall'] is None else round(x['recall'], 2)!s:5} "
          f"chance {x['chance']!s:5} gold {x['gold_lines']:3} files {x['files_named']} {x['instance_id']}")
