"""The pre-registered scoring. A wrong definition here changes every result."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo.metrics import score_run, count_tests  # noqa: E402

REPORT = {"resolved": False, "patch_successfully_applied": True, "tests_status": {
    "FAIL_TO_PASS": {"success": ["a"] * 12, "failure": ["b"] * 8},
    "PASS_TO_PASS": {"success": ["c"] * 318, "failure": ["d"] * 4}}}


def test_partial_progress_is_measured():
    c = count_tests(REPORT, 20)
    assert (c["resolved"], c["f2p_passed"], c["f2p_total"], c["p2p_broken"]) == (False, 12, 20, 4)
    assert c["f2p_fraction"] == 0.6


def test_empty_patch_scores_zero_and_breaks_nothing():
    c = count_tests(None, 3)
    assert (c["resolved"], c["f2p_passed"], c["f2p_total"], c["p2p_broken"]) == (False, 0, 3, 0)


def _run(tmp_path, submission, sub_report=None, final_report=None, same=False):
    iid = "x__x-1"
    d = tmp_path / iid
    d.mkdir()
    (tmp_path / "final_policy.json").write_text(json.dumps({"final_equals_submitted": same}))
    (d / f"{iid}.traj.json").write_text(json.dumps({
        "info": {"exit_status": "Submitted" if submission else "ContextWindowExceededError",
                 "submission": submission}, "messages": []}))
    for eid, rep in (("submitted", sub_report), ("final", final_report)):
        if rep is not None:
            p = tmp_path / "logs/run_evaluation" / eid / "model" / iid
            p.mkdir(parents=True)
            (p / "report.json").write_text(json.dumps({iid: rep}))
    return score_run(tmp_path, iid, 20)


def test_final_reuses_submitted_score_only_when_changes_match(tmp_path):
    r = _run(tmp_path, "PATCH", sub_report=REPORT, same=True)
    assert r["f2p_passed"] == r["f2p_passed_final"] == 12


def test_submission_that_omits_a_changed_file_is_scored_separately(tmp_path):
    """The agent picks which files go into patch.txt; it can leave out a fix."""
    fixed = dict(REPORT, resolved=True, tests_status={
        "FAIL_TO_PASS": {"success": ["a"] * 20, "failure": []},
        "PASS_TO_PASS": {"success": ["c"] * 322, "failure": []}})
    r = _run(tmp_path, "PATCH", sub_report=REPORT, final_report=fixed, same=False)
    assert r["resolved"] is False and r["resolved_final"] is True


def test_overflowed_run_primary_zero_final_counts(tmp_path):
    fixed = dict(REPORT, resolved=True, tests_status={
        "FAIL_TO_PASS": {"success": ["a"] * 20, "failure": []},
        "PASS_TO_PASS": {"success": ["c"] * 322, "failure": []}})
    r = _run(tmp_path, "", final_report=fixed)
    assert r["resolved"] is False, "primary policy scores only what was submitted"
    assert r["resolved_final"] is True, "final-state policy sees the working fix"
