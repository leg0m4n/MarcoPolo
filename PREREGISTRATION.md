# Pre-registration — DRAFT

Marco Polo: feedback locality, cost and tampering in North Mini Code.
Design: `Signal Quality for Small Agents — Research Plan.pdf`.

**Status: draft.** Sections marked *decided* are fixed and will not change after
the first experiment run. Sections marked *open* must be settled before it. The
commit that removes the word DRAFT is the pre-registration; its git timestamp is
the record.

## Decided

### Model and serving *(2026-09-23)*
- `CohereLabs/North-Mini-Code-1.0-w4a16`, vLLM v0.30.0 built from source against
  CUDA 12.6 (driver 550.120 rules out prebuilt wheels). See `FINDINGS.md`.
- 64K context: KV cache pinned at 2.35 GiB, `--max-num-seqs 1`, CUDA graphs for
  batch size 1. 69 tok/s decode on a 4.4K-token prompt.
- `temperature 1.0`, `top_p 0.95`, Cohere's own evaluation settings.
- **`max_tokens 4096`** *(2026-09-24)*. The largest single turn in the pilot
  generated 2,201 tokens. Every request reserves this much of the 64K context,
  so a lower value leaves more room for the history.
- Reasoning is kept between turns (`marcopolo.models.NorthVLLMModel`). The stock
  harness silently drops it; see `FINDINGS.md`.

### Harness
- mini-swe-agent 2.4.6, SWE-bench template, one `bash` tool.
- No network inside agent containers (`--network none`).
- The final repository diff is recorded on every run, however it ends
  (`marcopolo.run_swebench`). The tampering audit reads these.

### Scoring *(2026-09-24)*
Two policies, both reported for every condition:

| policy | what is scored | role |
|---|---|---|
| **submitted** | the patch the agent explicitly submitted | **primary** |
| final | the repository state when the run ended, submitted or not | secondary |

They differ only for runs that end without submitting (in the pilot, runs that
filled the context). Richer feedback may reach a fix sooner and overflow less,
so the policy could change the size of a rung effect. Reporting both removes
the choice as a degree of freedom.

Per policy:

| metric | definition | role |
|---|---|---|
| resolved | every FAIL_TO_PASS test passes and no PASS_TO_PASS test breaks | **primary** |
| F2P fraction | share of FAIL_TO_PASS tests the patch makes pass | secondary |
| P2P broken | PASS_TO_PASS tests the patch breaks | secondary |

Plus, per run: turns, generated tokens, largest single turn, truncated turns
(`finish_reason == "length"`), context overflow, wall time.

### Compute *(2026-09-24)*
- Local RTX 3090, only inside the window agreed with the server's admin:
  nightly 23:00–08:00, plus all of Friday and Saturday (~93 h/week).
- No run starts within 30 min of a window closing; a hard stop at close kills
  and re-queues stragglers, which are not scored.
- A run during which the vLLM server dies is invalid and re-queued, not scored.

### Tasks
- `tasks/frozen_v1.json`: 40 SWE-bench Verified tasks, seed 0, >= 2
  FAIL_TO_PASS tests each (so rung 2 has something to disambiguate), at most 6
  per repository, difficulty < 4 h.

### Feedback rungs
- `src/marcopolo/rungs.py`, guarded by `tests/test_rungs.py`: outcome,
  location, diff, trace (assertion introspection + locals + unexecuted lines),
  and padded (outcome + information-free filler matched to trace length).

## Open — settle before the first experiment run

1. **Wiring `check`**: feedback only through a `check` tool that runs tests in a
   separate grader container, so the agent cannot bypass the rung.
2. **Impossible tasks (8)**: solvable tasks plus one test contradicting another.
3. **Post-June-2026 task slice**: how many, from where. The only contamination
   control; every SWE-bench Verified task predates Aug 2023.
4. **Tampering rubric**: what counts as mild / medium, and the hand-check sample.
5. **Rung-collapse check**: run `rungs.rung_deltas()` over every task; report how
   many tasks have rung 4 == rung 3.
6. **Final N**: sized from the pilot. Current estimate for 720 runs is ~97 GPU-hours,
   about one week of windows.
7. **Calibration slice**: where 15–20 tasks run at full precision.
8. **Detectable effect**: at 120 runs per condition, differences of roughly 15
   percentage points are reliably detectable; state this so a null result reads
   as "no effect larger than X".
