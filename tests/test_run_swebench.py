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


SRC = "diff --git a/pkg/cart.py b/pkg/cart.py\n--- a/pkg/cart.py\n+++ b/pkg/cart.py\n@@ -1 +1 @@\n-a\n+b\n"
TST = "diff --git a/pkg/tests/test_cart.py b/pkg/tests/test_cart.py\n--- a/pkg/tests/test_cart.py\n+++ b/pkg/tests/test_cart.py\n@@ -1 +1 @@\n-assert x == 99\n+assert True\n"


def test_submitted_source_change_is_scored_test_edit_is_kept_aside(tmp_path):
    calls, meta = _run(tmp_path, FakeEnv(), submitted=SRC + TST)
    assert calls[0][3] == SRC, "only the source change reaches preds.json"
    assert meta["submitted_test_file_changes"] == ["pkg/tests/test_cart.py"]
    assert (tmp_path / "i1" / "i1.submitted_raw.diff").read_text() == SRC + TST


def test_capture_includes_untracked_files(tmp_path):
    env = FakeEnv()
    _run(tmp_path, env)
    assert "git add -A" in env.commands[0]


def test_dead_container_is_recorded_not_raised(tmp_path):
    _, meta = _run(tmp_path, FakeEnv(boom=True))
    assert meta["capture_status"].startswith("error")
    assert not (tmp_path / "i1" / "i1.final.diff").exists()
