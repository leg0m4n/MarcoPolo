# Day-one serving test — result

**Date:** 2026-09-22
**Question (plan, p.7):** does `North-Mini-Code-1.0-w4a16` serve in vLLM on an
RTX 3090 (Ampere, compute 8.6), given the model card names only Hopper and Ada?

## Result: blocked before the question could be answered

The Ampere question is **still open**. A prior constraint stops us first:

> **vLLM cannot run on this machine at all, at any version, with driver 550.120.**

This is not an Ampere limitation. It would block an A100 or a 4090 on the same
driver equally.

## Evidence

| Step | Outcome |
|---|---|
| vLLM 0.30.0 stock | `CUDA initialization: driver too old (found 12040)` — ships torch 2.13.0+**cu130**, needs driver ≥580 |
| Every release 0.23.0–0.30.0 | all pin `torch==2.11.0`/`2.13.0`, default builds are cu130 |
| vLLM 0.26.0 + torch 2.11.0+**cu128** | GPU initialises. Model load fails: `AttributeError: 'RoutedExperts' object has no attribute 'w2_bias'` — model code predates this checkpoint |
| vLLM 0.30.0 + torch 2.13.0+**cu126** (+ matching torchvision/torchaudio) | imports, loads model code, then dies in vLLM's own kernel: `cuda_view.cu:38 cudaHostGetDevicePointer failed: CUDA driver version is insufficient for CUDA runtime version` |

Root cause: vLLM's precompiled extensions link `libcudart.so.13` and call CUDA 13
runtime APIs. Supplying the CUDA 13 libraries lets the module *import*, but the
kernels still require a CUDA 13-capable driver at execution time. Swapping torch
to a CUDA 12 build cannot fix this — the CUDA 13 dependency is in vLLM's binary,
not torch's.

## Environment

- GPU: RTX 3090, 24 GB, compute capability 8.6
- Driver: 550.120 (max CUDA 12.4), Lambda stack on Ubuntu 20.04
- nvcc: 12.6 available locally
- Checkpoint: downloaded and verified, 19.4 GB, 13 files
- `cohere_melody` 0.15.0 installs cleanly
- `cohere_command4` tool + reasoning parsers present in vLLM ≥0.23.0

## Consequence for the plan

