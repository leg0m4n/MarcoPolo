"""The check parser, pinned to real pytest output.

Each fixture is verbatim pytest text (local paths replaced by the container's).
If parsing drifts, a rung shows the agent more or less than pre-registered.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from marcopolo.check import parse, statuses  # noqa: E402
from marcopolo.rungs import render  # noqa: E402

FX = Path(__file__).parent / "fixtures"
failures = (FX / "pytest_sample_failures.txt").read_text()
collect = (FX / "pytest_sample_collect_error.txt").read_text()
setup = (FX / "pytest_sample_setup_error.txt").read_text()

DISCOUNT = "test_cart.py::TestCart::test_discount"
PARSE_X = "test_cart.py::test_parse[x]"
PARSE_12 = "test_cart.py::test_parse[12]"


def test_statuses_from_summary():
    st = statuses(failures)
    assert st[PARSE_12][0] == "PASSED" and st[DISCOUNT][0] == "FAILED"


def test_only_the_tasks_tests_are_counted():
    res = parse(failures, [DISCOUNT, PARSE_12])
    assert (res.passed, res.failed) == (1, 1)


def test_assertion_failure_detail():
    f = parse(failures, [DISCOUNT]).failures[0]
    assert f["message"] == "AssertionError: assert 100.0 == 99.0"
    assert (f["path"], f["lineno"]) == ("test_cart.py", 10)
    assert any(v.startswith("where 100.0 = cart_total(") for v in f["values"])
    assert "expected = 99.0" in f["values"]


def test_exception_is_located_where_raised_in_source():
    f = parse(failures, [PARSE_X]).failures[0]
    assert f["message"].startswith("ValueError: invalid literal")
    assert (f["path"], f["lineno"]) == ("pkg/cart.py", 7)
    assert f["frames"] == ["test_cart.py:15", "pkg/cart.py:7"]     # the execution path


def test_nondeterministic_reprs_are_dropped():
    vals = parse(failures, [DISCOUNT]).failures[0]["values"]
    assert not any(v.startswith("self =") or " at 0x" in v for v in vals)


def test_collection_error_fails_every_test_with_the_real_cause():
    res = parse(collect, [DISCOUNT, PARSE_12])
    assert res.failed == 2
    f = res.failures[0]
    assert f["message"] == "SyntaxError: invalid syntax"
    assert f["path"] == "pkg/cart.py"
    assert all("site-packages" not in fr and "<frozen" not in fr for fr in f["frames"])


def test_setup_error():
    f = parse(setup, ["test_fixture.py::test_uses_db"]).failures[0]
    assert f["message"] == "RuntimeError: db unavailable"
    assert (f["path"], f["lineno"]) == ("test_fixture.py", 4)


def test_rendered_rungs_stay_monotonic_on_real_output():
    res = parse(failures, [DISCOUNT, PARSE_X, PARSE_12])
    lens = [len(render(res, r)) for r in ("outcome", "location", "diff", "trace")]
    assert lens == sorted(lens) and len(set(lens)) == 4, lens


def test_expected_vs_actual_on_continuation_lines_reaches_rung_3():
    """numpy puts x/y (actual/expected) after a bare "AssertionError:"."""
    out = (FX / "pytest_astropy_numpy_assert.txt").read_text()
    nid = "astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]"
    f = parse(out, [nid]).failures[0]
    assert "x: array([False, False, False, False])" in f["message"]
    assert "y: array([False, False,  True,  True])" in f["message"]
    diff = render(parse(out, [nid]), "diff")
    assert "y: array(" in diff and "values at failure" not in diff
