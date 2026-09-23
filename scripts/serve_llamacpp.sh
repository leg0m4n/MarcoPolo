#!/bin/bash
# Fallback serving path: llama.cpp + Unsloth GGUF.
#
# Why this exists: vLLM's prebuilt wheels require a CUDA 13 driver (>=580);
# this box runs 550.120. llama.cpp builds against CUDA 12.4 and works today.
# See FINDINGS.md.
#
# --jinja is load-bearing: it makes llama-server use the model's own chat
# template for tool calls. Without it tool calling silently degrades, which
# the research plan warns would read as a model failure rather than a
# harness bug.
set -u
cd /home/avocoral/Documents/MarcoPolo

GGUF=${GGUF:-$HOME/.cache/huggingface/hub/models--unsloth--North-Mini-Code-1.0-GGUF/snapshots/*/North-Mini-Code-1.0-UD-Q4_K_S.gguf}
GGUF=$(ls $GGUF 2>/dev/null | head -1)
[ -z "$GGUF" ] && { echo "GGUF not found — is the download finished?"; exit 1; }

PORT=${PORT:-8101}
CTX=${CTX:-65536}

echo "serving: $GGUF"
exec ./vendor/llama.cpp/build/bin/llama-server \
  -m "$GGUF" \
  -ngl 99 \
  -c "$CTX" \
  --host 127.0.0.1 \
  --port "$PORT" \
  --jinja \
  --temp 1.0 \
  --top-p 0.95
