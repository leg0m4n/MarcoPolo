#!/bin/bash
# One GPU window: start vLLM, drain the active experiment's queue while new
# runs may still start, stop vLLM. Idempotent; cron calls it every 15 minutes.
# The active experiment is named in results/ACTIVE_EXPERIMENT. No file = no-op.
set -u
cd /home/avocoral/Documents/MarcoPolo
export PYTHONPATH="$PWD/src"
PY=$PWD/.venv/bin/python
ts() { date '+%F %T'; }

$PY -m marcopolo.schedule is-open || exit 0
[ -s results/ACTIVE_EXPERIMENT ] || exit 0
EXP=$(tr -d '[:space:]' < results/ACTIVE_EXPERIMENT)
# under tmux sessions older than the docker group, re-enter with the group
docker ps >/dev/null 2>&1 || exec sg docker -c "bash $0"

exec 9>/tmp/marcopolo_window.lock
flock -n 9 || exit 0                       # another window runner is active
$PY -m marcopolo.schedule can-start || exit 0
$PY -m marcopolo.runqueue next "$EXP" >/dev/null || exit 0     # nothing to do

echo "$(ts) window open: $($PY -m marcopolo.schedule status) | $($PY -m marcopolo.runqueue stats $EXP)"
bash scripts/vllm_ctl.sh start || { echo "$(ts) vLLM would not start; giving up this round"; exit 1; }

while $PY -m marcopolo.schedule can-start; do
  spec=$($PY -m marcopolo.runqueue next "$EXP") || { echo "$(ts) queue empty"; break; }
  read -r RUN_ID IID COND NF2P <<< "$spec"
  echo "$(ts) start $RUN_ID"
  bash scripts/run_one.sh "$EXP" "$RUN_ID" "$IID" "$COND" "$NF2P"
  rc=$?
  if [ $rc -eq 3 ]; then                   # server died: restart once, retry the run later
    bash scripts/vllm_ctl.sh stop; bash scripts/vllm_ctl.sh start || break
  fi
  # last run of this task done: remove its image if we pulled it
  if [ "$($PY -m marcopolo.runqueue pending-for "$EXP" "$IID")" = 0 ]; then
    lid=${IID,,}; img="docker.io/swebench/sweb.eval.x86_64.${lid//__/_1776_}:latest"
    grep -qxF "$img" "results/$EXP/pulled_images" 2>/dev/null && docker rmi "$img" >/dev/null 2>&1
  fi
done
bash scripts/vllm_ctl.sh stop
echo "$(ts) window runner exiting | $($PY -m marcopolo.runqueue stats $EXP)"
