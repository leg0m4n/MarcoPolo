"""Tests for the feedback rungs.

These encode the experimental guarantees, not just code behaviour. If one of
these fails, the rung conditions are no longer what was pre-registered and any
run using them is invalid.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo.rungs import CheckResult, RUNGS, render, rung_deltas  # noqa: E402


def _failing() -> CheckResult:
    return CheckResult(
        passed=1, failed=1,
        failures=[{
            "test": "test_cart.py::test_ten_percent_discount",
            "message": "AssertionError: assert 100.0 == 99.0",
            "path": "/repo/test_cart.py",
            "lineno": 9,
            "longrepr": (
                "def test_ten_percent_discount():\n"
                ">       assert cart_total(ITEMS, discount=10.0) == 99.0\n"
                "E       AssertionError: assert 100.0 == 99.0\n"
                "E        +  where 100.0 = cart_total([{'price': 50.0}], discount=10.0)\n"
            ),
        }],
        uncovered=["cart.py:12 never executed"],
    )


def test_passing_is_identical_across_rungs():
    """A pass carries no fault information, so every rung says the same thing."""
    ok = CheckResult(passed=2, failed=0)
    assert {render(ok, r) for r in RUNGS} == {"All tests passed."}


def test_rungs_are_monotonic_in_length():
    """Each rung must be at least as informative as the one below it."""
    res = _failing()
    lens = [len(render(res, r, Path("/repo"))) for r in ("outcome", "location", "diff", "trace")]
    assert lens == sorted(lens), lens
    assert len(set(lens)) == len(lens), f"a rung collapsed into its neighbour: {lens}"


def test_outcome_leaks_no_test_name():
    """Rung 1 must not identify which test failed — that is rung 2's job."""
    body = render(_failing(), "outcome")
    assert "test_ten_percent_discount" not in body
    assert body == "1 test failed."


def test_location_leaks_no_values():
    """Rung 2 names the test but must not reveal expected vs actual."""
    body = render(_failing(), "location")
    assert "test_ten_percent_discount" in body
    assert "100.0" not in body and "99.0" not in body


def test_trace_adds_probe_over_diff():
    """Rung 4's whole purpose is signal rung 3 does not have."""
    res = _failing()
    diff = render(res, "diff", Path("/repo"))
    trace = render(res, "trace", Path("/repo"))
    assert trace != diff
    assert "where" in trace and "where" not in diff


def test_padded_matches_trace_length_but_not_content():
    """The control equalises volume while carrying no fault information."""
    res = _failing()
    trace = render(res, "trace", Path("/repo"))
    padded = render(res, "padded", Path("/repo"))
    assert abs(len(padded) - len(trace)) <= 2, (len(padded), len(trace))
    assert "test_ten_percent_discount" not in padded
    assert "100.0" not in padded


def test_padded_is_deterministic():
    """Same seed, same filler — runs must be reproducible."""
    res = _failing()
    a = render(res, "padded", Path("/repo"), seed=7)
    b = render(res, "padded", Path("/repo"), seed=7)
    assert a == b


def test_paths_are_relative():
    """Absolute paths leak harness layout and inflate the padded target."""
    body = render(_failing(), "diff", Path("/repo"))
    assert "/repo/" not in body
    assert "test_cart.py:9" in body


def test_unknown_rung_rejected():
    with pytest.raises(ValueError):
        render(_failing(), "verbose")


def test_deltas_flag_healthy_task():
    d = rung_deltas(_failing(), Path("/repo"))
    assert d["trace_adds_over_diff"] is True
    assert d["padded_matches_trace"] is True


def test_padding_makes_no_claim_about_the_run():
    """Filler must be neutral: no counts, no outcomes, nothing to contradict rung 1."""
    import re
    body = render(_failing(), "padded", Path("/repo"))
    filler = body.split("\n", 1)[1]
    assert not re.search(r"\d+ (items|tests?|passed|failed)|no tests ran|error", filler, re.I)


def test_detail_cap_at_rungs_3_and_4():
    """Only the first 5 failing tests get full detail; the rest are named."""
    from marcopolo.rungs import MAX_DETAILED
    fails = [{"test": f"t.py::test_{i}", "message": f"AssertionError: case {i}", "path": "/repo/t.py",
              "lineno": i, "longrepr": "", "values": [f"x = {i}"], "frames": []} for i in range(8)]
    res = CheckResult(passed=0, failed=8, failures=fails)
    for rung in ("diff", "trace"):
        body = render(res, rung, Path("/repo"))
        assert body.count("AssertionError: case") == MAX_DETAILED == 5, rung
        assert "t.py::test_7 failed" in body and "case 7" not in body, rung
    assert render(res, "trace", Path("/repo")).count("values at failure") == 5
