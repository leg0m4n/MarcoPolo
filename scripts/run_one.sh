#!/bin/bash
# One run: agent -> evaluate submitted patch -> evaluate final state -> DONE.
#   bash scripts/run_one.sh <exp> <run_id> <instance_id> <condition> <n_fail_to_pass> [dataset]
# dataset: a Hugging Face name (default SWE-bench/SWE-bench_Verified) or a local task
# folder such as tasks/impossible_v1 (the agent loads the folder, the evaluator its test.jsonl)
# Needs docker access and a live vLLM. Exit 3 = run invalid (server died), not scored.
set -u
cd /home/avocoral/Documents/MarcoPolo
export PYTHONPATH="$PWD/src" MSWEA_COST_TRACKING=ignore_errors
EXP=$1 RUN_ID=$2 IID=$3 COND=$4 NF2P=$5 DS=${6:-SWE-bench/SWE-bench_Verified}
PY=$PWD/.venv/bin/python
EVAL_DS=$DS; [ -d "$DS" ] && EVAL_DS="$PWD/$DS/test.jsonl"
RUN=results/$EXP/runs/$RUN_ID
# image: explicit image_name for local tasks (impossible tasks are renamed), else derived
if [ -d "$DS" ]; then
  IMG=$($PY -c "import json,sys;print(next(json.loads(l)['image_name'] for l in open('$DS/test.jsonl') if json.loads(l)['instance_id']=='$IID'))")
else
  lid=${IID,,}; IMG="docker.io/swebench/sweb.eval.x86_64.${lid//__/_1776_}:latest"
fi
lid=${IID,,}
up() { curl -sf -o /dev/null --max-time 10 http://127.0.0.1:8100/v1/models; }

rm -rf "$RUN"; mkdir -p "$RUN"          # never inherit a half-finished predecessor
docker image inspect "$IMG" >/dev/null 2>&1 || {
  docker pull -q "$IMG" >/dev/null || { echo "PULL FAILED $IID"; exit 2; }
  echo "$IMG" >> "results/$EXP/pulled_images"; }

# experiment conditions add the check-aware template and their rung; "native" adds nothing
EXTRA=()
if [ "$COND" != native ]; then
  [ -f "configs/condition_${COND}.yaml" ] || { echo "UNKNOWN CONDITION $COND"; exit 5; }
  EXTRA=(-c configs/check_harness.yaml -c "configs/condition_${COND}.yaml")
fi
t0=$(date +%s)
$PY -m marcopolo.run_swebench --subset "$DS" --split test --filter "^${IID}\$" -o "$RUN" -w 1 \
    -c swebench.yaml -c configs/north_vllm.yaml -c configs/pilot_env.yaml "${EXTRA[@]}" >"$RUN/agent.log" 2>&1
t1=$(date +%s)
docker ps -a -q --filter "ancestor=$IMG" | xargs -r docker rm -f >/dev/null 2>&1   # idle agent container

if ! up; then echo "INVALID $RUN_ID: vLLM died during the run"; exit 3; fi

# primary policy: the submitted patch
( cd "$RUN" && $PY -m swebench.harness.run_evaluation -d "$EVAL_DS" -s test -i "$IID" \
    -p preds.json -id submitted --max_workers 1 >eval_submitted.log 2>&1 )
# secondary policy: final repository state. Evaluated separately unless it makes
# the same change as the submitted patch (the agent picks which files it submits).
FINAL="$RUN/$IID/$IID.final.diff"
SAME=$($PY -c "
import json, sys; sys.path.insert(0, 'src')
from marcopolo.patches import same_changes
sub = json.load(open('$RUN/preds.json'))['$IID'].get('model_patch') or ''
fin = open('$FINAL').read() if __import__('os').path.exists('$FINAL') else ''
same = same_changes(sub, fin)
json.dump({'final_equals_submitted': same, 'final_empty': not fin.strip()}, open('$RUN/final_policy.json', 'w'))
print('1' if same else '0')")
if [ "$SAME" = 0 ] && [ -s "$FINAL" ]; then
  $PY -c "import json;json.dump({'$IID':{'instance_id':'$IID','model_name_or_path':'final-state','model_patch':open('$FINAL').read()}},open('$RUN/final_preds.json','w'))"
  ( cd "$RUN" && $PY -m swebench.harness.run_evaluation -d "$EVAL_DS" -s test -i "$IID" \
      -p final_preds.json -id final --max_workers 1 >eval_final.log 2>&1 )
fi
t2=$(date +%s)
docker ps -a -q --filter "name=sweb.eval.${lid}" | xargs -r docker rm -f >/dev/null 2>&1

$PY -m marcopolo.metrics "$RUN" "$IID" "$NF2P" > "$RUN/metrics.json" || { echo "SCORING FAILED $RUN_ID"; exit 4; }
$PY -c "import json;m=json.load(open('$RUN/metrics.json'));m.update(condition='$COND',agent_s=$((t1-t0)),eval_s=$((t2-t1)));json.dump(m,open('$RUN/DONE','w'),indent=2)"
echo "DONE $RUN_ID: resolved=$($PY -c "import json;print(json.load(open('$RUN/DONE'))['resolved'])") agent $((t1-t0))s"
