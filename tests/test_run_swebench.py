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


def _run(tmp_path, env, submitted=""):
    calls = []
    get_env = rs._wrap_get_env(lambda config, inst: env)
    update = rs._wrap_update_preds(lambda *a: calls.append(a))
    get_env({}, {"instance_id": "i1"})
    update(tmp_path / "preds.json", "i1", "m", submitted)
    return calls, json.loads((tmp_path / "i1" / "i1.final.json").read_text())


def test_diff_captured_even_when_nothing_submitted(tmp_path):
    calls, meta = _run(tmp_path, FakeEnv())
    assert (tmp_path / "i1" / "i1.final.diff").read_text().startswith("diff --git")
    assert meta["capture_status"] == "ok" and meta["submitted"] is False
    assert calls, "original update_preds_file must still be called"


def test_submitted_prediction_is_passed_through_unchanged(tmp_path):
    calls, _ = _run(tmp_path, FakeEnv(), submitted="PATCH")
    assert calls[0][3] == "PATCH"


def test_capture_includes_untracked_files(tmp_path):
    env = FakeEnv()
    _run(tmp_path, env)
    assert "git add -A" in env.commands[0]


def test_dead_container_is_recorded_not_raised(tmp_path):
    _, meta = _run(tmp_path, FakeEnv(boom=True))
    assert meta["capture_status"].startswith("error")
    assert not (tmp_path / "i1" / "i1.final.diff").exists()
