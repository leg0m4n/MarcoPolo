#!/bin/bash
# Week-1 pilot: 5 SWE-bench Verified tasks at native feedback (no rung filtering).
# Measures what the plan's scale-up rule needs: tokens/run, turns, truncation,
# wall time. Tasks are pre-registered in tasks/pilot_v1.json.
#
# Run under the docker group:   sg docker -c "bash scripts/run_pilot.sh"
#
# Shared host: this only ever removes images it pulled itself, and the
# evaluation container it created. Never prunes.
set -u
cd /home/avocoral/Documents/MarcoPolo
export PYTHONPATH="$PWD/src"
export MSWEA_COST_TRACKING=ignore_errors

OUT=results/pilot
DS=SWE-bench/SWE-bench_Verified
PY=.venv/bin/python
mkdir -p "$OUT"
[ -f "$OUT/timing.tsv" ] || printf "instance_id\tpull_s\tagent_s\teval_s\timage_preexisted\n" > "$OUT/timing.tsv"

IDS=$($PY -c "import json;print(' '.join(t['instance_id'] for t in json.load(open('tasks/pilot_v1.json'))['tasks']))")

for id in $IDS; do
  echo "=================== $id ==================="
  if ! curl -sf -o /dev/null --max-time 10 http://127.0.0.1:8100/v1/models; then
    echo "ABORT: vLLM not answering on :8100 — results from here would be server failures, not agent failures"
    exit 2
  fi

  lid=${id,,}
  img="docker.io/swebench/sweb.eval.x86_64.${lid//__/_1776_}:latest"
  pre=0; docker image inspect "$img" >/dev/null 2>&1 && pre=1

  t0=$(date +%s)
  [ $pre -eq 1 ] || docker pull -q "$img" || { echo "PULL FAILED $id"; continue; }
  t1=$(date +%s)

  .venv/bin/mini-extra swebench --subset "$DS" --split test --filter "^${id}\$" \
      -o "$OUT" -w 1 \
      -c swebench.yaml -c configs/north_vllm.yaml -c configs/pilot_env.yaml
  t2=$(date +%s)

  ( cd "$OUT" && ../../$PY -m swebench.harness.run_evaluation \
      -d "$DS" -s test -i "$id" -p preds.json -id pilot \
      --max_workers 1 --report_dir eval )
  t3=$(date +%s)

  printf "%s\t%s\t%s\t%s\t%s\n" "$id" $((t1-t0)) $((t2-t1)) $((t3-t2)) $pre >> "$OUT/timing.tsv"

  # mini-swe-agent does not always stop its container when a run ends on an
  # exception (e.g. context overflow); it idles on `sleep 2h` and keeps the
  # image in use. Remove only containers started from OUR image, then the image.
  docker rm -f "sweb.eval.${lid}.pilot" >/dev/null 2>&1
  docker ps -a -q --filter "ancestor=$img" | xargs -r docker rm -f >/dev/null 2>&1
  if [ $pre -eq 0 ] && ! docker rmi "$img" >/dev/null 2>&1; then
    echo "WARNING: could not remove $img — check for leftover containers"
  fi
  echo "done $id: agent $((t2-t1))s, eval $((t3-t2))s | disk free: $(df -h /home | awk 'NR==2{print $4}')"
done
echo PILOT_DONE
