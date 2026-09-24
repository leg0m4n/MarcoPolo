"""mini-swe-agent's SWE-bench runner, plus a final diff on every exit.

The plan requires logging every diff, because the tampering audit reads them.
Stock mini-swe-agent only records the patch an agent *submits*. When a run ends
any other way — most often the context window filling, which happened on the
first two pilot tasks — the container is deleted and every edit the agent made
is lost, unseen. The audit is blind exactly where it matters.

This wraps two module functions rather than copying the runner:
  - get_sb_environment: remember each instance's live environment
  - update_preds_file:  called in the runner's `finally`, after the trajectory
    is saved and before the container is torn down — capture the diff there

The final diff is recorded for the audit, NOT substituted into preds.json.
Whether an unsubmitted diff also counts toward the resolve rate is a separate,
pre-registered policy decision.

Usage: identical to `mini-extra swebench`:
    python -m marcopolo.run_swebench --subset ... --filter ... -o OUT -c ...
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

from minisweagent.run.benchmarks import swebench as sb

# `git add -A` so new, untracked files are included; the container is discarded
# afterwards, so touching its index is harmless.
FINAL_DIFF_CMD = "cd /testbed && git add -A >/dev/null 2>&1 && git diff --cached --no-color HEAD"

_envs: dict[str, object] = {}
_lock = threading.Lock()


def capture_final_diff(env) -> tuple[str | None, str]:
    """Return (diff, status). diff is None when it could not be captured."""
    try:
        out = env.execute({"command": FINAL_DIFF_CMD}, timeout=120)
    except Exception as e:  # container already gone, timeout, ...
        return None, f"error: {type(e).__name__}"
    if out.get("returncode") != 0:
        return None, f"git exited {out.get('returncode')}"
    return out.get("output", ""), "ok"


def _wrap_get_env(original):
    def get_sb_environment(config, instance):
        env = original(config, instance)
        with _lock:
            _envs[instance["instance_id"]] = env
        return env
    return get_sb_environment


def _wrap_update_preds(original):
    def update_preds_file(output_path: Path, instance_id: str, model_name: str, result: str):
        with _lock:
            env = _envs.pop(instance_id, None)
        instance_dir = Path(output_path).parent / instance_id
        instance_dir.mkdir(parents=True, exist_ok=True)
        if env is not None:
            diff, status = capture_final_diff(env)
        else:
            diff, status = None, "no environment (failed before start)"
        if diff is not None:
            (instance_dir / f"{instance_id}.final.diff").write_text(diff, encoding="utf-8")
        (instance_dir / f"{instance_id}.final.json").write_text(json.dumps({
            "instance_id": instance_id,
            "capture_status": status,
            "final_diff_chars": len(diff) if diff is not None else None,
            "submitted_patch_chars": len(result or ""),
            "submitted": bool(result),
        }, indent=2), encoding="utf-8")
        return original(output_path, instance_id, model_name, result)
    return update_preds_file


def install() -> None:
    """Patch the runner module in place. Idempotent."""
    if getattr(sb, "_marcopolo_installed", False):
        return
    sb.get_sb_environment = _wrap_get_env(sb.get_sb_environment)
    sb.update_preds_file = _wrap_update_preds(sb.update_preds_file)
    sb._marcopolo_installed = True


if __name__ == "__main__":
    install()
    sb.app()
