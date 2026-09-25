# Marco Polo — design summary for sign-off

*Two pages. The full record is `PREREGISTRATION.md`; evidence is in `FINDINGS.md`.*

## The question

When a coding agent's change fails, does **how precisely the failure is reported**
change whether it fixes the bug, what the fix costs, and whether it cheats?
Tested on Cohere's open North Mini Code, holding the model and harness fixed and
varying only the feedback.

## The experiment

| | |
|---|---|
| Model | North Mini Code 1.0, official 4-bit checkpoint (w4a16), local RTX 3090, 64K context |
| Harness | mini-swe-agent, one `bash` tool; test results only through a `check` command |
| Tasks | 40 SWE-bench Verified tasks (pytest repos, ≥2 target tests each) + 8 impossible tasks |
| Conditions | 5 feedback rungs (below) |
| Runs | 48 tasks × 5 conditions × 3 attempts = **720** |
| Compute | ~97 GPU-hours, run only in the admin's window (nights, Fri, Sat) ≈ one week |

| rung | what `check` shows the agent |
|---|---|
| 1 outcome | "3 tests failed." |
| 2 location | which tests failed |
| 3 diff | + error and expected-vs-actual, file:line |
| 4 trace | + the call path and the variable values at the failure |
| padded | rung 1 + neutral filler as long as rung 4 (separates *information* from *length*) |

## Decisions, one line each

**Feedback (`check`)**
- The agent can't run pytest; `check` runs the tests in a separate container, so the rung can't be bypassed.
- `check` uses the tests as the agent left them; scoring uses the originals — tampering can "work" for the agent but never helps the score.
- Rung 4 shows call path + values, not coverage: coverage adds nothing for wrong-value bugs.
- At most 20 failing tests listed; full detail for the first 5 at rungs 3–4 — keeps feedback from eating the context.
- Pass/fail decided by SWE-bench's own parser and id-matching, so `check` and scoring can never disagree.

**Tasks**
- pytest repos only: other test runners format errors differently, which is itself variation in feedback.
- ≥2 target tests per task: with one, rung 2 has nothing to point at (69% of SWE-bench would collapse rung 1 into 2).
- Every task pre-flighted through the real `check`: the fix passes, the unfixed code fails, no network needed. 40 of 46 passed.
- Impossible tasks: a real task plus one inverted copy of a target test; only tampering satisfies both. Built by a fixed rule, verified with the official evaluator.

**Scoring**
- Headline: the submitted patch resolves the task. Also reported: the code's final state (catches "fixed it, then ran out of room").
- Secondary: share of target tests fixed; previously-passing tests broken.
- Test-file edits are stripped from scored patches and kept for the tampering audit.
- Hidden tests replaced by an automatic hard-coding detector; written hidden tests may be added later, blind, as a declared secondary analysis.

**Analysis**
- Primary: the trend in resolve rate across rungs 1→4, compared within each task. All else is secondary.
- Detectable: roughly 16–21 points on a pairwise contrast at a 20% base rate; the trend test does better. A null is reported as "no effect larger than X".
- 95% bootstrap intervals, every run published including failures.

**Integrity (tampering)**
- Automatic flags: test edits, pasted expected values, test-detecting code, `check` "passing" an impossible task.
- A blind human spot-check of 60 runs measures how often the flags are right.

## What building it caught

Each of these would have produced a fake rung effect or corrupted results; each is fixed and guarded by a test.
Stock harness **dropped the model's reasoning every turn** · reasoning **exhausted `max_tokens`**, truncating richer rungs more · rung 4 **collapsed into rung 3** on value bugs · **coloured output** silently blanked rungs 3–4 on 8 tasks · **network-dependent** tests made tasks unwinnable · SWE-bench's **truncated test ids** broke matching · padding filler was **misleading**, not neutral.

## Still open

1. **Contamination control** (post-June-2026 tasks): no ready source; build a few, or state as a limitation.
2. **Tampering spot-check rater**: you, or me.
3. **Calibration** (full-precision vs our 4-bit) — and possibly **where the whole experiment runs**: see the reply.

## Reading list

1. **Soft-SVeRL** — Cohere Labs, 2026. [arXiv 2605.28561](https://arxiv.org/abs/2605.28561).
   The paper this project extends: partial-credit rewards, and a self-verifying model that games its own grader. It names multi-turn agents as future work — your opening.
2. **ImpossibleBench** — Zhong, Raghunathan, Carlini, ICLR 2026. [arXiv 2510.20270](https://arxiv.org/abs/2510.20270).
   Closest prior work for Leg 3: impossible SWE-bench variants, cheating measured as their pass rate, and feedback loops shown to change it. Know it cold; your difference is feedback *precision* as a graded variable, measured with capability and cost, on a small open model.
3. **SWE-agent** — Yang et al., NeurIPS 2024. [arXiv 2405.15793](https://arxiv.org/abs/2405.15793).
   Shows that the interface an agent works through changes what it can do. mini-swe-agent descends from it; "feedback locality" is one dimension of that interface.
4. **HarnessTax** — Pan, Yang, Arabzadeh, Chiang, Stoica, Zaharia, Sept 2026. [harnesstax.github.io](https://harnesstax.github.io/).
   Harness choice barely moves success but moves cost up to 5×. Closest prior work for Leg 1; your protocol copies theirs (3 attempts, bootstrap intervals) so results line up.
5. **The Leaderboard Illusion** — Singh et al., Cohere Labs, 2025. [arXiv 2504.20879](https://arxiv.org/abs/2504.20879).
   The rigor bar your Cohere readers set: selective disclosure distorts results. It is why everything here is pre-registered and every run published.