Page 11 marked the compute path as settled ("local RTX 3090 at 4-bit plus a
hosted calibration slice"). That decision predates this constraint and needs
revisiting. Three options:

1. **Build vLLM from source against CUDA 12.6.** nvcc 12.6 is present. Produces
   kernels linking libcudart.so.12. Multi-hour build, historically fragile.
2. **Upgrade driver to ≥580.** Cleanest. Requires admin: unloading the NVIDIA
   module kills two long-running services (root's `server_pool_detect`, 33d;
   banknote's `readfromvid`, 22d).
3. **llama.cpp + Unsloth GGUF.** The plan's stated fallback; driver-agnostic.
   Plan's own caveat applies: verify tool-call and reasoning parsing match
   vLLM's, or parser errors will read as model failures.

Only after one of these can the original Ampere/w4a16 question be tested.

## Note for the write-up

"Runs on a single H100" is true and also insufficient as a deployment claim. The
binding constraint here was the CUDA toolchain floor in the serving stack, not
the model or the card's memory. For a project about small models being locally
deployable, that gap between "fits in 24 GB" and "runs on the machine you have"
is worth a paragraph.

---

# llama.cpp fallback — WORKING (2026-09-22)

The fallback path serves North Mini Code on the 3090 today, on driver 550.120.

## Configuration

- llama.cpp built from source, `GGML_CUDA=ON`, `CMAKE_CUDA_ARCHITECTURES=86`,
  gcc 9.4 (system). Builds in ~15 min.
- `unsloth/North-Mini-Code-1.0-UD-Q4_K_S.gguf`, 18.0 GB
- `llama-server -ngl 99 -c 65536 --jinja --temp 1.0 --top-p 0.95`
- GPU: 22347 / 24576 MiB with 64K context. Q4_K_M (19.2 GB) would likely not
  leave enough for KV at this context length.

## Smoke test results

| Check | Result |
|---|---|
| Server responds | PASS |
| Tool call parses | **PASS** — `run_tests({"path": "tests/test_cart.py"})` |
| Reasoning returned separately | PASS — `reasoning_content`, 162 chars |
| Reasoning preserved between turns | enabled by default per chat template |

## Throughput

**118.7 tok/s** generation (800 completion tokens in 6.7 s, 140-token prompt).

Fast because only ~3B of the 30B parameters are active per token. At this rate a
trajectory averaging 20K output tokens takes ~3 min, so the plan's 720 runs are
roughly 34 GPU-hours. Feasible. This is generation only — prefill cost at long
context is not yet measured and matters once trajectories fill 64K.

## Gotcha: reasoning consumes the max_tokens budget

With reasoning enabled, short completion budgets return **empty content**:

| max_tokens | content | reasoning | finish_reason |
|---|---|---|---|
| 32 | `''` | 136 chars | `length` |
| 512 | `'OK'` | 162 chars | `stop` |

The model is fine; the budget is spent on reasoning before any content is
emitted. A harness that caps completion tokens tightly will record empty
responses and score them as failures.

This is the plan's "parser errors pass as model failures" hazard in a different
guise, and it interacts directly with Leg 1: **richer feedback rungs produce
longer reasoning**, so a fixed max_tokens would truncate high-rung conditions
more often than low-rung ones — manufacturing a rung effect that is purely an
artifact of the token budget.

**Mitigation:** set a generous max_tokens, and log `finish_reason` on every turn.
Any run with `finish_reason == "length"` must be identifiable at analysis time.
Consider it a pre-registered exclusion or a reported category.

---

# vLLM on Ampere — ANSWERED: yes (2026-09-22)

The plan's day-one question — does `North-Mini-Code-1.0-w4a16` serve in vLLM on
an RTX 3090 (compute 8.6), given the card names only Hopper and Ada?

**Yes.** The card's omission of Ampere is incomplete documentation, not a
limitation.

## How

Prebuilt wheels cannot work (CUDA 13 driver requirement). vLLM v0.30.0 built
from source against CUDA 12.6:

- conda-forge gcc 13.4 (system gcc 9.4 is too old; no sudo needed)
- `TORCH_CUDA_ARCH_LIST=8.6`, `MAX_JOBS=8`, torch 2.13.0+cu126
- torchvision/torchaudio must be force-reinstalled from the cu126 index *after*
  the build — the build pulls cu130 versions back in and breaks the match
- Rust extensions (`vllm-rs`, `_rust_tool_parser`) fail to build: system cargo
  1.75 does not accept `resolver = "3"` (needs >= 1.84). **They are optional**;
  both Cohere parsers load via the Python path.
- Build takes ~3 h, much of it on Hopper-only FA3 kernels this card cannot use.

## Confirmation from the server log

```
Using 'MARLIN' NvFp4 MoE backend out of potential backends: [...]
WARNING: Your GPU does not have native support for FP4 computation but
         FP4 quantization is being used
Application startup complete.
```

The Marlin path is real and selected automatically. FP4 is emulated.

## Hard limit: 32K context, concurrency 1

```
GPU KV cache size: 34,056 tokens
Maximum concurrency for 32,768 tokens per request: 1.04x
```

Free memory is 22.01 / 23.68 GiB — two other tenants hold 1.67 GiB — so
`gpu_memory_utilization` cannot exceed ~0.93. After ~19.4 GiB of weights and
0.73 GiB of CUDA graphs, the KV cache holds **34,056 tokens total**.

**The plan's 64K context cap is not achievable under vLLM on this card**, and
only one request can be in flight. llama.cpp reaches 64K with the same card
because its Q4_K_S weights are 18.0 GB rather than 19.4 GB and it captures no
CUDA graphs.

## Both stacks agree on tool calls; they disagree on reasoning

| | llama.cpp Q4_K_S | vLLM w4a16 |
|---|---|---|
| Tool call | `run_tests({"path": "tests/test_cart.py"})` | **identical** |
| Generation | 118.7 tok/s | 90.7 tok/s |
| Max context | 65,536 | 32,768 |
| reasoning field | `reasoning_content`, 162 chars | **`reasoning`**, 588 chars |
| max_tokens=32 | `''`, finish=length | `None`, finish=length |

Tool-call agreement across two independent stacks is strong evidence the
parsing is right — the cross-check the plan wanted.

**RESOLVED — the stacks use different field names.** Both emit reasoning
correctly. vLLM returns it as `reasoning`; llama.cpp returns it as
`reasoning_content`. An earlier entry here claimed vLLM emitted none; that was
an artifact of checking only `reasoning_content`.

The hazard is real but different from what it first looked like: **any harness
reading only one field name silently drops reasoning on the other stack.** The
model card requires reasoning to be kept between tool calls, and the plan notes
that dropping it forces replanning — so this would sandbag one stack and read
as a capability difference between quantizations. `scripts/smoke_test.py` and
`trajectory.py` now accept either name and warn when neither is present.

The truncation behaviour is identical on both, confirming that confound is a
property of the model, not of one serving stack.

---

# vLLM at 64K context (2026-09-23)

The 32K limit above was a sizing artifact, not a hard limit.

| Attempt | KV cache | Outcome |
|---|---|---|
| util 0.92, CUDA graphs | 34,056 tokens | serves, 32K only |
| util 0.92, `--enforce-eager` | 89,901 tokens | OOM during warmup — KV oversized |
| util 0.87 / 0.89, `--enforce-eager` | 1.88 GiB | refused: 64K needs **2.24 GiB** |
| util 0.90, `--enforce-eager`, `--kv-cache-memory-bytes 2.35GiB` | **68,885 tokens** | **serves 64K**, concurrency 1.05x |

- One 64K request needs **2.24 GiB** of KV cache. The plan's estimate was 1.9.
- `--enforce-eager` frees the ~0.7 GiB CUDA graphs use, at some speed cost
  (not yet measured at 64K).
- Pinning KV directly avoids vLLM's utilization-based sizing, which overshoots
  on a card this full.

**Risk:** ~0.5 GiB headroom. Other tenants' GPU usage drifted from 1.1 to
2.0 GiB in a day. Startup will fail if they grow further, and a serve that
dies mid-run must be detected and the affected runs re-queued, not scored.
