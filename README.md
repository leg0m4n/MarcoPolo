# Marco Polo

Feedback locality, cost and tampering in North Mini Code.

Does the *precision* of an agent's failure signal drive its capability, cost and
cheating as much as model choice does? This repo runs Cohere's open
[North Mini Code](https://huggingface.co/CohereLabs/North-Mini-Code-1.0) across
four feedback rungs on a frozen task set and reports all three side by side.

Full design: `Signal Quality for Small Agents — Research Plan.pdf`.
Environment constraints and what they cost: `FINDINGS.md`.

## The rungs

One bug, four levels of precision. Each rung narrows where the fault could be.

| Rung | What the agent sees | Example |
|---|---|---|
| 1 outcome | pass/fail only | `1 test failed.` |
| 2 location | which test failed | `test_ten_percent_discount failed` |
| 3 diff | expected vs actual, file and line | `assert 100.0 == 99.0` at `test_cart.py:9` |
| 4 trace | execution path or targeted probe | `where 100.0 = cart_total(..., discount=10.0)` |
| padded | rung 1 + information-free filler sized to rung 4 | controls for volume, not precision |

`padded` exists because more precise feedback is also more text. Without it, a
rung effect could be explained by token count alone.

## Layout

```
scripts/serve_llamacpp.sh    serve North Mini Code locally (llama.cpp, :8101)
scripts/serve_north.sh       same via vLLM (needs driver >=580 — see FINDINGS.md)
scripts/smoke_test.py        endpoint / tool-call parsing / reasoning separation
configs/north_llamacpp.yaml  mini-swe-agent pointed at the local endpoint
configs/check_harness.yaml   agent instructions for experiment runs (same for every rung)
configs/condition_*.yaml     one per feedback rung
src/marcopolo/rungs.py       the check tool: rung-limited feedback
src/marcopolo/tasks.py       frozen task-set selection
src/marcopolo/trajectory.py  trajectory analysis, truncation detection
tasks/frozen_v1.json         the pre-registered task set (40 tasks, 11 repos)
src/marcopolo/models.py      keeps the model's reasoning across turns on vLLM
src/marcopolo/run_swebench.py  runner that records the final diff on every exit
src/marcopolo/grader.py      the `check` tool: grader container, agent setup, interception
src/marcopolo/check.py       pytest output -> what each rung may show
src/marcopolo/patches.py     what is scored vs kept for the tampering audit
src/marcopolo/hardcoding.py  flags runs that paste a test's expected value into source
src/marcopolo/metrics.py     pre-registered scoring (both policies, secondary metrics)
src/marcopolo/schedule.py    the GPU window agreed with the server's admin
src/marcopolo/runqueue.py    resumable run queue
scripts/run_window.sh        cron entry: one window's worth of runs
scripts/run_one.sh           one run: agent, evaluation, scoring
scripts/report.py            per-condition summary of an experiment
scripts/preflight.py         validates every candidate task through the real `check`
tests/                       experimental guarantees as tests
PREREGISTRATION.md           decided and open design choices
```

## Running

```bash
# serve the model
bash scripts/serve_llamacpp.sh          # :8101

# verify it before trusting any numbers
.venv/bin/python scripts/smoke_test.py http://127.0.0.1:8101

# the rung logic must hold
.venv/bin/python -m pytest tests/ -q
```

## Three things that would have faked a result

Each is a condition that looks distinct in the design but collapses into its
neighbour on real data, in the direction the hypothesis predicts.

1. **Rung 3 → 4 collapse.** Coverage-based tracing only separates rung 4 from
   rung 3 for control-flow bugs. A wrong-value bug executes every line, so the
   two rungs become identical and the top of the curve flattens for reasons
   unrelated to the agent. Rung 4 now uses pytest's assertion introspection,
   which works for both bug classes. `rungs.rung_deltas()` reports per task
   whether the rungs are actually distinct — run it over the task set before
   the first real run.

2. **Rung 1 → 2 collapse.** 345 of 500 SWE-bench Verified instances have exactly
   one failing test, so rung 2 has nothing to disambiguate and differs from
   rung 1 by a name. `tasks.select(min_failing=2)` excludes them.

3. **Truncation masquerading as failure.** North Mini Code emits reasoning
   before content, so a tight `max_tokens` returns *empty content* with
   `finish_reason="length"` from a model that was working correctly. Richer
   rungs produce longer reasoning and therefore truncate more often — a rung
   effect that is purely a budget artifact. `trajectory.summarize()` reports
   truncation rate; it must be published next to any resolve rate.

## Environment

RTX 3090 (24 GB, compute 8.6), driver 550.120. vLLM's prebuilt wheels require a
CUDA 13 driver (>= 580), so the working path is llama.cpp with the Unsloth
Q4_K_S GGUF: 22.3 / 24.6 GB at 64K context, ~119 tok/s. `FINDINGS.md` has the
full diagnosis.
