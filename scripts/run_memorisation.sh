#!/bin/bash
# One-off: the memorisation probe on the local model, inside the GPU window.
# Starts vLLM only if it is not already up, and stops it only if it started it.
set -u
cd /home/avocoral/Documents/MarcoPolo
export PYTHONPATH="$PWD/src"
PY=$PWD/.venv/bin/python
docker ps >/dev/null 2>&1 || exec sg docker -c "bash $0"
$PY -m marcopolo.schedule is-open || { echo "$(date '+%F %T') window closed; not running"; exit 0; }
up() { curl -sf -o /dev/null --max-time 10 http://127.0.0.1:8100/v1/models; }
started=0
if ! up; then bash scripts/vllm_ctl.sh start || exit 1; started=1; fi
$PY scripts/memorisation_probe.py vllm tasks/frozen_v3.json results/memorisation_v1_vllm
[ $started = 1 ] && bash scripts/vllm_ctl.sh stop
echo "$(date '+%F %T') memorisation probe finished"
