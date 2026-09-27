"""Resumability: a run killed at the window's close must run again, not vanish."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo import runqueue as rq  # noqa: E402


def _setup(tmp_path, monkeypatch):
    monkeypatch.setattr(rq, "ROOT", tmp_path)
    tf = tmp_path / "tasks.json"
    tf.write_text(json.dumps({"tasks": [{"instance_id": "a__a-1", "n_fail_to_pass": 2},
                                        {"instance_id": "b__b-2", "n_fail_to_pass": 3}]}))
    return rq.build("exp", str(tf), ["rung1", "rung2"], 2)


def test_ordered_by_task_so_images_are_reused(tmp_path, monkeypatch):
    specs = _setup(tmp_path, monkeypatch)
    assert [s["instance_id"] for s in specs] == ["a__a-1"] * 4 + ["b__b-2"] * 4


def test_run_without_done_stays_pending(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    first = rq.pending("exp")[0]["run_id"]
    (tmp_path / "exp/runs" / first).mkdir(parents=True)          # killed mid-run: dir, no DONE
    assert rq.pending("exp")[0]["run_id"] == first
    (tmp_path / "exp/runs" / first / "DONE").write_text("{}")
    assert rq.pending("exp")[0]["run_id"] != first


def test_queue_is_never_overwritten(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    try:
        rq.build("exp", str(tmp_path / "tasks.json"), ["x"], 1)
    except SystemExit:
        return
    raise AssertionError("rebuilding a queue must refuse")


def test_run_failing_for_infrastructure_is_parked_not_retried_forever(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    first = rq.pending("exp")[0]["run_id"]
    for _ in range(rq.MAX_INVALID - 1):
        rq.record_invalid("exp", first)
    assert rq.pending("exp")[0]["run_id"] == first, "still retried"
    rq.record_invalid("exp", first)
    assert first not in [r["run_id"] for r in rq.pending("exp")], "parked after the limit"


def test_leaking_task_is_parked_at_once(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    first = rq.pending("exp")[0]["run_id"]
    rq.park("exp", first)
    assert first not in [r["run_id"] for r in rq.pending("exp")]
