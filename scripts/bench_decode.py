"""Benchmark one serving config: prompt processing vs decode, on a realistic prompt.

Pilot agent turns averaged ~4,800 prompt tokens and ~120 generated, so the
prompt here is sized to match. Streaming separates time-to-first-token
(prefill) from the inter-token rate (decode). Each round uses a fresh prompt
prefix so the prefix cache does not flatter prefill.

Usage: python scripts/bench_decode.py [base_url] [label]
"""
import json
import statistics
import sys
import time
import urllib.request
from pathlib import Path

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8100"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "config"
ROUNDS, GEN = 3, 512

model = json.loads(urllib.request.urlopen(f"{BASE}/v1/models", timeout=30).read())["data"][0]["id"]
# ~4,800 tokens of real Python source, like an agent reading files
src = Path(".venv/lib/python3.11/site-packages/minisweagent/run/benchmarks/swebench.py").read_text()
body = (src * 3)[:19000]

ttfts, rates = [], []
for i in range(ROUNDS):
    prompt = f"[round {i} {time.time()}]\n" + body + "\n\nExplain what process_instance does, in detail."
    req = urllib.request.Request(f"{BASE}/v1/chat/completions", data=json.dumps({
        "model": model, "messages": [{"role": "user", "content": prompt}],
        "max_tokens": GEN, "min_tokens": GEN, "temperature": 0, "stream": True,
        "stream_options": {"include_usage": True}}).encode(),
        headers={"Content-Type": "application/json"})
    t0, first, n, ptoks = time.time(), None, 0, 0
    with urllib.request.urlopen(req, timeout=600) as r:
        for raw in r:
            line = raw.decode().strip()
            if not line.startswith("data: ") or line == "data: [DONE]":
                continue
            ev = json.loads(line[6:])
            if ev.get("usage"):
                ptoks, n = ev["usage"]["prompt_tokens"], ev["usage"]["completion_tokens"]
            if ev.get("choices") and first is None:
                d = ev["choices"][0].get("delta", {})
                if d.get("content") or d.get("reasoning") or d.get("reasoning_content"):
                    first = time.time()
    end = time.time()
    ttfts.append(first - t0)
    rates.append((n - 1) / (end - first))
    print(f"  round {i}: prompt {ptoks} tok | TTFT {first - t0:.2f}s | decode {rates[-1]:.1f} tok/s ({n} tok)")

print(f"{LABEL}: median TTFT {statistics.median(ttfts):.2f}s | median decode {statistics.median(rates):.1f} tok/s")
