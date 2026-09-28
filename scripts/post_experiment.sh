#!/bin/bash
# Runs in the GPU window once every experiment queue is empty (run_window.sh),
# with vLLM up. Resumable: exit 0 only when finished, and run_window.sh then
# writes results/post_experiment.done so it never runs again.
# 2026-09-28: the sampled memorisation probe (3 samples/task; FINDINGS.md).
set -u
cd /home/avocoral/Documents/MarcoPolo
export PYTHONPATH="$PWD/src"
.venv/bin/python scripts/memorisation_probe.py vllm tasks/frozen_v3.json results/memorisation_v2_sampled 3
