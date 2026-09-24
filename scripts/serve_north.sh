#!/bin/bash
# Day-one test: serve North Mini Code w4a16 on RTX 3090 (compute 8.6, Ampere).
#
# Deviations from the model card's launch command, all forced by this box:
#  1. max-model-len 64K, not 320K. The card assumes an H100.
#     One 64K request needs 2.24 GiB of KV cache (measured; the plan estimated
#     1.9). Sizing KV from --gpu-memory-utilization overshoots in both
#     directions on this card: 0.87 gives too little KV, 0.92 sizes KV so large
#     that warmup OOMs. So KV is pinned directly at 2.35 GiB (~5% margin).
#     Result: 68,885-token KV cache, concurrency 1.05x at 64K.
#  2. --max-num-seqs 1. Only one 64K request fits anyway, and it makes vLLM
#     capture CUDA graphs for batch size 1 only: 0.07 GiB instead of 0.73.
#     Disabling graphs entirely (--enforce-eager) also reaches 64K but decodes
#     3x slower (22.7 vs 69.2 tok/s on a 4.4K-token prompt, measured with
#     scripts/bench_decode.py). Decode is ~90% of agent wall time.
#     Headroom ~1.3 GiB. Other tenants' GPU usage drifts (1.1 -> 2.0 GiB
#     observed in one day); if they grow further this will fail at startup.
#  3. torch is the cu126 build, not the cu130 default, because driver 550.120
#     caps at CUDA 12.4. vLLM's own kernels still link libcudart.so.13, so the
#     CUDA 13 runtime libs must be on LD_LIBRARY_PATH for import to succeed.
set -u
cd /home/avocoral/Documents/MarcoPolo

export LD_LIBRARY_PATH="$PWD/.venv-vllm26/lib/python3.11/site-packages/nvidia/cu13/lib:${LD_LIBRARY_PATH:-}"

MODEL=CohereLabs/North-Mini-Code-1.0-w4a16
PORT=${PORT:-8100}
MAXLEN=${MAXLEN:-65536}
UTIL=${UTIL:-0.90}
# 2.35 GiB = 2523293286 bytes
EXTRA=${EXTRA:---max-num-seqs 1 --kv-cache-memory-bytes 2523293286}

exec .venv-vllm/bin/vllm serve "$MODEL" \
  -tp 1 \
  --port "$PORT" \
  --max-model-len "$MAXLEN" \
  --gpu-memory-utilization "$UTIL" \
  --tool-call-parser cohere_command4 \
  --reasoning-parser cohere_command4 \
  --enable-auto-tool-choice \
  $EXTRA
