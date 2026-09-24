#!/bin/bash
# Hard stop at the window's close (cron, 08:00 Sun-Thu). The runner should
# already have drained; this kills any straggler. Killed runs have no DONE and
# re-run next window. Only touches our processes and swebench containers.
cd /home/avocoral/Documents/MarcoPolo
docker ps >/dev/null 2>&1 || exec sg docker -c "bash $0"
pkill -f "scripts/run_window.sh"; pkill -f "scripts/run_one.sh"
pkill -f "marcopolo.run_swebench"; pkill -f "swebench.harness.run_evaluation"
docker ps -a --format '{{.ID}} {{.Image}}' | awk '$2 ~ /swebench\/sweb\.eval/ {print $1}' | xargs -r docker rm -f >/dev/null 2>&1
bash scripts/vllm_ctl.sh stop
echo "$(date '+%F %T') hard stop at window close"
