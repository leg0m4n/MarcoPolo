#!/bin/bash
# One GPU window: start vLLM, drain the active experiment's queue while new
# runs may still start, stop vLLM. Idempotent; cron calls it every 15 minutes.
# results/ACTIVE_EXPERIMENT lists experiments, one per line, run in that order:
# the first with pending runs is worked on. No file (or nothing pending) = no-op.
set -u
cd /home/avocoral/Documents/MarcoPolo
export PYTHONPATH="$PWD/src"
PY=$PWD/.venv/bin/python
ts() { date '+%F %T'; }

$PY -m marcopolo.schedule is-open || exit 0
[ -s results/ACTIVE_EXPERIMENT ] || exit 0
next_exp() {   # first listed experiment that still has pending runs
  while read -r e; do
    [ -n "$e" ] && [ -f "results/$e/queue.json" ] && $PY -m marcopolo.runqueue next "$e" >/dev/null && { echo "$e"; return 0; }
  done < results/ACTIVE_EXPERIMENT
  return 1
}
# under tmux sessions older than the docker group, re-enter with the group
docker ps >/dev/null 2>&1 || exec sg docker -c "bash $0"

exec 9>/tmp/marcopolo_window.lock
flock -n 9 || exit 0                       # another window runner is active
$PY -m marcopolo.schedule can-start || exit 0
EXP=$(next_exp) || exit 0                  # nothing to do

echo "$(ts) window open: $($PY -m marcopolo.schedule status) | $($PY -m marcopolo.runqueue stats $EXP)"
bash scripts/vllm_ctl.sh start || { echo "$(ts) vLLM would not start; giving up this round"; exit 1; }

while $PY -m marcopolo.schedule can-start; do
  EXP=$(next_exp) || { echo "$(ts) all queues empty"; break; }
  spec=$($PY -m marcopolo.runqueue next "$EXP")
  read -r RUN_ID IID COND NF2P DS <<< "$spec"
  echo "$(ts) [$EXP] start $RUN_ID"
  bash scripts/run_one.sh "$EXP" "$RUN_ID" "$IID" "$COND" "$NF2P" "$DS"
  rc=$?
  if [ $rc -eq 3 ]; then                   # invalid (server/API error): not scored, retried later
    n=$($PY -m marcopolo.runqueue invalid "$EXP" "$RUN_ID")
    [ "$n" -ge 3 ] && echo "$(ts) PARKED $RUN_ID after $n infrastructure failures: needs a human"
    bash scripts/vllm_ctl.sh stop; bash scripts/vllm_ctl.sh start || break
  elif [ $rc -eq 7 ]; then                 # the fix is findable in the task's container: never retried
    $PY -m marcopolo.runqueue park "$EXP" "$RUN_ID" >/dev/null
    echo "$(ts) PARKED $RUN_ID: the task's real fix is findable in its container (leak_check in final.json)"
  fi
  # no pending run needs this image any more: remove it if we pulled it
  img=$($PY -c "import json,sys;print(next(r.get('image','') for r in json.load(open('results/$EXP/queue.json'))['runs'] if r['run_id']=='$RUN_ID'))")
  if [ -n "$img" ] && [ "$($PY -m marcopolo.runqueue pending-image "$EXP" "$img")" = 0 ]; then
    grep -qxF "$img" "results/$EXP/pulled_images" 2>/dev/null && docker rmi "$img" >/dev/null 2>&1
  fi
done
bash scripts/vllm_ctl.sh stop
echo "$(ts) window runner exiting"
while read -r e; do [ -f "results/$e/queue.json" ] && echo "  $($PY -m marcopolo.runqueue stats $e)"; done < results/ACTIVE_EXPERIMENT
