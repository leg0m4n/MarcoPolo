#!/bin/bash
# Start / stop / check the vLLM server as a background process (no tmux).
# Used by the window runner under cron; safe to call by hand.
#   bash scripts/vllm_ctl.sh start|stop|status
set -u
cd /home/avocoral/Documents/MarcoPolo
PIDF=results/vllm.pid
LOG=results/vllm.log
URL=http://127.0.0.1:8100/v1/models
mkdir -p results

up() { curl -sf -o /dev/null --max-time 5 "$URL"; }

case "${1:-status}" in
  start)
    up && { echo "vLLM already up"; exit 0; }
    # refuse to start if the admin's processes are using more than expected
    used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
    if [ "$used" -gt 3000 ]; then
      echo "REFUSING: GPU already has ${used} MiB in use (expected ~1200 from other tenants)"; exit 1
    fi
    setsid nohup bash scripts/serve_north.sh >"$LOG" 2>&1 < /dev/null &
    echo $! > "$PIDF"
    for i in $(seq 1 60); do
      sleep 10
      up && { echo "vLLM up after $((i*10))s (pid $(cat $PIDF))"; exit 0; }
      kill -0 "$(cat $PIDF)" 2>/dev/null || break
    done
    echo "vLLM FAILED to start; last log lines:"; tail -5 "$LOG"
    bash "$0" stop; exit 1 ;;
  stop)
    [ -f "$PIDF" ] && kill -- -"$(cat $PIDF)" 2>/dev/null
    pkill -f "vllm serve CohereLabs/North-Mini-Code" 2>/dev/null
    for i in $(seq 1 30); do
      pgrep -f "vllm serve CohereLabs/North-Mini-Code" >/dev/null || break; sleep 2
    done
    pkill -9 -f "vllm serve CohereLabs/North-Mini-Code" 2>/dev/null
    rm -f "$PIDF"
    echo "vLLM stopped; GPU in use: $(nvidia-smi --query-gpu=memory.used --format=csv,noheader)" ;;
  status)
    up && echo "vLLM UP" || echo "vLLM DOWN" ;;
esac
