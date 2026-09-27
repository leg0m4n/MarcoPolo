#!/bin/bash
# One-off: the memorisation probe on the local model, inside the GPU window,
# then hand the GPU to the main experiment (appended to ACTIVE_EXPERIMENT, which
# the window runner picks up on its next 15-minute tick, reusing this vLLM).
# Run first so the two never share the GPU: the experiment's timings stay clean.
set -u
cd /home/avocoral/Documents/MarcoPolo
export PYTHONPATH="$PWD/src"
PY=$PWD/.venv/bin/python
docker ps >/dev/null 2>&1 || exec sg docker -c "bash $0"
$PY -m marcopolo.schedule is-open || { echo "$(date '+%F %T') window closed; not running"; exit 0; }
up() { curl -sf -o /dev/null --max-time 10 http://127.0.0.1:8100/v1/models; }
up || bash scripts/vllm_ctl.sh start || exit 1
$PY scripts/memorisation_probe.py vllm tasks/frozen_v3.json results/memorisation_v1_vllm
echo "$(date '+%F %T') memorisation probe finished (exit $?)"
grep -qx "${HANDOVER:-final_v1}" results/ACTIVE_EXPERIMENT || echo "${HANDOVER:-final_v1}" >> results/ACTIVE_EXPERIMENT
echo "$(date '+%F %T') handed over to ${HANDOVER:-final_v1}"
$PY -m marcopolo.schedule can-start || bash scripts/vllm_ctl.sh stop
