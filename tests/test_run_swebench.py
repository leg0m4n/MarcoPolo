"""The final-diff capture. If this breaks, overflowed runs lose their edits and
the tampering audit silently goes blind on most of the data."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo import run_swebench as rs  # noqa: E402


class FakeEnv:
    def __init__(self, output="diff --git a/x b/x\n", rc=0, boom=False):
        self.output, self.rc, self.boom, self.commands = output, rc, boom, []

    def execute(self, action, timeout=None):
        self.commands.append(action["command"])
        if self.boom:
            raise RuntimeError("container gone")
        return {"output": self.output, "returncode": self.rc}


CLEAN = {"leak": False, "future_commits": [], "fixed_files_found": [], "fix_lines_found_in": {}}


def _run(tmp_path, env, submitted="", leak=CLEAN, monkeypatch=None):
    calls, seen = [], {}
    env.container_id = "c1"
    own = monkeypatch is None
    if own:
        import pytest
        monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(rs.leakcheck, "check", lambda c, inst: leak)
    monkeypatch.setattr(rs.sandbox, "prepare_user", lambda c: None)
    monkeypatch.setattr(rs.sandbox, "sanitize", lambda c: None)
    get_env = rs._wrap_get_env(lambda config, inst: seen.update(config=config) or env)
    update = rs._wrap_update_preds(lambda *a: calls.append(a))
    try:
        get_env({"environment": {"run_args": ["--rm"]}}, {"instance_id": "i1"})
    finally:
        update(tmp_path / "preds.json", "i1", "m", submitted)
        if own:
            monkeypatch.undo()
    return calls, json.loads((tmp_path / "i1" / "i1.final.json").read_text()), seen


def test_diff_captured_even_when_nothing_submitted(tmp_path):
    calls, meta, _ = _run(tmp_path, FakeEnv())
    assert (tmp_path / "i1" / "i1.final.diff").read_text().startswith("diff --git")
    assert meta["capture_status"] == "ok" and meta["submitted"] is False
    assert calls, "original update_preds_file must still be called"


SRC = "diff --git a/pkg/cart.py b/pkg/cart.py\n--- a/pkg/cart.py\n+++ b/pkg/cart.py\n@@ -1 +1 @@\n-a\n+b\n"
TST = "diff --git a/pkg/tests/test_cart.py b/pkg/tests/test_cart.py\n--- a/pkg/tests/test_cart.py\n+++ b/pkg/tests/test_cart.py\n@@ -1 +1 @@\n-assert x == 99\n+assert True\n"


def test_submitted_source_change_is_scored_test_edit_is_kept_aside(tmp_path):
    calls, meta, _ = _run(tmp_path, FakeEnv(), submitted=SRC + TST)
    assert calls[0][3] == SRC, "only the source change reaches preds.json"
    assert meta["submitted_test_file_changes"] == ["pkg/tests/test_cart.py"]
    assert (tmp_path / "i1" / "i1.submitted_raw.diff").read_text() == SRC + TST


def test_capture_includes_untracked_files(tmp_path):
    env = FakeEnv()
    _run(tmp_path, env)
    assert "git add -A" in env.commands[0]


def test_dead_container_is_recorded_not_raised(tmp_path):
    _, meta, _ = _run(tmp_path, FakeEnv(boom=True))
    assert meta["capture_status"].startswith("error")
    assert not (tmp_path / "i1" / "i1.final.diff").exists()


def test_agent_container_is_always_sandboxed(tmp_path, monkeypatch):
    _, meta, seen = _run(tmp_path, FakeEnv(), monkeypatch=monkeypatch)
    assert seen["config"]["environment"]["run_args"] == rs.sandbox.AGENT_RUN_ARGS, "config cannot weaken it"
    assert seen["config"]["environment"]["env"]["BASH_ENV"] == rs.sandbox.BASH_ENV, "the agent's user gets the env"
    assert meta["leak_check"]["leak"] is False, "the leak check is recorded for every run"


def test_leaking_task_stops_before_the_agent_starts(tmp_path, monkeypatch):
    import pytest
    leak = {**CLEAN, "leak": True, "future_commits": ["abc 1 fix"]}
    with pytest.raises(rs.TaskLeak):
        _run(tmp_path, FakeEnv(), leak=leak, monkeypatch=monkeypatch)
    meta = json.loads((tmp_path / "i1" / "i1.final.json").read_text())
    assert meta["leak_check"]["future_commits"] == ["abc 1 fix"]


def test_setup_failure_is_invalid_not_an_agent_failure(tmp_path, monkeypatch):
    import pytest
    def broken(c):
        raise RuntimeError("no conda activation line")
    monkeypatch.setattr(rs.leakcheck, "check", lambda c, inst: CLEAN)
    monkeypatch.setattr(rs.sandbox, "prepare_user", broken)
    monkeypatch.setattr(rs.sandbox, "sanitize", lambda c: None)
    get_env = rs._wrap_get_env(lambda config, inst: FakeEnv())
    with pytest.raises(rs.SetupError):
        get_env({}, {"instance_id": "i2"})
