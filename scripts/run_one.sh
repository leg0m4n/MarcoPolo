#!/bin/bash
# One run: agent -> evaluate submitted patch -> evaluate final state -> DONE.
#   bash scripts/run_one.sh <exp> <run_id> <instance_id> <condition> <n_fail_to_pass>
# Needs docker access and a live vLLM. Exit 3 = run invalid (server died), not scored.
set -u
cd /home/avocoral/Documents/MarcoPolo
export PYTHONPATH="$PWD/src" MSWEA_COST_TRACKING=ignore_errors
EXP=$1 RUN_ID=$2 IID=$3 COND=$4 NF2P=$5
PY=$PWD/.venv/bin/python
DS=SWE-bench/SWE-bench_Verified
RUN=results/$EXP/runs/$RUN_ID
lid=${IID,,}; IMG="docker.io/swebench/sweb.eval.x86_64.${lid//__/_1776_}:latest"
up() { curl -sf -o /dev/null --max-time 10 http://127.0.0.1:8100/v1/models; }

rm -rf "$RUN"; mkdir -p "$RUN"          # never inherit a half-finished predecessor
docker image inspect "$IMG" >/dev/null 2>&1 || {
  docker pull -q "$IMG" >/dev/null || { echo "PULL FAILED $IID"; exit 2; }
  echo "$IMG" >> "results/$EXP/pulled_images"; }

EXTRA=(); [ -f "configs/condition_${COND}.yaml" ] && EXTRA=(-c "configs/condition_${COND}.yaml")
t0=$(date +%s)
$PY -m marcopolo.run_swebench --subset "$DS" --split test --filter "^${IID}\$" -o "$RUN" -w 1 \
    -c swebench.yaml -c configs/north_vllm.yaml -c configs/pilot_env.yaml "${EXTRA[@]}" >"$RUN/agent.log" 2>&1
t1=$(date +%s)
docker ps -a -q --filter "ancestor=$IMG" | xargs -r docker rm -f >/dev/null 2>&1   # idle agent container

if ! up; then echo "INVALID $RUN_ID: vLLM died during the run"; exit 3; fi

# primary policy: the submitted patch
( cd "$RUN" && $PY -m swebench.harness.run_evaluation -d "$DS" -s test -i "$IID" \
    -p preds.json -id submitted --max_workers 1 >eval_submitted.log 2>&1 )
# secondary policy: final repository state, only needed when nothing was submitted
FINAL="$RUN/$IID/$IID.final.diff"
if ! $PY -c "import json,sys;sys.exit(0 if json.load(open('$RUN/preds.json'))['$IID'].get('model_patch') else 1)" \
   && [ -s "$FINAL" ]; then
  $PY -c "import json;json.dump({'$IID':{'instance_id':'$IID','model_name_or_path':'final-state','model_patch':open('$FINAL').read()}},open('$RUN/final_preds.json','w'))"
  ( cd "$RUN" && $PY -m swebench.harness.run_evaluation -d "$DS" -s test -i "$IID" \
      -p final_preds.json -id final --max_workers 1 >eval_final.log 2>&1 )
fi
t2=$(date +%s)
docker ps -a -q --filter "name=sweb.eval.${lid}" | xargs -r docker rm -f >/dev/null 2>&1

$PY -m marcopolo.metrics "$RUN" "$IID" "$NF2P" > "$RUN/metrics.json" || { echo "SCORING FAILED $RUN_ID"; exit 4; }
$PY -c "import json;m=json.load(open('$RUN/metrics.json'));m.update(condition='$COND',agent_s=$((t1-t0)),eval_s=$((t2-t1)));json.dump(m,open('$RUN/DONE','w'),indent=2)"
echo "DONE $RUN_ID: resolved=$($PY -c "import json;print(json.load(open('$RUN/DONE'))['resolved'])") agent $((t1-t0))s"
